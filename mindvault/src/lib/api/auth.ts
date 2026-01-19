import { httpRequest } from "./http";

export interface CaptchaInfo {
  enable: boolean;
  key: string;
  img_base: string;
}

/** 登录表单数据 */
export interface LoginFormData {
  username: string;
  password: string;
  captcha_key: string;
  captcha: string;
  remember: boolean;
  login_type: string;
}

/** 登录响应 */
export interface LoginResult {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export async function fetchCaptcha(): Promise<CaptchaInfo> {
  return httpRequest<CaptchaInfo>("/system/auth/captcha/get", {
    method: "GET",
  });
}

export async function login(data: LoginFormData): Promise<LoginResult> {
  // 使用 FormData 方式提交
  const formData = new FormData();
  formData.append("username", data.username);
  formData.append("password", data.password);
  formData.append("captcha_key", data.captcha_key);
  formData.append("captcha", data.captcha);
  formData.append("remember", String(data.remember));
  formData.append("login_type", data.login_type);

  return httpRequest<LoginResult>("/system/auth/login", {
    method: "POST",
    body: formData,
  });
}


