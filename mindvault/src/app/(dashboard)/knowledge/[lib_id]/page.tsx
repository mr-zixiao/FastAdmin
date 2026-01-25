"use client"

import { useState, useEffect, useCallback, useRef } from "react"
import { useRouter, useParams } from "next/navigation"
import Link from "next/link"
import {
  ChevronRight,
  Upload,
  FileText,
  Trash2,
  AlertCircle,
  CheckCircle2,
  Clock,
  Loader2,
  HardDrive,
  Calendar,
  User,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"
import { Progress } from "@/components/ui/progress"
import { Skeleton } from "@/components/ui/skeleton"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"
import { toast } from "sonner"
import { detailSysLibraries, type SysLibrariesTable } from "@/lib/api/sys_libraries"
import {
  listSysDocuments,
  createSysDocuments,
  deleteSysDocuments,
  type SysDocumentsTable,
} from "@/lib/api/sys_documents"
import { uploadFile, type SysFileUploadTable } from "@/lib/api/sys_file_upload"

// 扩展文档类型以包含额外字段
interface DocumentWithDetails extends SysDocumentsTable {
  file_info?: SysFileUploadTable
  origin_name?: string
}

// 文档状态类型
type ProcessingStatus = "pending" | "processing" | "completed" | "failed"

// 配置弹窗组件
function ConfigDialog({
  open,
  onOpenChange,
  onConfirm,
  fileInfo,
  loading,
}: {
  open: boolean
  onOpenChange: (open: boolean) => void
  onConfirm: (chunkSize: number, chunkOverlap: number) => void
  fileInfo: SysFileUploadTable | null
  loading: boolean
}) {
  const [chunkSize, setChunkSize] = useState(500)
  const [chunkOverlap, setChunkOverlap] = useState(50)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onConfirm(chunkSize, chunkOverlap)
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <form onSubmit={handleSubmit}>
          <DialogHeader>
            <DialogTitle>配置文档切片参数</DialogTitle>
            <DialogDescription>
              文件已上传成功，请配置文档切片参数后提交处理
            </DialogDescription>
          </DialogHeader>

          <div className="grid gap-4 py-4">
            {/* 文件信息 */}
            <div className="rounded-lg border bg-muted/50 p-4 space-y-2">
              <div className="flex items-center gap-2">
                <FileText className="size-4 text-muted-foreground" />
                <span className="text-sm font-medium">{fileInfo?.origin_name}</span>
              </div>
              <div className="text-xs text-muted-foreground">
                大小：{fileInfo?.file_size} | 类型：{fileInfo?.file_type}
              </div>
            </div>

            {/* 分段长度 */}
            <div className="grid gap-2">
              <label htmlFor="chunk_size" className="text-sm font-medium">
                分段长度 (chunk_size)
              </label>
              <Input
                id="chunk_size"
                type="number"
                min="100"
                max="10000"
                value={chunkSize}
                onChange={(e) => setChunkSize(Number(e.target.value))}
                disabled={loading}
                required
              />
              <p className="text-xs text-muted-foreground">
                推荐值：500-2000，影响检索精度和性能
              </p>
            </div>

            {/* 分段重叠 */}
            <div className="grid gap-2">
              <label htmlFor="chunk_overlap" className="text-sm font-medium">
                分段重叠 (chunk_overlap)
              </label>
              <Input
                id="chunk_overlap"
                type="number"
                min="0"
                max="500"
                value={chunkOverlap}
                onChange={(e) => setChunkOverlap(Number(e.target.value))}
                disabled={loading}
                required
              />
              <p className="text-xs text-muted-foreground">
                推荐值：50-200，保持上下文连贯性
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
              {loading ? "处理中..." : "确认并提交"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

// 状态徽章组件
function StatusBadge({ status, errorMsg }: { status: ProcessingStatus; errorMsg?: string }) {
  const statusConfig = {
    pending: {
      variant: "secondary" as const,
      icon: Clock,
      label: "排队中",
      className: "bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300",
    },
    processing: {
      variant: "default" as const,
      icon: Loader2,
      label: "解析中",
      className: "bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300",
    },
    completed: {
      variant: "default" as const,
      icon: CheckCircle2,
      label: "已完成",
      className: "bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300",
    },
    failed: {
      variant: "destructive" as const,
      icon: AlertCircle,
      label: "失败",
      className: "bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300",
    },
  }

  const config = statusConfig[status]
  const Icon = config.icon

  const badge = (
    <Badge variant={config.variant} className={config.className}>
      <Icon className={status === "processing" ? "animate-spin" : ""} />
      {config.label}
    </Badge>
  )

  if (status === "failed" && errorMsg) {
    return (
      <Tooltip>
        <TooltipTrigger asChild>{badge}</TooltipTrigger>
        <TooltipContent>
          <p className="max-w-xs">{errorMsg}</p>
        </TooltipContent>
      </Tooltip>
    )
  }

  return badge
}

// 文档行组件
function DocumentRow({
  document,
  onDelete,
}: {
  document: DocumentWithDetails
  onDelete: (id: number) => void
}) {
  const [deleting, setDeleting] = useState(false)

  const handleDelete = async () => {
    if (!document.id) return
    if (!confirm("确定要删除这个文档吗？")) return

    setDeleting(true)
    try {
      await deleteSysDocuments([document.id])
      toast.success("文档删除成功")
      onDelete(document.id)
    } catch (error) {
      toast.error("删除失败")
    } finally {
      setDeleting(false)
    }
  }

  // 根据 processing_status 推断状态
  const getStatus = (): ProcessingStatus => {
    if (document.error_msg) return "failed"
    if (document.processing_status === false) return "pending"
    if (document.processing_status === true) return "completed"
    return "processing"
  }

  const status = getStatus()

  // 格式化文件大小
  const formatFileSize = (size?: string) => {
    if (!size) return "-"
    const numSize = Number(size)
    if (isNaN(numSize)) return size
    if (numSize < 1024) return `${numSize} B`
    if (numSize < 1024 * 1024) return `${(numSize / 1024).toFixed(2)} KB`
    if (numSize < 1024 * 1024 * 1024) return `${(numSize / (1024 * 1024)).toFixed(2)} MB`
    return `${(numSize / (1024 * 1024 * 1024)).toFixed(2)} GB`
  }

  // 格式化时间
  const formatTime = (time?: string) => {
    if (!time) return "-"
    try {
      const date = new Date(time)
      return date.toLocaleString("zh-CN", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
      })
    } catch {
      return time
    }
  }

  return (
    <TableRow>
      <TableCell>
        <div className="flex items-center gap-2">
          <FileText className="size-4 text-muted-foreground shrink-0" />
          <div className="flex flex-col min-w-0">
            <span className="font-medium truncate">
              {document.file_info?.origin_name || "未知文件"}
            </span>
            {document.file_info?.file_type && (
              <span className="text-xs text-muted-foreground">
                {document.file_info.file_type}
              </span>
            )}
          </div>
        </div>
      </TableCell>
      <TableCell>
        <div className="flex items-center gap-1.5 text-sm">
          <HardDrive className="size-3.5 text-muted-foreground" />
          <span className="text-muted-foreground">
            {formatFileSize(document.file_info?.file_size)}
          </span>
        </div>
      </TableCell>
      <TableCell>
        <span className="text-sm text-muted-foreground">
          {document.chunk_size || 0} / {document.chunk_overlap || 0}
        </span>
      </TableCell>
      <TableCell>
        <div className="flex items-center gap-1.5 text-sm">
          <Calendar className="size-3.5 text-muted-foreground" />
          <span className="text-muted-foreground">
            {formatTime(document.created_time || document.file_info?.created_time)}
          </span>
        </div>
      </TableCell>
      <TableCell>
        {document.created_by?.name ? (
          <div className="flex items-center gap-1.5 text-sm">
            <User className="size-3.5 text-muted-foreground" />
            <span className="text-muted-foreground">{document.created_by.name}</span>
          </div>
        ) : (
          <span className="text-sm text-muted-foreground">-</span>
        )}
      </TableCell>
      <TableCell>
        <StatusBadge status={status} errorMsg={document.error_msg} />
      </TableCell>
      <TableCell className="text-right">
        <Button
          variant="ghost"
          size="icon"
          onClick={handleDelete}
          disabled={deleting}
          className="size-8"
        >
          <Trash2 className="size-4" />
        </Button>
      </TableCell>
    </TableRow>
  )
}

// 主页面
export default function KnowledgeDetailPage() {
  const router = useRouter()
  const params = useParams()
  const libId = params.lib_id as string

  const [library, setLibrary] = useState<SysLibrariesTable | null>(null)
  const [documents, setDocuments] = useState<DocumentWithDetails[]>([])
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [configDialogOpen, setConfigDialogOpen] = useState(false)
  const [uploadedFile, setUploadedFile] = useState<SysFileUploadTable | null>(null)
  const [submitting, setSubmitting] = useState(false)

  const fileInputRef = useRef<HTMLInputElement>(null)
  const pollingRef = useRef<NodeJS.Timeout | null>(null)

  // 加载知识库详情
  const loadLibrary = useCallback(async () => {
    try {
      const data = await detailSysLibraries(Number(libId))
      setLibrary(data)
    } catch (error) {
      toast.error("加载知识库信息失败")
      router.push("/knowledge")
    }
  }, [libId, router])

  // 加载文档列表
  const loadDocuments = useCallback(async () => {
    try {
      const result = await listSysDocuments({
        page_no: 1,
        page_size: 100,
        lib_id: libId,
      })
      setDocuments(result.items || [])
      
      // 检查是否需要轮询
      const hasProcessing = (result.items || []).some(
        (doc) => !doc.error_msg && doc.processing_status === false
      )
      
      if (hasProcessing) {
        startPolling()
      } else {
        stopPolling()
      }
    } catch (error) {
      toast.error("加载文档列表失败")
    } finally {
      setLoading(false)
    }
  }, [libId])

  // 开始轮询
  const startPolling = () => {
    if (pollingRef.current) return
    pollingRef.current = setInterval(() => {
      loadDocuments()
    }, 10000)
  }

  // 停止轮询
  const stopPolling = () => {
    if (pollingRef.current) {
      clearInterval(pollingRef.current)
      pollingRef.current = null
    }
  }

  // 初始加载
  useEffect(() => {
    loadLibrary()
    loadDocuments()

    return () => {
      stopPolling()
    }
  }, [loadLibrary, loadDocuments])

  // 处理文件选择
  const handleFileSelect = async (files: FileList | null) => {
    if (!files || files.length === 0) return

    const file = files[0]
    
    setUploading(true)
    try {
      const uploadedFileInfo = await uploadFile(file)
      setUploadedFile(uploadedFileInfo)
      setConfigDialogOpen(true)
      toast.success("文件上传成功，请配置切片参数")
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "文件上传失败")
    } finally {
      setUploading(false)
      if (fileInputRef.current) {
        fileInputRef.current.value = ""
      }
    }
  }

  // 处理配置确认
  const handleConfigConfirm = async (chunkSize: number, chunkOverlap: number) => {
    if (!uploadedFile?.id) return

    setSubmitting(true)
    try {
      await createSysDocuments({
        lib_id: libId,
        file_upload_id: String(uploadedFile.id),
        chunk_size: chunkSize,
        chunk_overlap: chunkOverlap,
      })
      toast.success("文档已提交处理")
      setConfigDialogOpen(false)
      setUploadedFile(null)
      loadDocuments()
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "提交失败")
    } finally {
      setSubmitting(false)
    }
  }

  // 处理拖拽
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    handleFileSelect(e.dataTransfer.files)
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
  }

  return (
    <div className="space-y-6">
      {/* 面包屑导航 */}
      <Breadcrumb>
        <BreadcrumbList>
          <BreadcrumbItem>
            <BreadcrumbLink asChild>
              <Link href="/knowledge">知识库</Link>
            </BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator>
            <ChevronRight />
          </BreadcrumbSeparator>
          <BreadcrumbItem>
            <BreadcrumbPage>{library?.lib_name || "加载中..."}</BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>

      {/* 上传区域 */}
      <Card>
        <CardHeader>
          <CardTitle>上传文档</CardTitle>
          <CardDescription>
            支持拖拽上传或点击选择文件
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            className="border-2 border-dashed rounded-lg p-8 text-center hover:border-primary/50 transition-colors cursor-pointer"
            onClick={() => fileInputRef.current?.click()}
          >
            {uploading ? (
              <div className="space-y-2">
                <Loader2 className="size-12 mx-auto text-primary animate-spin" />
                <p className="text-sm text-muted-foreground">上传中...</p>
              </div>
            ) : (
              <div className="space-y-2">
                <Upload className="size-12 mx-auto text-muted-foreground" />
                <p className="text-sm font-medium">点击上传或拖拽文件到这里</p>
                <p className="text-xs text-muted-foreground">
                  支持 PDF、TXT、DOCX 等格式
                </p>
              </div>
            )}
            <input
              ref={fileInputRef}
              type="file"
              className="hidden"
              onChange={(e) => handleFileSelect(e.target.files)}
              disabled={uploading}
            />
          </div>
        </CardContent>
      </Card>

      {/* 文档列表 */}
      <Card>
        <CardHeader>
          <CardTitle>文档列表</CardTitle>
          <CardDescription>
            共 {documents.length} 个文档
          </CardDescription>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="space-y-2">
              {Array.from({ length: 3 }).map((_, i) => (
                <Skeleton key={i} className="h-12 w-full" />
              ))}
            </div>
          ) : documents.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12">
              <FileText className="mb-4 size-12 text-muted-foreground/50" />
              <h3 className="mb-2 text-lg font-semibold">尚未上传文档</h3>
              <p className="mb-4 text-sm text-muted-foreground">
                上传您的第一个文档开始构建知识库
              </p>
              <Button onClick={() => fileInputRef.current?.click()}>
                <Upload className="mr-2 size-4" />
                上传文档
              </Button>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>文件名</TableHead>
                  <TableHead>文件大小</TableHead>
                  <TableHead>切片参数</TableHead>
                  <TableHead>上传时间</TableHead>
                  <TableHead>创建人</TableHead>
                  <TableHead>状态</TableHead>
                  <TableHead className="text-right">操作</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {documents.map((doc) => (
                  <DocumentRow
                    key={doc.id}
                    document={doc}
                    onDelete={() => loadDocuments()}
                  />
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>

      {/* 配置弹窗 */}
      <ConfigDialog
        open={configDialogOpen}
        onOpenChange={setConfigDialogOpen}
        onConfirm={handleConfigConfirm}
        fileInfo={uploadedFile}
        loading={submitting}
      />
    </div>
  )
}

