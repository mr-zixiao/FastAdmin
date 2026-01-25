"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Plus, Search, Database, Sparkles, Package, Pencil, FileText, User, Calendar } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Skeleton } from "@/components/ui/skeleton"
import { toast } from "sonner"
import {
  listSysLibraries,
  createSysLibraries,
  updateSysLibraries,
  type SysLibrariesTable,
  type SysLibrariesForm,
} from "@/lib/api/sys_libraries"
import { listSysDocuments } from "@/lib/api/sys_documents"

// 嵌入模型选项
const EMBEDDING_MODELS = [
  { value: "text-embedding-3-small", label: "text-embedding-3-small" },
  { value: "text-embedding-3-large", label: "text-embedding-3-large" },
  { value: "text-embedding-v3", label: "text-embedding-v3" },
  { value: "text-embedding-ada-002", label: "text-embedding-ada-002" },
]

// 知识库卡片骨架屏
function KnowledgeCardSkeleton() {
  return (
    <Card className="cursor-pointer transition-all hover:shadow-lg">
      <CardHeader>
        <Skeleton className="h-6 w-3/4" />
        <Skeleton className="h-4 w-1/2" />
      </CardHeader>
      <CardContent className="space-y-3">
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-2/3" />
      </CardContent>
    </Card>
  )
}

// 知识库卡片组件
function KnowledgeCard({ 
  library, 
  onEdit,
  docCount 
}: { 
  library: SysLibrariesTable
  onEdit: (library: SysLibrariesTable) => void
  docCount?: number
}) {
  const router = useRouter()

  const handleEdit = (e: React.MouseEvent) => {
    e.stopPropagation()
    onEdit(library)
  }

  return (
    <Card
      className="group cursor-pointer transition-all hover:shadow-lg hover:-translate-y-1"
      onClick={() => router.push(`/knowledge/${library.id}`)}
    >
      <CardHeader>
        <div className="flex items-start justify-between">
          <CardTitle className="flex items-center gap-2 flex-1">
            <Database className="size-5 text-primary shrink-0" />
            <span className="line-clamp-1">{library.lib_name}</span>
          </CardTitle>
          <Button
            variant="ghost"
            size="icon"
            className="size-8 shrink-0 opacity-0 group-hover:opacity-100 transition-opacity"
            onClick={handleEdit}
          >
            <Pencil className="size-4" />
          </Button>
        </div>
        <CardDescription className="line-clamp-2">
          {library.description || library.collection_name}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-2">
        <div className="flex items-center gap-2 text-sm">
          <Sparkles className="size-4 text-muted-foreground" />
          <span className="text-muted-foreground">嵌入模型：</span>
          <span className="rounded-md bg-primary/10 px-2 py-0.5 text-xs font-medium text-primary">
            {library.embedding_model}
          </span>
        </div>
        {library.lib_type && (
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Package className="size-4" />
            <span>类型：{library.lib_type}</span>
          </div>
        )}
      </CardContent>
      <CardFooter className="border-t pt-4 text-xs text-muted-foreground">
        <div className="flex items-center justify-between w-full gap-4">
          <div className="flex items-center gap-1">
            <FileText className="size-3.5" />
            <span>{docCount ?? 0} 个文档</span>
          </div>
          {library.created_by?.name && (
            <div className="flex items-center gap-1">
              <User className="size-3.5" />
              <span className="truncate">{library.created_by.name}</span>
            </div>
          )}
        </div>
      </CardFooter>
    </Card>
  )
}

