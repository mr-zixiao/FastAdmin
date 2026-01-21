# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query

from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema, UserBySchema

class SysDeptLibrariesCreateSchema(BaseModel):
    """
    部门与知识库权限关联新增模型
    """
    dept_id: int = Field(default=..., description='部门ID')
    dept_code: str = Field(default=..., description='部门编码(冗余存储，便于检索匹配)')
    lib_id: int = Field(default=..., description='知识库ID')
    privilege_type: str = Field(default=..., description='权限类型(1:只读 2:可上传/管理文档 3:完全控制)')
    status: str = Field(default="0", description='状态(0:启用 1:禁用)')
    description: str | None = Field(default=None, max_length=255, description='备注/描述')


class SysDeptLibrariesUpdateSchema(SysDeptLibrariesCreateSchema):
    """
    部门与知识库权限关联更新模型
    """
    ...


class SysDeptLibrariesOutSchema(SysDeptLibrariesCreateSchema, BaseSchema, UserBySchema):
    """
    部门与知识库权限关联响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class SysDeptLibrariesQueryParam:
    """部门与知识库权限关联查询参数"""

    def __init__(
        self,
        dept_code: str | None = Query(None, description="部门编码(冗余存储，便于检索匹配)"),
        privilege_type: str | None = Query(None, description="权限类型(1:只读 2:可上传/管理文档 3:完全控制)"),
        status: str | None = Query(None, description="状态(0:启用 1:禁用)"),
        dept_id: int | None = Query(None, description="部门ID"),
        lib_id: int | None = Query(None, description="知识库ID"),
        created_id: int | None = Query(None, description="创建人ID"),
        updated_id: int | None = Query(None, description="更新人ID"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 精确查询字段
        self.dept_id = dept_id
        # 模糊查询字段
        self.dept_code = ("like", dept_code)
        # 精确查询字段
        self.lib_id = lib_id
        # 模糊查询字段
        self.privilege_type = ("like", privilege_type)
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
