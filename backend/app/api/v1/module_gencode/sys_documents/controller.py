# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, UploadFile, Body, Path, Query
from fastapi.responses import StreamingResponse, JSONResponse

from app.common.response import SuccessResponse, StreamResponse
from app.core.dependencies import AuthPermission
from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_params import PaginationQueryParam
from app.utils.common_util import bytes2file_response
from app.core.logger import log
from app.core.base_schema import BatchSetAvailable

from .service import SysDocumentsService
from .schema import SysDocumentsCreateSchema, SysDocumentsUpdateSchema, SysDocumentsQueryParam

SysDocumentsRouter = APIRouter(prefix='/sys_documents', tags=["文档资产管理模块"]) 

@SysDocumentsRouter.get("/detail/{id}", summary="获取文档资产管理详情", description="获取文档资产管理详情")
async def get_sys_documents_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_documents:query"]))
) -> JSONResponse:
    """获取文档资产管理详情接口"""
    result_dict = await SysDocumentsService.detail_sys_documents_service(auth=auth, id=id)
    log.info(f"获取文档资产管理详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取文档资产管理详情成功")

@SysDocumentsRouter.get("/list", summary="查询文档资产管理列表", description="查询文档资产管理列表")
async def get_sys_documents_list_controller(
    page: PaginationQueryParam = Depends(),
    search: SysDocumentsQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_documents:query"]))
) -> JSONResponse:
    """查询文档资产管理列表接口（数据库分页）"""
    result_dict = await SysDocumentsService.page_sys_documents_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询文档资产管理列表成功")
    return SuccessResponse(data=result_dict, msg="查询文档资产管理列表成功")

@SysDocumentsRouter.post("/create", summary="创建文档资产管理", description="创建文档资产管理")
async def create_sys_documents_controller(
    data: SysDocumentsCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_documents:create"]))
) -> JSONResponse:
    """创建文档资产管理接口"""
    result_dict = await SysDocumentsService.create_sys_documents_service(auth=auth, data=data)
    log.info("创建文档资产管理成功")
    return SuccessResponse(data=result_dict, msg="创建文档资产管理成功")

@SysDocumentsRouter.put("/update/{id}", summary="修改文档资产管理", description="修改文档资产管理")
async def update_sys_documents_controller(
    data: SysDocumentsUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_documents:update"]))
) -> JSONResponse:
    """修改文档资产管理接口"""
    result_dict = await SysDocumentsService.update_sys_documents_service(auth=auth, id=id, data=data)
    log.info("修改文档资产管理成功")
    return SuccessResponse(data=result_dict, msg="修改文档资产管理成功")

@SysDocumentsRouter.delete("/delete", summary="删除文档资产管理", description="删除文档资产管理")
async def delete_sys_documents_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_documents:delete"]))
) -> JSONResponse:
    """删除文档资产管理接口"""
    await SysDocumentsService.delete_sys_documents_service(auth=auth, ids=ids)
    log.info(f"删除文档资产管理成功: {ids}")
    return SuccessResponse(msg="删除文档资产管理成功")

@SysDocumentsRouter.patch("/available/setting", summary="批量修改文档资产管理状态", description="批量修改文档资产管理状态")
async def batch_set_available_sys_documents_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_documents:patch"]))
) -> JSONResponse:
    """批量修改文档资产管理状态接口"""
    await SysDocumentsService.set_available_sys_documents_service(auth=auth, data=data)
    log.info(f"批量修改文档资产管理状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改文档资产管理状态成功")

@SysDocumentsRouter.post('/export', summary="导出文档资产管理", description="导出文档资产管理")
async def export_sys_documents_list_controller(
    search: SysDocumentsQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_documents:export"]))
) -> StreamingResponse:
    """导出文档资产管理接口"""
    result_dict_list = await SysDocumentsService.list_sys_documents_service(search=search, auth=auth)
    export_result = await SysDocumentsService.batch_export_sys_documents_service(obj_list=result_dict_list)
    log.info('导出文档资产管理成功')

    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=sys_documents.xlsx'
        }
    )

@SysDocumentsRouter.post('/import', summary="导入文档资产管理", description="导入文档资产管理")
async def import_sys_documents_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_documents:import"]))
) -> JSONResponse:
    """导入文档资产管理接口"""
    batch_import_result = await SysDocumentsService.batch_import_sys_documents_service(file=file, auth=auth, update_support=True)
    log.info("导入文档资产管理成功")
    
    return SuccessResponse(data=batch_import_result, msg="导入文档资产管理成功")

@SysDocumentsRouter.post('/download/template', summary="获取文档资产管理导入模板", description="获取文档资产管理导入模板", dependencies=[Depends(AuthPermission(["module_gencode:sys_documents:download"]))])
async def export_sys_documents_template_controller() -> StreamingResponse:
    """获取文档资产管理导入模板接口"""
    import_template_result = await SysDocumentsService.import_template_download_sys_documents_service()
    log.info('获取文档资产管理导入模板成功')

    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=sys_documents_template.xlsx'}
    )