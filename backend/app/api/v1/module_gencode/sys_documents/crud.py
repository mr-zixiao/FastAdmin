# -*- coding: utf-8 -*-

from typing import Sequence

from app.core.base_crud import CRUDBase
from app.api.v1.module_system.auth.schema import AuthSchema
from .model import SysDocumentsModel
from .schema import SysDocumentsCreateSchema, SysDocumentsUpdateSchema, SysDocumentsOutSchema


class SysDocumentsCRUD(CRUDBase[SysDocumentsModel, SysDocumentsCreateSchema, SysDocumentsUpdateSchema]):
    """文档管理数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """
        初始化CRUD数据层
        
        参数:
        - auth (AuthSchema): 认证信息模型
        """
        super().__init__(model=SysDocumentsModel, auth=auth)

    async def get_by_id_sys_documents_crud(self, id: int, preload: list | None = None) -> SysDocumentsModel | None:
        """
        详情
        
        参数:
        - id (int): 对象ID
        - preload (list | None): 预加载关系，未提供时使用模型默认项
        
        返回:
        - SysDocumentsModel | None: 模型实例或None
        """
        return await self.get(id=id, preload=preload)
    
    async def list_sys_documents_crud(self, search: dict | None = None, order_by: list[dict] | None = None, preload: list | None = None) -> Sequence[SysDocumentsModel]:
        """
        列表查询
        
        参数:
        - search (dict | None): 查询参数
        - order_by (list[dict] | None): 排序参数，未提供时使用模型默认项
        - preload (list | None): 预加载关系，未提供时使用模型默认项
        
        返回:
        - Sequence[SysDocumentsModel]: 模型实例序列
        """
        return await self.list(search=search, order_by=order_by, preload=preload)
    
    async def create_sys_documents_crud(self, data: SysDocumentsCreateSchema) -> SysDocumentsModel | None:
        """
        创建
        
        参数:
        - data (SysDocumentsCreateSchema): 创建模型
        
        返回:
        - SysDocumentsModel | None: 模型实例或None
        """
        return await self.create(data=data)
    
    async def update_sys_documents_crud(self, id: int, data: SysDocumentsUpdateSchema) -> SysDocumentsModel | None:
        """
        更新
        
        参数:
        - id (int): 对象ID
        - data (SysDocumentsUpdateSchema): 更新模型
        
        返回:
        - SysDocumentsModel | None: 模型实例或None
        """
        return await self.update(id=id, data=data)
    
    async def delete_sys_documents_crud(self, ids: list[int]) -> None:
        """
        批量删除
        
        参数:
        - ids (list[int]): 对象ID列表
        
        返回:
        - None
        """
        return await self.delete(ids=ids)
    
    async def set_available_sys_documents_crud(self, ids: list[int], status: str) -> None:
        """
        批量设置可用状态
        
        参数:
        - ids (list[int]): 对象ID列表
        - status (str): 可用状态
        
        返回:
        - None
        """
        return await self.set(ids=ids, status=status)
    
    async def page_sys_documents_crud(self, offset: int, limit: int, order_by: list[dict] | None = None, search: dict | None = None, preload: list | None = None) -> dict:
        """
        分页查询（返回原始对象，用于后续处理文件信息）
        
        参数:
        - offset (int): 偏移量
        - limit (int): 每页数量
        - order_by (list[dict] | None): 排序参数，未提供时使用模型默认项
        - search (dict | None): 查询参数，未提供时查询所有
        - preload (list | None): 预加载关系，未提供时使用模型默认项
        
        返回:
        - Dict: 分页数据（包含原始对象列表）
        """
        from sqlalchemy import func, select
        from sqlalchemy import inspect as sa_inspect
        from app.core.exceptions import CustomException
        
        try:
            conditions = await self._CRUDBase__build_conditions(**search) if search else []
            order = order_by or [{'id': 'asc'}]
            sql = select(self.model).where(*conditions).order_by(*self._CRUDBase__order_by(order))
            # 应用预加载选项
            for opt in self._CRUDBase__loader_options(preload):
                sql = sql.options(opt)
            sql = await self._CRUDBase__filter_permissions(sql)

            # 优化count查询：使用主键计数而非全表扫描
            mapper = sa_inspect(self.model)
            pk_cols = list(getattr(mapper, "primary_key", []))
            if pk_cols:
                # 使用主键的第一列进行计数（主键必定非NULL，性能更好）
                count_sql = select(func.count(pk_cols[0])).select_from(self.model)
            else:
                # 降级方案：使用count(*)
                count_sql = select(func.count()).select_from(self.model)
            
            if conditions:
                count_sql = count_sql.where(*conditions)
            count_sql = await self._CRUDBase__filter_permissions(count_sql)
            
            total_result = await self.auth.db.execute(count_sql)
            total = total_result.scalar() or 0

            result = await self.auth.db.execute(sql.offset(offset).limit(limit))
            objs = result.scalars().all()

            return {
                "page_no": offset // limit + 1 if limit else 1,
                "page_size": limit if limit else 10,
                "total": total,
                "has_next": offset + limit < total,
                "items": objs,  # 返回原始对象列表
                "_raw_items": True  # 标记为原始对象，需要在service层处理
            }
        except Exception as e:
            raise CustomException(msg=f"分页查询失败: {str(e)}")