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

from .service import SysUserLibrariesService
from .schema import SysUserLibrariesCreateSchema, SysUserLibrariesUpdateSchema, SysUserLibrariesQueryParam, SysUserLibrariesBatchAssociateSchema

SysUserLibrariesRouter = APIRouter(prefix='/sys_user_libraries', tags=["用户与知识库关联模块"]) 

@SysUserLibrariesRouter.get("/detail/{id}", summary="获取用户与知识库关联详情", description="获取用户与知识库关联详情")
async def get_sys_user_libraries_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_user_libraries:query"]))
) -> JSONResponse:
    """获取用户与知识库关联详情接口"""
    result_dict = await SysUserLibrariesService.detail_sys_user_libraries_service(auth=auth, id=id)
    log.info(f"获取用户与知识库关联详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取用户与知识库关联详情成功")

@SysUserLibrariesRouter.get("/list", summary="查询用户与知识库关联列表", description="查询用户与知识库关联列表")
async def get_sys_user_libraries_list_controller(
    page: PaginationQueryParam = Depends(),
    search: SysUserLibrariesQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_user_libraries:query"]))
) -> JSONResponse:
    """查询用户与知识库关联列表接口（数据库分页）"""
    result_dict = await SysUserLibrariesService.page_sys_user_libraries_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询用户与知识库关联列表成功")
    return SuccessResponse(data=result_dict, msg="查询用户与知识库关联列表成功")

@SysUserLibrariesRouter.post("/create", summary="创建用户与知识库关联", description="创建用户与知识库关联")
async def create_sys_user_libraries_controller(
    data: SysUserLibrariesCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_user_libraries:create"]))
) -> JSONResponse:
    """创建用户与知识库关联接口"""
    result_dict = await SysUserLibrariesService.create_sys_user_libraries_service(auth=auth, data=data)
    log.info("创建用户与知识库关联成功")
    return SuccessResponse(data=result_dict, msg="创建用户与知识库关联成功")

@SysUserLibrariesRouter.put("/update/{id}", summary="修改用户与知识库关联", description="修改用户与知识库关联")
async def update_sys_user_libraries_controller(
    data: SysUserLibrariesUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_user_libraries:update"]))
) -> JSONResponse:
    """修改用户与知识库关联接口"""
    result_dict = await SysUserLibrariesService.update_sys_user_libraries_service(auth=auth, id=id, data=data)
    log.info("修改用户与知识库关联成功")
    return SuccessResponse(data=result_dict, msg="修改用户与知识库关联成功")

@SysUserLibrariesRouter.delete("/delete", summary="删除用户与知识库关联", description="删除用户与知识库关联")
async def delete_sys_user_libraries_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_user_libraries:delete"]))
) -> JSONResponse:
    """删除用户与知识库关联接口"""
    await SysUserLibrariesService.delete_sys_user_libraries_service(auth=auth, ids=ids)
    log.info(f"删除用户与知识库关联成功: {ids}")
    return SuccessResponse(msg="删除用户与知识库关联成功")

@SysUserLibrariesRouter.patch("/available/setting", summary="批量修改用户与知识库关联状态", description="批量修改用户与知识库关联状态")
async def batch_set_available_sys_user_libraries_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_user_libraries:patch"]))
) -> JSONResponse:
    """批量修改用户与知识库关联状态接口"""
    await SysUserLibrariesService.set_available_sys_user_libraries_service(auth=auth, data=data)
    log.info(f"批量修改用户与知识库关联状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改用户与知识库关联状态成功")

@SysUserLibrariesRouter.post('/export', summary="导出用户与知识库关联", description="导出用户与知识库关联")
async def export_sys_user_libraries_list_controller(
    search: SysUserLibrariesQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_user_libraries:export"]))
) -> StreamingResponse:
    """导出用户与知识库关联接口"""
    result_dict_list = await SysUserLibrariesService.list_sys_user_libraries_service(search=search, auth=auth)
    export_result = await SysUserLibrariesService.batch_export_sys_user_libraries_service(obj_list=result_dict_list)
    log.info('导出用户与知识库关联成功')

    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=sys_user_libraries.xlsx'
        }
    )

@SysUserLibrariesRouter.post('/import', summary="导入用户与知识库关联", description="导入用户与知识库关联")
async def import_sys_user_libraries_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_user_libraries:import"]))
) -> JSONResponse:
    """导入用户与知识库关联接口"""
    batch_import_result = await SysUserLibrariesService.batch_import_sys_user_libraries_service(file=file, auth=auth, update_support=True)
    log.info("导入用户与知识库关联成功")
    
    return SuccessResponse(data=batch_import_result, msg="导入用户与知识库关联成功")

@SysUserLibrariesRouter.post('/batch/associate', summary="批量关联用户与知识库", description="批量关联用户与知识库")
async def batch_associate_sys_user_libraries_controller(
    data: SysUserLibrariesBatchAssociateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_user_libraries:create"]))
) -> JSONResponse:
    """批量关联用户与知识库接口"""
    result_dict = await SysUserLibrariesService.batch_associate_sys_user_libraries_service(auth=auth, data=data)
    log.info(f"批量关联用户与知识库成功: {result_dict.get('success_count', 0)} 个用户")
    return SuccessResponse(data=result_dict, msg=result_dict.get('message', '批量关联用户与知识库成功'))

@SysUserLibrariesRouter.post('/download/template', summary="获取用户与知识库关联导入模板", description="获取用户与知识库关联导入模板", dependencies=[Depends(AuthPermission(["module_gencode:sys_user_libraries:download"]))])
async def export_sys_user_libraries_template_controller() -> StreamingResponse:
    """获取用户与知识库关联导入模板接口"""
    import_template_result = await SysUserLibrariesService.import_template_download_sys_user_libraries_service()
    log.info('获取用户与知识库关联导入模板成功')

    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=sys_user_libraries_template.xlsx'}
    )