"use client"

import { useEffect, useMemo, useState } from "react"
import Link from "next/link"
import { useParams, usePathname } from "next/navigation"
import { ChevronRight, FileText, FlaskConical, Settings } from "lucide-react"

import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"
import { cn } from "@/lib/utils"
import { detailSysLibraries, type SysLibrariesTable } from "@/lib/api/sys_libraries"

type TabItem = {
  label: string
  href: string
  icon: React.ComponentType<{ className?: string }>
}

export default function KnowledgeLibLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const params = useParams()
  const pathname = usePathname()
  const libId = params.lib_id as string

  const [library, setLibrary] = useState<SysLibrariesTable | null>(null)

  useEffect(() => {
    let cancelled = false
    ;(async () => {
      try {
        const data = await detailSysLibraries(Number(libId))
        if (!cancelled) setLibrary(data)
      } catch {
        if (!cancelled) setLibrary(null)
      }
    })()
    return () => {
      cancelled = true
    }
  }, [libId])

  const tabs: TabItem[] = useMemo(
    () => [
      { label: "文档", href: `/knowledge/${libId}/documents`, icon: FileText },
      { label: "召回测试", href: `/knowledge/${libId}/recall-test`, icon: FlaskConical },
      { label: "设置", href: `/knowledge/${libId}/settings`, icon: Settings },
    ],
    [libId]
  )

  return (
    <div className="space-y-6">
      {/* 面包屑 */}
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
            <BreadcrumbPage>{library?.lib_name || `库 #${libId}`}</BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>

      {/* 二级导航 */}
      <div className="flex items-center gap-2 border-b">
        {tabs.map((tab) => {
          const isActive = pathname === tab.href || pathname?.startsWith(tab.href + "/")
          const Icon = tab.icon
          return (
            <Link
              key={tab.href}
              href={tab.href}
              className={cn(
                "inline-flex items-center gap-2 px-3 py-2 text-sm font-medium transition-colors border-b-2 -mb-px",
                isActive
                  ? "border-primary text-foreground"
                  : "border-transparent text-muted-foreground hover:text-foreground"
              )}
            >
              <Icon className="size-4" />
              {tab.label}
            </Link>
          )
        })}
      </div>

      {children}
    </div>
  )
}


