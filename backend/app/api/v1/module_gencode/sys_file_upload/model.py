# -*- coding: utf-8 -*-

from sqlalchemy import DateTime, String, Integer, BigInteger, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class SysFileUploadModel(ModelMixin, UserMixin):
    """
    文件上传表
    """
    __tablename__: str = 'sys_file_upload'
    __table_args__: dict[str, str] = {'comment': '文件上传'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    origin_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment='原始文件名')
    file_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment='新文件名（生成后的文件名）')
    file_path: Mapped[str | None] = mapped_column(String(500), nullable=True, comment='文件存储路径')
    file_size: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment='文件大小（字节）')
    file_type: Mapped[str | None] = mapped_column(String(50), nullable=True, comment='文件类型/扩展名')

