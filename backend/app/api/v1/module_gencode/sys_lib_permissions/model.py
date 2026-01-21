# -*- coding: utf-8 -*-

from sqlalchemy import String, Integer, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class SysLibPermissionsModel(ModelMixin, UserMixin):
    """
    知识库多维权限授权表
    """
    __tablename__: str = 'sys_lib_permissions'
    __table_args__: dict[str, str] = {'comment': '知识库多维权限授权'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    target_type: Mapped[str | None] = mapped_column(String(10), nullable=True, comment='授权对象类型(1:部门 2:角色 3:用户)')
    target_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='对应对象的主键ID(sys_dept/sys_role/sys_user的ID)')
    lib_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='知识库主表ID')
    privilege_type: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='权限级别(1:查看/提问 2:上传/编辑文档 3:管理库配置)')

