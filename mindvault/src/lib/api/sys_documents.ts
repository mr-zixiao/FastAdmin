import { httpRequest, httpRequestBlob } from "./http";
import type {
  PageQuery,
  PageResult,
  BaseType,
  BaseFormType,
  CommonType,
  BatchType,
} from "./types";

const API_PATH = "/gencode/sys_documents";

// 列表查询参数
export interface SysDocumentsPageQuery extends PageQuery {
  lib_id?: string;
  file_upload_id?: string;
  chunk_size?: number;
  chunk_overlap?: number;
  processing_status?: string;
  error_msg?: string;
  status?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface SysDocumentsTable extends BaseType {
  lib_id?: string;
  file_upload_id?: string;
  chunk_size?: number;
  chunk_overlap?: number;
  processing_status?: boolean;
  error_msg?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface SysDocumentsForm extends BaseFormType {
  lib_id?: string;
  file_upload_id?: string;
  chunk_size?: number;
  chunk_overlap?: number;
  processing_status?: boolean;
  error_msg?: string;
}

/**
 * 列表查询
 */
export async function listSysDocuments(
  query: SysDocumentsPageQuery,
): Promise<PageResult<SysDocumentsTable[]>> {
  const params = new URLSearchParams();
  Object.entries(query).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      if (Array.isArray(value)) {
        value.forEach((v) => params.append(key, String(v)));
      } else {
        params.append(key, String(value));
      }
    }
  });
  return httpRequest<PageResult<SysDocumentsTable[]>>(
    `${API_PATH}/list?${params.toString()}`,
    {
      method: "GET",
    },
  );
}

/**
 * 详情查询
 */
export async function detailSysDocuments(
  id: number,
): Promise<SysDocumentsTable> {
  return httpRequest<SysDocumentsTable>(`${API_PATH}/detail/${id}`, {
    method: "GET",
  });
}

/**
 * 新增
 */
export async function createSysDocuments(body: SysDocumentsForm): Promise<void> {
  return httpRequest<void>(`${API_PATH}/create`, {
    method: "POST",
    body: JSON.stringify(body),
  });
}

/**
 * 修改（带主键）
 */
export async function updateSysDocuments(
  id: number,
  body: SysDocumentsForm,
): Promise<void> {
  return httpRequest<void>(`${API_PATH}/update/${id}`, {
    method: "PUT",
    body: JSON.stringify(body),
  });
}

/**
 * 删除（支持批量）
 */
export async function deleteSysDocuments(ids: number[]): Promise<void> {
  return httpRequest<void>(`${API_PATH}/delete`, {
    method: "DELETE",
    body: JSON.stringify(ids),
  });
}

/**
 * 批量启用/停用
 */
export async function batchSysDocuments(body: BatchType): Promise<void> {
  return httpRequest<void>(`${API_PATH}/available/setting`, {
    method: "PATCH",
    body: JSON.stringify(body),
  });
}

/**
 * 导出
 */
export async function exportSysDocuments(
  query: SysDocumentsPageQuery,
): Promise<Blob> {
  return httpRequestBlob(`${API_PATH}/export`, {
    method: "POST",
    body: JSON.stringify(query),
  });
}

/**
 * 下载导入模板
 */
export async function downloadTemplateSysDocuments(): Promise<Blob> {
  return httpRequestBlob(`${API_PATH}/download/template`, {
    method: "POST",
  });
}

/**
 * 导入
 */
export async function importSysDocuments(body: FormData): Promise<void> {
  return httpRequest<void>(`${API_PATH}/import`, {
    method: "POST",
    body: body,
  });
}

