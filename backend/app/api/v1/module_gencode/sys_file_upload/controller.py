# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, UploadFile, Body, Path, Query, Form
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse

from app.common.response import SuccessResponse, StreamResponse
from app.core.dependencies import AuthPermission
from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_params import PaginationQueryParam
from app.utils.common_util import bytes2file_response
from app.core.logger import log
from app.core.base_schema import BatchSetAvailable

from .service import SysFileUploadService
from .schema import SysFileUploadCreateSchema, SysFileUploadUpdateSchema, SysFileUploadQueryParam

SysFileUploadRouter = APIRouter(prefix='/sys_file_upload', tags=["文件上传模块"]) 

@SysFileUploadRouter.get("/detail/{id}", summary="获取文件上传详情", description="获取文件上传详情")
async def get_sys_file_upload_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_file_upload:query"]))
) -> JSONResponse:
    """获取文件上传详情接口"""
    result_dict = await SysFileUploadService.detail_sys_file_upload_service(auth=auth, id=id)
    log.info(f"获取文件上传详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取文件上传详情成功")

@SysFileUploadRouter.get("/list", summary="查询文件上传列表", description="查询文件上传列表")
async def get_sys_file_upload_list_controller(
    page: PaginationQueryParam = Depends(),
    search: SysFileUploadQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_file_upload:query"]))
) -> JSONResponse:
    """查询文件上传列表接口（数据库分页）"""
    result_dict = await SysFileUploadService.page_sys_file_upload_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询文件上传列表成功")
    return SuccessResponse(data=result_dict, msg="查询文件上传列表成功")

@SysFileUploadRouter.post("/create", summary="创建文件上传", description="创建文件上传")
async def create_sys_file_upload_controller(
    data: SysFileUploadCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_file_upload:create"]))
) -> JSONResponse:
    """创建文件上传接口"""
    result_dict = await SysFileUploadService.create_sys_file_upload_service(auth=auth, data=data)
    log.info("创建文件上传成功")
    return SuccessResponse(data=result_dict, msg="创建文件上传成功")

@SysFileUploadRouter.put("/update/{id}", summary="修改文件上传", description="修改文件上传")
async def update_sys_file_upload_controller(
    data: SysFileUploadUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_file_upload:update"]))
) -> JSONResponse:
    """修改文件上传接口"""
    result_dict = await SysFileUploadService.update_sys_file_upload_service(auth=auth, id=id, data=data)
    log.info("修改文件上传成功")
    return SuccessResponse(data=result_dict, msg="修改文件上传成功")

@SysFileUploadRouter.delete("/delete", summary="删除文件上传", description="删除文件上传")
async def delete_sys_file_upload_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_file_upload:delete"]))
) -> JSONResponse:
    """删除文件上传接口"""
    await SysFileUploadService.delete_sys_file_upload_service(auth=auth, ids=ids)
    log.info(f"删除文件上传成功: {ids}")
    return SuccessResponse(msg="删除文件上传成功")

@SysFileUploadRouter.patch("/available/setting", summary="批量修改文件上传状态", description="批量修改文件上传状态")
async def batch_set_available_sys_file_upload_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_file_upload:patch"]))
) -> JSONResponse:
    """批量修改文件上传状态接口"""
    await SysFileUploadService.set_available_sys_file_upload_service(auth=auth, data=data)
    log.info(f"批量修改文件上传状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改文件上传状态成功")

@SysFileUploadRouter.post('/export', summary="导出文件上传", description="导出文件上传")
async def export_sys_file_upload_list_controller(
    search: SysFileUploadQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_file_upload:export"]))
) -> StreamingResponse:
    """导出文件上传接口"""
    result_dict_list = await SysFileUploadService.list_sys_file_upload_service(search=search, auth=auth)
    export_result = await SysFileUploadService.batch_export_sys_file_upload_service(obj_list=result_dict_list)
    log.info('导出文件上传成功')

    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=sys_file_upload.xlsx'
        }
    )

@SysFileUploadRouter.post('/import', summary="导入文件上传", description="导入文件上传")
async def import_sys_file_upload_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_file_upload:import"]))
) -> JSONResponse:
    """导入文件上传接口"""
    batch_import_result = await SysFileUploadService.batch_import_sys_file_upload_service(file=file, auth=auth, update_support=True)
    log.info("导入文件上传成功")
    
    return SuccessResponse(data=batch_import_result, msg="导入文件上传成功")

@SysFileUploadRouter.post('/download/template', summary="获取文件上传导入模板", description="获取文件上传导入模板", dependencies=[Depends(AuthPermission(["module_gencode:sys_file_upload:download"]))])
async def export_sys_file_upload_template_controller() -> StreamingResponse:
    """获取文件上传导入模板接口"""
    import_template_result = await SysFileUploadService.import_template_download_sys_file_upload_service()
    log.info('获取文件上传导入模板成功')

    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=sys_file_upload_template.xlsx'}
    )

@SysFileUploadRouter.post("/upload/file", summary="上传文件", description="上传文件，以ID命名", dependencies=[Depends(AuthPermission(["module_gencode:sys_file_upload:upload"]))])
async def upload_file_controller(
    file: UploadFile,
    description: str | None = Form(None, description="文件描述"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_file_upload:upload"]))
) -> JSONResponse:
    """
    上传文件接口
    
    参数:
    - file (UploadFile): 上传的文件
    - description (str | None): 文件描述
    - auth (AuthSchema): 认证信息
    
    返回:
    - JSONResponse: 包含文件信息的JSON响应
    """
    result_dict = await SysFileUploadService.upload_file_service(auth=auth, file=file, description=description)
    log.info(f"文件上传成功: {result_dict.get('id')}")
    return SuccessResponse(data=result_dict, msg="文件上传成功")

@SysFileUploadRouter.get("/file/{id}", summary="访问文件", description="通过ID访问文件", dependencies=[Depends(AuthPermission(["module_gencode:sys_file_upload:query"]))])
async def get_file_controller(
    id: int = Path(..., description="文件ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:sys_file_upload:query"]))
) -> FileResponse:
    """
    通过ID访问文件接口
    
    参数:
    - id (int): 文件ID
    - auth (AuthSchema): 认证信息
    
    返回:
    - FileResponse: 文件响应
    """
    file_path = await SysFileUploadService.get_file_path_service(auth=auth, id=id)
    
    # 获取文件信息以确定文件名
    obj = await SysFileUploadService.detail_sys_file_upload_service(auth=auth, id=id)
    filename = obj.get('origin_name', f'file_{id}')
    
    log.info(f"访问文件成功: ID={id}, 文件名={filename}")
    
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type='application/octet-stream'
    )