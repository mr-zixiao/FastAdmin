import { httpRequest, httpRequestBlob } from "./http";
import type {
  PageQuery,
  PageResult,
  BaseType,
  BaseFormType,
  CommonType,
  BatchType,
} from "./types";

const API_PATH = "/gencode/sys_file_upload";

// 列表查询参数
export interface SysFileUploadPageQuery extends PageQuery {
  origin_name?: string;
  file_name?: string;
  file_path?: string;
  file_size?: string;
  file_type?: string;
  status?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface SysFileUploadTable extends BaseType {
  origin_name?: string;
  file_name?: string;
  file_path?: string;
  file_size?: string;
  file_type?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface SysFileUploadForm extends BaseFormType {
  origin_name?: string;
  file_name?: string;
  file_path?: string;
  file_size?: string;
  file_type?: string;
}

/**
 * 列表查询
 */
export async function listSysFileUpload(
  query: SysFileUploadPageQuery,
): Promise<PageResult<SysFileUploadTable[]>> {
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
  return httpRequest<PageResult<SysFileUploadTable[]>>(
    `${API_PATH}/list?${params.toString()}`,
    {
      method: "GET",
    },
  );
}

/**
 * 详情查询
 */
export async function detailSysFileUpload(
  id: number,
): Promise<SysFileUploadTable> {
  return httpRequest<SysFileUploadTable>(`${API_PATH}/detail/${id}`, {
    method: "GET",
  });
}

/**
 * 新增
 */
export async function createSysFileUpload(
  body: SysFileUploadForm,
): Promise<void> {
  return httpRequest<void>(`${API_PATH}/create`, {
    method: "POST",
    body: JSON.stringify(body),
  });
}

/**
 * 修改（带主键）
 */
export async function updateSysFileUpload(
  id: number,
  body: SysFileUploadForm,
): Promise<void> {
  return httpRequest<void>(`${API_PATH}/update/${id}`, {
    method: "PUT",
    body: JSON.stringify(body),
  });
}

/**
 * 删除（支持批量）
 */
export async function deleteSysFileUpload(ids: number[]): Promise<void> {
  return httpRequest<void>(`${API_PATH}/delete`, {
    method: "DELETE",
    body: JSON.stringify(ids),
  });
}

/**
 * 批量启用/停用
 */
export async function batchSysFileUpload(body: BatchType): Promise<void> {
  return httpRequest<void>(`${API_PATH}/available/setting`, {
    method: "PATCH",
    body: JSON.stringify(body),
  });
}

/**
 * 导出
 */
export async function exportSysFileUpload(
  query: SysFileUploadPageQuery,
): Promise<Blob> {
  return httpRequestBlob(`${API_PATH}/export`, {
    method: "POST",
    body: JSON.stringify(query),
  });
}

/**
 * 下载导入模板
 */
export async function downloadTemplateSysFileUpload(): Promise<Blob> {
  return httpRequestBlob(`${API_PATH}/download/template`, {
    method: "POST",
  });
}

/**
 * 导入
 */
export async function importSysFileUpload(body: FormData): Promise<void> {
  return httpRequest<void>(`${API_PATH}/import`, {
    method: "POST",
    body: body,
  });
}

/**
 * 上传文件
 */
export async function uploadFile(
  file: File,
  description?: string,
): Promise<SysFileUploadTable> {
  const formData = new FormData();
  formData.append("file", file);
  if (description) {
    formData.append("description", description);
  }
  return httpRequest<SysFileUploadTable>(`${API_PATH}/upload/file`, {
    method: "POST",
    body: formData,
  });
}

/**
 * 访问文件（通过ID）
 */
export async function getFile(id: number): Promise<Blob> {
  return httpRequestBlob(`${API_PATH}/file/${id}`, {
    method: "GET",
  });
}

