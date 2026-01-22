import request from "@/utils/request";

const API_PATH = "/gencode/sys_lib_permissions";

const SysLibPermissionsAPI = {
  // 列表查询
  listSysLibPermissions(query: SysLibPermissionsPageQuery) {
    return request<ApiResponse<PageResult<SysLibPermissionsTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailSysLibPermissions(id: number) {
    return request<ApiResponse<SysLibPermissionsTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createSysLibPermissions(body: SysLibPermissionsForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateSysLibPermissions(id: number, body: SysLibPermissionsForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteSysLibPermissions(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchSysLibPermissions(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportSysLibPermissions(query: SysLibPermissionsPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateSysLibPermissions() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importSysLibPermissions(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },

  // 批量关联知识库权限
  batchAssociateSysLibPermissions(body: SysLibPermissionsBatchAssociateForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/batch/associate`,
      method: "post",
      data: body,
    });
  },
};

export default SysLibPermissionsAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface SysLibPermissionsPageQuery extends PageQuery {
  target_type?: string;
  target_id?: string;
  lib_id?: string;
  privilege_type?: string;
  status?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface SysLibPermissionsTable extends BaseType{
  target_type?: string;
  target_id?: string;
  lib_id?: string;
  privilege_type?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface SysLibPermissionsForm extends BaseFormType{
  target_type?: string;
  target_id?: string;
  lib_id?: string;
  privilege_type?: string;
}

// 批量关联表单参数
export interface SysLibPermissionsBatchAssociateForm {
  target_type: string;
  target_ids: string; // 逗号分隔的ID字符串
  lib_id: number;
  privilege_type: string;
  status?: string;
  description?: string;
}
