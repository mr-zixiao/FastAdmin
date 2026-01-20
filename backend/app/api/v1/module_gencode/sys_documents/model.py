# -*- coding: utf-8 -*-

from sqlalchemy import String, DateTime, BigInteger, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class SysDocumentsModel(ModelMixin, UserMixin):
    """
    文档资产管理表
    """
    __tablename__: str = 'sys_documents'
    __table_args__: dict[str, str] = {'comment': '文档资产管理'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    lib_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='所属知识库ID')
    dept_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='所属部门ID(用于权限隔离)')
    file_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment='文件名')
    file_path: Mapped[str | None] = mapped_column(String(512), nullable=True, comment='存储路径(云端或本地路径)')
    file_size: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment='文件大小(Byte)')
    file_ext: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='文件后缀')
    file_hash: Mapped[str | None] = mapped_column(String(64), nullable=True, comment='文件Hash(用于秒传/去重)')
    chunk_count: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='切片数量')
    error_msg: Mapped[str | None] = mapped_column(Text, nullable=True, comment='失败原因描述')

