<!-- 文件上传 -->
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
        <el-form-item label="文件名" prop="origin_name">
          <el-input v-model="queryFormData.origin_name" placeholder="请输入文件名" clearable style="width: 200px" />
        </el-form-item>
        <el-form-item label="文件类型" prop="file_type">
          <el-input v-model="queryFormData.file_type" placeholder="请输入文件类型，如：pdf、jpg" clearable style="width: 200px" />
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
        <!-- 查询、重置、展开/收起按钮 -->
        <el-form-item>
          <el-button
            v-hasPerm="['module_gencode:sys_file_upload:query']"
            type="primary"
            icon="search"
            @click="handleQuery"
          >
            查询
          </el-button>
          <el-button
            v-hasPerm="['module_gencode:sys_file_upload:query']"
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
            文件上传列表
            <el-tooltip content="文件上传列表">
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
                v-hasPerm="['module_gencode:sys_file_upload:upload']"
                type="primary"
                icon="upload"
                @click="handleOpenUploadDialog"
              >
                上传文件
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_gencode:sys_file_upload:create']"
                type="success"
                icon="plus"
                @click="handleOpenDialog('create')"
              >
                新增
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_gencode:sys_file_upload:delete']"
                type="danger"
                icon="delete"
                :disabled="selectIds.length === 0"
                @click="handleDelete(selectIds)"
              >
                批量删除
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-dropdown v-hasPerm="['module_gencode:sys_file_upload:batch']" trigger="click">
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
                  v-hasPerm="['module_gencode:sys_file_upload:import']"
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
                  v-hasPerm="['module_gencode:sys_file_upload:export']"
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
                  v-hasPerm="['module_gencode:sys_file_upload:query']"
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
        <el-table-column v-if="tableColumns.find((col) => col.prop === 'origin_name')?.show" label="文件名" prop="origin_name" min-width="180" show-overflow-tooltip>
        </el-table-column>
        <el-table-column v-if="tableColumns.find((col) => col.prop === 'file_type')?.show" label="文件类型" prop="file_type" min-width="100" align="center">
        </el-table-column>
        <el-table-column v-if="tableColumns.find((col) => col.prop === 'file_size')?.show" label="大小" prop="file_size" min-width="100" align="right">
          <template #default="scope">
            {{ formatFileSize(scope.row.file_size) }}
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find((col) => col.prop === 'status')?.show" label="状态" prop="status" min-width="80" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.status == '0' ? 'success' : 'info'" size="small">
              {{ scope.row.status == '0' ? '启用' : '停用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find((col) => col.prop === 'description')?.show" label="备注" prop="description" min-width="150" show-overflow-tooltip>
        </el-table-column>
        <el-table-column v-if="tableColumns.find((col) => col.prop === 'created_time')?.show" label="上传时间" prop="created_time" min-width="160">
        </el-table-column>
        <el-table-column v-if="tableColumns.find((col) => col.prop === 'created_id')?.show" label="上传人" prop="created_id" min-width="100">
          <template #default="scope">
            <el-tag size="small">{{ scope.row.created_by?.name || '-' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'operation')?.show"
          fixed="right"
          label="操作"
          align="center"
          min-width="220"
        >
          <template #default="scope">
            <el-button
              v-hasPerm="['module_gencode:sys_file_upload:query']"
              v-if="scope.row.file_path"
              type="success"
              size="small"
              link
              icon="download"
              @click="handleDownloadFile(scope.row.id, scope.row.origin_name)"
            >
              下载
            </el-button>
            <el-button
              v-hasPerm="['module_gencode:sys_file_upload:detail']"
              type="info"
              size="small"
              link
              icon="document"
              @click="handleOpenDialog('detail', scope.row.id)"
            >
              详情
            </el-button>
            <el-button
              v-hasPerm="['module_gencode:sys_file_upload:update']"
              type="primary"
              size="small"
              link
              icon="edit"
              @click="handleOpenDialog('update', scope.row.id)"
            >
              编辑
            </el-button>
            <el-button
              v-hasPerm="['module_gencode:sys_file_upload:delete']"
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
        <el-descriptions :column="2" border>
            <el-descriptions-item label="文件名" :span="2">
              {{ detailFormData.origin_name }}
            </el-descriptions-item>
            <el-descriptions-item label="文件类型" :span="1">
              {{ detailFormData.file_type || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="文件大小" :span="1">
              {{ formatFileSize(detailFormData.file_size) }}
            </el-descriptions-item>
            <el-descriptions-item label="状态" :span="1">
              <el-tag :type="detailFormData.status == '0' ? 'success' : 'info'" size="small">
                {{ detailFormData.status == '0' ? "启用" : "停用" }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="上传时间" :span="1">
              {{ detailFormData.created_time }}
            </el-descriptions-item>
            <el-descriptions-item label="备注" :span="2">
              {{ detailFormData.description || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="上传人" :span="1">
              {{ detailFormData.created_by?.name || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="更新时间" :span="1">
              {{ detailFormData.updated_time || '-' }}
            </el-descriptions-item>
        </el-descriptions>
      </template>

      <!-- 新增、编辑表单 -->
      <template v-else>
        <el-form ref="dataFormRef" :model="formData" :rules="rules" label-suffix=":" label-width="auto" label-position="right">
          <el-form-item label="原始文件名" prop="origin_name" :required="false">
            <el-input v-model="formData.origin_name" placeholder="请输入原始文件名" />
          </el-form-item>
          <el-form-item label="新文件名" prop="file_name" :required="false">
            <el-input v-model="formData.file_name" placeholder="请输入新文件名" />
          </el-form-item>
          <el-form-item label="文件存储路径" prop="file_path" :required="false">
            <el-input v-model="formData.file_path" placeholder="请输入文件存储路径" />
          </el-form-item>
          <el-form-item label="文件大小" prop="file_size" :required="false">
            <el-input v-model="formData.file_size" placeholder="请输入文件大小" />
          </el-form-item>
          <el-form-item label="文件类型/扩展名" prop="file_type" :required="false">
            <el-input v-model="formData.file_type" placeholder="请输入文件类型/扩展名" />
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

    <!-- 文件上传弹窗 -->
    <el-dialog
      v-model="uploadDialogVisible"
      title="批量上传文件"
      width="800px"
      @close="handleCloseUploadDialog"
    >
      <el-form ref="uploadFormRef" :model="uploadFormData" label-width="100px">
        <el-form-item label="选择文件" prop="file" :required="true">
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
                支持一次选择多个文件，最多50个文件，单个文件不超过20MB<br>
                <span style="color: var(--el-color-primary); font-size: 12px;">
                  ✨ 支持最多{{MAX_CONCURRENT_UPLOADS }}个文件并发上传，提升上传速度
                </span>
              </div>
            </template>
          </el-upload>
        </el-form-item>
        <el-form-item label="文件描述" prop="description">
          <el-input
            v-model="uploadFormData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入文件描述（可选，将应用于所有文件）"
            maxlength="255"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      
      <!-- 上传进度显示 -->
      <div v-if="uploadProgressList.length > 0" class="upload-progress-container">
        <el-divider>上传进度</el-divider>
        <div v-for="(item, index) in uploadProgressList" :key="index" class="upload-progress-item">
          <div class="progress-header">
            <span class="file-name">{{ item.fileName }}</span>
            <el-tag :type="item.status === 'success' ? 'success' : item.status === 'error' ? 'danger' : 'info'" size="small">
              {{ item.status === 'success' ? '成功' : item.status === 'error' ? '失败' : '上传中' }}
            </el-tag>
          </div>
          <el-progress
            v-if="item.status === 'uploading' || item.status === 'error'"
            :percentage="item.progress"
            :status="item.status === 'error' ? 'exception' : undefined"
          />
          <div v-if="item.errorMsg" class="error-msg">{{ item.errorMsg }}</div>
        </div>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="handleCloseUploadDialog" :disabled="isUploading">取消</el-button>
          <el-button type="primary" :loading="isUploading" @click="handleSubmitUpload" :disabled="fileList.length === 0 || isUploading">
            {{ isUploading ? `上传中 (${uploadSuccessCount + uploadErrorCount}/${fileList.length})` : '开始上传' }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "SysFileUpload",
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
import SysFileUploadAPI, { SysFileUploadPageQuery, SysFileUploadTable, SysFileUploadForm } from '@/api/module_gencode/sys_file_upload'

const visible = ref(true);
const queryFormRef = ref();
const dataFormRef = ref();
const total = ref(0);
const selectIds = ref<number[]>([]);
const selectionRows = ref<SysFileUploadTable[]>([]);
const loading = ref(false);

// 字典仓库与需要加载的字典类型
const dictStore = useDictStore()
const dictTypes: any = [
]

// 分页表单
const pageTableData = ref<SysFileUploadTable[]>([]);

// 表格列配置
const tableColumns = ref([
  { prop: "selection", label: "选择框", show: true },
  { prop: "index", label: "序号", show: true },
  { prop: 'origin_name', label: '文件名', show: true },
  { prop: 'file_type', label: '文件类型', show: true },
  { prop: 'file_size', label: '大小', show: true },
  { prop: 'status', label: '状态', show: true },
  { prop: 'description', label: '备注', show: true },
  { prop: 'created_time', label: '上传时间', show: true },
  { prop: 'created_id', label: '上传人', show: true },
  { prop: 'operation', label: '操作', show: true }
]);

// 导出列（不含选择/序号/操作）
// 导出列（不含选择/序号/操作）
const exportColumns = [
  { prop: 'origin_name', label: '文件名' },
  { prop: 'file_type', label: '文件类型' },
  { prop: 'file_size', label: '文件大小' },
  { prop: 'status', label: '状态' },
  { prop: 'description', label: '备注' },
  { prop: 'created_time', label: '上传时间' },
  { prop: 'created_id', label: '上传人' },
]

// 导入/导出配置
const curdContentConfig = {
  permPrefix: "module_gencode:sys_file_upload",
  cols: exportColumns as any,
  importTemplate: () => SysFileUploadAPI.downloadTemplateSysFileUpload(),
  exportsAction: async (params: any) => {
    const query: any = { ...params };
    query.status = '0';
    query.page_no = 1;
    query.page_size = 9999;
    const all: any[] = [];
    while (true) {
      const res = await SysFileUploadAPI.listSysFileUpload(query);
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
const detailFormData = ref<SysFileUploadTable>({});


// 分页查询参数
const queryFormData = reactive<SysFileUploadPageQuery>({
  page_no: 1,
  page_size: 10,
  origin_name: undefined,
  file_name: undefined,
  file_path: undefined,
  file_size: undefined,
  file_type: undefined,
  status: undefined,
  created_time: undefined,
  updated_time: undefined,
  created_id: undefined,
  updated_id: undefined,
});


// 编辑表单
const formData = reactive<SysFileUploadForm>({
  origin_name: undefined,
  file_name: undefined,
  file_path: undefined,
  file_size: undefined,
  file_type: undefined,
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
  origin_name: [
    { required: true, message: '请输入原始文件名', trigger: 'blur' },
  ],
  file_name: [
    { required: true, message: '请输入新文件名（生成后的文件名）', trigger: 'blur' },
  ],
  file_path: [
    { required: true, message: '请输入文件存储路径', trigger: 'blur' },
  ],
  file_size: [
    { required: false, message: '请输入文件大小（字节）', trigger: 'blur' },
  ],
  file_type: [
    { required: false, message: '请输入文件类型/扩展名', trigger: 'blur' },
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

// 文件上传相关
const uploadDialogVisible = ref(false);
const uploadFormRef = ref();
const uploadRef = ref();
const isUploading = ref(false);
const fileList = ref<any[]>([]);
const uploadFormData = reactive({
  description: '',
});

// 上传进度相关
interface UploadProgressItem {
  fileName: string;
  status: 'waiting' | 'uploading' | 'success' | 'error';
  progress: number;
  errorMsg?: string;
}
const uploadProgressList = ref<UploadProgressItem[]>([]);
const uploadSuccessCount = ref(0);
const uploadErrorCount = ref(0);

// 并发上传配置
const MAX_CONCURRENT_UPLOADS = 3; // 最大并发上传数

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
    const response = await SysFileUploadAPI.listSysFileUpload(queryFormData);
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


// 重置查询
async function handleResetQuery() {
  queryFormRef.value.resetFields();
  queryFormData.page_no = 1;
  loadingData();
}

// 格式化文件大小
function formatFileSize(size: number | string | undefined): string {
  if (!size) return '-';
  const numSize = typeof size === 'string' ? parseInt(size) : size;
  if (numSize === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(numSize) / Math.log(k));
  return Math.round((numSize / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

// 定义初始表单数据常量
const initialFormData: SysFileUploadForm = {
  origin_name: undefined,
  file_name: undefined,
  file_path: undefined,
  file_size: undefined,
  file_type: undefined,
  id: undefined,
  status: undefined,
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
  if (id) {
    const response = await SysFileUploadAPI.detailSysFileUpload(id);
    if (type === "detail") {
      dialogVisible.title = "详情";
      Object.assign(detailFormData.value, response.data.data);
    } else if (type === "update") {
      dialogVisible.title = "修改";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增SysFileUpload";
    formData.origin_name = undefined;
    formData.file_name = undefined;
    formData.file_path = undefined;
    formData.file_size = undefined;
    formData.file_type = undefined;
    formData.id = undefined;
    formData.status = undefined;
    formData.description = undefined;
  }
  dialogVisible.visible = true;
}

// 提交表单（防抖）
async function handleSubmit() {
  // 表单校验
  dataFormRef.value.validate(async (valid: any) => {
    if (valid) {
      loading.value = true;
      // 根据弹窗传入的参数(deatil\create\update)判断走什么逻辑
      const id = formData.id;
      if (id) {
        try {
          await SysFileUploadAPI.updateSysFileUpload(id, { id, ...formData });
          dialogVisible.visible = false;
          resetForm();
          handleCloseDialog();
          handleResetQuery();
        } catch (error: any) {
          console.error(error);
        } finally {
          loading.value = false;
        }
      } else {
        try {
          await SysFileUploadAPI.createSysFileUpload(formData);
          dialogVisible.visible = false;
          resetForm();
          handleCloseDialog();
          handleResetQuery();
        } catch (error: any) {
          console.error(error);
        } finally {
          loading.value = false;
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
        await SysFileUploadAPI.deleteSysFileUpload(ids);
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
          await SysFileUploadAPI.batchSysFileUpload({ ids: selectIds.value, status });
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
    const response = await SysFileUploadAPI.importSysFileUpload(formData);
    if (response.data.code === ResultEnum.SUCCESS) {
      ElMessage.success(`${response.data.msg}，${response.data.data}`);
      importDialogVisible.value = false;
      await handleQuery();
    }
  } catch (error: any) {
    console.error(error);
  }
};

// 打开文件上传弹窗
function handleOpenUploadDialog() {
  uploadDialogVisible.value = true;
  fileList.value = [];
  uploadFormData.description = '';
  uploadProgressList.value = [];
  uploadSuccessCount.value = 0;
  uploadErrorCount.value = 0;
}

// 关闭文件上传弹窗
function handleCloseUploadDialog() {
  if (isUploading.value) {
    ElMessageBox.confirm('文件正在上传中，确定要关闭吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }).then(() => {
      uploadDialogVisible.value = false;
      resetUploadDialog();
    }).catch(() => {});
  } else {
    uploadDialogVisible.value = false;
    resetUploadDialog();
  }
}

// 重置上传弹窗
function resetUploadDialog() {
  fileList.value = [];
  uploadFormData.description = '';
  uploadProgressList.value = [];
  uploadSuccessCount.value = 0;
  uploadErrorCount.value = 0;
  if (uploadFormRef.value) {
    uploadFormRef.value.resetFields();
  }
  if (uploadRef.value) {
    uploadRef.value.clearFiles();
  }
}

// 文件选择变化
function handleFileChange(file: any, fileListParam: any[]) {
  // 更新本地的 fileList，确保按钮状态正确
  fileList.value = [...fileListParam];
}

// 文件移除
function handleFileRemove(file: any, fileListParam: any[]) {
  // 更新本地的 fileList
  fileList.value = [...fileListParam];
  
  // 从进度列表中移除对应的项
  const index = uploadProgressList.value.findIndex(item => item.fileName === file.name);
  if (index > -1) {
    uploadProgressList.value.splice(index, 1);
  }
}

// 并发上传控制器
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
        this.process(); // 处理队列中的下一个任务
      }
    }
  }

  reset() {
    this.running = 0;
    this.queue = [];
  }
}

// 上传单个文件的函数
async function uploadSingleFile(file: File, index: number, description: string): Promise<void> {
  // 更新状态为上传中
  uploadProgressList.value[index].status = 'uploading';
  uploadProgressList.value[index].progress = 0;

  try {
    // 模拟进度更新（实际进度需要后端支持，这里使用简单模拟）
    const progressInterval = setInterval(() => {
      if (uploadProgressList.value[index].status === 'uploading' && uploadProgressList.value[index].progress < 90) {
        uploadProgressList.value[index].progress += 10;
      }
    }, 100);

    const response = await SysFileUploadAPI.uploadFile(file, description);
    
    clearInterval(progressInterval);
    
    if (response.data.code === ResultEnum.SUCCESS) {
      uploadProgressList.value[index].status = 'success';
      uploadProgressList.value[index].progress = 100;
      uploadSuccessCount.value++;
    } else {
      throw new Error(response.data.msg || '上传失败');
    }
  } catch (error: any) {
    uploadProgressList.value[index].status = 'error';
    uploadProgressList.value[index].progress = 0;
    uploadProgressList.value[index].errorMsg = error?.response?.data?.msg || error?.message || '上传失败';
    uploadErrorCount.value++;
  }
}

// 提交文件上传（并发批量上传）
async function handleSubmitUpload() {
  // 从el-upload组件获取文件列表
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

  // 初始化上传进度列表
  uploadProgressList.value = validFiles.map((file: any) => ({
    fileName: file.name || '未知文件',
    status: 'waiting' as const,
    progress: 0,
  }));

  uploadSuccessCount.value = 0;
  uploadErrorCount.value = 0;
  isUploading.value = true;

  // 创建并发上传控制器
  const uploader = new ConcurrentUploader(MAX_CONCURRENT_UPLOADS);

  // 创建所有上传任务
  const uploadTasks = validFiles.map((file: File, index: number) => 
    uploader.add(() => uploadSingleFile(file, index, uploadFormData.description))
  );

  try {
    // 等待所有文件上传完成
    await Promise.allSettled(uploadTasks);
  } catch (error) {
    console.error('批量上传过程中出现错误:', error);
  }

  isUploading.value = false;

  // 显示上传结果
  if (uploadSuccessCount.value > 0 && uploadErrorCount.value === 0) {
    ElMessage.success(`成功上传 ${uploadSuccessCount.value} 个文件`);
    // 延迟关闭弹窗，让用户看到成功提示
    setTimeout(() => {
      handleCloseUploadDialog();
      handleQuery();
    }, 1500);
  } else if (uploadSuccessCount.value > 0 && uploadErrorCount.value > 0) {
    ElMessage.warning(`成功上传 ${uploadSuccessCount.value} 个文件，失败 ${uploadErrorCount.value} 个`);
    // 不自动关闭，让用户查看失败的文件
    handleQuery();
  } else {
    ElMessage.error(`所有文件上传失败，共 ${uploadErrorCount.value} 个文件`);
    // 不自动关闭，让用户查看失败原因
  }
}

// 下载文件
async function handleDownloadFile(id: number, filename?: string) {
  try {
    const response = await SysFileUploadAPI.getFile(id);
    // 创建 blob 对象
    const blob = new Blob([response.data]);
    // 创建下载链接
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename || `file_${id}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
    ElMessage.success('文件下载成功');
  } catch (error: any) {
    console.error(error);
    ElMessage.error(error?.response?.data?.msg || '文件下载失败');
  }
}

onMounted(async () => {
  // 预加载字典数据
  if (dictTypes.length > 0) {
    await dictStore.getDict(dictTypes)
  }
  loadingData();
});
</script>

<style lang="scss" scoped>
.upload-progress-container {
  margin-top: 20px;
  max-height: 300px;
  overflow-y: auto;
}

.upload-progress-item {
  margin-bottom: 15px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;

  .progress-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;

    .file-name {
      flex: 1;
      font-size: 14px;
      color: #606266;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      margin-right: 10px;
    }
  }

  .error-msg {
    margin-top: 5px;
    font-size: 12px;
    color: #f56c6c;
  }
}

:deep(.el-upload-list) {
  max-height: 200px;
  overflow-y: auto;
}

.upload-demo {
width: 100%;
  
}
</style>