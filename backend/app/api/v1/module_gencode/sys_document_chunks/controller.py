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

from .service import SysDocumentChunksService
from .schema import SysDocumentChunksCreateSchema, SysDocumentChunksUpdateSchema, SysDocumentChunksQueryParam

SysDocumentChunksRouter = APIRouter(prefix='/sys_document_chunks', tags=["文档切片明细模块"]) 

@SysDocumentChunksRouter.get("/detail/{id}", summary="获取文档切片明细详情", description="获取文档切片明细详情")
async def get_sys_document_chunks_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_document_chunks:query"]))
) -> JSONResponse:
    """获取文档切片明细详情接口"""
    result_dict = await SysDocumentChunksService.detail_sys_document_chunks_service(auth=auth, id=id)
    log.info(f"获取文档切片明细详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取文档切片明细详情成功")

@SysDocumentChunksRouter.get("/list", summary="查询文档切片明细列表", description="查询文档切片明细列表")
async def get_sys_document_chunks_list_controller(
    page: PaginationQueryParam = Depends(),
    search: SysDocumentChunksQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_document_chunks:query"]))
) -> JSONResponse:
    """查询文档切片明细列表接口（数据库分页）"""
    result_dict = await SysDocumentChunksService.page_sys_document_chunks_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询文档切片明细列表成功")
    return SuccessResponse(data=result_dict, msg="查询文档切片明细列表成功")

@SysDocumentChunksRouter.post("/create", summary="创建文档切片明细", description="创建文档切片明细")
async def create_sys_document_chunks_controller(
    data: SysDocumentChunksCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_document_chunks:create"]))
) -> JSONResponse:
    """创建文档切片明细接口"""
    result_dict = await SysDocumentChunksService.create_sys_document_chunks_service(auth=auth, data=data)
    log.info("创建文档切片明细成功")
    return SuccessResponse(data=result_dict, msg="创建文档切片明细成功")

@SysDocumentChunksRouter.put("/update/{id}", summary="修改文档切片明细", description="修改文档切片明细")
async def update_sys_document_chunks_controller(
    data: SysDocumentChunksUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_document_chunks:update"]))
) -> JSONResponse:
    """修改文档切片明细接口"""
    result_dict = await SysDocumentChunksService.update_sys_document_chunks_service(auth=auth, id=id, data=data)
    log.info("修改文档切片明细成功")
    return SuccessResponse(data=result_dict, msg="修改文档切片明细成功")

@SysDocumentChunksRouter.delete("/delete", summary="删除文档切片明细", description="删除文档切片明细")
async def delete_sys_document_chunks_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_document_chunks:delete"]))
) -> JSONResponse:
    """删除文档切片明细接口"""
    await SysDocumentChunksService.delete_sys_document_chunks_service(auth=auth, ids=ids)
    log.info(f"删除文档切片明细成功: {ids}")
    return SuccessResponse(msg="删除文档切片明细成功")

@SysDocumentChunksRouter.patch("/available/setting", summary="批量修改文档切片明细状态", description="批量修改文档切片明细状态")
async def batch_set_available_sys_document_chunks_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_document_chunks:patch"]))
) -> JSONResponse:
    """批量修改文档切片明细状态接口"""
    await SysDocumentChunksService.set_available_sys_document_chunks_service(auth=auth, data=data)
    log.info(f"批量修改文档切片明细状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改文档切片明细状态成功")

@SysDocumentChunksRouter.post('/export', summary="导出文档切片明细", description="导出文档切片明细")
async def export_sys_document_chunks_list_controller(
    search: SysDocumentChunksQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_document_chunks:export"]))
) -> StreamingResponse:
    """导出文档切片明细接口"""
    result_dict_list = await SysDocumentChunksService.list_sys_document_chunks_service(search=search, auth=auth)
    export_result = await SysDocumentChunksService.batch_export_sys_document_chunks_service(obj_list=result_dict_list)
    log.info('导出文档切片明细成功')

    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=sys_document_chunks.xlsx'
        }
    )

@SysDocumentChunksRouter.post('/import', summary="导入文档切片明细", description="导入文档切片明细")
async def import_sys_document_chunks_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_document_chunks:import"]))
) -> JSONResponse:
    """导入文档切片明细接口"""
    batch_import_result = await SysDocumentChunksService.batch_import_sys_document_chunks_service(file=file, auth=auth, update_support=True)
    log.info("导入文档切片明细成功")
    
    return SuccessResponse(data=batch_import_result, msg="导入文档切片明细成功")

@SysDocumentChunksRouter.post('/download/template', summary="获取文档切片明细导入模板", description="获取文档切片明细导入模板", dependencies=[Depends(AuthPermission(["module_gencode:sys_document_chunks:download"]))])
async def export_sys_document_chunks_template_controller() -> StreamingResponse:
    """获取文档切片明细导入模板接口"""
    import_template_result = await SysDocumentChunksService.import_template_download_sys_document_chunks_service()
    log.info('获取文档切片明细导入模板成功')

    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=sys_document_chunks_template.xlsx'}
    )