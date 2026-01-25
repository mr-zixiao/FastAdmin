<!-- 文档管理 -->
<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <div v-show="visible" class="search-container">
      <el-form
        ref="queryFormRef"
        :model="queryFormData"
        label-suffix=":"
        :inline="true"
        @submit.prevent="handleQuery"
      >
        <el-form-item label="知识库" prop="lib_id">
          <el-select
            v-model="queryFormData.lib_id"
            placeholder="请选择知识库"
            clearable
            filterable
            style="width: 200px"
          >
            <el-option
              v-for="lib in librariesList"
              :key="lib.id"
              :label="lib.lib_name"
              :value="String(lib.id)"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="处理状态" prop="processing_status">
          <el-select
            v-model="queryFormData.processing_status"
            placeholder="请选择处理状态"
            clearable
            style="width: 150px"
          >
            <el-option label="待处理" value="pending" />
            <el-option label="处理中" value="processing" />
            <el-option label="已完成" value="completed" />
            <el-option label="处理失败" value="failed" />
          </el-select>
        </el-form-item>
        <el-form-item prop="status" label="状态">
          <el-select
            v-model="queryFormData.status"
            placeholder="请选择状态"
            style="width: 120px"
            clearable
          >
            <el-option value="0" label="启用" />
            <el-option value="1" label="停用" />
          </el-select>
        </el-form-item>
        <!-- 查询、重置按钮 -->
        <el-form-item>
          <el-button
            v-hasPerm="['module_gencode:sys_documents:query']"
            type="primary"
            icon="search"
            @click="handleQuery"
          >
            查询
          </el-button>
          <el-button
            v-hasPerm="['module_gencode:sys_documents:query']"
            icon="refresh"
            @click="handleResetQuery"
          >
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 内容区域 -->
    <el-card class="data-table">
      <template #header>
        <div class="card-header">
          <span>
            文档管理列表
            <el-tooltip content="文档管理列表">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
          </span>
        </div>
      </template>

      <!-- 功能区域 -->
      <div class="data-table__toolbar">
        <div class="data-table__toolbar--left">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_gencode:sys_documents:create']"
                type="success"
                icon="plus"
                @click="handleOpenDialog('create')"
              >
                新增
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_gencode:sys_documents:delete']"
                type="danger"
                icon="delete"
                :disabled="selectIds.length === 0"
                @click="handleDelete(selectIds)"
              >
                批量删除
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-dropdown v-hasPerm="['module_gencode:sys_documents:batch']" trigger="click">
                <el-button type="default" :disabled="selectIds.length === 0" icon="ArrowDown">
                  更多
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item :icon="Check" @click="handleMoreClick('0')">
                      批量启用
                    </el-dropdown-item>
                    <el-dropdown-item :icon="CircleClose" @click="handleMoreClick('1')">
                      批量停用
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </el-col>
          </el-row>
        </div>
        <div class="data-table__toolbar--right">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-tooltip content="导入">
                <el-button
                  v-hasPerm="['module_gencode:sys_documents:import']"
                  type="success"
                  icon="upload"
                  circle
                  @click="handleOpenImportDialog"
                />
              </el-tooltip>
            </el-col>
            <el-col :span="1.5">
              <el-tooltip content="导出">
                <el-button
                  v-hasPerm="['module_gencode:sys_documents:export']"
                  type="warning"
                  icon="download"
                  circle
                  @click="handleOpenExportsModal"
                />
              </el-tooltip>
            </el-col>
            <el-col :span="1.5">
              <el-tooltip content="搜索显示/隐藏">
                <el-button
                  v-hasPerm="['*:*:*']"
                  type="info"
                  icon="search"
                  circle
                  @click="visible = !visible"
                />
              </el-tooltip>
            </el-col>
            <el-col :span="1.5">
              <el-tooltip content="刷新">
                <el-button
                  v-hasPerm="['module_gencode:sys_documents:query']"
                  type="primary"
                  icon="refresh"
                  circle
                  @click="handleRefresh"
                />
              </el-tooltip>
            </el-col>
            <el-col :span="1.5">
              <el-popover placement="bottom" trigger="click">
                <template #reference>
                  <el-button type="danger" icon="operation" circle></el-button>
                </template>
                <el-scrollbar max-height="350px">
                  <template v-for="column in tableColumns" :key="column.prop">
                    <el-checkbox v-if="column.prop" v-model="column.show" :label="column.label" />
                  </template>
                </el-scrollbar>
              </el-popover>
            </el-col>
          </el-row>
        </div>
      </div>

      <!-- 表格区域：系统配置列表 -->
      <el-table
        ref="tableRef"
        v-loading="loading"
        :data="pageTableData"
        highlight-current-row
        class="data-table__content"
        :height="450"
        border
        stripe
        @selection-change="handleSelectionChange"
      >
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'selection')?.show"
          type="selection"
          min-width="55"
          align="center"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'index')?.show"
          fixed
          label="序号"
          min-width="60"
        >
          <template #default="scope">
            {{ (queryFormData.page_no - 1) * queryFormData.page_size + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find((col) => col.prop === 'lib_id')?.show" label="知识库" prop="lib_id" min-width="150">
          <template #default="scope">
            {{ getLibraryName(scope.row.lib_id) }}
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find((col) => col.prop === 'file_upload_id')?.show" label="文件名" prop="file_upload_id" min-width="180" show-overflow-tooltip>
          <template #default="scope">
            {{ scope.row.file_upload_id }}
          </template>
        </el-table-column>
        <el-table-column type="number" v-if="tableColumns.find((col) => col.prop === 'chunk_size')?.show" label="切片大小" prop="chunk_size" min-width="100" align="center">
        </el-table-column>
        <el-table-column  type="number" v-if="tableColumns.find((col) => col.prop === 'chunk_overlap')?.show" label="切片重叠" prop="chunk_overlap" min-width="100" align="center">
        </el-table-column>
        <el-table-column v-if="tableColumns.find((col) => col.prop === 'processing_status')?.show" label="处理状态" prop="processing_status" min-width="120" align="center">
          <template #default="scope">
            <el-tag 
              :type="getProcessingStatusType(scope.row.processing_status)" 
              size="small"
            >
              {{ getProcessingStatusText(scope.row.processing_status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find((col) => col.prop === 'error_msg')?.show" label="错误信息" prop="error_msg" min-width="200" show-overflow-tooltip>
        </el-table-column>
        <el-table-column v-if="tableColumns.find((col) => col.prop === 'status')?.show" label="状态" prop="status" min-width="80" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.status == '0' ? 'success' : 'info'" size="small">
              {{ scope.row.status == '0' ? '启用' : '停用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find((col) => col.prop === 'created_time')?.show" label="创建时间" prop="created_time" min-width="160">
        </el-table-column>
        <el-table-column v-if="tableColumns.find((col) => col.prop === 'created_id')?.show" label="创建人" prop="created_id" min-width="100">
          <template #default="scope">
            <el-tag size="small">{{ scope.row.created_by?.name || '-' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'operation')?.show"
          fixed="right"
          label="操作"
          align="center"
          min-width="180"
        >
          <template #default="scope">
            <el-button
              v-hasPerm="['module_gencode:sys_documents:detail']"
              type="info"
              size="small"
              link
              icon="document"
              @click="handleOpenDialog('detail', scope.row.id)"
            >
              详情
            </el-button>
            <el-button
              v-hasPerm="['module_gencode:sys_documents:update']"
              type="primary"
              size="small"
              link
              icon="edit"
              @click="handleOpenDialog('update', scope.row.id)"
            >
              编辑
            </el-button>
            <el-button
              v-hasPerm="['module_gencode:sys_documents:delete']"
              type="danger"
              size="small"
              link
              icon="delete"
              @click="handleDelete([scope.row.id])"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页区域 -->
      <template #footer>
        <pagination
          v-model:total="total"
          v-model:page="queryFormData.page_no"
          v-model:limit="queryFormData.page_size"
          @pagination="loadingData"
        />
      </template>
    </el-card>

    <!-- 弹窗区域 -->
    <el-dialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      @close="handleCloseDialog"
    >
      <!-- 详情 -->
      <template v-if="dialogVisible.type === 'detail'">
        <el-descriptions :column="4" border>
            <el-descriptions-item label="知识库ID" :span="2">
              {{ detailFormData.lib_id }}
            </el-descriptions-item>
            <el-descriptions-item label="文件上传ID" :span="2">
              {{ detailFormData.file_upload_id }}
            </el-descriptions-item>
            <el-descriptions-item label="文档切片大小" :span="2">
              {{ detailFormData.chunk_size }}
            </el-descriptions-item>
            <el-descriptions-item label="文档切片重叠大小" :span="2">
              {{ detailFormData.chunk_overlap }}
            </el-descriptions-item>
            <el-descriptions-item label="处理状态(pending:待处理 processing:处理中 completed:已完成 failed:处理失败)" :span="2">
              {{ detailFormData.processing_status }}
            </el-descriptions-item>
            <el-descriptions-item label="错误信息" :span="2">
              {{ detailFormData.error_msg }}
            </el-descriptions-item>
            <el-descriptions-item label="主键ID" :span="2">
              {{ detailFormData.id }}
            </el-descriptions-item>
            <el-descriptions-item label="UUID全局唯一标识" :span="2">
              {{ detailFormData.uuid }}
            </el-descriptions-item>
            <el-descriptions-item label="状态" :span="2">
              <el-tag :type="detailFormData.status == '0' ? 'success' : 'danger'">
                {{ detailFormData.status == '0' ? "启用" : "停用" }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="备注/描述" :span="2">
              {{ detailFormData.description }}
            </el-descriptions-item>
            <el-descriptions-item label="创建时间" :span="2">
              {{ detailFormData.created_time }}
            </el-descriptions-item>
            <el-descriptions-item label="更新时间" :span="2">
              {{ detailFormData.updated_time }}
            </el-descriptions-item>
            <el-descriptions-item label="创建人" :span="2">
              {{ detailFormData.created_by?.name }}
            </el-descriptions-item>
            <el-descriptions-item label="更新人" :span="2">
              {{ detailFormData.updated_by?.name }}
            </el-descriptions-item>
        </el-descriptions>
      </template>

      <!-- 新增、编辑表单 -->
      <template v-else>
        <el-form ref="dataFormRef" :model="formData" :rules="rules" label-suffix=":" label-width="120px" label-position="right">
          <el-form-item label="知识库" prop="lib_id" :required="true">
            <el-select
              v-model="formData.lib_id"
              placeholder="请选择知识库"
              filterable
              style="width: 100%"
            >
              <el-option
                v-for="lib in librariesList"
                :key="lib.id"
                :label="lib.lib_name"
                :value="String(lib.id)"
              />
            </el-select>
          </el-form-item>
          
          <!-- 文件上传区域 -->
          <el-form-item label="切片大小" prop="chunk_size">
            <el-input-number v-model="formData.chunk_size" :min="100" :max="10000" :step="100" placeholder="请输入切片大小" style="width: 100%" />
          </el-form-item>
          <el-form-item label="切片重叠" prop="chunk_overlap">
            <el-input-number v-model="formData.chunk_overlap" :min="0" :max="1000" :step="10" placeholder="请输入切片重叠大小" style="width: 100%" />
          </el-form-item>
          
          <el-form-item label="上传文件" :required="dialogVisible.type === 'create'">
            <el-upload
              ref="uploadRef"
              class="upload-demo"
              drag
              :auto-upload="false"
              :multiple="true"
              :on-change="handleFileChange"
              :on-remove="handleFileRemove"
              :file-list="fileList"
              :limit="50"
            >
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">
                将文件拖拽到此处，或<em>点击上传</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  支持一次选择多个文件，最多50个文件，单个文件不超过10MB<br>
                  <span style="color: var(--el-color-primary); font-size: 12px;">
                    ✨ 支持最多5个文件并发上传，提升上传速度
                  </span>
                </div>
              </template>
            </el-upload>
          </el-form-item>
          
          <el-form-item label="状态" prop="status" :required="true">
            <el-radio-group v-model="formData.status">
              <el-radio value="0">启用</el-radio>
              <el-radio value="1">停用</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="描述" prop="description">
            <el-input
              v-model="formData.description"
              :rows="4"
              :maxlength="100"
              show-word-limit
              type="textarea"
              placeholder="请输入描述"
            />
          </el-form-item>
        </el-form>
      </template>

      <template #footer>
        <div class="dialog-footer">
          <!-- 详情弹窗不需要确定按钮的提交逻辑 -->
          <el-button @click="handleCloseDialog">取消</el-button>
          <el-button v-if="dialogVisible.type !== 'detail'" type="primary" @click="handleSubmit">
            确定
          </el-button>
          <el-button v-else type="primary" @click="handleCloseDialog">确定</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 导入弹窗 -->
    <ImportModal
      v-model="importDialogVisible"
      :content-config="curdContentConfig"
      @upload="handleUpload"
    />

    <!-- 导出弹窗 -->
    <ExportModal
      v-model="exportsDialogVisible"
      :content-config="curdContentConfig"
      :query-params="queryFormData"
      :page-data="pageTableData"
      :selection-data="selectionRows"
    />
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "SysDocuments",
  inheritAttrs: false,
});

import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { QuestionFilled, Check, CircleClose, UploadFilled } from '@element-plus/icons-vue'
import { useDictStore } from "@/store";
import { ResultEnum } from '@/enums/api/result.enum'
import type { IContentConfig } from "@/components/CURD/types";
import ImportModal from "@/components/CURD/ImportModal.vue";
import ExportModal from "@/components/CURD/ExportModal.vue";
import SysDocumentsAPI, { SysDocumentsPageQuery, SysDocumentsTable, SysDocumentsForm } from '@/api/module_gencode/sys_documents'
import SysLibrariesAPI, { SysLibrariesTable } from '@/api/module_gencode/sys_libraries'
import SysFileUploadAPI from '@/api/module_gencode/sys_file_upload'

const visible = ref(true);
const queryFormRef = ref();
const dataFormRef = ref();
const total = ref(0);
const selectIds = ref<number[]>([]);
const selectionRows = ref<SysDocumentsTable[]>([]);
const loading = ref(false);

// 字典仓库与需要加载的字典类型
const dictStore = useDictStore()
const dictTypes: any = []

// 知识库列表
const librariesList = ref<SysLibrariesTable[]>([])

// 文件上传相关
const uploadRef = ref()
const fileList = ref<any[]>([])
const isUploading = ref(false)

// 并发上传配置
const MAX_CONCURRENT_UPLOADS = 5

// 分页表单
const pageTableData = ref<SysDocumentsTable[]>([]);

// 表格列配置
const tableColumns = ref([
  { prop: "selection", label: "选择框", show: true },
  { prop: "index", label: "序号", show: true },
  { prop: 'lib_id', label: '知识库', show: true },
  { prop: 'file_upload_id', label: '文件名', show: true },
  { prop: 'chunk_size', label: '切片大小', show: true },
  { prop: 'chunk_overlap', label: '切片重叠', show: true },
  { prop: 'processing_status', label: '处理状态', show: true },
  { prop: 'error_msg', label: '错误信息', show: true },
  { prop: 'status', label: '状态', show: true },
  { prop: 'created_time', label: '创建时间', show: true },
  { prop: 'created_id', label: '创建人', show: true },
  { prop: 'operation', label: '操作', show: true }
]);

// 导出列（不含选择/序号/操作）
const exportColumns = [
  { prop: 'lib_id', label: '知识库' },
  { prop: 'file_upload_id', label: '文件名' },
  { prop: 'chunk_size', label: '切片大小' },
  { prop: 'chunk_overlap', label: '切片重叠' },
  { prop: 'processing_status', label: '处理状态' },
  { prop: 'error_msg', label: '错误信息' },
  { prop: 'status', label: '状态' },
  { prop: 'created_time', label: '创建时间' },
  { prop: 'created_id', label: '创建人' },
]

// 导入/导出配置
const curdContentConfig = {
  permPrefix: "module_gencode:sys_documents",
  cols: exportColumns as any,
  importTemplate: () => SysDocumentsAPI.downloadTemplateSysDocuments(),
  exportsAction: async (params: any) => {
    const query: any = { ...params };
    query.status = '0';
    query.page_no = 1;
    query.page_size = 9999;
    const all: any[] = [];
    while (true) {
      const res = await SysDocumentsAPI.listSysDocuments(query);
      const items = res.data?.data?.items || [];
      const total = res.data?.data?.total || 0;
      all.push(...items);
      if (all.length >= total || items.length === 0) break;
      query.page_no += 1;
    }
    return all;
  },
} as unknown as IContentConfig;

// 详情表单
const detailFormData = ref<SysDocumentsTable>({});

// 分页查询参数
const queryFormData = reactive<SysDocumentsPageQuery>({
  page_no: 1,
  page_size: 10,
  lib_id: undefined,
  processing_status: undefined,
  status: undefined,
});


// 编辑表单
const formData = reactive<SysDocumentsForm>({
  lib_id: undefined,
  file_upload_id: undefined,
  chunk_size: undefined,
  chunk_overlap: undefined,
  processing_status: undefined,
  error_msg: undefined,
  id: undefined,
  status: undefined,
  description: undefined,
});

// 弹窗状态
const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
});

// 表单验证规则
const rules = reactive({
  lib_id: [
    { required: false, message: '请输入知识库ID', trigger: 'blur' },
  ],
  file_upload_id: [
    { required: false, message: '请输入文件上传ID', trigger: 'blur' },
  ],
  chunk_size: [
    { required: false, message: '请输入文档切片大小', trigger: 'blur' },
  ],
  chunk_overlap: [
    { required: false, message: '请输入文档切片重叠大小', trigger: 'blur' },
  ],
  processing_status: [
    { required: false, message: '请输入处理状态(pending:待处理 processing:处理中 completed:已完成 failed:处理失败)', trigger: 'blur' },
  ],
  error_msg: [
    { required: false, message: '请输入错误信息（处理失败时）', trigger: 'blur' },
  ],
  id: [
    { required: false, message: '请输入主键ID', trigger: 'blur' },
  ],
  uuid: [
    { required: true, message: '请输入UUID全局唯一标识', trigger: 'blur' },
  ],
  status: [
    { required: true, message: '请输入是否启用(0:启用 1:禁用)', trigger: 'blur' },
  ],
  description: [
    { required: false, message: '请输入备注/描述', trigger: 'blur' },
  ],
  created_time: [
    { required: true, message: '请输入创建时间', trigger: 'blur' },
  ],
  updated_time: [
    { required: true, message: '请输入更新时间', trigger: 'blur' },
  ],
  created_id: [
    { required: false, message: '请输入创建人ID', trigger: 'blur' },
  ],
  updated_id: [
    { required: false, message: '请输入更新人ID', trigger: 'blur' },
  ],
});

// 导入弹窗显示状态
const importDialogVisible = ref(false);

// 导出弹窗显示状态
const exportsDialogVisible = ref(false);

// 打开导入弹窗
function handleOpenImportDialog() {
  importDialogVisible.value = true;
}

// 打开导出弹窗
function handleOpenExportsModal() {
  exportsDialogVisible.value = true;
}

// 列表刷新
async function handleRefresh() {
  await loadingData();
}

// 加载表格数据
async function loadingData() {
  loading.value = true;
  try {
    const response = await SysDocumentsAPI.listSysDocuments(queryFormData);
    pageTableData.value = response.data.data.items;
    total.value = response.data.data.total;
  } catch (error: any) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

// 查询（重置页码后获取数据）
async function handleQuery() {
  queryFormData.page_no = 1;
  loadingData();
}

// 选择创建人后触发查询
function handleConfirm() {
  handleQuery();
}

// 重置查询
async function handleResetQuery() {
  queryFormRef.value.resetFields();
  queryFormData.page_no = 1;
  loadingData();
}

// 获取知识库名称
function getLibraryName(libId: any): string {
  const lib = librariesList.value.find(l => l.id === libId)
  return lib?.lib_name || libId || '-'
}

// 获取处理状态文本
function getProcessingStatusText(status: any): string {
  const statusMap: Record<string, string> = {
    'pending': '待处理',
    'processing': '处理中',
    'completed': '已完成',
    'failed': '处理失败'
  }
  return statusMap[status] || status || '-'
}

// 获取处理状态类型
function getProcessingStatusType(status: any): 'info' | 'warning' | 'success' | 'danger' {
  const typeMap: Record<string, 'info' | 'warning' | 'success' | 'danger'> = {
    'pending': 'info',
    'processing': 'warning',
    'completed': 'success',
    'failed': 'danger'
  }
  return typeMap[status] || 'info'
}

// 加载知识库列表
async function loadLibraries() {
  try {
    const response = await SysLibrariesAPI.listSysLibraries({
      page_no: 1,
      page_size: 100,
      status: '0'
    })
    librariesList.value = response.data.data.items || []
  } catch (error) {
    console.error('加载知识库列表失败:', error)
  }
}

// 文件选择变化
function handleFileChange(file: any, fileListParam: any[]) {
  fileList.value = [...fileListParam]
}

// 文件移除
function handleFileRemove(file: any, fileListParam: any[]) {
  fileList.value = [...fileListParam]
}

// 定义初始表单数据常量
const initialFormData: SysDocumentsForm = {
  lib_id: undefined,
  chunk_size: 1000,
  chunk_overlap: 200,
  status: '0',
  description: undefined,
};

// 重置表单
async function resetForm() {
  if (dataFormRef.value) {
    dataFormRef.value.resetFields();
    dataFormRef.value.clearValidate();
  }
  // 完全重置 formData 为初始状态
  Object.assign(formData, initialFormData);
  // 清空文件列表
  fileList.value = [];
  if (uploadRef.value) {
    uploadRef.value.clearFiles();
  }
}

// 行复选框选中项变化
async function handleSelectionChange(selection: any) {
  selectIds.value = selection.map((item: any) => item.id);
  selectionRows.value = selection;
}

// 关闭弹窗
async function handleCloseDialog() {
  dialogVisible.visible = false;
  resetForm();
}

// 打开弹窗
async function handleOpenDialog(type: "create" | "update" | "detail", id?: number) {
  dialogVisible.type = type;
  // 确保知识库列表已加载
  if (librariesList.value.length === 0) {
    await loadLibraries();
  }
  
  if (id) {
    const response = await SysDocumentsAPI.detailSysDocuments(id);
    if (type === "detail") {
      dialogVisible.title = "详情";
      Object.assign(detailFormData.value, response.data.data);
    } else if (type === "update") {
      dialogVisible.title = "修改";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增文档";
    Object.assign(formData, initialFormData);
    fileList.value = [];
  }
  dialogVisible.visible = true;
}

// 并发上传控制器（复用上传逻辑）
class ConcurrentUploader {
  private maxConcurrent: number;
  private running: number = 0;
  private queue: (() => Promise<void>)[] = [];

  constructor(maxConcurrent: number = MAX_CONCURRENT_UPLOADS) {
    this.maxConcurrent = maxConcurrent;
  }

  async add<T>(task: () => Promise<T>): Promise<T> {
    return new Promise((resolve, reject) => {
      this.queue.push(async () => {
        try {
          const result = await task();
          resolve(result);
        } catch (error) {
          reject(error);
        }
      });
      this.process();
    });
  }

  private async process() {
    if (this.running >= this.maxConcurrent || this.queue.length === 0) {
      return;
    }

    this.running++;
    const task = this.queue.shift();
    
    if (task) {
      try {
        await task();
      } finally {
        this.running--;
        this.process();
      }
    }
  }
}

// 提交表单（防抖）
async function handleSubmit() {
  // 表单校验
  dataFormRef.value.validate(async (valid: any) => {
    if (valid) {
      // 根据弹窗类型判断是新增还是修改
      const id = formData.id;
      
      if (id) {
        // 修改逻辑
        try {
          loading.value = true;
          await SysDocumentsAPI.updateSysDocuments(id, { id, ...formData });
          ElMessage.success('修改成功');
          dialogVisible.visible = false;
          resetForm();
          handleCloseDialog();
          handleResetQuery();
        } catch (error: any) {
          console.error(error);
          ElMessage.error(error?.response?.data?.msg || '修改失败');
        } finally {
          loading.value = false;
        }
      } else {
        // 新增逻辑 - 先上传文件，然后循环新增
        const files = uploadRef.value?.fileList || fileList.value;
        if (!files || files.length === 0) {
          ElMessage.warning('请选择要上传的文件');
          return;
        }

        // 获取所有有效的文件对象
        const validFiles = files.map((fileItem: any) => fileItem.raw || fileItem).filter((file: any) => file);

        if (validFiles.length === 0) {
          ElMessage.warning('没有有效的文件');
          return;
        }

        loading.value = true;
        isUploading.value = true;

        let successCount = 0;
        let errorCount = 0;
        const errors: string[] = [];

        try {
          // 创建并发上传控制器
          const uploader = new ConcurrentUploader(MAX_CONCURRENT_UPLOADS);

          // 为每个文件创建上传+新增任务
          const tasks = validFiles.map((file: File, index: number) => 
            uploader.add(async () => {
              try {
                // 1. 先上传文件
                const uploadResponse = await SysFileUploadAPI.uploadFile(file, formData.description);
                
                if (uploadResponse.data.code !== ResultEnum.SUCCESS) {
                  throw new Error(uploadResponse.data.msg || '文件上传失败');
                }

                const uploadedFile = uploadResponse.data.data;

                // 2. 创建文档记录
                const documentData: SysDocumentsForm = {
                  lib_id: formData.lib_id,
                  file_upload_id: String(uploadedFile.id),
                  chunk_size: formData.chunk_size,
                  chunk_overlap: formData.chunk_overlap,
                  status: formData.status,
                  description: formData.description,
                };

                const createResponse = await SysDocumentsAPI.createSysDocuments(documentData);
                
                if (createResponse.data.code !== ResultEnum.SUCCESS) {
                  throw new Error(createResponse.data.msg || '创建文档记录失败');
                }

                successCount++;
              } catch (error: any) {
                errorCount++;
                const errorMsg = error?.response?.data?.msg || error?.message || '处理失败';
                errors.push(`文件 ${file.name}: ${errorMsg}`);
                console.error(`处理文件 ${file.name} 失败:`, error);
              }
            })
          );

          // 等待所有任务完成
          await Promise.allSettled(tasks);

          // 显示结果
          if (successCount > 0 && errorCount === 0) {
            ElMessage.success(`成功上传并创建 ${successCount} 个文档`);
            dialogVisible.visible = false;
            resetForm();
            handleCloseDialog();
            handleResetQuery();
          } else if (successCount > 0 && errorCount > 0) {
            ElMessage.warning(
              `成功: ${successCount} 个，失败: ${errorCount} 个\n${errors.slice(0, 3).join('\n')}${errors.length > 3 ? '\n...' : ''}`
            );
            handleResetQuery();
          } else {
            ElMessage.error(
              `所有文件处理失败\n${errors.slice(0, 3).join('\n')}${errors.length > 3 ? '\n...' : ''}`
            );
          }
        } catch (error: any) {
          console.error(error);
          ElMessage.error('批量处理失败');
        } finally {
          loading.value = false;
          isUploading.value = false;
        }
      }
    }
  });
}

// 删除、批量删除
async function handleDelete(ids: number[]) {
  ElMessageBox.confirm("确认删除该项数据?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        loading.value = true;
        await SysDocumentsAPI.deleteSysDocuments(ids);
        handleResetQuery();
      } catch (error: any) {
        console.error(error);
      } finally {
        loading.value = false;
      }
    })
    .catch(() => {
      ElMessageBox.close();
    });
}

// 批量启用/停用
async function handleMoreClick(status: string) {
  if (selectIds.value.length) {
    ElMessageBox.confirm(`确认${status === "0" ? "启用" : "停用"}该项数据?`, "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    })
      .then(async () => {
        try {
          loading.value = true;
          await SysDocumentsAPI.batchSysDocuments({ ids: selectIds.value, status });
          handleResetQuery();
        } catch (error: any) {
          console.error(error);
        } finally {
          loading.value = false;
        }
      })
      .catch(() => {
        ElMessageBox.close();
      });
  }
}

// 处理上传
const handleUpload = async (formData: FormData) => {
  try {
    const response = await SysDocumentsAPI.importSysDocuments(formData);
    if (response.data.code === ResultEnum.SUCCESS) {
      ElMessage.success(`${response.data.msg}，${response.data.data}`);
      importDialogVisible.value = false;
      await handleQuery();
    }
  } catch (error: any) {
    console.error(error);
  }
};

onMounted(async () => {
  // 预加载字典数据
  if (dictTypes.length > 0) {
    await dictStore.getDict(dictTypes)
  }
  // 加载知识库列表
  await loadLibraries();
  // 加载数据
  loadingData();
});
</script>

<style lang="scss" scoped>
.upload-demo {
  width: 100%;
}
</style>