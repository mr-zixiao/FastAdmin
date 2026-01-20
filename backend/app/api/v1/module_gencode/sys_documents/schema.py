# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query

from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema, UserBySchema

class SysDocumentsCreateSchema(BaseModel):
    """
    文档资产管理新增模型
    """
    lib_id: int = Field(default=..., description='所属知识库ID')
    dept_id: int = Field(default=..., description='所属部门ID(用于权限隔离)')
    file_name: str = Field(default=..., description='文件名')
    file_path: str = Field(default=..., description='存储路径(云端或本地路径)')
    file_size: int = Field(default=..., description='文件大小(Byte)')
    file_ext: str = Field(default=..., description='文件后缀')
    file_hash: str = Field(default=..., description='文件Hash(用于秒传/去重)')
    status: str = Field(default="0", description='状态(0:待处理 1:解析中 2:向量化中 3:已就绪 4:失败)')
    chunk_count: int = Field(default=..., description='切片数量')
    error_msg: str = Field(default=..., description='失败原因描述')
    description: str | None = Field(default=None, max_length=255, description='备注/描述')


class SysDocumentsUpdateSchema(SysDocumentsCreateSchema):
    """
    文档资产管理更新模型
    """
    ...


class SysDocumentsOutSchema(SysDocumentsCreateSchema, BaseSchema, UserBySchema):
    """
    文档资产管理响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class SysDocumentsQueryParam:
    """文档资产管理查询参数"""

    def __init__(
        self,
        file_name: str | None = Query(None, description="文件名"),
        file_path: str | None = Query(None, description="存储路径(云端或本地路径)"),
        file_ext: str | None = Query(None, description="文件后缀"),
        file_hash: str | None = Query(None, description="文件Hash(用于秒传/去重)"),
        status: str | None = Query(None, description="状态(0:待处理 1:解析中 2:向量化中 3:已就绪 4:失败)"),
        error_msg: str | None = Query(None, description="失败原因描述"),
        lib_id: int | None = Query(None, description="所属知识库ID"),
        dept_id: int | None = Query(None, description="所属部门ID(用于权限隔离)"),
        file_size: int | None = Query(None, description="文件大小(Byte)"),
        chunk_count: int | None = Query(None, description="切片数量"),
        created_id: int | None = Query(None, description="创建人ID"),
        updated_id: int | None = Query(None, description="更新人ID"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 精确查询字段
        self.lib_id = lib_id
        # 精确查询字段
        self.dept_id = dept_id
        # 模糊查询字段
        self.file_name = ("like", file_name)
        # 模糊查询字段
        self.file_path = ("like", file_path)
        # 精确查询字段
        self.file_size = file_size
        # 模糊查询字段
        self.file_ext = ("like", file_ext)
        # 模糊查询字段
        self.file_hash = ("like", file_hash)
        # 模糊查询字段
        self.status = ("like", status)
        # 精确查询字段
        self.chunk_count = chunk_count
        # 模糊查询字段
        self.error_msg = ("like", error_msg)
        # 精确查询字段
        self.created_id = created_id
        # 精确查询字段
        self.updated_id = updated_id
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))
