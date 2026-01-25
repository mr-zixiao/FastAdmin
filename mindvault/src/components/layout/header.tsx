"use client"

import { usePathname } from "next/navigation"
import Link from "next/link"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { LogOut, User, Moon, Sun, Menu } from "lucide-react"
import { useTheme } from "next-themes"
import { useEffect, useState } from "react"
import { MobileSidebarContent } from "./sidebar"
import { Auth } from "@/lib/auth"
import type { UserInfo } from "@/lib/api/user"

// 路径到面包屑的映射
const pathToBreadcrumb: Record<string, string[]> = {
  "/dashboard": ["首页"],
  "/knowledge": ["知识库"],
  "/knowledge/my-documents": ["知识库", "我的文档"],
  "/apps": ["应用"],
  "/settings": ["设置"],
}

export function Header() {
  const pathname = usePathname()
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null)

  useEffect(() => {
    setMounted(true)
    // 获取用户信息
    const info = Auth.getUserInfo<UserInfo>()
    setUserInfo(info)
  }, [])

  // 根据路径生成面包屑
  const getBreadcrumbs = () => {
    // 尝试精确匹配
    if (pathToBreadcrumb[pathname]) {
      return pathToBreadcrumb[pathname]
    }

    // 尝试匹配父路径
    const pathSegments = pathname.split("/").filter(Boolean)
    if (pathSegments.length === 0) return ["首页"]

    const breadcrumbs: string[] = []
    let currentPath = ""

    pathSegments.forEach((segment, index) => {
      currentPath += `/${segment}`
      if (pathToBreadcrumb[currentPath]) {
        breadcrumbs.push(...pathToBreadcrumb[currentPath])
      } else if (index === 0) {
        // 如果没有匹配，使用第一个段作为默认
        const firstSegmentMap: Record<string, string> = {
          dashboard: "首页",
          knowledge: "知识库",
          apps: "应用",
          settings: "设置",
        }
        breadcrumbs.push(firstSegmentMap[segment] || segment)
      }
    })

    return breadcrumbs.length > 0 ? breadcrumbs : ["首页"]
  }

  const breadcrumbs = getBreadcrumbs()

  const toggleTheme = () => {
    setTheme(theme === "dark" ? "light" : "dark")
  }

  return (
    <header className="sticky top-0 z-40 flex h-16 items-center gap-4 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 px-6">
      {/* 移动端菜单按钮 */}
      <Sheet>
        <SheetTrigger asChild>
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
          >
            <Menu className="size-5" />
            <span className="sr-only">Toggle menu</span>
          </Button>
        </SheetTrigger>
        <SheetContent side="left" className="w-[260px] p-0">
          <div className="flex h-full flex-col bg-sidebar">
            <MobileSidebarContent />
          </div>
        </SheetContent>
      </Sheet>

      {/* 面包屑导航 */}
      <div className="flex-1">
        <Breadcrumb>
          <BreadcrumbList>
            {breadcrumbs.map((crumb, index) => {
              const isLast = index === breadcrumbs.length - 1
              return (
                <div key={index} className="flex items-center">
                  <BreadcrumbItem>
                    {isLast ? (
                      <BreadcrumbPage>{crumb}</BreadcrumbPage>
                    ) : (
                      <>
                        <BreadcrumbLink asChild>
                          <Link href="#">{crumb}</Link>
                        </BreadcrumbLink>
                        <BreadcrumbSeparator />
                      </>
                    )}
                  </BreadcrumbItem>
                </div>
              )
            })}
          </BreadcrumbList>
        </Breadcrumb>
      </div>

      {/* 右侧操作区 */}
      <div className="flex items-center gap-2">
        {/* 主题切换按钮 */}
        <Button
          variant="ghost"
          size="icon"
          onClick={toggleTheme}
          aria-label="Toggle theme"
        >
          {mounted ? (
            theme === "dark" ? (
              <Sun className="size-5" />
            ) : (
              <Moon className="size-5" />
            )
          ) : (
            <Sun className="size-5" />
          )}
        </Button>

        {/* 用户头像下拉菜单 */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="relative h-8 w-8 rounded-full">
              <Avatar className="size-8">
                <AvatarImage src={userInfo?.avatar} alt={userInfo?.name || "User"} />
                <AvatarFallback>
                  {userInfo?.name?.[0]?.toUpperCase() || userInfo?.username?.[0]?.toUpperCase() || "U"}
                </AvatarFallback>
              </Avatar>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="w-56" align="end" forceMount>
            <DropdownMenuLabel className="font-normal">
              <div className="flex flex-col space-y-1">
                <p className="text-sm font-medium leading-none">
                  {userInfo?.name || userInfo?.username || "用户"}
                </p>
                <p className="text-xs leading-none text-muted-foreground">
                  {userInfo?.email || userInfo?.username || ""}
                </p>
              </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem asChild>
              <Link href="/settings" className="flex items-center">
                <User className="mr-2 size-4" />
                <span>个人信息</span>
              </Link>
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem
              className="text-destructive"
              onClick={() => {
                Auth.clearAuth()
                window.location.href = "/login"
              }}
            >
              <LogOut className="mr-2 size-4" />
              <span>退出登录</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  )
}

