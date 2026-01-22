# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query

from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema, UserBySchema


class SysLibrariesCreateSchema(BaseModel):
    """
    知识库定义新增模型
    """
    name: str = Field(default=..., description='知识库名称')
    collection_name: str = Field(default=..., description='对应向量库Collection名称')
    status: str = Field(default="0", description='状态(0:启用 1:禁用)')


class SysLibrariesWithPermissionCreateSchema(SysLibrariesCreateSchema):
    """
    带权限关联的知识库创建模型
    """
    target_type: str | None = Field(
        default=None, description='授权对象类型(1:部门 2:角色 3:用户)')
    target_ids: str | None = Field(
        default=None, description='对应对象的主键ID序列(sys_dept/sys_role/sys_user的ID)')
    privilege_type: str | None = Field(
        default=None, description='权限级别(1:查看/提问 2:上传/编辑文档 3:管理库配置)')


class SysLibrariesWithPermissionUpdateSchema(SysLibrariesCreateSchema):
    """
    带权限关联的知识库更新模型
    """
    target_type: str | None = Field(
        default=None, description='授权对象类型(1:部门 2:角色 3:用户)')
    target_ids: str | None = Field(
        default=None, description='对应对象的主键ID序列(sys_dept/sys_role/sys_user的ID)')
    privilege_type: str | None = Field(
        default=None, description='权限级别(1:查看/提问 2:上传/编辑文档 3:管理库配置)')


# 保持原有更新模型兼容性
SysLibrariesUpdateSchema = SysLibrariesWithPermissionUpdateSchema


class SysLibrariesOutSchema(SysLibrariesCreateSchema, BaseSchema, UserBySchema):
    """
    知识库定义响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class SysLibrariesQueryParam:
    """知识库定义查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="知识库名称"),
        collection_name: str | None = Query(
            None, description="对应向量库Collection名称"),
        status: str | None = Query(None, description="状态(0:启用 1:禁用)"),
        created_id: int | None = Query(None, description="创建人ID"),
        updated_id: int | None = Query(None, description="更新人ID"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=[
                                                       "2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=[
                                                       "2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 模糊查询字段
        self.name = ("like", name)
        # 模糊查询字段
        self.collection_name = ("like", collection_name)
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
