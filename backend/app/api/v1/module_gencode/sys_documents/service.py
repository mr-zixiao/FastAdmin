# -*- coding: utf-8 -*-

import io
from fastapi import UploadFile
import pandas as pd

from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.utils.excel_util import ExcelUtil
from app.core.logger import log
from app.api.v1.module_system.auth.schema import AuthSchema
from .schema import SysDocumentsCreateSchema, SysDocumentsUpdateSchema, SysDocumentsOutSchema, SysDocumentsQueryParam
from .crud import SysDocumentsCRUD
from app.api.v1.module_gencode.sys_file_upload.schema import SysFileUploadOutSchema
from app.doc_processing.tasks import  process_document_task

class SysDocumentsService:
    """
    文档管理服务层
    """
    
    @classmethod
    async def detail_sys_documents_service(cls, auth: AuthSchema, id: int) -> dict:
        """详情"""
        obj = await SysDocumentsCRUD(auth).get_by_id_sys_documents_crud(id=id, preload=["file_upload"])
        if not obj:
            raise CustomException(msg="该数据不存在")
        result = SysDocumentsOutSchema.model_validate(obj).model_dump()
        # 处理文件信息
        if obj.file_upload:
            result['file_info'] = SysFileUploadOutSchema.model_validate(obj.file_upload).model_dump()
        else:
            result['file_info'] = None
        return result
    
    @classmethod
    async def list_sys_documents_service(cls, auth: AuthSchema, search: SysDocumentsQueryParam | None = None, order_by: list[dict] | None = None) -> list[dict]:
        """列表查询"""
        search_dict = search.__dict__ if search else None
        obj_list = await SysDocumentsCRUD(auth).list_sys_documents_crud(search=search_dict, order_by=order_by, preload=["file_upload"])
        result_list = []
        for obj in obj_list:
            result = SysDocumentsOutSchema.model_validate(obj).model_dump()
            # 处理文件信息
            if obj.file_upload:
                result['file_info'] = SysFileUploadOutSchema.model_validate(obj.file_upload).model_dump()
            else:
                result['file_info'] = None
            result_list.append(result)
        return result_list

    @classmethod
    async def page_sys_documents_service(cls, auth: AuthSchema, page_no: int, page_size: int, search: SysDocumentsQueryParam | None = None, order_by: list[dict] | None = None) -> dict:
        """分页查询（数据库分页）"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{'id': 'asc'}]
        offset = (page_no - 1) * page_size
        result = await SysDocumentsCRUD(auth).page_sys_documents_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
            preload=["file_upload"]
        )

        # 处理文件信息
        items_with_file_info = []
        if result.get('_raw_items'):
            # 如果返回的是原始对象，需要序列化并添加文件信息
            for obj in result.get('items', []):
                result_item = SysDocumentsOutSchema.model_validate(obj).model_dump()
                if obj.file_upload:
                    result_item['file_info'] = SysFileUploadOutSchema.model_validate(obj.file_upload).model_dump()
                else:
                    result_item['file_info'] = None
                items_with_file_info.append(result_item)
            result['items'] = items_with_file_info
            del result['_raw_items']
        else:
            # 如果已经是序列化后的字典，需要重新查询对象获取文件信息
            items_with_file_info = []
            for item in result.get('items', []):
                doc_id = item.get('id')
                if doc_id:
                    obj = await SysDocumentsCRUD(auth).get_by_id_sys_documents_crud(id=doc_id, preload=["file_upload"])
                    if obj:
                        result_item = SysDocumentsOutSchema.model_validate(obj).model_dump()
                        if obj.file_upload:
                            result_item['file_info'] = SysFileUploadOutSchema.model_validate(obj.file_upload).model_dump()
                        else:
                            result_item['file_info'] = None
                        items_with_file_info.append(result_item)
                    else:
                        items_with_file_info.append(item)
                else:
                    items_with_file_info.append(item)
            result['items'] = items_with_file_info
        return result
    
    @classmethod
    async def create_sys_documents_service(cls, auth: AuthSchema, data: SysDocumentsCreateSchema) -> dict:
        """创建"""
        # 检查唯一性约束
        obj = await SysDocumentsCRUD(auth).create_sys_documents_crud(data=data)
        process_document_task.delay(
            doc_id=obj.id,
            lib_id=obj.lib_id,
            file_path="storage/uploads/test.pdf",  # 实际应从数据库查
            chunk_size=obj.chunk_size,
            chunk_overlap=obj.chunk_overlap
        )
        return SysDocumentsOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_sys_documents_service(cls, auth: AuthSchema, id: int, data: SysDocumentsUpdateSchema) -> dict:
        """更新"""
        # 检查数据是否存在
        obj = await SysDocumentsCRUD(auth).get_by_id_sys_documents_crud(id=id)
        if not obj:
            raise CustomException(msg='更新失败，该数据不存在')
        
        # 检查唯一性约束
            
        obj = await SysDocumentsCRUD(auth).update_sys_documents_crud(id=id, data=data)
        return SysDocumentsOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_sys_documents_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """删除"""
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        for id in ids:
            obj = await SysDocumentsCRUD(auth).get_by_id_sys_documents_crud(id=id)
            if not obj:
                raise CustomException(msg=f'删除失败，ID为{id}的数据不存在')
        await SysDocumentsCRUD(auth).delete_sys_documents_crud(ids=ids)
    
    @classmethod
    async def set_available_sys_documents_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """批量设置状态"""
        await SysDocumentsCRUD(auth).set_available_sys_documents_crud(ids=data.ids, status=data.status)
    
    @classmethod
    async def batch_export_sys_documents_service(cls, obj_list: list[dict]) -> bytes:
        """批量导出"""
        mapping_dict = {
            'lib_id': '知识库ID',
            'file_upload_id': '文件上传ID',
            'chunk_size': '文档切片大小',
            'chunk_overlap': '文档切片重叠大小',
            'processing_status': '处理状态(pending:待处理 processing:处理中 completed:已完成 failed:处理失败)',
            'error_msg': '错误信息（处理失败时）',
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
    async def batch_import_sys_documents_service(cls, auth: AuthSchema, file: UploadFile, update_support: bool = False) -> str:
        """批量导入"""
        header_dict = {
            '知识库ID': 'lib_id',
            '文件上传ID': 'file_upload_id',
            '文档切片大小': 'chunk_size',
            '文档切片重叠大小': 'chunk_overlap',
            '处理状态(pending:待处理 processing:处理中 completed:已完成 failed:处理失败)': 'processing_status',
            '错误信息（处理失败时）': 'error_msg',
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
                        "lib_id": row['lib_id'],
                        "file_upload_id": row['file_upload_id'],
                        "chunk_size": row['chunk_size'],
                        "chunk_overlap": row['chunk_overlap'],
                        "processing_status": row['processing_status'],
                        "error_msg": row['error_msg'],
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
                    create_schema = SysDocumentsCreateSchema.model_validate(data)
                    
                    # 检查唯一性约束
                    
                    await SysDocumentsCRUD(auth).create_sys_documents_crud(data=create_schema)
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
    async def import_template_download_sys_documents_service(cls) -> bytes:
        """下载导入模板"""
        header_list = [
            '知识库ID',
            '文件上传ID',
            '文档分块数量',
            '文档切片大小',
            '文档切片重叠大小',
            '处理状态(pending:待处理 processing:处理中 completed:已完成 failed:处理失败)',
            '错误信息（处理失败时）',
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