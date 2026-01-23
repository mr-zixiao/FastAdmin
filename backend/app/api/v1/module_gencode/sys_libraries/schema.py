# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query

from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema, UserBySchema

class SysLibrariesCreateSchema(BaseModel):
    """
    知识库定义新增模型
    """
    status: str = Field(default="0", description='是否启用(0:启用 1:禁用)')
    description: str | None = Field(default=None, max_length=255, description='备注/描述')
    lib_name: str = Field(default=..., description='知识库名称')
    collection_name: str = Field(default=..., description='向量数据库的集合名称')
    lib_type: str = Field(default=..., description='知识库类型(vector:向量库 text:文本库)')
    embedding_model: str = Field(default=..., description='嵌入模型名称')
    chunk_size: int = Field(default=..., description='文档切片大小')
    chunk_overlap: int = Field(default=..., description='文档切片重叠大小')
    similarity_threshold: int = Field(default=..., description='相似度阈值')
    max_chunks: int = Field(default=..., description='最大切片数量')


class SysLibrariesUpdateSchema(SysLibrariesCreateSchema):
    """
    知识库定义更新模型
    """
    ...


class SysLibrariesOutSchema(SysLibrariesCreateSchema, BaseSchema, UserBySchema):
    """
    知识库定义响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class SysLibrariesQueryParam:
    """知识库定义查询参数"""

    def __init__(
        self,
        status: str | None = Query(None, description="是否启用(0:启用 1:禁用)"),
        lib_name: str | None = Query(None, description="知识库名称"),
        collection_name: str | None = Query(None, description="向量数据库的集合名称"),
        lib_type: str | None = Query(None, description="知识库类型(vector:向量库 text:文本库)"),
        embedding_model: str | None = Query(None, description="嵌入模型名称"),
        created_id: int | None = Query(None, description="创建人ID"),
        updated_id: int | None = Query(None, description="更新人ID"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 模糊查询字段
        self.status = ("like", status)
        # 精确查询字段
        self.created_id = created_id
        # 精确查询字段
        self.updated_id = updated_id
        # 模糊查询字段
        self.lib_name = ("like", lib_name)
        # 模糊查询字段
        self.collection_name = ("like", collection_name)
        # 模糊查询字段
        self.lib_type = ("like", lib_type)
        # 模糊查询字段
        self.embedding_model = ("like", embedding_model)
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))
