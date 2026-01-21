# -*- coding: utf-8 -*-

from sqlalchemy import DateTime, Text, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class SysDeptLibrariesModel(ModelMixin, UserMixin):
    """
    部门与知识库权限关联表
    """
    __tablename__: str = 'sys_dept_libraries'
    __table_args__: dict[str, str] = {'comment': '部门与知识库权限关联'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    dept_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='部门ID')
    dept_code: Mapped[str | None] = mapped_column(String(64), nullable=True, comment='部门编码(冗余存储，便于检索匹配)')
    lib_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='知识库ID')
    privilege_type: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='权限类型(1:只读 2:可上传/管理文档 3:完全控制)')

