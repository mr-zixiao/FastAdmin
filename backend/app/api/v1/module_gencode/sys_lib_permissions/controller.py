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

from .service import SysLibPermissionsService
from .schema import SysLibPermissionsCreateSchema, SysLibPermissionsUpdateSchema, SysLibPermissionsQueryParam

SysLibPermissionsRouter = APIRouter(prefix='/sys_lib_permissions', tags=["知识库多维权限授权模块"]) 

@SysLibPermissionsRouter.get("/detail/{id}", summary="获取知识库多维权限授权详情", description="获取知识库多维权限授权详情")
async def get_sys_lib_permissions_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_lib_permissions:query"]))
) -> JSONResponse:
    """获取知识库多维权限授权详情接口"""
    result_dict = await SysLibPermissionsService.detail_sys_lib_permissions_service(auth=auth, id=id)
    log.info(f"获取知识库多维权限授权详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取知识库多维权限授权详情成功")

@SysLibPermissionsRouter.get("/list", summary="查询知识库多维权限授权列表", description="查询知识库多维权限授权列表")
async def get_sys_lib_permissions_list_controller(
    page: PaginationQueryParam = Depends(),
    search: SysLibPermissionsQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_lib_permissions:query"]))
) -> JSONResponse:
    """查询知识库多维权限授权列表接口（数据库分页）"""
    result_dict = await SysLibPermissionsService.page_sys_lib_permissions_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询知识库多维权限授权列表成功")
    return SuccessResponse(data=result_dict, msg="查询知识库多维权限授权列表成功")

@SysLibPermissionsRouter.post("/create", summary="创建知识库多维权限授权", description="创建知识库多维权限授权")
async def create_sys_lib_permissions_controller(
    data: SysLibPermissionsCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_lib_permissions:create"]))
) -> JSONResponse:
    """创建知识库多维权限授权接口"""
    result_dict = await SysLibPermissionsService.create_sys_lib_permissions_service(auth=auth, data=data)
    log.info("创建知识库多维权限授权成功")
    return SuccessResponse(data=result_dict, msg="创建知识库多维权限授权成功")

@SysLibPermissionsRouter.put("/update/{id}", summary="修改知识库多维权限授权", description="修改知识库多维权限授权")
async def update_sys_lib_permissions_controller(
    data: SysLibPermissionsUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_lib_permissions:update"]))
) -> JSONResponse:
    """修改知识库多维权限授权接口"""
    result_dict = await SysLibPermissionsService.update_sys_lib_permissions_service(auth=auth, id=id, data=data)
    log.info("修改知识库多维权限授权成功")
    return SuccessResponse(data=result_dict, msg="修改知识库多维权限授权成功")

@SysLibPermissionsRouter.delete("/delete", summary="删除知识库多维权限授权", description="删除知识库多维权限授权")
async def delete_sys_lib_permissions_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_lib_permissions:delete"]))
) -> JSONResponse:
    """删除知识库多维权限授权接口"""
    await SysLibPermissionsService.delete_sys_lib_permissions_service(auth=auth, ids=ids)
    log.info(f"删除知识库多维权限授权成功: {ids}")
    return SuccessResponse(msg="删除知识库多维权限授权成功")

@SysLibPermissionsRouter.patch("/available/setting", summary="批量修改知识库多维权限授权状态", description="批量修改知识库多维权限授权状态")
async def batch_set_available_sys_lib_permissions_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_lib_permissions:patch"]))
) -> JSONResponse:
    """批量修改知识库多维权限授权状态接口"""
    await SysLibPermissionsService.set_available_sys_lib_permissions_service(auth=auth, data=data)
    log.info(f"批量修改知识库多维权限授权状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改知识库多维权限授权状态成功")

@SysLibPermissionsRouter.post('/export', summary="导出知识库多维权限授权", description="导出知识库多维权限授权")
async def export_sys_lib_permissions_list_controller(
    search: SysLibPermissionsQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_lib_permissions:export"]))
) -> StreamingResponse:
    """导出知识库多维权限授权接口"""
    result_dict_list = await SysLibPermissionsService.list_sys_lib_permissions_service(search=search, auth=auth)
    export_result = await SysLibPermissionsService.batch_export_sys_lib_permissions_service(obj_list=result_dict_list)
    log.info('导出知识库多维权限授权成功')

    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=sys_lib_permissions.xlsx'
        }
    )

@SysLibPermissionsRouter.post('/import', summary="导入知识库多维权限授权", description="导入知识库多维权限授权")
async def import_sys_lib_permissions_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_lib_permissions:import"]))
) -> JSONResponse:
    """导入知识库多维权限授权接口"""
    batch_import_result = await SysLibPermissionsService.batch_import_sys_lib_permissions_service(file=file, auth=auth, update_support=True)
    log.info("导入知识库多维权限授权成功")
    
    return SuccessResponse(data=batch_import_result, msg="导入知识库多维权限授权成功")

@SysLibPermissionsRouter.post('/download/template', summary="获取知识库多维权限授权导入模板", description="获取知识库多维权限授权导入模板", dependencies=[Depends(AuthPermission(["module_gencode:sys_lib_permissions:download"]))])
async def export_sys_lib_permissions_template_controller() -> StreamingResponse:
    """获取知识库多维权限授权导入模板接口"""
    import_template_result = await SysLibPermissionsService.import_template_download_sys_lib_permissions_service()
    log.info('获取知识库多维权限授权导入模板成功')

    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=sys_lib_permissions_template.xlsx'}
    )