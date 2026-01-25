/**
 * 存储键常量统一管理
 * 包括 localStorage、sessionStorage 等各种存储的键名
 */

// 🔐 用户认证相关
export const ACCESS_TOKEN_KEY = "access_token";
export const REFRESH_TOKEN_KEY = "refresh_token";
export const REMEMBER_ME_KEY = "remember_me";
export const USER_INFO_KEY = "user_info";


// 🎯 功能分组的键映射对象

// 认证相关键集合
export const AUTH_KEYS = {
  ACCESS_TOKEN: ACCESS_TOKEN_KEY,
  REFRESH_TOKEN: REFRESH_TOKEN_KEY,
  REMEMBER_ME: REMEMBER_ME_KEY,
  USER_INFO: USER_INFO_KEY,
} as const;

// 📦 所有存储键的统一集合
export const ALL_STORAGE_KEYS = {
  ...AUTH_KEYS,
} as const;
