-- 统一的菜单 SQL（兼容 MySQL / PostgreSQL），对齐到 sys_menu 表结构

-- 父菜单（类型=2：菜单）
INSERT INTO `sys_menu`
(`name`, `type`, `order`, `permission`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `uuid`, `status`, `description`, `created_time`, `updated_time`)
VALUES 
('部门与知识库权限关联', 2, 9999, 'module_gencode:sys_dept_libraries:query', 'menu', 'SysDeptLibraries', '/module_gencode/sys_dept_libraries', 'module_gencode/sys_dept_libraries/index', NULL, 0, 1, 0, '部门与知识库权限关联', NULL, 0, 7, UUID(), '0', '部门与知识库权限关联菜单', NOW(), NOW());
-- 获取父菜单ID（MySQL）
SELECT @parentId := LAST_INSERT_ID();

-- 按钮权限（类型=3：按钮/权限）
INSERT INTO `sys_menu` 
(`name`, `type`, `order`, `permission`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `uuid`, `status`, `description`, `created_time`, `updated_time`)
VALUES 
('部门与知识库权限关联查询', 3, 1, 'module_gencode:sys_dept_libraries:query', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '部门与知识库权限关联查询', NULL, 0, @parentId, UUID(), '0', '部门与知识库权限关联菜单', NOW(), NOW()),
('部门与知识库权限关联新增', 3, 2, 'module_gencode:sys_dept_libraries:create', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '部门与知识库权限关联新增', NULL, 0, @parentId, UUID(), '0', '部门与知识库权限关联菜单', NOW(), NOW()),
('部门与知识库权限关联修改', 3, 3, 'module_gencode:sys_dept_libraries:update', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '部门与知识库权限关联修改', NULL, 0, @parentId, UUID(), '0', '部门与知识库权限关联菜单', NOW(), NOW()),
('部门与知识库权限关联删除', 3, 4, 'module_gencode:sys_dept_libraries:delete', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '部门与知识库权限关联删除', NULL, 0, @parentId, UUID(), '0', '部门与知识库权限关联菜单', NOW(), NOW()),
('部门与知识库权限关联导出', 3, 5, 'module_gencode:sys_dept_libraries:export', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '部门与知识库权限关联导出', NULL, 0, @parentId, UUID(), '0', '部门与知识库权限关联菜单', NOW(), NOW()),
('部门与知识库权限关联导入', 3, 6, 'module_gencode:sys_dept_libraries:import', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '部门与知识库权限关联导入', NULL, 0, @parentId, UUID(), '0', '部门与知识库权限关联菜单', NOW(), NOW()),
('部门与知识库权限关联批量状态修改', 3, 7, 'module_gencode:sys_dept_libraries:patch', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '部门与知识库权限关联批量状态修改', NULL, 0, @parentId, UUID(), '0', '部门与知识库权限关联菜单', NOW(), NOW()),
('部门与知识库权限关联下载导入模板', 3, 8, 'module_gencode:sys_dept_libraries:download', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '部门与知识库权限关联下载导入模板', NULL, 0, @parentId, UUID(), '0', '部门与知识库权限关联菜单', NOW(), NOW());

