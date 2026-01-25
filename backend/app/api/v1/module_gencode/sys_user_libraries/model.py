# -*- coding: utf-8 -*-

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class SysUserLibrariesModel(ModelMixin, UserMixin):
    """
    用户与知识库关联表
    """
    __tablename__: str = 'sys_user_libraries'
    __table_args__: dict[str, str] = {'comment': '用户与知识库关联'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    user_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='用户ID')
    lib_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='知识库ID')
    privilege_type: Mapped[str | None] = mapped_column(String(50), nullable=True, comment='权限类型(read:只读 write:读写 admin:管理员)')

