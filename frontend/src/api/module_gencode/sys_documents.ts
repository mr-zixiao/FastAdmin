import request from "@/utils/request";

const API_PATH = "/gencode/sys_documents";

const SysDocumentsAPI = {
  // 列表查询
  listSysDocuments(query: SysDocumentsPageQuery) {
    return request<ApiResponse<PageResult<SysDocumentsTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailSysDocuments(id: number) {
    return request<ApiResponse<SysDocumentsTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createSysDocuments(body: SysDocumentsForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateSysDocuments(id: number, body: SysDocumentsForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteSysDocuments(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchSysDocuments(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportSysDocuments(query: SysDocumentsPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateSysDocuments() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importSysDocuments(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default SysDocumentsAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface SysDocumentsPageQuery extends PageQuery {
  lib_id?: string;
  dept_id?: string;
  file_name?: string;
  file_path?: string;
  file_size?: string;
  file_ext?: string;
  file_hash?: string;
  status?: string;
  chunk_count?: string;
  error_msg?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface SysDocumentsTable extends BaseType{
  lib_id?: string;
  dept_id?: string;
  file_name?: string;
  file_path?: string;
  file_size?: string;
  file_ext?: string;
  file_hash?: string;
  chunk_count?: string;
  error_msg?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface SysDocumentsForm extends BaseFormType{
  lib_id?: string;
  dept_id?: string;
  file_name?: string;
  file_path?: string;
  file_size?: string;
  file_ext?: string;
  file_hash?: string;
  chunk_count?: string;
  error_msg?: string;
}
