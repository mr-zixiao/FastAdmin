# -*- coding: utf-8 -*-

from sqlalchemy import String, DateTime, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class SysDocumentChunksModel(ModelMixin, UserMixin):
    """
    文档切片明细表
    """
    __tablename__: str = 'sys_document_chunks'
    __table_args__: dict[str, str] = {'comment': '文档切片明细'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    doc_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='关联文档主表ID')
    vector_id: Mapped[str | None] = mapped_column(String(64), nullable=True, comment='关联向量数据库中的唯一ID')
    content: Mapped[str | None] = mapped_column(Text, nullable=True, comment='切片原文内容')
    page_number: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='所在文档原始页码')
    chunk_order: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='在原文档中的切片顺序')
    token_count: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='该切片的Token预估数量')

