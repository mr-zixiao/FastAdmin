# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from sqlalchemy import Text, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_model import ModelMixin, UserMixin

if TYPE_CHECKING:
    from app.api.v1.module_gencode.sys_file_upload.model import SysFileUploadModel


class SysDocumentsModel(ModelMixin, UserMixin):
    """
    文档管理表
    """
    __tablename__: str = 'sys_documents'
    __table_args__: dict[str, str] = {'comment': '文档管理'}
    __loader_options__: list[str] = ["created_by", "updated_by", "file_upload"]

    lib_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='知识库ID')
    file_upload_id: Mapped[int | None] = mapped_column(
        Integer, 
        ForeignKey('sys_file_upload.id', ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True, 
        comment='文件上传ID'
    )
    chunk_size: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='文档切片大小')
    chunk_overlap: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='文档切片重叠大小')
    processing_status: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='处理状态(pending:待处理 processing:处理中 completed:已完成 failed:处理失败)')
    error_msg: Mapped[str | None] = mapped_column(Text, nullable=True, comment='错误信息（处理失败时）')
    
    # 关联关系
    file_upload: Mapped["SysFileUploadModel | None"] = relationship(
        "SysFileUploadModel",
        foreign_keys=[file_upload_id],
        lazy="selectin",
        uselist=False
    )

