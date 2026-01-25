"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import {
  LayoutDashboard,
  BookOpen,
  AppWindow,
  Settings,
  Sparkles,
  ChevronLeft,
  ChevronRight,
} from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Storage } from "@/lib/storage"

const SIDEBAR_COLLAPSED_KEY = "sidebar_collapsed"

const navigation = [
  {
    name: "首页",
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    name: "知识库",
    href: "/knowledge",
    icon: BookOpen,
  },
  {
    name: "应用",
    href: "/apps",
    icon: AppWindow,
  },
  {
    name: "设置",
    href: "/settings",
    icon: Settings,
  },
]

export function Sidebar() {
  const pathname = usePathname()
  const [collapsed, setCollapsed] = useState(false)

  useEffect(() => {
    // 从 localStorage 读取收起状态
    const saved = Storage.get<boolean>(SIDEBAR_COLLAPSED_KEY, false)
    setCollapsed(saved)
  }, [])

  const toggleCollapsed = () => {
    const newCollapsed = !collapsed
    setCollapsed(newCollapsed)
    Storage.set(SIDEBAR_COLLAPSED_KEY, newCollapsed)
  }

  return (
    <aside
      className={cn(
        "hidden flex-col border-r border-sidebar-border bg-sidebar transition-all duration-300 md:flex",
        collapsed ? "w-16" : "w-[260px]"
      )}
    >
      {/* Logo 区 */}
      <div className="flex h-16 items-center gap-2 border-b border-sidebar-border px-6">
        <div className="flex items-center gap-2">
          <div className="flex size-8 shrink-0 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <Sparkles className="size-5" />
          </div>
          {!collapsed && (
            <span className="font-semibold text-foreground whitespace-nowrap">
              AI Knowledge Base
            </span>
          )}
        </div>
      </div>

      {/* 导航菜单 */}
      <nav className="flex-1 space-y-1 px-3 py-4">
        {navigation.map((item) => {
          const isActive = pathname === item.href || pathname?.startsWith(item.href + "/")
          const Icon = item.icon

          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "group flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                collapsed ? "justify-center" : "",
                isActive
                  ? "bg-sidebar-accent text-sidebar-accent-foreground"
                  : "text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
              )}
              title={collapsed ? item.name : undefined}
            >
              <Icon className="size-5 shrink-0" />
              {!collapsed && <span className="whitespace-nowrap">{item.name}</span>}
            </Link>
          )
        })}
      </nav>

      {/* 收起/展开按钮 */}
      <div className="border-t border-sidebar-border p-2">
        <Button
          variant="ghost"
          size="icon"
          onClick={toggleCollapsed}
          className="w-full"
          title={collapsed ? "展开侧边栏" : "收起侧边栏"}
        >
          {collapsed ? (
            <ChevronRight className="size-4" />
          ) : (
            <ChevronLeft className="size-4" />
          )}
        </Button>
      </div>
    </aside>
  )
}

// 移动端侧边栏内容组件（供 Header 使用）
export function MobileSidebarContent() {
  const pathname = usePathname()

  return (
    <>
      {/* Logo 区 */}
      <div className="flex h-16 items-center gap-2 border-b border-sidebar-border px-6">
        <div className="flex items-center gap-2">
          <div className="flex size-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <Sparkles className="size-5" />
          </div>
          <span className="font-semibold text-foreground">AI Knowledge Base</span>
        </div>
      </div>

      {/* 导航菜单 */}
      <nav className="flex-1 space-y-1 px-3 py-4">
        {navigation.map((item) => {
          const isActive = pathname === item.href || pathname?.startsWith(item.href + "/")
          const Icon = item.icon

          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "group flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                isActive
                  ? "bg-sidebar-accent text-sidebar-accent-foreground"
                  : "text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
              )}
            >
              <Icon className="size-5 shrink-0" />
              <span>{item.name}</span>
            </Link>
          )
        })}
      </nav>
    </>
  )
}

