/**
 * 分页查询参数
 */
export interface PageQuery {
  /** 当前页码 */
  page_no: number;
  /** 每页条数 */
  page_size: number;
}

/**
 * 分页响应对象
 */
export interface PageResult<T> {
  /** 数据列表 */
  items: T;
  /** 总数 */
  total: number;
  page_no: number;
  page_size: number;
  has_next: boolean;
}

/**
 * 创建人
 */
export interface CommonType {
  id?: number;
  name?: string;
}

/**
 * 基础类型
 */
export interface BaseType {
  index?: number;
  id?: number;
  uuid?: string;
  status?: string;
  description?: string;
  created_time?: string;
  updated_time?: string;
}

/**
 * 基础表单类型
 */
export interface BaseFormType {
  id?: number;
  status?: string;
  description?: string;
}

/**
 * 批量启用、停用
 */
export interface BatchType {
  ids?: number[];
  status?: string;
}

