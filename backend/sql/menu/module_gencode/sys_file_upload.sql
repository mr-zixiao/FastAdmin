-- 统一的菜单 SQL（兼容 MySQL / PostgreSQL），对齐到 sys_menu 表结构

-- 父菜单（类型=2：菜单）
INSERT INTO `sys_menu`
(`name`, `type`, `order`, `permission`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `uuid`, `status`, `description`, `created_time`, `updated_time`)
VALUES 
('文件上传', 2, 9999, 'module_gencode:sys_file_upload:query', 'menu', 'SysFileUpload', '/module_gencode/sys_file_upload', 'module_gencode/sys_file_upload/index', NULL, 0, 1, 0, '文件上传', NULL, 0, 7, UUID(), '0', '文件上传菜单', NOW(), NOW());
-- 获取父菜单ID（MySQL）
SELECT @parentId := LAST_INSERT_ID();

-- 按钮权限（类型=3：按钮/权限）
INSERT INTO `sys_menu` 
(`name`, `type`, `order`, `permission`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `uuid`, `status`, `description`, `created_time`, `updated_time`)
VALUES 
('文件上传查询', 3, 1, 'module_gencode:sys_file_upload:query', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '文件上传查询', NULL, 0, @parentId, UUID(), '0', '文件上传菜单', NOW(), NOW()),
('文件上传新增', 3, 2, 'module_gencode:sys_file_upload:create', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '文件上传新增', NULL, 0, @parentId, UUID(), '0', '文件上传菜单', NOW(), NOW()),
('文件上传修改', 3, 3, 'module_gencode:sys_file_upload:update', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '文件上传修改', NULL, 0, @parentId, UUID(), '0', '文件上传菜单', NOW(), NOW()),
('文件上传删除', 3, 4, 'module_gencode:sys_file_upload:delete', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '文件上传删除', NULL, 0, @parentId, UUID(), '0', '文件上传菜单', NOW(), NOW()),
('文件上传导出', 3, 5, 'module_gencode:sys_file_upload:export', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '文件上传导出', NULL, 0, @parentId, UUID(), '0', '文件上传菜单', NOW(), NOW()),
('文件上传导入', 3, 6, 'module_gencode:sys_file_upload:import', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '文件上传导入', NULL, 0, @parentId, UUID(), '0', '文件上传菜单', NOW(), NOW()),
('文件上传批量状态修改', 3, 7, 'module_gencode:sys_file_upload:patch', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '文件上传批量状态修改', NULL, 0, @parentId, UUID(), '0', '文件上传菜单', NOW(), NOW()),
('文件上传下载导入模板', 3, 8, 'module_gencode:sys_file_upload:download', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '文件上传下载导入模板', NULL, 0, @parentId, UUID(), '0', '文件上传菜单', NOW(), NOW());

