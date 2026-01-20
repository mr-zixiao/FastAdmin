-- 统一的菜单 SQL（兼容 MySQL / PostgreSQL），对齐到 sys_menu 表结构

-- 父菜单（类型=2：菜单）
INSERT INTO `sys_menu`
(`name`, `type`, `order`, `permission`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `uuid`, `status`, `description`, `created_time`, `updated_time`)
VALUES 
('文档切片明细', 2, 9999, 'module_gencode:sys_document_chunks:query', 'menu', 'SysDocumentChunks', '/module_gencode/sys_document_chunks', 'module_gencode/sys_document_chunks/index', NULL, 0, 1, 0, '文档切片明细', NULL, 0, 7, UUID(), '0', '文档切片明细菜单', NOW(), NOW());
-- 获取父菜单ID（MySQL）
SELECT @parentId := LAST_INSERT_ID();

-- 按钮权限（类型=3：按钮/权限）
INSERT INTO `sys_menu` 
(`name`, `type`, `order`, `permission`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `uuid`, `status`, `description`, `created_time`, `updated_time`)
VALUES 
('文档切片明细查询', 3, 1, 'module_gencode:sys_document_chunks:query', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '文档切片明细查询', NULL, 0, @parentId, UUID(), '0', '文档切片明细菜单', NOW(), NOW()),
('文档切片明细新增', 3, 2, 'module_gencode:sys_document_chunks:create', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '文档切片明细新增', NULL, 0, @parentId, UUID(), '0', '文档切片明细菜单', NOW(), NOW()),
('文档切片明细修改', 3, 3, 'module_gencode:sys_document_chunks:update', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '文档切片明细修改', NULL, 0, @parentId, UUID(), '0', '文档切片明细菜单', NOW(), NOW()),
('文档切片明细删除', 3, 4, 'module_gencode:sys_document_chunks:delete', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '文档切片明细删除', NULL, 0, @parentId, UUID(), '0', '文档切片明细菜单', NOW(), NOW()),
('文档切片明细导出', 3, 5, 'module_gencode:sys_document_chunks:export', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '文档切片明细导出', NULL, 0, @parentId, UUID(), '0', '文档切片明细菜单', NOW(), NOW()),
('文档切片明细导入', 3, 6, 'module_gencode:sys_document_chunks:import', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '文档切片明细导入', NULL, 0, @parentId, UUID(), '0', '文档切片明细菜单', NOW(), NOW()),
('文档切片明细批量状态修改', 3, 7, 'module_gencode:sys_document_chunks:patch', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '文档切片明细批量状态修改', NULL, 0, @parentId, UUID(), '0', '文档切片明细菜单', NOW(), NOW()),
('文档切片明细下载导入模板', 3, 8, 'module_gencode:sys_document_chunks:download', NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '文档切片明细下载导入模板', NULL, 0, @parentId, UUID(), '0', '文档切片明细菜单', NOW(), NOW());

