import { redirect } from "next/navigation"

export default function KnowledgeLibIndexPage({
  params,
}: {
  params: { lib_id: string }
}) {
  redirect(`/knowledge/${params.lib_id}/documents`)
}


