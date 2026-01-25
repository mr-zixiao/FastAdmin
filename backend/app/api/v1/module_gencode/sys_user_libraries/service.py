# -*- coding: utf-8 -*-

import io
from fastapi import UploadFile
import pandas as pd

from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.utils.excel_util import ExcelUtil
from app.core.logger import log
from app.api.v1.module_system.auth.schema import AuthSchema
from .schema import SysUserLibrariesCreateSchema, SysUserLibrariesUpdateSchema, SysUserLibrariesOutSchema, SysUserLibrariesQueryParam, SysUserLibrariesBatchAssociateSchema
from .crud import SysUserLibrariesCRUD


class SysUserLibrariesService:
    """
    用户与知识库关联服务层
    """
    
    @classmethod
    async def detail_sys_user_libraries_service(cls, auth: AuthSchema, id: int) -> dict:
        """详情"""
        obj = await SysUserLibrariesCRUD(auth).get_by_id_sys_user_libraries_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")
        return SysUserLibrariesOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def list_sys_user_libraries_service(cls, auth: AuthSchema, search: SysUserLibrariesQueryParam | None = None, order_by: list[dict] | None = None) -> list[dict]:
        """列表查询"""
        search_dict = search.__dict__ if search else None
        obj_list = await SysUserLibrariesCRUD(auth).list_sys_user_libraries_crud(search=search_dict, order_by=order_by)
        return [SysUserLibrariesOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_sys_user_libraries_service(cls, auth: AuthSchema, page_no: int, page_size: int, search: SysUserLibrariesQueryParam | None = None, order_by: list[dict] | None = None) -> dict:
        """分页查询（数据库分页）"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{'id': 'asc'}]
        offset = (page_no - 1) * page_size
        result = await SysUserLibrariesCRUD(auth).page_sys_user_libraries_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict
        )
        return result
    
    @classmethod
    async def create_sys_user_libraries_service(cls, auth: AuthSchema, data: SysUserLibrariesCreateSchema) -> dict:
        """创建"""
        # 检查唯一性约束
        obj = await SysUserLibrariesCRUD(auth).create_sys_user_libraries_crud(data=data)
        return SysUserLibrariesOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_sys_user_libraries_service(cls, auth: AuthSchema, id: int, data: SysUserLibrariesUpdateSchema) -> dict:
        """更新"""
        # 检查数据是否存在
        obj = await SysUserLibrariesCRUD(auth).get_by_id_sys_user_libraries_crud(id=id)
        if not obj:
            raise CustomException(msg='更新失败，该数据不存在')
        
        # 检查唯一性约束
            
        obj = await SysUserLibrariesCRUD(auth).update_sys_user_libraries_crud(id=id, data=data)
        return SysUserLibrariesOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_sys_user_libraries_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """删除"""
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        for id in ids:
            obj = await SysUserLibrariesCRUD(auth).get_by_id_sys_user_libraries_crud(id=id)
            if not obj:
                raise CustomException(msg=f'删除失败，ID为{id}的数据不存在')
        await SysUserLibrariesCRUD(auth).delete_sys_user_libraries_crud(ids=ids)
    
    @classmethod
    async def set_available_sys_user_libraries_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """批量设置状态"""
        await SysUserLibrariesCRUD(auth).set_available_sys_user_libraries_crud(ids=data.ids, status=data.status)
    
    @classmethod
    async def batch_export_sys_user_libraries_service(cls, obj_list: list[dict]) -> bytes:
        """批量导出"""
        mapping_dict = {
            'user_id': '用户ID',
            'lib_id': '知识库ID',
            'privilege_type': '权限类型(read:只读 write:读写 admin:管理员)',
            'id': '主键ID',
            'uuid': 'UUID全局唯一标识',
            'status': '是否启用(0:启用 1:禁用)',
            'description': '备注/描述',
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
    async def batch_import_sys_user_libraries_service(cls, auth: AuthSchema, file: UploadFile, update_support: bool = False) -> str:
        """批量导入"""
        header_dict = {
            '用户ID': 'user_id',
            '知识库ID': 'lib_id',
            '权限类型(read:只读 write:读写 admin:管理员)': 'privilege_type',
            '主键ID': 'id',
            'UUID全局唯一标识': 'uuid',
            '是否启用(0:启用 1:禁用)': 'status',
            '备注/描述': 'description',
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
                        "user_id": row['user_id'],
                        "lib_id": row['lib_id'],
                        "privilege_type": row['privilege_type'],
                        "id": row['id'],
                        "uuid": row['uuid'],
                        "status": row['status'],
                        "description": row['description'],
                        "created_time": row['created_time'],
                        "updated_time": row['updated_time'],
                        "created_id": row['created_id'],
                        "updated_id": row['updated_id'],
                    }
                    # 使用CreateSchema做校验后入库
                    create_schema = SysUserLibrariesCreateSchema.model_validate(data)
                    
                    # 检查唯一性约束
                    
                    await SysUserLibrariesCRUD(auth).create_sys_user_libraries_crud(data=create_schema)
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
    async def batch_associate_sys_user_libraries_service(cls, auth: AuthSchema, data: SysUserLibrariesBatchAssociateSchema) -> dict:
        """批量关联用户与知识库"""
        if not data.user_ids or len(data.user_ids) == 0:
            raise CustomException(msg="用户ID列表不能为空")
        
        success_count = 0
        error_msgs = []
        
        for user_id in data.user_ids:
            try:
                # 检查是否已存在关联
                search_dict = {"user_id": user_id, "lib_id": data.lib_id}
                existing_list = await SysUserLibrariesCRUD(auth).list_sys_user_libraries_crud(search=search_dict)
                
                if existing_list:
                    # 如果已存在，更新权限类型和状态
                    existing = existing_list[0]
                    update_data = SysUserLibrariesUpdateSchema(
                        user_id=user_id,
                        lib_id=data.lib_id,
                        privilege_type=data.privilege_type,
                        status=data.status,
                        description=data.description
                    )
                    await SysUserLibrariesCRUD(auth).update_sys_user_libraries_crud(id=existing.id, data=update_data)
                else:
                    # 如果不存在，创建新关联
                    create_data = SysUserLibrariesCreateSchema(
                        user_id=user_id,
                        lib_id=data.lib_id,
                        privilege_type=data.privilege_type,
                        status=data.status,
                        description=data.description
                    )
                    await SysUserLibrariesCRUD(auth).create_sys_user_libraries_crud(data=create_data)
                
                success_count += 1
            except Exception as e:
                error_msgs.append(f"用户ID {user_id}: {str(e)}")
                continue
        
        result_msg = f"成功关联 {success_count} 个用户"
        if error_msgs:
            result_msg += f"，失败 {len(error_msgs)} 个：\n" + "\n".join(error_msgs)
        
        return {
            "success_count": success_count,
            "total_count": len(data.user_ids),
            "error_count": len(error_msgs),
            "message": result_msg
        }
    
    @classmethod
    async def import_template_download_sys_user_libraries_service(cls) -> bytes:
        """下载导入模板"""
        header_list = [
            '用户ID',
            '知识库ID',
            '权限类型(read:只读 write:读写 admin:管理员)',
            '主键ID',
            'UUID全局唯一标识',
            '是否启用(0:启用 1:禁用)',
            '备注/描述',
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