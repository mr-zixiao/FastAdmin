# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query

from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema, UserBySchema


class SysDocumentsCreateSchema(BaseModel):
    """
    文档管理新增模型
    """
    lib_id: int = Field(default=..., description='知识库ID')
    file_upload_id: int = Field(default=..., description='文件上传ID')
    chunk_size: int | None = Field(default=None, description='文档切片大小')
    chunk_overlap: int | None = Field(default=None, description='文档切片重叠大小')
    processing_status: str = Field(default='pending',
                                   description='处理状态(pending:待处理 processing:处理中 completed:已完成 failed:处理失败)')
    error_msg: str | None = Field(default=None, description='错误信息（处理失败时）')
    status: str = Field(default="0", description='是否启用(0:启用 1:禁用)')
    description: str | None = Field(default=None, max_length=255, description='备注/描述')


class SysDocumentsUpdateSchema(SysDocumentsCreateSchema):
    """
    文档管理更新模型
    """
    ...


class SysDocumentsOutSchema(SysDocumentsCreateSchema, BaseSchema, UserBySchema):
    """
    文档管理响应模型
    """
    file_info: dict | None = Field(default=None, description='文件信息')
    model_config = ConfigDict(from_attributes=True)


class SysDocumentsQueryParam:
    """文档管理查询参数"""

    def __init__(
            self,
            processing_status: str | None = Query(None,
                                                  description="处理状态(pending:待处理 processing:处理中 completed:已完成 failed:处理失败)"),
            error_msg: str | None = Query(None, description="错误信息（处理失败时）"),
            status: str | None = Query(None, description="是否启用(0:启用 1:禁用)"),
            lib_id: int | None = Query(None, description="知识库ID"),
            file_upload_id: int | None = Query(None, description="文件上传ID"),
            chunk_size: int | None = Query(None, description="文档切片大小"),
            chunk_overlap: int | None = Query(None, description="文档切片重叠大小"),
            created_id: int | None = Query(None, description="创建人ID"),
            updated_id: int | None = Query(None, description="更新人ID"),
            created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围",
                                                           examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
            updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围",
                                                           examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 精确查询字段
        self.lib_id = lib_id
        # 精确查询字段
        self.file_upload_id = file_upload_id
        # 精确查询字段
        self.chunk_size = chunk_size
        # 精确查询字段
        self.chunk_overlap = chunk_overlap
        # 模糊查询字段
        self.processing_status = ("like", processing_status)
        # 模糊查询字段
        self.error_msg = ("like", error_msg)
        # 模糊查询字段
        self.status = ("like", status)
        # 精确查询字段
        self.created_id = created_id
        # 精确查询字段
        self.updated_id = updated_id
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))
