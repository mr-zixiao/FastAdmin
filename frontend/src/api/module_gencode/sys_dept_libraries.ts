import request from "@/utils/request";

const API_PATH = "/gencode/sys_dept_libraries";

const SysDeptLibrariesAPI = {
  // 列表查询
  listSysDeptLibraries(query: SysDeptLibrariesPageQuery) {
    return request<ApiResponse<PageResult<SysDeptLibrariesTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailSysDeptLibraries(id: number) {
    return request<ApiResponse<SysDeptLibrariesTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createSysDeptLibraries(body: SysDeptLibrariesForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateSysDeptLibraries(id: number, body: SysDeptLibrariesForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteSysDeptLibraries(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchSysDeptLibraries(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportSysDeptLibraries(query: SysDeptLibrariesPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateSysDeptLibraries() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importSysDeptLibraries(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default SysDeptLibrariesAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface SysDeptLibrariesPageQuery extends PageQuery {
  dept_id?: string;
  dept_code?: string;
  lib_id?: string;
  privilege_type?: string;
  status?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface SysDeptLibrariesTable extends BaseType{
  dept_id?: string;
  dept_code?: string;
  lib_id?: string;
  privilege_type?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface SysDeptLibrariesForm extends BaseFormType{
  dept_id?: string;
  dept_code?: string;
  lib_id?: string;
  privilege_type?: string;
}