// 创建知识库弹窗
function CreateLibraryDialog({
  open,
  onOpenChange,
  onSuccess,
}: {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSuccess: () => void
}) {
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState<SysLibrariesForm>({
    lib_name: "",
    description: "",
    embedding_model: "text-embedding-3-small",
    collection_name: "",
    lib_type: "knowledge",
    chunk_size: "1000",
    chunk_overlap: "200",
    similarity_threshold: "0.7",
    max_chunks: "5",
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!formData.lib_name?.trim()) {
      toast.error("请输入知识库名称")
      return
    }

    if (!formData.collection_name?.trim()) {
      toast.error("请输入集合名称")
      return
    }

    setLoading(true)
    try {
      await createSysLibraries(formData)
      toast.success("知识库创建成功")
      onOpenChange(false)
      onSuccess()
      // 重置表单
      setFormData({
        lib_name: "",
        description: "",
        embedding_model: "text-embedding-3-small",
        collection_name: "",
        lib_type: "knowledge",
        chunk_size: "1000",
        chunk_overlap: "200",
        similarity_threshold: "0.7",
        max_chunks: "5",
      })
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "创建失败")
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <form onSubmit={handleSubmit}>
          <DialogHeader>
            <DialogTitle>新建知识库</DialogTitle>
            <DialogDescription>
              创建一个新的知识库来管理和存储您的文档
            </DialogDescription>
          </DialogHeader>

          <div className="grid gap-4 py-4">
            {/* 知识库名称 */}
            <div className="grid gap-2">
              <label htmlFor="lib_name" className="text-sm font-medium">
                知识库名称 <span className="text-destructive">*</span>
              </label>
              <Input
                id="lib_name"
                placeholder="请输入知识库名称"
                value={formData.lib_name || ""}
                onChange={(e) =>
                  setFormData({ ...formData, lib_name: e.target.value })
                }
                disabled={loading}
                required
              />
            </div>

            {/* 备注 */}
            <div className="grid gap-2">
              <label htmlFor="description" className="text-sm font-medium">
                备注说明
              </label>
              <Textarea
                id="description"
                placeholder="请输入知识库备注信息"
                value={formData.description || ""}
                onChange={(e) =>
                  setFormData({ ...formData, description: e.target.value })
                }
                disabled={loading}
                rows={3}
              />
            </div>

            {/* 集合名称 */}
            <div className="grid gap-2">
              <label htmlFor="collection_name" className="text-sm font-medium">
                集合名称 <span className="text-destructive">*</span>
              </label>
              <Input
                id="collection_name"
                placeholder="请输入向量库集合名称"
                value={formData.collection_name || ""}
                onChange={(e) =>
                  setFormData({ ...formData, collection_name: e.target.value })
                }
                disabled={loading}
                required
              />
              <p className="text-xs text-muted-foreground">
                用于向量数据库中的集合标识
              </p>
            </div>

            {/* 嵌入模型 */}
            <div className="grid gap-2">
              <label htmlFor="embedding_model" className="text-sm font-medium">
                嵌入模型 <span className="text-destructive">*</span>
              </label>
              <Select
                value={formData.embedding_model}
                onValueChange={(value) =>
                  setFormData({ ...formData, embedding_model: value })
                }
                disabled={loading}
              >
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="选择嵌入模型" />
                </SelectTrigger>
                <SelectContent>
                  {EMBEDDING_MODELS.map((model) => (
                    <SelectItem key={model.value} value={model.value}>
                      {model.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              disabled={loading}
            >
              取消
            </Button>
            <Button type="submit" disabled={loading}>
              {loading ? "创建中..." : "创建"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

// 编辑知识库弹窗
function EditLibraryDialog({
  open,
  onOpenChange,
  onSuccess,
  library,
}: {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSuccess: () => void
  library: SysLibrariesTable | null
}) {
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState<SysLibrariesForm>({
    lib_name: "",
    description: "",
    collection_name: "",
    embedding_model: "",
  })

  // 当 library 变化时更新表单
  useEffect(() => {
    if (library) {
      setFormData({
        lib_name: library.lib_name || "",
        description: library.description || "",
        collection_name: library.collection_name || "",
        embedding_model: library.embedding_model || "",
        // 保留其他字段
        lib_type: library.lib_type,
        chunk_size: library.chunk_size,
        chunk_overlap: library.chunk_overlap,
        similarity_threshold: library.similarity_threshold,
        max_chunks: library.max_chunks,
      })
    }
  }, [library])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!library?.id) return

    if (!formData.lib_name?.trim()) {
      toast.error("请输入知识库名称")
      return
    }

    setLoading(true)
    try {
      await updateSysLibraries(library.id, formData)
      toast.success("知识库更新成功")
      onOpenChange(false)
      onSuccess()
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "更新失败")
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <form onSubmit={handleSubmit}>
          <DialogHeader>
            <DialogTitle>编辑知识库</DialogTitle>
            <DialogDescription>
              修改知识库的名称和备注信息
            </DialogDescription>
          </DialogHeader>

          <div className="grid gap-4 py-4">
            {/* 知识库名称 */}
            <div className="grid gap-2">
              <label htmlFor="edit_lib_name" className="text-sm font-medium">
                知识库名称 <span className="text-destructive">*</span>
              </label>
              <Input
                id="edit_lib_name"
                placeholder="请输入知识库名称"
                value={formData.lib_name || ""}
                onChange={(e) =>
                  setFormData({ ...formData, lib_name: e.target.value })
                }
                disabled={loading}
                required
              />
            </div>

            {/* 备注 */}
            <div className="grid gap-2">
              <label htmlFor="edit_description" className="text-sm font-medium">
                备注说明
              </label>
              <Textarea
                id="edit_description"
                placeholder="请输入知识库备注信息"
                value={formData.description || ""}
                onChange={(e) =>
                  setFormData({ ...formData, description: e.target.value })
                }
                disabled={loading}
                rows={3}
              />
            </div>

            {/* 不可编辑字段的展示 */}
            <div className="rounded-lg border bg-muted/50 p-4 space-y-3">
              <div className="text-sm">
                <span className="text-muted-foreground">集合名称：</span>
                <span className="font-medium">{library?.collection_name}</span>
              </div>
              <div className="text-sm">
                <span className="text-muted-foreground">嵌入模型：</span>
                <span className="font-medium">{library?.embedding_model}</span>
              </div>
              <p className="text-xs text-muted-foreground">
                注：集合名称和嵌入模型创建后不可修改
              </p>
            </div>
          </div>

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              disabled={loading}
            >
              取消
            </Button>
            <Button type="submit" disabled={loading}>
              {loading ? "保存中..." : "保存"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

// 主页面
export default function KnowledgePage() {
  const [libraries, setLibraries] = useState<SysLibrariesTable[]>([])
  const [filteredLibraries, setFilteredLibraries] = useState<SysLibrariesTable[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState("")
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editDialogOpen, setEditDialogOpen] = useState(false)
  const [editingLibrary, setEditingLibrary] = useState<SysLibrariesTable | null>(null)
  const [docCounts, setDocCounts] = useState<Record<number, number>>({})

  // 加载知识库列表
  const loadLibraries = async () => {
    try {
      setLoading(true)
      const result = await listSysLibraries({
        page_no: 1,
        page_size: 100,
      })
      setLibraries(result.items || [])
      setFilteredLibraries(result.items || [])
      
      // 加载每个知识库的文档数量
      loadDocCounts(result.items || [])
    } catch (error) {
      toast.error("加载知识库列表失败")
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  // 加载文档数量
  const loadDocCounts = async (libs: SysLibrariesTable[]) => {
    const counts: Record<number, number> = {}
    
    await Promise.all(
      libs.map(async (lib) => {
        if (lib.id) {
          try {
            const result = await listSysDocuments({
              page_no: 1,
              page_size: 1,
              lib_id: String(lib.id),
            })
            counts[lib.id] = result.total || 0
          } catch (error) {
            counts[lib.id] = 0
          }
        }
      })
    )
    
    setDocCounts(counts)
  }

  // 处理编辑
  const handleEdit = (library: SysLibrariesTable) => {
    setEditingLibrary(library)
    setEditDialogOpen(true)
  }

  // 初始加载
  useEffect(() => {
    loadLibraries()
  }, [])

  // 搜索过滤
  useEffect(() => {
    if (!searchQuery.trim()) {
      setFilteredLibraries(libraries)
    } else {
      const query = searchQuery.toLowerCase()
      setFilteredLibraries(
        libraries.filter((lib) =>
          lib.lib_name?.toLowerCase().includes(query)
        )
      )
    }
  }, [searchQuery, libraries])

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">知识库</h1>
          <p className="text-muted-foreground">
            管理和浏览您的知识库内容
          </p>
        </div>
        <Button onClick={() => setDialogOpen(true)}>
          <Plus className="mr-2 size-4" />
          新建知识库
        </Button>
      </div>

      {/* 搜索框 */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
        <Input
          placeholder="搜索知识库名称..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="pl-10"
        />
      </div>

      {/* 内容区域 */}
      {loading ? (
        // 骨架屏
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <KnowledgeCardSkeleton key={i} />
          ))}
        </div>
      ) : filteredLibraries.length === 0 ? (
        // 空状态
        <div className="flex flex-col items-center justify-center rounded-lg border border-dashed py-16">
          <Database className="mb-4 size-12 text-muted-foreground/50" />
          <h3 className="mb-2 text-lg font-semibold">
            {searchQuery ? "未找到匹配的知识库" : "暂无知识库"}
          </h3>
          <p className="mb-4 text-sm text-muted-foreground">
            {searchQuery
              ? "请尝试其他关键词"
              : "开始创建您的第一个知识库"}
          </p>
          {!searchQuery && (
            <Button onClick={() => setDialogOpen(true)}>
              <Plus className="mr-2 size-4" />
              创建知识库
            </Button>
          )}
        </div>
      ) : (
        // 知识库列表
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          {filteredLibraries.map((library) => (
            <KnowledgeCard 
              key={library.id} 
              library={library}
              onEdit={handleEdit}
              docCount={library.id ? docCounts[library.id] : 0}
            />
          ))}
        </div>
      )}

      {/* 创建弹窗 */}
      <CreateLibraryDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        onSuccess={loadLibraries}
      />

      {/* 编辑弹窗 */}
      <EditLibraryDialog
        open={editDialogOpen}
        onOpenChange={setEditDialogOpen}
        onSuccess={loadLibraries}
        library={editingLibrary}
      />
    </div>
  )
}
