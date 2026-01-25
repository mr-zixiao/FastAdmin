import request from "@/utils/request";

const API_PATH = "/gencode/sys_file_upload";

const SysFileUploadAPI = {
  // 列表查询
  listSysFileUpload(query: SysFileUploadPageQuery) {
    return request<ApiResponse<PageResult<SysFileUploadTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailSysFileUpload(id: number) {
    return request<ApiResponse<SysFileUploadTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createSysFileUpload(body: SysFileUploadForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateSysFileUpload(id: number, body: SysFileUploadForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteSysFileUpload(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchSysFileUpload(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportSysFileUpload(query: SysFileUploadPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateSysFileUpload() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importSysFileUpload(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },

  // 上传文件
  uploadFile(file: File, description?: string) {
    const formData = new FormData();
    formData.append("file", file);
    if (description) {
      formData.append("description", description);
    }
    return request<ApiResponse<SysFileUploadTable>>({
      url: `${API_PATH}/upload/file`,
      method: "post",
      data: formData,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },

  // 访问文件（通过ID）
  getFile(id: number) {
    return request<Blob>({
      url: `${API_PATH}/file/${id}`,
      method: "get",
      responseType: "blob",
    });
  },
};

export default SysFileUploadAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

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
export interface SysFileUploadTable extends BaseType{
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
export interface SysFileUploadForm extends BaseFormType{
  origin_name?: string;
  file_name?: string;
  file_path?: string;
  file_size?: string;
  file_type?: string;
}
