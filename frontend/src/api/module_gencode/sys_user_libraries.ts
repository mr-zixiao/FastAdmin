import request from "@/utils/request";

const API_PATH = "/gencode/sys_user_libraries";

const SysUserLibrariesAPI = {
  // 列表查询
  listSysUserLibraries(query: SysUserLibrariesPageQuery) {
    return request<ApiResponse<PageResult<SysUserLibrariesTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailSysUserLibraries(id: number) {
    return request<ApiResponse<SysUserLibrariesTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createSysUserLibraries(body: SysUserLibrariesForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateSysUserLibraries(id: number, body: SysUserLibrariesForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteSysUserLibraries(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchSysUserLibraries(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportSysUserLibraries(query: SysUserLibrariesPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateSysUserLibraries() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importSysUserLibraries(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },

  // 批量关联用户与知识库
  batchAssociateSysUserLibraries(body: SysUserLibrariesBatchAssociateForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/batch/associate`,
      method: "post",
      data: body,
    });
  },
};

export default SysUserLibrariesAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

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
export interface SysUserLibrariesTable extends BaseType{
  user_id?: string;
  lib_id?: string;
  privilege_type?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface SysUserLibrariesForm extends BaseFormType{
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
