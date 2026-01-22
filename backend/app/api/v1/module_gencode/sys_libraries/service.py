# -*- coding: utf-8 -*-

import io
from fastapi import UploadFile
import pandas as pd

from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.utils.excel_util import ExcelUtil
from app.core.logger import log
from app.api.v1.module_system.auth.schema import AuthSchema
from .schema import SysLibrariesCreateSchema, SysLibrariesWithPermissionCreateSchema, SysLibrariesWithPermissionUpdateSchema, SysLibrariesUpdateSchema, SysLibrariesOutSchema, SysLibrariesQueryParam
from .crud import SysLibrariesCRUD
from app.api.v1.module_gencode.sys_lib_permissions.service import SysLibPermissionsService
from app.api.v1.module_gencode.sys_lib_permissions.schema import SysLibPermissionsCreateSchema


class SysLibrariesService:
    """
    知识库定义服务层
    """
    
    @classmethod
    async def detail_sys_libraries_service(cls, auth: AuthSchema, id: int) -> dict:
        """详情"""
        obj = await SysLibrariesCRUD(auth).get_by_id_sys_libraries_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")
        return SysLibrariesOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def list_sys_libraries_service(cls, auth: AuthSchema, search: SysLibrariesQueryParam | None = None, order_by: list[dict] | None = None) -> list[dict]:
        """列表查询"""
        search_dict = search.__dict__ if search else None
        obj_list = await SysLibrariesCRUD(auth).list_sys_libraries_crud(search=search_dict, order_by=order_by)
        return [SysLibrariesOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_sys_libraries_service(cls, auth: AuthSchema, page_no: int, page_size: int, search: SysLibrariesQueryParam | None = None, order_by: list[dict] | None = None) -> dict:
        """分页查询（数据库分页）"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{'id': 'asc'}]
        offset = (page_no - 1) * page_size
        result = await SysLibrariesCRUD(auth).page_sys_libraries_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict
        )
        return result
    
    @classmethod
    async def create_sys_libraries_service(cls, auth: AuthSchema, data: SysLibrariesWithPermissionCreateSchema) -> dict:
        """创建"""
        # 提取权限关联字段
        target_type = data.target_type
        target_ids = data.target_ids
        privilege_type = data.privilege_type
        
        # 准备基础创建数据（排除权限关联字段）
        base_data_dict = data.model_dump()
        for field in ['target_type', 'target_ids', 'privilege_type']:
            base_data_dict.pop(field, None)
        
        base_data = SysLibrariesCreateSchema(**base_data_dict)
        
        # 检查唯一性约束
        obj = await SysLibrariesCRUD(auth).create_sys_libraries_crud(data=base_data)
        
        # 如果提供了权限关联字段，则创建对应的权限记录
        if target_type and target_ids and privilege_type:
            await cls._handle_library_permissions(auth, obj.id, target_type, target_ids, privilege_type)
        
        return SysLibrariesOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def _handle_library_permissions(cls, auth: AuthSchema, lib_id: int, target_type: str, target_ids: str, privilege_type: str):
        """
        处理知识库权限关联
        
        参数:
        - auth: 认证信息
        - lib_id: 知识库ID
        - target_type: 授权对象类型(dept:部门 role:角色 user:用户)
        - target_ids: 对应对象的主键ID序列(逗号分隔)
        - privilege_type: 权限级别
        """
        # 解析目标ID列表
        target_id_list = [int(id.strip()) for id in target_ids.split(',') if id.strip().isdigit()]
        
        # 直接使用传入的target_type值
        # 为每个目标ID创建权限记录
        for target_id in target_id_list:
            permission_data = SysLibPermissionsCreateSchema(
                target_type=target_type,
                target_id=target_id,
                lib_id=lib_id,
                privilege_type=privilege_type,
                status="0"  # 默认启用状态
            )
            await SysLibPermissionsService.create_sys_lib_permissions_service(auth, permission_data)
    
    @classmethod
    async def update_sys_libraries_service(cls, auth: AuthSchema, id: int, data: SysLibrariesWithPermissionUpdateSchema) -> dict:
        """更新"""
        # 检查数据是否存在
        obj = await SysLibrariesCRUD(auth).get_by_id_sys_libraries_crud(id=id)
        if not obj:
            raise CustomException(msg='更新失败，该数据不存在')
        
        # 检查唯一性约束
            
        # 提取权限关联字段
        target_type = getattr(data, 'target_type', None)
        target_ids = getattr(data, 'target_ids', None)
        privilege_type = getattr(data, 'privilege_type', None)
        
        # 准备基础更新数据（排除权限关联字段）
        base_data_dict = data.model_dump()
        for field in ['target_type', 'target_ids', 'privilege_type']:
            base_data_dict.pop(field, None)
        
        base_data = SysLibrariesUpdateSchema(**base_data_dict)
        
        obj = await SysLibrariesCRUD(auth).update_sys_libraries_crud(id=id, data=base_data)
        
        # 如果提供了权限关联字段，则处理对应的权限记录
        if target_type and target_ids and privilege_type:
            await cls._handle_library_permissions_on_update(auth, obj.id, target_type, target_ids, privilege_type)
        
        return SysLibrariesOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def _handle_library_permissions_on_update(cls, auth: AuthSchema, lib_id: int, target_type: str, target_ids: str, privilege_type: str):
        """
        更新知识库权限关联（先删除旧权限，再创建新权限）
        
        参数:
        - auth: 认证信息
        - lib_id: 知识库ID
        - target_type: 授权对象类型(dept:部门 role:角色 user:用户)
        - target_ids: 对应对象的主键ID序列(逗号分隔)
        - privilege_type: 权限级别
        """
        from app.api.v1.module_gencode.sys_lib_permissions.crud import SysLibPermissionsCRUD
        from app.api.v1.module_gencode.sys_lib_permissions.schema import SysLibPermissionsQueryParam
        
        # 先删除该知识库的所有现有权限记录
        search_param = SysLibPermissionsQueryParam(lib_id=lib_id)
        existing_permissions = await SysLibPermissionsCRUD(auth).list_sys_lib_permissions_crud(search=search_param.__dict__)
        
        # 收集需要删除的权限ID
        permission_ids_to_delete = [perm.id for perm in existing_permissions]
        
        # 删除现有权限
        if permission_ids_to_delete:
            await SysLibPermissionsCRUD(auth).delete_sys_lib_permissions_crud(ids=permission_ids_to_delete)
        
        # 解析目标ID列表
        target_id_list = [int(id.strip()) for id in target_ids.split(',') if id.strip().isdigit()]
        
        # 直接使用传入的target_type值
        
        # 为每个目标ID创建新的权限记录
        for target_id in target_id_list:
            permission_data = SysLibPermissionsCreateSchema(
                target_type=target_type,
                target_id=target_id,
                lib_id=lib_id,
                privilege_type=privilege_type,
                status="0"  # 默认启用状态
            )
            await SysLibPermissionsService.create_sys_lib_permissions_service(auth, permission_data)
    
    @classmethod
    async def delete_sys_libraries_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """删除"""
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        for id in ids:
            obj = await SysLibrariesCRUD(auth).get_by_id_sys_libraries_crud(id=id)
            if not obj:
                raise CustomException(msg=f'删除失败，ID为{id}的数据不存在')
        await SysLibrariesCRUD(auth).delete_sys_libraries_crud(ids=ids)
    
    @classmethod
    async def set_available_sys_libraries_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """批量设置状态"""
        await SysLibrariesCRUD(auth).set_available_sys_libraries_crud(ids=data.ids, status=data.status)
    
    @classmethod
    async def batch_export_sys_libraries_service(cls, obj_list: list[dict]) -> bytes:
        """批量导出"""
        mapping_dict = {
            'id': '主键ID',
            'uuid': 'UUID全局唯一标识',
            'name': '知识库名称',
            'collection_name': '对应向量库Collection名称',
            'status': '状态(0:启用 1:禁用)',
            'created_time': '创建时间',
            'updated_time': '更新时间',
            'created_id': '创建人ID',
            'updated_id': '更新人ID',
            'updated_id': '更新者ID',
        }

        data = obj_list.copy()
        for item in data:
            # 状态转换
            if 'status' in item:
                item['status'] = '启用' if item.get('status') == '0' else '停用'
            # 创建者转换
            creator_info = item.get('creator')
            if isinstance(creator_info, dict):
                item['creator'] = creator_info.get('name', '未知')
            elif creator_info is None:
                item['creator'] = '未知'

        return ExcelUtil.export_list2excel(list_data=data, mapping_dict=mapping_dict)

    @classmethod
    async def batch_import_sys_libraries_service(cls, auth: AuthSchema, file: UploadFile, update_support: bool = False) -> str:
        """批量导入"""
        header_dict = {
            '主键ID': 'id',
            'UUID全局唯一标识': 'uuid',
            '知识库名称': 'name',
            '对应向量库Collection名称': 'collection_name',
            '状态(0:启用 1:禁用)': 'status',
            '创建时间': 'created_time',
            '更新时间': 'updated_time',
            '创建人ID': 'created_id',
            '更新人ID': 'updated_id',
        }

        try:
            contents = await file.read()
            df = pd.read_excel(io.BytesIO(contents))
            await file.close()
            
            if df.empty:
                raise CustomException(msg="导入文件为空")
            
            missing_headers = [header for header in header_dict.keys() if header not in df.columns]
            if missing_headers:
                raise CustomException(msg=f"导入文件缺少必要的列: {', '.join(missing_headers)}")
            
            df.rename(columns=header_dict, inplace=True)
            
            # 验证必填字段
            
            error_msgs = []
            success_count = 0
            count = 0
            
            for index, row in df.iterrows():
                count += 1
                try:
                    data = {
                        "id": row['id'],
                        "uuid": row['uuid'],
                        "name": row['name'],
                        "collection_name": row['collection_name'],
                        "status": row['status'],
                        "created_time": row['created_time'],
                        "updated_time": row['updated_time'],
                        "created_id": row['created_id'],
                        "updated_id": row['updated_id'],
                    }
                    # 使用CreateSchema做校验后入库
                    create_schema = SysLibrariesCreateSchema.model_validate(data)
                    
                    # 检查唯一性约束
                    
                    await SysLibrariesCRUD(auth).create_sys_libraries_crud(data=create_schema)
                    success_count += 1
                except Exception as e:
                    error_msgs.append(f"第{count}行: {str(e)}")
                    continue

            result = f"成功导入 {success_count} 条数据"
            if error_msgs:
                result += "\n错误信息:\n" + "\n".join(error_msgs)
            return result
            
        except Exception as e:
            log.error(f"批量导入失败: {str(e)}")
            raise CustomException(msg=f"导入失败: {str(e)}")
    
    @classmethod
    async def import_template_download_sys_libraries_service(cls) -> bytes:
        """下载导入模板"""
        header_list = [
            '主键ID',
            'UUID全局唯一标识',
            '知识库名称',
            '对应向量库Collection名称',
            '关联部门编码',
            '状态(0:启用 1:禁用)',
            '创建时间',
            '更新时间',
            '创建人ID',
            '更新人ID',
        ]
        selector_header_list = []
        option_list = []
        
        # 添加下拉选项
        
        return ExcelUtil.get_excel_template(
            header_list=header_list,
            selector_header_list=selector_header_list,
            option_list=option_list
        )