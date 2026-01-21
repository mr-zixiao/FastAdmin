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

from .service import SysLibrariesService
from .schema import SysLibrariesCreateSchema, SysLibrariesUpdateSchema, SysLibrariesQueryParam

SysLibrariesRouter = APIRouter(prefix='/sys_libraries', tags=["知识库定义模块"]) 

@SysLibrariesRouter.get("/detail/{id}", summary="获取知识库定义详情", description="获取知识库定义详情")
async def get_sys_libraries_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_libraries:query"]))
) -> JSONResponse:
    """获取知识库定义详情接口"""
    result_dict = await SysLibrariesService.detail_sys_libraries_service(auth=auth, id=id)
    log.info(f"获取知识库定义详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取知识库定义详情成功")

@SysLibrariesRouter.get("/list", summary="查询知识库定义列表", description="查询知识库定义列表")
async def get_sys_libraries_list_controller(
    page: PaginationQueryParam = Depends(),
    search: SysLibrariesQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_libraries:query"]))
) -> JSONResponse:
    """查询知识库定义列表接口（数据库分页）"""
    result_dict = await SysLibrariesService.page_sys_libraries_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询知识库定义列表成功")
    return SuccessResponse(data=result_dict, msg="查询知识库定义列表成功")

@SysLibrariesRouter.post("/create", summary="创建知识库定义", description="创建知识库定义")
async def create_sys_libraries_controller(
    data: SysLibrariesCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_libraries:create"]))
) -> JSONResponse:
    """创建知识库定义接口"""
    result_dict = await SysLibrariesService.create_sys_libraries_service(auth=auth, data=data)
    log.info("创建知识库定义成功")
    return SuccessResponse(data=result_dict, msg="创建知识库定义成功")

@SysLibrariesRouter.put("/update/{id}", summary="修改知识库定义", description="修改知识库定义")
async def update_sys_libraries_controller(
    data: SysLibrariesUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_libraries:update"]))
) -> JSONResponse:
    """修改知识库定义接口"""
    result_dict = await SysLibrariesService.update_sys_libraries_service(auth=auth, id=id, data=data)
    log.info("修改知识库定义成功")
    return SuccessResponse(data=result_dict, msg="修改知识库定义成功")

@SysLibrariesRouter.delete("/delete", summary="删除知识库定义", description="删除知识库定义")
async def delete_sys_libraries_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_libraries:delete"]))
) -> JSONResponse:
    """删除知识库定义接口"""
    await SysLibrariesService.delete_sys_libraries_service(auth=auth, ids=ids)
    log.info(f"删除知识库定义成功: {ids}")
    return SuccessResponse(msg="删除知识库定义成功")

@SysLibrariesRouter.patch("/available/setting", summary="批量修改知识库定义状态", description="批量修改知识库定义状态")
async def batch_set_available_sys_libraries_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_libraries:patch"]))
) -> JSONResponse:
    """批量修改知识库定义状态接口"""
    await SysLibrariesService.set_available_sys_libraries_service(auth=auth, data=data)
    log.info(f"批量修改知识库定义状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改知识库定义状态成功")

@SysLibrariesRouter.post('/export', summary="导出知识库定义", description="导出知识库定义")
async def export_sys_libraries_list_controller(
    search: SysLibrariesQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_libraries:export"]))
) -> StreamingResponse:
    """导出知识库定义接口"""
    result_dict_list = await SysLibrariesService.list_sys_libraries_service(search=search, auth=auth)
    export_result = await SysLibrariesService.batch_export_sys_libraries_service(obj_list=result_dict_list)
    log.info('导出知识库定义成功')

    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=sys_libraries.xlsx'
        }
    )

@SysLibrariesRouter.post('/import', summary="导入知识库定义", description="导入知识库定义")
async def import_sys_libraries_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_libraries:import"]))
) -> JSONResponse:
    """导入知识库定义接口"""
    batch_import_result = await SysLibrariesService.batch_import_sys_libraries_service(file=file, auth=auth, update_support=True)
    log.info("导入知识库定义成功")
    
    return SuccessResponse(data=batch_import_result, msg="导入知识库定义成功")

@SysLibrariesRouter.post('/download/template', summary="获取知识库定义导入模板", description="获取知识库定义导入模板", dependencies=[Depends(AuthPermission(["module_gencode:sys_libraries:download"]))])
async def export_sys_libraries_template_controller() -> StreamingResponse:
    """获取知识库定义导入模板接口"""
    import_template_result = await SysLibrariesService.import_template_download_sys_libraries_service()
    log.info('获取知识库定义导入模板成功')

    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=sys_libraries_template.xlsx'}
    )