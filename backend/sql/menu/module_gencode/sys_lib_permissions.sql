-- 统一的菜单 SQL（兼容 MySQL / PostgreSQL），对齐到 sys_menu 表结构

-- 父菜单（类型=2：菜单）
INSERT INTO `sys_menu`
(`name`, `type`, `order`, `permission`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `uuid`, `status`, `description`, `created_time`, `updated_time`)
VALUES 
('知识库多维权限授权', 2, 9999, 'module_gencode:sys_lib_permissions:query', 'menu', 'SysLibPermissions', '/module_gencode/sys_lib_permissions', 'module_gencode/sys_lib_permissions/index', NULL, 0, 1, 0, '知识库多维权限授权', NULL, 0, 7, UUID(), '0', '知识库多维权限授权菜单', NOW(), NOW());
-- 获取父菜单ID（MySQL）
SELECT @parentId := LAST_INSERT_ID();

-- 按钮权限（类型=3：按钮/权限）
INSERT INTO `sys_menu` 
(`name`, `type`, `order`, `permission`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `uuid`, `status`, `description`, `created_time`, `updated_time`)
VALUES 
('知识库多维权限授权查询', 3, 1, 'module_gencode:sys_lib_permissions:query', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '知识库多维权限授权查询', NULL, 0, @parentId, UUID(), '0', '知识库多维权限授权菜单', NOW(), NOW()),
('知识库多维权限授权新增', 3, 2, 'module_gencode:sys_lib_permissions:create', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '知识库多维权限授权新增', NULL, 0, @parentId, UUID(), '0', '知识库多维权限授权菜单', NOW(), NOW()),
('知识库多维权限授权修改', 3, 3, 'module_gencode:sys_lib_permissions:update', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '知识库多维权限授权修改', NULL, 0, @parentId, UUID(), '0', '知识库多维权限授权菜单', NOW(), NOW()),
('知识库多维权限授权删除', 3, 4, 'module_gencode:sys_lib_permissions:delete', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '知识库多维权限授权删除', NULL, 0, @parentId, UUID(), '0', '知识库多维权限授权菜单', NOW(), NOW()),
('知识库多维权限授权导出', 3, 5, 'module_gencode:sys_lib_permissions:export', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '知识库多维权限授权导出', NULL, 0, @parentId, UUID(), '0', '知识库多维权限授权菜单', NOW(), NOW()),
('知识库多维权限授权导入', 3, 6, 'module_gencode:sys_lib_permissions:import', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '知识库多维权限授权导入', NULL, 0, @parentId, UUID(), '0', '知识库多维权限授权菜单', NOW(), NOW()),
('知识库多维权限授权批量状态修改', 3, 7, 'module_gencode:sys_lib_permissions:patch', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '知识库多维权限授权批量状态修改', NULL, 0, @parentId, UUID(), '0', '知识库多维权限授权菜单', NOW(), NOW()),
('知识库多维权限授权下载导入模板', 3, 8, 'module_gencode:sys_lib_permissions:download', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '知识库多维权限授权下载导入模板', NULL, 0, @parentId, UUID(), '0', '知识库多维权限授权菜单', NOW(), NOW());

