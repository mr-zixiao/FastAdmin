import { ResultEnum } from "@/enums/api/result.enum";
import { Auth } from "@/lib/auth";

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

  const res = await fetch(`${API_PREFIX}${path}`, {
    headers: isFormData
      ? {
          // 对于 FormData，不显式设置 Content-Type，交给浏览器自动生成带 boundary 的 header
          ...(init?.headers ?? {}),
        }
      : {
          "Content-Type": "application/json",
          ...(init?.headers ?? {}),
        },
    ...init,
    cache: "no-store",
  });

  if (!res.ok) {
    // 网络层错误依然作为 Promise 拒绝抛给上层（一般会被全局错误边界捕获）
    return Promise.reject<TData>(new Error(`网络错误：${res.status}`));
  }

  const json = (await res.json()) as ApiResponse<TData>;

  // 基于统一的返回码进行差异化处理（不直接 throw，采用跳转或弹窗提示）
  switch (json.code) {
    case ResultEnum.SUCCESS: {
      return json.data;
    }
    case ResultEnum.UNAUTHORIZED: {
      if (typeof window !== "undefined") {
        // 清理本地认证信息并跳转到登录页
        Auth.clearAuth();
        window.location.href = "/login";
      }
      return Promise.reject<TData>();
    }
    case ResultEnum.TOKEN_EXPIRED: {
      if (typeof window !== "undefined") {
        Auth.clearAuth();
        window.location.href = "/login";
      }
      return Promise.reject<TData>();
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

