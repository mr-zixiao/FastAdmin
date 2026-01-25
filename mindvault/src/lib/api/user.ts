import { httpRequest } from "./http";

export interface UserInfo {
  created_id: number | null;
  created_by: string | null;
  updated_id: number | null;
  updated_by: string | null;
  id: number;
  uuid: string;
  status: string;
  description: string;
  created_time: string;
  updated_time: string;
  name: string;
  mobile: string | null;
  email: string | null;
  gender: string;
  avatar: string;
  username: string;
  password: string;
  is_superuser: boolean;
  dept_id: number;
  role_ids: number[];
  position_ids: number[];
  last_login: string;
  gitee_login: string | null;
  github_login: string | null;
  wx_login: string | null;
  qq_login: string | null;
  dept_name: string | null;
  dept: {
    id: number;
    name: string;
  } | null;
  positions: any[];
  roles: Array<{
    id: number;
    uuid: string;
    status: string;
    description: string;
    created_time: string;
    updated_time: string;
    name: string;
    code: string;
    order: number;
    data_scope: number;
    menus: any[];
    depts: any[];
  }>;
}

/**
 * 获取当前用户信息
 */
export async function getCurrentUserInfo(): Promise<UserInfo> {
  return httpRequest<UserInfo>("/system/user/current/info", {
    method: "GET",
  });
}

