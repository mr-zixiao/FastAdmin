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

from .service import SysDeptLibrariesService
from .schema import SysDeptLibrariesCreateSchema, SysDeptLibrariesUpdateSchema, SysDeptLibrariesQueryParam

SysDeptLibrariesRouter = APIRouter(prefix='/sys_dept_libraries', tags=["部门与知识库权限关联模块"]) 

@SysDeptLibrariesRouter.get("/detail/{id}", summary="获取部门与知识库权限关联详情", description="获取部门与知识库权限关联详情")
async def get_sys_dept_libraries_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_dept_libraries:query"]))
) -> JSONResponse:
    """获取部门与知识库权限关联详情接口"""
    result_dict = await SysDeptLibrariesService.detail_sys_dept_libraries_service(auth=auth, id=id)
    log.info(f"获取部门与知识库权限关联详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取部门与知识库权限关联详情成功")

@SysDeptLibrariesRouter.get("/list", summary="查询部门与知识库权限关联列表", description="查询部门与知识库权限关联列表")
async def get_sys_dept_libraries_list_controller(
    page: PaginationQueryParam = Depends(),
    search: SysDeptLibrariesQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_dept_libraries:query"]))
) -> JSONResponse:
    """查询部门与知识库权限关联列表接口（数据库分页）"""
    result_dict = await SysDeptLibrariesService.page_sys_dept_libraries_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询部门与知识库权限关联列表成功")
    return SuccessResponse(data=result_dict, msg="查询部门与知识库权限关联列表成功")

@SysDeptLibrariesRouter.post("/create", summary="创建部门与知识库权限关联", description="创建部门与知识库权限关联")
async def create_sys_dept_libraries_controller(
    data: SysDeptLibrariesCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_dept_libraries:create"]))
) -> JSONResponse:
    """创建部门与知识库权限关联接口"""
    result_dict = await SysDeptLibrariesService.create_sys_dept_libraries_service(auth=auth, data=data)
    log.info("创建部门与知识库权限关联成功")
    return SuccessResponse(data=result_dict, msg="创建部门与知识库权限关联成功")

@SysDeptLibrariesRouter.put("/update/{id}", summary="修改部门与知识库权限关联", description="修改部门与知识库权限关联")
async def update_sys_dept_libraries_controller(
    data: SysDeptLibrariesUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_dept_libraries:update"]))
) -> JSONResponse:
    """修改部门与知识库权限关联接口"""
    result_dict = await SysDeptLibrariesService.update_sys_dept_libraries_service(auth=auth, id=id, data=data)
    log.info("修改部门与知识库权限关联成功")
    return SuccessResponse(data=result_dict, msg="修改部门与知识库权限关联成功")

@SysDeptLibrariesRouter.delete("/delete", summary="删除部门与知识库权限关联", description="删除部门与知识库权限关联")
async def delete_sys_dept_libraries_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_dept_libraries:delete"]))
) -> JSONResponse:
    """删除部门与知识库权限关联接口"""
    await SysDeptLibrariesService.delete_sys_dept_libraries_service(auth=auth, ids=ids)
    log.info(f"删除部门与知识库权限关联成功: {ids}")
    return SuccessResponse(msg="删除部门与知识库权限关联成功")

@SysDeptLibrariesRouter.patch("/available/setting", summary="批量修改部门与知识库权限关联状态", description="批量修改部门与知识库权限关联状态")
async def batch_set_available_sys_dept_libraries_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_dept_libraries:patch"]))
) -> JSONResponse:
    """批量修改部门与知识库权限关联状态接口"""
    await SysDeptLibrariesService.set_available_sys_dept_libraries_service(auth=auth, data=data)
    log.info(f"批量修改部门与知识库权限关联状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改部门与知识库权限关联状态成功")

@SysDeptLibrariesRouter.post('/export', summary="导出部门与知识库权限关联", description="导出部门与知识库权限关联")
async def export_sys_dept_libraries_list_controller(
    search: SysDeptLibrariesQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_dept_libraries:export"]))
) -> StreamingResponse:
    """导出部门与知识库权限关联接口"""
    result_dict_list = await SysDeptLibrariesService.list_sys_dept_libraries_service(search=search, auth=auth)
    export_result = await SysDeptLibrariesService.batch_export_sys_dept_libraries_service(obj_list=result_dict_list)
    log.info('导出部门与知识库权限关联成功')

    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=sys_dept_libraries.xlsx'
        }
    )

@SysDeptLibrariesRouter.post('/import', summary="导入部门与知识库权限关联", description="导入部门与知识库权限关联")
async def import_sys_dept_libraries_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_dept_libraries:import"]))
) -> JSONResponse:
    """导入部门与知识库权限关联接口"""
    batch_import_result = await SysDeptLibrariesService.batch_import_sys_dept_libraries_service(file=file, auth=auth, update_support=True)
    log.info("导入部门与知识库权限关联成功")
    
    return SuccessResponse(data=batch_import_result, msg="导入部门与知识库权限关联成功")

@SysDeptLibrariesRouter.post('/download/template', summary="获取部门与知识库权限关联导入模板", description="获取部门与知识库权限关联导入模板", dependencies=[Depends(AuthPermission(["module_gencode:sys_dept_libraries:download"]))])
async def export_sys_dept_libraries_template_controller() -> StreamingResponse:
    """获取部门与知识库权限关联导入模板接口"""
    import_template_result = await SysDeptLibrariesService.import_template_download_sys_dept_libraries_service()
    log.info('获取部门与知识库权限关联导入模板成功')

    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=sys_dept_libraries_template.xlsx'}
    )