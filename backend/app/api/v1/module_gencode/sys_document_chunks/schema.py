# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query

from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema, UserBySchema

class SysDocumentChunksCreateSchema(BaseModel):
    """
    文档切片明细新增模型
    """
    doc_id: int = Field(default=..., description='关联文档主表ID')
    vector_id: str = Field(default=..., description='关联向量数据库中的唯一ID')
    content: str = Field(default=..., description='切片原文内容')
    page_number: int = Field(default=..., description='所在文档原始页码')
    chunk_order: int = Field(default=..., description='在原文档中的切片顺序')
    token_count: int = Field(default=..., description='该切片的Token预估数量')
    status: str = Field(default="0", description='状态(0:启用 1:禁用)')
    description: str | None = Field(default=None, max_length=255, description='备注/描述')


class SysDocumentChunksUpdateSchema(SysDocumentChunksCreateSchema):
    """
    文档切片明细更新模型
    """
    ...


class SysDocumentChunksOutSchema(SysDocumentChunksCreateSchema, BaseSchema, UserBySchema):
    """
    文档切片明细响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class SysDocumentChunksQueryParam:
    """文档切片明细查询参数"""

    def __init__(
        self,
        vector_id: str | None = Query(None, description="关联向量数据库中的唯一ID"),
        status: str | None = Query(None, description="状态(0:启用 1:禁用)"),
        doc_id: int | None = Query(None, description="关联文档主表ID"),
        content: str | None = Query(None, description="切片原文内容"),
        page_number: int | None = Query(None, description="所在文档原始页码"),
        chunk_order: int | None = Query(None, description="在原文档中的切片顺序"),
        token_count: int | None = Query(None, description="该切片的Token预估数量"),
        created_id: int | None = Query(None, description="创建人ID"),
        updated_id: int | None = Query(None, description="更新人ID"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 精确查询字段
        self.doc_id = doc_id
        # 模糊查询字段
        self.vector_id = ("like", vector_id)
        # 精确查询字段
        self.content = content
        # 精确查询字段
        self.page_number = page_number
        # 精确查询字段
        self.chunk_order = chunk_order
        # 精确查询字段
        self.token_count = token_count
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
