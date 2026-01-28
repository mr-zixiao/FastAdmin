import { ResultEnum } from "@/enums/api/result.enum";
import { Auth } from "@/lib/auth";
import { toast } from "sonner";
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
  const isFormData = init?.body instanceof FormData;
  const accessToken = Auth.getAccessToken();

  // 构建请求头
  const headers: any = {
    ...(init?.headers ?? {}),
  };

  // 如果 Authorization 未设置且有 token，则添加
  if (!headers.Authorization && accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }

  // 如果不是 FormData，添加 Content-Type
  if (!isFormData && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  const res = await fetch(`${API_PREFIX}${path}`, {
    headers,
    ...init,
    cache: "no-store",
  });
  if (res.status == 401) {
    toast.error("登录已过期，请重新登录！");
    Auth.clearAuth();
    window.location.href = "/login";
    return Promise.reject<TData>();
  }

  if (!res.ok) {
    // 网络层错误依然作为 Promise 拒绝抛给上层（一般会被全局错误边界捕获）
    return Promise.reject<TData>(new Error(`网络错误：${res.status}`));
  }

  const json = (await res.json()) as ApiResponse<TData>;
  switch (json.code) {
    case ResultEnum.SUCCESS: {
      return json.data;
    }
    case ResultEnum.ERROR: {
      if (typeof window !== "undefined") {
        // 业务请求错误，给出弹窗提示
        alert(json.msg || "请求错误");
      }
      return Promise.reject<TData>(json);
    }
    case ResultEnum.EXCEPTION: {
      if (typeof window !== "undefined") {
        alert(json.msg || "服务器异常");
      }
      return Promise.reject<TData>(json);
    }
    default: {
      // 如果后端 success 字段标记失败，优先提示后端信息
      if (json.success === false) {
        if (typeof window !== "undefined") {
          alert(json.msg || "请求失败");
        }
        return Promise.reject<TData>(json);
      }
      if (typeof window !== "undefined") {
        alert(json.msg || "未知响应状态");
      }
      return Promise.reject<TData>(json);
    }
  }
}

/**
 * 处理 Blob 响应的请求（用于文件下载等）
 */
export async function httpRequestBlob(
  path: string,
  init?: RequestInit,
): Promise<Blob> {
  const isFormData = init?.body instanceof FormData;
  const accessToken = Auth.getAccessToken();

  // 构建请求头
  const headers: any = {
    ...(init?.headers ?? {}),
  };

  // 如果 Authorization 未设置且有 token，则添加
  if (!headers.Authorization && accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }

  // 如果不是 FormData，添加 Content-Type
  if (!isFormData && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  const res = await fetch(`${API_PREFIX}${path}`, {
    headers,
    ...init,
    cache: "no-store",
  });

  if (!res.ok) {
    return Promise.reject<Blob>(new Error(`网络错误：${res.status}`));
  }

  return res.blob();
}
