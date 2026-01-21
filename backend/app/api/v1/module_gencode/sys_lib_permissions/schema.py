# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query

from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema, UserBySchema

class SysLibPermissionsCreateSchema(BaseModel):
    """
    知识库多维权限授权新增模型
    """
    target_type: str = Field(default=..., description='授权对象类型(1:部门 2:角色 3:用户)')
    target_id: int = Field(default=..., description='对应对象的主键ID(sys_dept/sys_role/sys_user的ID)')
    lib_id: int = Field(default=..., description='知识库主表ID')
    privilege_type: str = Field(default=..., description='权限级别(1:查看/提问 2:上传/编辑文档 3:管理库配置)')
    status: str = Field(default="0", description='状态(0:启用 1:禁用)')
    description: str | None = Field(default=None, max_length=255, description='备注/描述')


class SysLibPermissionsUpdateSchema(SysLibPermissionsCreateSchema):
    """
    知识库多维权限授权更新模型
    """
    ...


class SysLibPermissionsOutSchema(SysLibPermissionsCreateSchema, BaseSchema, UserBySchema):
    """
    知识库多维权限授权响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class SysLibPermissionsQueryParam:
    """知识库多维权限授权查询参数"""

    def __init__(
        self,
        target_type: str | None = Query(None, description="授权对象类型(1:部门 2:角色 3:用户)"),
        privilege_type: str | None = Query(None, description="权限级别(1:查看/提问 2:上传/编辑文档 3:管理库配置)"),
        status: str | None = Query(None, description="状态(0:启用 1:禁用)"),
        target_id: int | None = Query(None, description="对应对象的主键ID(sys_dept/sys_role/sys_user的ID)"),
        lib_id: int | None = Query(None, description="知识库主表ID"),
        created_id: int | None = Query(None, description="创建人ID"),
        updated_id: int | None = Query(None, description="更新人ID"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 模糊查询字段
        self.target_type = ("like", target_type)
        # 精确查询字段
        self.target_id = target_id
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
