import request from "@/utils/request";

const API_PATH = "/gencode/sys_document_chunks";

const SysDocumentChunksAPI = {
  // 列表查询
  listSysDocumentChunks(query: SysDocumentChunksPageQuery) {
    return request<ApiResponse<PageResult<SysDocumentChunksTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailSysDocumentChunks(id: number) {
    return request<ApiResponse<SysDocumentChunksTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createSysDocumentChunks(body: SysDocumentChunksForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateSysDocumentChunks(id: number, body: SysDocumentChunksForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteSysDocumentChunks(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchSysDocumentChunks(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportSysDocumentChunks(query: SysDocumentChunksPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateSysDocumentChunks() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importSysDocumentChunks(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default SysDocumentChunksAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface SysDocumentChunksPageQuery extends PageQuery {
  doc_id?: string;
  vector_id?: string;
  content?: string;
  page_number?: string;
  chunk_order?: string;
  token_count?: string;
  status?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface SysDocumentChunksTable extends BaseType{
  doc_id?: string;
  vector_id?: string;
  content?: string;
  page_number?: string;
  chunk_order?: string;
  token_count?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface SysDocumentChunksForm extends BaseFormType{
  doc_id?: string;
  vector_id?: string;
  content?: string;
  page_number?: string;
  chunk_order?: string;
  token_count?: string;
}
