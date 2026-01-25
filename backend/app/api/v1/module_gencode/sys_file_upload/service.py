# -*- coding: utf-8 -*-

import io
import os
import aiofiles
from pathlib import Path
from fastapi import UploadFile
import pandas as pd

from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.utils.excel_util import ExcelUtil
from app.core.logger import log
from app.api.v1.module_system.auth.schema import AuthSchema
from app.config.path_conf import FILE_UPLOAD_DIR
from app.config.setting import settings
from .schema import SysFileUploadCreateSchema, SysFileUploadUpdateSchema, SysFileUploadOutSchema, SysFileUploadQueryParam
from .crud import SysFileUploadCRUD


class SysFileUploadService:
    """
    文件上传服务层
    """
    
    @classmethod
    async def detail_sys_file_upload_service(cls, auth: AuthSchema, id: int) -> dict:
        """详情"""
        obj = await SysFileUploadCRUD(auth).get_by_id_sys_file_upload_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")
        return SysFileUploadOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def list_sys_file_upload_service(cls, auth: AuthSchema, search: SysFileUploadQueryParam | None = None, order_by: list[dict] | None = None) -> list[dict]:
        """列表查询"""
        search_dict = search.__dict__ if search else None
        obj_list = await SysFileUploadCRUD(auth).list_sys_file_upload_crud(search=search_dict, order_by=order_by)
        return [SysFileUploadOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_sys_file_upload_service(cls, auth: AuthSchema, page_no: int, page_size: int, search: SysFileUploadQueryParam | None = None, order_by: list[dict] | None = None) -> dict:
        """分页查询（数据库分页）"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{'id': 'asc'}]
        offset = (page_no - 1) * page_size
        result = await SysFileUploadCRUD(auth).page_sys_file_upload_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict
        )
        return result
    
    @classmethod
    async def create_sys_file_upload_service(cls, auth: AuthSchema, data: SysFileUploadCreateSchema) -> dict:
        """创建"""
        # 检查唯一性约束
        obj = await SysFileUploadCRUD(auth).create_sys_file_upload_crud(data=data)
        return SysFileUploadOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_sys_file_upload_service(cls, auth: AuthSchema, id: int, data: SysFileUploadUpdateSchema) -> dict:
        """更新"""
        # 检查数据是否存在
        obj = await SysFileUploadCRUD(auth).get_by_id_sys_file_upload_crud(id=id)
        if not obj:
            raise CustomException(msg='更新失败，该数据不存在')
        
        # 检查唯一性约束
            
        obj = await SysFileUploadCRUD(auth).update_sys_file_upload_crud(id=id, data=data)
        return SysFileUploadOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_sys_file_upload_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """删除"""
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        
        # 删除物理文件
        for id in ids:
            obj = await SysFileUploadCRUD(auth).get_by_id_sys_file_upload_crud(id=id)
            if not obj:
                raise CustomException(msg=f'删除失败，ID为{id}的数据不存在')
            
            # 如果存在文件路径，删除物理文件
            if obj.file_path:
                try:
                    file_path = settings.STATIC_ROOT / obj.file_path
                    if file_path.exists() and file_path.is_file():
                        file_path.unlink()
                        log.info(f"删除物理文件成功: {file_path}")
                except Exception as e:
                    log.warning(f"删除物理文件失败: {e}")
        
        # 删除数据库记录
        await SysFileUploadCRUD(auth).delete_sys_file_upload_crud(ids=ids)
    
    @classmethod
    async def set_available_sys_file_upload_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """批量设置状态"""
        await SysFileUploadCRUD(auth).set_available_sys_file_upload_crud(ids=data.ids, status=data.status)
    
    @classmethod
    async def batch_export_sys_file_upload_service(cls, obj_list: list[dict]) -> bytes:
        """批量导出"""
        mapping_dict = {
            'origin_name': '原始文件名',
            'file_name': '新文件名（生成后的文件名）',
            'file_path': '文件存储路径',
            'file_size': '文件大小（字节）',
            'file_type': '文件类型/扩展名',
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
    async def batch_import_sys_file_upload_service(cls, auth: AuthSchema, file: UploadFile, update_support: bool = False) -> str:
        """批量导入"""
        header_dict = {
            '原始文件名': 'origin_name',
            '新文件名（生成后的文件名）': 'file_name',
            '文件存储路径': 'file_path',
            '文件大小（字节）': 'file_size',
            '文件类型/扩展名': 'file_type',
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
                        "origin_name": row['origin_name'],
                        "file_name": row['file_name'],
                        "file_path": row['file_path'],
                        "file_size": row['file_size'],
                        "file_type": row['file_type'],
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
                    create_schema = SysFileUploadCreateSchema.model_validate(data)
                    
                    # 检查唯一性约束
                    
                    await SysFileUploadCRUD(auth).create_sys_file_upload_crud(data=create_schema)
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
    async def import_template_download_sys_file_upload_service(cls) -> bytes:
        """下载导入模板"""
        header_list = [
            '原始文件名',
            '新文件名（生成后的文件名）',
            '文件存储路径',
            '文件大小（字节）',
            '文件类型/扩展名',
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
    
    @classmethod
    async def upload_file_service(cls, auth: AuthSchema, file: UploadFile, description: str | None = None) -> dict:
        """
        上传文件服务
        
        参数:
        - auth (AuthSchema): 认证信息
        - file (UploadFile): 上传的文件
        - description (str | None): 文件描述
        
        返回:
        - dict: 文件信息
        """
        if not file or not file.filename:
            raise CustomException(msg="请选择要上传的文件")
        
        # 检查文件大小
        if file.size and file.size > settings.MAX_FILE_SIZE:
            raise CustomException(msg=f"文件大小超过限制，最大支持 {settings.MAX_FILE_SIZE // (1024*1024)}MB")
        
        # 确保上传目录存在
        FILE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        
        # 获取文件扩展名
        origin_filename = file.filename
        file_ext = Path(origin_filename).suffix if origin_filename else ''
        
        # 先创建数据库记录以获取ID
        create_data = SysFileUploadCreateSchema(
            origin_name=origin_filename,
            file_name="",  # 临时值，稍后更新
            file_path="",  # 临时值，稍后更新
            file_size=file.size or 0,
            file_type=file_ext,
            status="0",
            description=description
        )
        
        # 创建记录
        obj = await SysFileUploadCRUD(auth).create_sys_file_upload_crud(data=create_data)
        file_id = obj.id
        
        # 以ID命名文件（保留扩展名）
        if file_ext:
            new_filename = f"{file_id}{file_ext}"
        else:
            new_filename = str(file_id)
        
        # 构建文件路径
        file_path = FILE_UPLOAD_DIR / new_filename
        
        try:
            # 保存文件
            chunk_size = 8 * 1024 * 1024  # 8MB chunks
            async with aiofiles.open(file_path, 'wb') as f:
                while chunk := await file.read(chunk_size):
                    await f.write(chunk)
            
            # 更新数据库记录（保存相对路径）
            # 计算相对于 STATIC_ROOT 的路径
            try:
                relative_path = file_path.relative_to(settings.STATIC_ROOT)
            except ValueError:
                # 如果无法计算相对路径，使用绝对路径的字符串形式
                relative_path = Path(str(file_path).replace(str(settings.STATIC_ROOT), '').lstrip('/\\'))
            
            update_data = SysFileUploadUpdateSchema(
                origin_name=origin_filename,
                file_name=new_filename,
                file_path=str(relative_path).replace('\\', '/'),  # 统一使用 / 作为路径分隔符
                file_size=file.size or 0,
                file_type=file_ext,
                status="0",
                description=description
            )
            
            updated_obj = await SysFileUploadCRUD(auth).update_sys_file_upload_crud(id=file_id, data=update_data)
            
            log.info(f"文件上传成功: {origin_filename} -> {new_filename} (ID: {file_id})")
            
            return SysFileUploadOutSchema.model_validate(updated_obj).model_dump()
            
        except Exception as e:
            # 如果文件保存失败，删除数据库记录
            try:
                await SysFileUploadCRUD(auth).delete_sys_file_upload_crud(ids=[file_id])
            except:
                pass
            log.error(f"文件上传失败: {e}")
            raise CustomException(msg=f"文件上传失败: {str(e)}")
    
    @classmethod
    async def get_file_path_service(cls, auth: AuthSchema, id: int) -> Path:
        """
        通过ID获取文件路径
        
        参数:
        - auth (AuthSchema): 认证信息
        - id (int): 文件ID
        
        返回:
        - Path: 文件路径
        """
        obj = await SysFileUploadCRUD(auth).get_by_id_sys_file_upload_crud(id=id)
        if not obj:
            raise CustomException(msg="文件不存在")
        
        if not obj.file_path:
            raise CustomException(msg="文件路径不存在")
        
        # 构建完整路径
        file_path = settings.STATIC_ROOT / obj.file_path
        
        if not file_path.exists():
            raise CustomException(msg="文件不存在")
        
        return file_path