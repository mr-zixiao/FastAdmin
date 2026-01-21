import request from "@/utils/request";

const API_PATH = "/gencode/sys_libraries";

const SysLibrariesAPI = {
  // 列表查询
  listSysLibraries(query: SysLibrariesPageQuery) {
    return request<ApiResponse<PageResult<SysLibrariesTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailSysLibraries(id: number) {
    return request<ApiResponse<SysLibrariesTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createSysLibraries(body: SysLibrariesForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateSysLibraries(id: number, body: SysLibrariesForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteSysLibraries(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchSysLibraries(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportSysLibraries(query: SysLibrariesPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateSysLibraries() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importSysLibraries(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default SysLibrariesAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface SysLibrariesPageQuery extends PageQuery {
  name?: string;
  collection_name?: string;
  dept_code?: string;
  status?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface SysLibrariesTable extends BaseType{
  name?: string;
  collection_name?: string;
  dept_code?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface SysLibrariesForm extends BaseFormType{
  name?: string;
  collection_name?: string;
  dept_code?: string;
}
