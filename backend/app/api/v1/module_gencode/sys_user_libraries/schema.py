# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query

from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema, UserBySchema

class SysUserLibrariesCreateSchema(BaseModel):
    """
    用户与知识库关联新增模型
    """
    user_id: int = Field(default=..., description='用户ID')
    lib_id: int = Field(default=..., description='知识库ID')
    privilege_type: str = Field(default=..., description='权限类型(read:只读 write:读写 admin:管理员)')
    status: str = Field(default="0", description='是否启用(0:启用 1:禁用)')
    description: str | None = Field(default=None, max_length=255, description='备注/描述')


class SysUserLibrariesUpdateSchema(SysUserLibrariesCreateSchema):
    """
    用户与知识库关联更新模型
    """
    ...


class SysUserLibrariesOutSchema(SysUserLibrariesCreateSchema, BaseSchema, UserBySchema):
    """
    用户与知识库关联响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class SysUserLibrariesQueryParam:
    """用户与知识库关联查询参数"""

    def __init__(
        self,
        privilege_type: str | None = Query(None, description="权限类型(read:只读 write:读写 admin:管理员)"),
        status: str | None = Query(None, description="是否启用(0:启用 1:禁用)"),
        user_id: int | None = Query(None, description="用户ID"),
        lib_id: int | None = Query(None, description="知识库ID"),
        created_id: int | None = Query(None, description="创建人ID"),
        updated_id: int | None = Query(None, description="更新人ID"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 精确查询字段
        self.user_id = user_id
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


class SysUserLibrariesBatchAssociateSchema(BaseModel):
    """
    批量关联用户与知识库模型
    """
    user_ids: list[int] = Field(default=..., description='用户ID列表')
    lib_id: int = Field(default=..., description='知识库ID')
    privilege_type: str = Field(default=..., description='权限类型(使用字典sys_lib_privilege_type)')
    status: str = Field(default="0", description='是否启用(0:启用 1:禁用)')
    description: str | None = Field(default=None, max_length=255, description='备注/描述')