"use client"

import { Sidebar } from "@/components/layout/sidebar"
import { Header } from "@/components/layout/header"

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex h-screen overflow-hidden">
      {/* 侧边栏 */}
      <Sidebar />
      
      {/* 主内容区 */}
      <div className="flex flex-1 flex-col overflow-hidden">
        {/* 顶部导航 */}
        <Header />
        
        {/* 页面内容 */}
        <main className="flex-1 overflow-y-auto bg-slate-50 dark:bg-zinc-950 p-6">
          {children}
        </main>
      </div>
    </div>
  )
}

