# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query

from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema, UserBySchema

class SysFileUploadCreateSchema(BaseModel):
    """
    文件上传新增模型
    """
    origin_name: str = Field(default=..., description='原始文件名')
    file_name: str = Field(default=..., description='新文件名（生成后的文件名）')
    file_path: str = Field(default=..., description='文件存储路径')
    file_size: int = Field(default=..., description='文件大小（字节）')
    file_type: str = Field(default=..., description='文件类型/扩展名')
    status: str = Field(default="0", description='是否启用(0:启用 1:禁用)')
    description: str | None = Field(default=None, max_length=255, description='备注/描述')


class SysFileUploadUpdateSchema(SysFileUploadCreateSchema):
    """
    文件上传更新模型
    """
    ...


class SysFileUploadOutSchema(SysFileUploadCreateSchema, BaseSchema, UserBySchema):
    """
    文件上传响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class SysFileUploadQueryParam:
    """文件上传查询参数"""

    def __init__(
        self,
        origin_name: str | None = Query(None, description="原始文件名"),
        file_name: str | None = Query(None, description="新文件名（生成后的文件名）"),
        file_path: str | None = Query(None, description="文件存储路径"),
        file_type: str | None = Query(None, description="文件类型/扩展名"),
        status: str | None = Query(None, description="是否启用(0:启用 1:禁用)"),
        file_size: int | None = Query(None, description="文件大小（字节）"),
        created_id: int | None = Query(None, description="创建人ID"),
        updated_id: int | None = Query(None, description="更新人ID"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 模糊查询字段
        self.origin_name = ("like", origin_name)
        # 模糊查询字段
        self.file_name = ("like", file_name)
        # 模糊查询字段
        self.file_path = ("like", file_path)
        # 精确查询字段
        self.file_size = file_size
        # 模糊查询字段
        self.file_type = ("like", file_type)
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
