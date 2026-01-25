<!-- 知识库管理 -->
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
        <el-form-item label="知识库名称" prop="lib_name">
          <el-input v-model="queryFormData.lib_name" placeholder="请输入知识库名称" clearable style="width: 200px" />
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
        <el-form-item prop="created_time" label="创建时间">
          <DatePicker v-model="createdDateRange" @update:model-value="handleCreatedDateRangeChange" />
        </el-form-item>
        <!-- 查询、重置按钮 -->
        <el-form-item>
          <el-button
            v-hasPerm="['module_gencode:sys_libraries:query']"
            type="primary"
            icon="search"
            @click="handleQuery"
          >
            查询
          </el-button>
          <el-button
            v-hasPerm="['module_gencode:sys_libraries:query']"
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
            知识库列表
            <el-tooltip content="知识库列表">
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
                v-hasPerm="['module_gencode:sys_libraries:create']"
                type="success"
                icon="plus"
                @click="handleOpenDialog('create')"
              >
                新建知识库
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_gencode:sys_libraries:delete']"
                type="danger"
                icon="delete"
                :disabled="selectIds.length === 0"
                @click="handleDelete(selectIds)"
              >
                批量移除
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-dropdown v-hasPerm="['module_gencode:sys_libraries:batch']" trigger="click">
                <el-button type="default" :disabled="selectIds.length === 0" icon="ArrowDown">
                  更多
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item :icon="Check" @click="handleMoreClick('0')">
                      批量启用
                    </el-dropdown-item>
                    <el-dropdown-item :icon="CircleClose" @click="handleMoreClick('1')">
                      批量禁用
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
                  v-hasPerm="['module_gencode:sys_libraries:import']"
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
                  v-hasPerm="['module_gencode:sys_libraries:export']"
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
                  v-hasPerm="['module_gencode:sys_libraries:query']"
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

      <!-- 表格区域：知识库列表 -->
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
        <el-table-column v-if="tableColumns.find((col) => col.prop === 'status')?.show" label="状态" prop="status" min-width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status == '0' ? 'success' : 'info'">
              {{ scope.row.status == '0' ? '启用' : '停用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find((col) => col.prop === 'lib_name')?.show" label="知识库名称" prop="lib_name" min-width="140">
        </el-table-column>
        <el-table-column v-if="tableColumns.find((col) => col.prop === 'description')?.show" label="描述" prop="description" min-width="140">
        </el-table-column>
        <el-table-column v-if="tableColumns.find((col) => col.prop === 'created_time')?.show" label="创建时间" prop="created_time" min-width="150">
        </el-table-column>
        <el-table-column v-if="tableColumns.find((col) => col.prop === 'created_id')?.show" label="创建人" prop="created_id" min-width="100">
          <template #default="scope">
            <el-tag>{{ scope.row.created_by?.name }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find((col) => col.prop === 'updated_time')?.show" label="更新时间" prop="updated_time" min-width="150">
        </el-table-column>
        <el-table-column v-if="tableColumns.find((col) => col.prop === 'updated_id')?.show" label="最后更新人" prop="updated_id" min-width="100">
          <template #default="scope">
            <el-tag>{{ scope.row.updated_by?.name }}</el-tag>
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
              v-hasPerm="['module_gencode:sys_libraries:detail']"
              type="info"
              size="small"
              link
              icon="document"
              @click="handleOpenDialog('detail', scope.row.id)"
            >
              查看
            </el-button>
            <el-button
              v-hasPerm="['module_gencode:sys_libraries:update']"
              type="primary"
              size="small"
              link
              icon="edit"
              @click="handleOpenDialog('update', scope.row.id)"
            >
              修改
            </el-button>
            <el-button
              v-hasPerm="['module_gencode:sys_libraries:delete']"
              type="danger"
              size="small"
              link
              icon="delete"
              @click="handleDelete([scope.row.id])"
            >
              移除
            </el-button>
            <el-button
              v-hasPerm="['module_gencode:sys_lib_permissions:create']"
              type="warning"
              size="small"
              link
              icon="setting"
              @click="handleOpenPermissionDialog(scope.row)"
            >
              权限设置
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
            <el-descriptions-item label="ID" :span="2">
              {{ detailFormData.id }}
            </el-descriptions-item>
            <el-descriptions-item label="唯一标识" :span="2">
              {{ detailFormData.uuid }}
            </el-descriptions-item>
            <el-descriptions-item label="启用状态" :span="2">
              <el-tag :type="detailFormData.status == '0' ? 'success' : 'danger'">
                {{ detailFormData.status == '0' ? "启用" : "停用" }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="描述" :span="2">
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
            <el-descriptions-item label="最后更新人" :span="2">
              {{ detailFormData.updated_by?.name }}
            </el-descriptions-item>
            <el-descriptions-item label="知识库名称" :span="2">
              {{ detailFormData.lib_name }}
            </el-descriptions-item>
            <el-descriptions-item label="集合名称" :span="2">
              {{ detailFormData.collection_name }}
            </el-descriptions-item>
            <el-descriptions-item label="知识库类型" :span="2">
              {{ detailFormData.lib_type }}
            </el-descriptions-item>
            <el-descriptions-item label="嵌入模型" :span="2">
              {{ detailFormData.embedding_model }}
            </el-descriptions-item>
        </el-descriptions>
      </template>

      <!-- 新增、编辑表单 -->
      <template v-else>
        <el-form ref="dataFormRef" :model="formData" :rules="rules" label-suffix=":" label-width="auto" label-position="right">
          <el-form-item label="启用状态" prop="status" :required="true">
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
          <el-form-item label="知识库名称" prop="lib_name" :required="false">
            <el-input v-model="formData.lib_name" placeholder="请输入知识库名称" />
          </el-form-item>
          <el-form-item label="集合名称" prop="collection_name" :required="false">
            <el-input v-model="formData.collection_name" placeholder="请输入集合名称" />
          </el-form-item>
          <el-form-item label="嵌入模型" prop="embedding_model" :required="false">
            <el-input v-model="formData.embedding_model" placeholder="请输入嵌入模型" />
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

    <!-- 权限设置弹窗 -->
    <el-dialog
      v-model="permissionDialogVisible"
      title="设置知识库权限"
      width="600px"
      @close="handleClosePermissionDialog"
    >
      <el-form
        ref="permissionFormRef"
        :model="permissionFormData"
        :rules="permissionRules"
        label-suffix=":"
        label-width="120px"
        label-position="right"
      >
        <el-form-item label="选择用户" prop="user_ids" :required="true">
          <TableSelect
            :text="userSelectText"
            :select-config="userSelectConfig"
            @confirm-click="handleUserConfirm"
            @clear-click="handleUserClear"
          />
        </el-form-item>
        <el-form-item label="权限类型" prop="privilege_type" :required="true">
          <el-select
            v-model="permissionFormData.privilege_type"
            placeholder="请选择权限类型"
            style="width: 100%"
          >
            <el-option
              v-for="item in dictStore.getDictArray('sys_lib_privilege_type')"
              :key="item.dict_value"
              :value="item.dict_value"
              :label="item.dict_label"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status" :required="true">
          <el-radio-group v-model="permissionFormData.status">
            <el-radio value="0">启用</el-radio>
            <el-radio value="1">停用</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注/描述" prop="description">
          <el-input
            v-model="permissionFormData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入备注/描述"
            maxlength="255"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="handleClosePermissionDialog">取消</el-button>
          <el-button type="primary" @click="handleSubmitPermission" :loading="permissionLoading">
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "SysLibraries",
  inheritAttrs: false,
});

import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { QuestionFilled, ArrowUp, ArrowDown, Check, CircleClose } from '@element-plus/icons-vue'
import { formatToDateTime } from "@/utils/dateUtil";
import { useDictStore } from "@/store";
import { ResultEnum } from '@/enums/api/result.enum'
import DatePicker from "@/components/DatePicker/index.vue";
import type { IContentConfig } from "@/components/CURD/types";
import ImportModal from "@/components/CURD/ImportModal.vue";
import ExportModal from "@/components/CURD/ExportModal.vue";
import TableSelect, { type ISelectConfig } from "@/components/TableSelect/index.vue";
import SysLibrariesAPI, { SysLibrariesPageQuery, SysLibrariesTable, SysLibrariesForm } from '@/api/module_gencode/sys_libraries'
import SysUserLibrariesAPI, { SysUserLibrariesBatchAssociateForm } from '@/api/module_gencode/sys_user_libraries'
import UserAPI from '@/api/module_system/user'

const visible = ref(true);
const isExpand = ref(false);
const isExpandable = ref(true);
const queryFormRef = ref();
const dataFormRef = ref();
const total = ref(0);
const selectIds = ref<number[]>([]);
const selectionRows = ref<SysLibrariesTable[]>([]);
const loading = ref(false);

// 字典仓库与需要加载的字典类型
const dictStore = useDictStore()
const dictTypes: any = [
  'sys_lib_privilege_type'
]

// 分页表单
const pageTableData = ref<SysLibrariesTable[]>([]);

// 表格列配置
const tableColumns = ref([
  { prop: "selection", label: "选择框", show: true },
  { prop: "index", label: "序号", show: true },
  { prop: 'status', label: '状态', show: true },
  { prop: 'lib_name', label: '知识库名称', show: true },
  { prop: 'description', label: '描述', show: true },
  { prop: 'created_time', label: '创建时间', show: true },
  { prop: 'created_id', label: '创建人', show: true },
  { prop: 'updated_time', label: '更新时间', show: true },
  { prop: 'updated_id', label: '最后更新人', show: true },
  { prop: 'operation', label: '操作', show: true }
]);

// 导出列（不含选择/序号/操作）
const exportColumns = [
  { prop: 'status', label: '状态' },
  { prop: 'lib_name', label: '知识库名称' },
  { prop: 'description', label: '描述' },
  { prop: 'created_time', label: '创建时间' },
  { prop: 'created_id', label: '创建人' },
  { prop: 'updated_time', label: '更新时间' },
  { prop: 'updated_id', label: '最后更新人' },
]

// 导入/导出配置
const curdContentConfig = {
  permPrefix: "module_gencode:sys_libraries",
  cols: exportColumns as any,
  importTemplate: () => SysLibrariesAPI.downloadTemplateSysLibraries(),
  exportsAction: async (params: any) => {
    const query: any = { ...params };
    query.status = '0';
    query.page_no = 1;
    query.page_size = 9999;
    const all: any[] = [];
    while (true) {
      const res = await SysLibrariesAPI.listSysLibraries(query);
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
const detailFormData = ref<SysLibrariesTable>({});
// 日期范围临时变量
const createdDateRange = ref<[Date, Date] | []>([]);
// 更新时间范围临时变量
const updatedDateRange = ref<[Date, Date] | []>([]);

// 处理创建时间范围变化
function handleCreatedDateRangeChange(range: [Date, Date]) {
  createdDateRange.value = range;
  if (range && range.length === 2) {
    queryFormData.created_time = [formatToDateTime(range[0]), formatToDateTime(range[1])];
  } else {
    queryFormData.created_time = undefined;
  }
}

// 处理更新时间范围变化
function handleUpdatedDateRangeChange(range: [Date, Date]) {
  updatedDateRange.value = range;
  if (range && range.length === 2) {
    queryFormData.updated_time = [formatToDateTime(range[0]), formatToDateTime(range[1])];
  } else {
    queryFormData.updated_time = undefined;
  }
}

// 分页查询参数
const queryFormData = reactive<SysLibrariesPageQuery>({
  page_no: 1,
  page_size: 10,
  status: undefined,
  created_time: undefined,
  updated_time: undefined,
  created_id: undefined,
  updated_id: undefined,
  lib_name: undefined,
  collection_name: undefined,
  embedding_model: undefined,
});


// 编辑表单
const formData = reactive<SysLibrariesForm>({
  id: undefined,
  status: undefined,
  description: undefined,
  lib_name: undefined,
  collection_name: undefined,
  lib_type: undefined,
  embedding_model: undefined,
  chunk_size: undefined,
  chunk_overlap: undefined,
  similarity_threshold: undefined,
  max_chunks: undefined,
});

// 弹窗启用状态
const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
});

// 表单验证规则
const rules = reactive({
  id: [
    { required: false, message: '请输入主键ID', trigger: 'blur' },
  ],
  uuid: [
    { required: true, message: '请输入UUID全局唯一标识', trigger: 'blur' },
  ],
  status: [
    { required: true, message: '请输入启用状态', trigger: 'blur' },
  ],
  description: [
    { required: false, message: '请输入描述', trigger: 'blur' },
  ],
  created_time: [
    { required: true, message: '请输入创建时间', trigger: 'blur' },
  ],
  updated_time: [
    { required: true, message: '请输入更新时间', trigger: 'blur' },
  ],
  created_id: [
    { required: false, message: '请输入创建人', trigger: 'blur' },
  ],
  updated_id: [
    { required: false, message: '请输入最后更新人', trigger: 'blur' },
  ],
  lib_name: [
    { required: true, message: '请输入知识库名称', trigger: 'blur' },
  ],
  collection_name: [
    { required: false, message: '请输入集合名称', trigger: 'blur' },
  ],
  embedding_model: [
    { required: false, message: '请输入嵌入模型', trigger: 'blur' },
  ],
});

// 导入弹窗显示启用状态
const importDialogVisible = ref(false);

// 导出弹窗显示启用状态
const exportsDialogVisible = ref(false);

// 权限设置弹窗相关
const permissionDialogVisible = ref(false);
const permissionFormRef = ref();
const permissionLoading = ref(false);
const currentLibrary = ref<SysLibrariesTable | null>(null);

// 权限表单数据
const permissionFormData = reactive<SysUserLibrariesBatchAssociateForm>({
  user_ids: [],
  lib_id: 0,
  privilege_type: "",
  status: "0",
  description: "",
});

// 选中的用户数据
const selectedUsers = ref<any[]>([]);

// 权限表单验证规则
const permissionRules = reactive({
  user_ids: [{ required: true, message: "请选择用户", trigger: "change" }],
  privilege_type: [{ required: true, message: "请选择权限类型", trigger: "change" }],
  status: [{ required: true, message: "请选择状态", trigger: "change" }],
});


// 用户选择器配置
const userSelectConfig: ISelectConfig = {
  pk: "id",
  multiple: true,
  width: "100%",
  placeholder: "请选择用户",
  popover: {
    width: 720,
  },
  formItems: [
    {
      type: "select",
      label: "状态",
      prop: "status",
      initialValue: "0",
      attrs: {
        placeholder: "全部",
        clearable: true,
      },
      options: [
        { label: "启用", value: "0" },
        { label: "停用", value: "1" },
      ],
    },
  ],
  indexAction(params: any) {
    const query: any = { ...params };
    Object.keys(query).forEach((k) => {
      const v = query[k];
      if (v === "" || v === null || v === undefined) {
        delete query[k];
      }
    });
    return UserAPI.listUser(query).then((res: any) => {
      return {
        total: res.data.data.total,
        list: res.data.data.items,
      };
    });
  },
  tableColumns: [
    { type: "selection", width: 50, align: "center" },
    { label: "编号", align: "center", prop: "id", width: 100 },
    { label: "账号", align: "center", prop: "username" },
    { label: "用户名", align: "center", prop: "name", width: 120 },
  ],
};

// 选择器显示文本
const userSelectText = computed(() => {
  if (selectedUsers.value.length === 0) return "";
  return `已选择 ${selectedUsers.value.length} 个用户`;
});

// 用户选择确认
function handleUserConfirm(data: any[]) {
  selectedUsers.value = data;
  permissionFormData.user_ids = data.map((item) => item.id);
  // 手动触发验证
  if (permissionFormRef.value) {
    permissionFormRef.value.validateField("user_ids");
  }
}

// 用户选择清空
function handleUserClear() {
  selectedUsers.value = [];
  permissionFormData.user_ids = [];
  // 手动触发验证
  if (permissionFormRef.value) {
    permissionFormRef.value.validateField("user_ids");
  }
}

// 打开权限设置弹窗
function handleOpenPermissionDialog(row: SysLibrariesTable) {
  currentLibrary.value = row;
  permissionFormData.lib_id = row.id!;
  permissionFormData.user_ids = [];
  const privilegeTypeDict = dictStore.getDictArray("sys_lib_privilege_type");
  permissionFormData.privilege_type = privilegeTypeDict.length > 0 ? privilegeTypeDict[0].dict_value : "";
  permissionFormData.status = "0";
  permissionFormData.description = "";
  selectedUsers.value = [];
  permissionDialogVisible.value = true;
}

// 关闭权限设置弹窗
function handleClosePermissionDialog() {
  permissionDialogVisible.value = false;
  if (permissionFormRef.value) {
    permissionFormRef.value.resetFields();
    permissionFormRef.value.clearValidate();
  }
  currentLibrary.value = null;
  selectedUsers.value = [];
}

// 提交权限设置
async function handleSubmitPermission() {
  if (!permissionFormRef.value) return;
  
  permissionFormRef.value.validate(async (valid: any) => {
    if (valid) {
      if (!permissionFormData.user_ids || permissionFormData.user_ids.length === 0) {
        ElMessage.warning("请选择用户");
        return;
      }
      
      permissionLoading.value = true;
      try {
        const response = await SysUserLibrariesAPI.batchAssociateSysUserLibraries(permissionFormData);
        if (response.data.code === ResultEnum.SUCCESS) {
          ElMessage.success(response.data.msg || response.data.data?.message || "批量关联用户成功");
          handleClosePermissionDialog();
        } else {
          ElMessage.error(response.data.msg || "批量关联用户失败");
        }
      } catch (error: any) {
        console.error(error);
        ElMessage.error(error?.response?.data?.msg || "批量关联用户失败");
      } finally {
        permissionLoading.value = false;
      }
    }
  });
}

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
    const response = await SysLibrariesAPI.listSysLibraries(queryFormData);
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
  // 重置日期范围选择器
  createdDateRange.value = [];
  updatedDateRange.value = [];
  queryFormData.created_time = undefined;
  queryFormData.updated_time = undefined;
  loadingData();
}

// 定义初始表单数据常量
const initialFormData: SysLibrariesForm = {
  id: undefined,
  status: undefined,
  description: undefined,
  lib_name: undefined,
  collection_name: undefined,
  lib_type: undefined,
  embedding_model: undefined,
  chunk_size: undefined,
  chunk_overlap: undefined,
  similarity_threshold: undefined,
  max_chunks: undefined,
};

// 重置表单
async function resetForm() {
  if (dataFormRef.value) {
    dataFormRef.value.resetFields();
    dataFormRef.value.clearValidate();
  }
  // 完全重置 formData 为初始启用状态
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
    const response = await SysLibrariesAPI.detailSysLibraries(id);
    if (type === "detail") {
      dialogVisible.title = "详情";
      Object.assign(detailFormData.value, response.data.data);
    } else if (type === "update") {
      dialogVisible.title = "修改知识库";
      Object.assign(formData, response.data.data);
    }
  } else {
      dialogVisible.title = "新建知识库";
    formData.id = undefined;
    formData.status = undefined;
    formData.description = undefined;
    formData.lib_name = undefined;
    formData.collection_name = undefined;
    formData.embedding_model = undefined;
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
          await SysLibrariesAPI.updateSysLibraries(id, { id, ...formData });
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
          await SysLibrariesAPI.createSysLibraries(formData);
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
        await SysLibrariesAPI.deleteSysLibraries(ids);
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
          await SysLibrariesAPI.batchSysLibraries({ ids: selectIds.value, status });
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
    const response = await SysLibrariesAPI.importSysLibraries(formData);
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
  loadingData();
});
</script>

<style lang="scss" scoped>
</style>