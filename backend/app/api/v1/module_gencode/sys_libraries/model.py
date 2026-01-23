# -*- coding: utf-8 -*-

from sqlalchemy import DateTime, DECIMAL, Text, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class SysLibrariesModel(ModelMixin, UserMixin):
    """
    知识库定义表
    """
    __tablename__: str = 'sys_libraries'
    __table_args__: dict[str, str] = {'comment': '知识库定义'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    lib_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment='知识库名称')
    collection_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment='向量数据库的集合名称')
    lib_type: Mapped[str | None] = mapped_column(String(50), nullable=True, comment='知识库类型(vector:向量库 text:文本库)')
    embedding_model: Mapped[str | None] = mapped_column(String(100), nullable=True, comment='嵌入模型名称')
    chunk_size: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='文档切片大小')
    chunk_overlap: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='文档切片重叠大小')
    similarity_threshold: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='相似度阈值')
    max_chunks: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='最大切片数量')

