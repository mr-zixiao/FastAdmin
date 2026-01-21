# -*- coding: utf-8 -*-

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class SysLibrariesModel(ModelMixin, UserMixin):
    """
    知识库定义表
    """
    __tablename__: str = 'sys_libraries'
    __table_args__: dict[str, str] = {'comment': '知识库定义'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str | None] = mapped_column(String(100), nullable=True, comment='知识库名称')
    collection_name: Mapped[str | None] = mapped_column(String(128), nullable=True, comment='对应向量库Collection名称')

