export interface ApiResponse<T = any> {
  code: number;
  data: T;
  msg: string;
  status_code: number;
  success: boolean;
}

const API_PREFIX = "/api/v1";

export async function httpRequest<TData>(
  path: string,
  init?: RequestInit,
): Promise<TData> {
  const res = await fetch(`${API_PREFIX}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    ...init,
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`网络错误：${res.status}`);
  }

  const json = (await res.json()) as ApiResponse<TData>;

  if (!json.success) {
    throw new Error(json.msg || "请求失败");
  }

  return json.data;
}


