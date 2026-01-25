import { httpRequest, httpRequestBlob } from "./http";
import type {
  PageQuery,
  PageResult,
  BaseType,
  BaseFormType,
  CommonType,
  BatchType,
} from "./types";

const API_PATH = "/gencode/sys_user_libraries";

// 列表查询参数
export interface SysUserLibrariesPageQuery extends PageQuery {
  user_id?: string;
  lib_id?: string;
  privilege_type?: string;
  status?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface SysUserLibrariesTable extends BaseType {
  user_id?: string;
  lib_id?: string;
  privilege_type?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface SysUserLibrariesForm extends BaseFormType {
  user_id?: string;
  lib_id?: string;
  privilege_type?: string;
}

// 批量关联表单参数
export interface SysUserLibrariesBatchAssociateForm {
  user_ids: number[]; // 用户ID列表
  lib_id: number; // 知识库ID
  privilege_type: string; // 权限类型(使用字典sys_lib_privilege_type)
  status?: string; // 状态
  description?: string; // 备注/描述
}

/**
 * 列表查询
 */
export async function listSysUserLibraries(
  query: SysUserLibrariesPageQuery,
): Promise<PageResult<SysUserLibrariesTable[]>> {
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
  return httpRequest<PageResult<SysUserLibrariesTable[]>>(
    `${API_PATH}/list?${params.toString()}`,
    {
      method: "GET",
    },
  );
}

/**
 * 详情查询
 */
export async function detailSysUserLibraries(
  id: number,
): Promise<SysUserLibrariesTable> {
  return httpRequest<SysUserLibrariesTable>(`${API_PATH}/detail/${id}`, {
    method: "GET",
  });
}

/**
 * 新增
 */
export async function createSysUserLibraries(
  body: SysUserLibrariesForm,
): Promise<void> {
  return httpRequest<void>(`${API_PATH}/create`, {
    method: "POST",
    body: JSON.stringify(body),
  });
}

/**
 * 修改（带主键）
 */
export async function updateSysUserLibraries(
  id: number,
  body: SysUserLibrariesForm,
): Promise<void> {
  return httpRequest<void>(`${API_PATH}/update/${id}`, {
    method: "PUT",
    body: JSON.stringify(body),
  });
}

/**
 * 删除（支持批量）
 */
export async function deleteSysUserLibraries(ids: number[]): Promise<void> {
  return httpRequest<void>(`${API_PATH}/delete`, {
    method: "DELETE",
    body: JSON.stringify(ids),
  });
}

/**
 * 批量启用/停用
 */
export async function batchSysUserLibraries(body: BatchType): Promise<void> {
  return httpRequest<void>(`${API_PATH}/available/setting`, {
    method: "PATCH",
    body: JSON.stringify(body),
  });
}

/**
 * 导出
 */
export async function exportSysUserLibraries(
  query: SysUserLibrariesPageQuery,
): Promise<Blob> {
  return httpRequestBlob(`${API_PATH}/export`, {
    method: "POST",
    body: JSON.stringify(query),
  });
}

/**
 * 下载导入模板
 */
export async function downloadTemplateSysUserLibraries(): Promise<Blob> {
  return httpRequestBlob(`${API_PATH}/download/template`, {
    method: "POST",
  });
}

/**
 * 导入
 */
export async function importSysUserLibraries(body: FormData): Promise<void> {
  return httpRequest<void>(`${API_PATH}/import`, {
    method: "POST",
    body: body,
  });
}

/**
 * 批量关联用户与知识库
 */
export async function batchAssociateSysUserLibraries(
  body: SysUserLibrariesBatchAssociateForm,
): Promise<void> {
  return httpRequest<void>(`${API_PATH}/batch/associate`, {
    method: "POST",
    body: JSON.stringify(body),
  });
}

