-- 统一的菜单 SQL（兼容 MySQL / PostgreSQL），对齐到 sys_menu 表结构

-- 父菜单（类型=2：菜单）
INSERT INTO `sys_menu`
(`name`, `type`, `order`, `permission`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `uuid`, `status`, `description`, `created_time`, `updated_time`)
VALUES 
('文档资产管理', 2, 9999, 'module_gencode:sys_documents:query', 'menu', 'SysDocuments', '/module_gencode/sys_documents', 'module_gencode/sys_documents/index', NULL, 0, 1, 0, '文档资产管理', NULL, 0, 7, UUID(), '0', '文档资产管理菜单', NOW(), NOW());
-- 获取父菜单ID（MySQL）
SELECT @parentId := LAST_INSERT_ID();

-- 按钮权限（类型=3：按钮/权限）
INSERT INTO `sys_menu` 
(`name`, `type`, `order`, `permission`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `uuid`, `status`, `description`, `created_time`, `updated_time`)
VALUES 
('文档资产管理查询', 3, 1, 'module_gencode:sys_documents:query', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '文档资产管理查询', NULL, 0, @parentId, UUID(), '0', '文档资产管理菜单', NOW(), NOW()),
('文档资产管理新增', 3, 2, 'module_gencode:sys_documents:create', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '文档资产管理新增', NULL, 0, @parentId, UUID(), '0', '文档资产管理菜单', NOW(), NOW()),
('文档资产管理修改', 3, 3, 'module_gencode:sys_documents:update', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '文档资产管理修改', NULL, 0, @parentId, UUID(), '0', '文档资产管理菜单', NOW(), NOW()),
('文档资产管理删除', 3, 4, 'module_gencode:sys_documents:delete', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '文档资产管理删除', NULL, 0, @parentId, UUID(), '0', '文档资产管理菜单', NOW(), NOW()),
('文档资产管理导出', 3, 5, 'module_gencode:sys_documents:export', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '文档资产管理导出', NULL, 0, @parentId, UUID(), '0', '文档资产管理菜单', NOW(), NOW()),
('文档资产管理导入', 3, 6, 'module_gencode:sys_documents:import', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '文档资产管理导入', NULL, 0, @parentId, UUID(), '0', '文档资产管理菜单', NOW(), NOW()),
('文档资产管理批量状态修改', 3, 7, 'module_gencode:sys_documents:patch', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '文档资产管理批量状态修改', NULL, 0, @parentId, UUID(), '0', '文档资产管理菜单', NOW(), NOW()),
('文档资产管理下载导入模板', 3, 8, 'module_gencode:sys_documents:download', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '文档资产管理下载导入模板', NULL, 0, @parentId, UUID(), '0', '文档资产管理菜单', NOW(), NOW());

