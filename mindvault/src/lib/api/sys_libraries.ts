import { httpRequest, httpRequestBlob } from "./http";
import type {
  PageQuery,
  PageResult,
  BaseType,
  BaseFormType,
  CommonType,
  BatchType,
} from "./types";

const API_PATH = "/gencode/sys_libraries";

// 列表查询参数
export interface SysLibrariesPageQuery extends PageQuery {
  status?: string;
  created_id?: number;
  updated_id?: number;
  lib_name?: string;
  collection_name?: string;
  lib_type?: string;
  embedding_model?: string;
  chunk_size?: string;
  chunk_overlap?: string;
  similarity_threshold?: string;
  max_chunks?: string;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface SysLibrariesTable extends BaseType {
  created_id?: string;
  updated_id?: string;
  lib_name?: string;
  collection_name?: string;
  lib_type?: string;
  embedding_model?: string;
  chunk_size?: string;
  chunk_overlap?: string;
  similarity_threshold?: string;
  max_chunks?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface SysLibrariesForm extends BaseFormType {
  lib_name?: string;
  collection_name?: string;
  lib_type?: string;
  embedding_model?: string;
  chunk_size?: string;
  chunk_overlap?: string;
  similarity_threshold?: string;
  max_chunks?: string;
}

/**
 * 列表查询
 */
export async function listSysLibraries(
  query: SysLibrariesPageQuery,
): Promise<PageResult<SysLibrariesTable[]>> {
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
  return httpRequest<PageResult<SysLibrariesTable[]>>(
    `${API_PATH}/list?${params.toString()}`,
    {
      method: "GET",
    },
  );
}

/**
 * 详情查询
 */
export async function detailSysLibraries(
  id: number,
): Promise<SysLibrariesTable> {
  return httpRequest<SysLibrariesTable>(`${API_PATH}/detail/${id}`, {
    method: "GET",
  });
}

/**
 * 新增
 */
export async function createSysLibraries(
  body: SysLibrariesForm,
): Promise<void> {
  return httpRequest<void>(`${API_PATH}/create`, {
    method: "POST",
    body: JSON.stringify(body),
  });
}

/**
 * 修改（带主键）
 */
export async function updateSysLibraries(
  id: number,
  body: SysLibrariesForm,
): Promise<void> {
  return httpRequest<void>(`${API_PATH}/update/${id}`, {
    method: "PUT",
    body: JSON.stringify(body),
  });
}

/**
 * 删除（支持批量）
 */
export async function deleteSysLibraries(ids: number[]): Promise<void> {
  return httpRequest<void>(`${API_PATH}/delete`, {
    method: "DELETE",
    body: JSON.stringify(ids),
  });
}

/**
 * 批量启用/停用
 */
export async function batchSysLibraries(body: BatchType): Promise<void> {
  return httpRequest<void>(`${API_PATH}/available/setting`, {
    method: "PATCH",
    body: JSON.stringify(body),
  });
}

/**
 * 导出
 */
export async function exportSysLibraries(
  query: SysLibrariesPageQuery,
): Promise<Blob> {
  return httpRequestBlob(`${API_PATH}/export`, {
    method: "POST",
    body: JSON.stringify(query),
  });
}

/**
 * 下载导入模板
 */
export async function downloadTemplateSysLibraries(): Promise<Blob> {
  return httpRequestBlob(`${API_PATH}/download/template`, {
    method: "POST",
  });
}

/**
 * 导入
 */
export async function importSysLibraries(body: FormData): Promise<void> {
  return httpRequest<void>(`${API_PATH}/import`, {
    method: "POST",
    body: body,
  });
}

