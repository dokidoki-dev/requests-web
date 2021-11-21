/* 环境变量表 */
CREATE TABLE `jk_variable` (
  `v_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '环境变量id',
  `v_name` varchar(255) NOT NULL COMMENT '变量名字',
  `v_data` varchar(255) NOT NULL COMMENT '变量内容',
  `group_id` int(11) NOT NULL COMMENT '所属分组',
  `status` int(10) NOT NULL DEFAULT '0' COMMENT '当前状态 1启用 0禁用',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `modfiy_time` datetime DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`v_id`) USING BTREE,
  KEY `group_id` (`group_id`) USING HASH COMMENT '所属分组id'
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8mb4;

/* 环境变量分组表 */
CREATE TABLE `jk_vgroups` (
  `group_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '分组id',
  `group_name` varchar(255) NOT NULL COMMENT '分组名称',
  `status` int(10) NOT NULL DEFAULT '0' COMMENT '是否启用 1启用 0禁用',
  `create_time` datetime NOT NULL,
  `modfiy_time` datetime DEFAULT NULL,
  PRIMARY KEY (`group_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8mb4;

/* 用户信息表 */
CREATE TABLE `user_info` (
  `u_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户id',
  `u_name` varchar(255) NOT NULL COMMENT '用户名称',
  `u_password` varchar(255) NOT NULL COMMENT '用户密码',
  `u_salt` varchar(255) NOT NULL COMMENT '密码盐',
  `u_phone` varchar(255) NOT NULL COMMENT '用户手机号',
  `is_admin` int(10) NOT NULL DEFAULT '0' COMMENT '是否管理员 1是 0普通用户 默认普通用户',
  `is_active` int(10) NOT NULL DEFAULT '1' COMMENT '是否启用账户  1启用 0禁用 默认启用',
  `is_delete` int(10) NOT NULL DEFAULT '0' COMMENT '是否删除 1已删除  0未删除 默认0',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `modfiy_time` datetime DEFAULT NULL COMMENT '修改时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  PRIMARY KEY (`u_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8mb4;

/* 测试用例表 */
CREATE TABLE `jk_testcase` (
  `case_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用例id',
  `case_name` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '用例名称',
  `method` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '请求方式 GET POST',
  `path` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '请求路径',
  `url` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '请求链接',
  `status` int(2) NOT NULL DEFAULT '0' COMMENT '状态码 0 处于未执行队列   1处于执行中队列  默认0',
  `sub_status` int(2) NOT NULL DEFAULT '0' COMMENT '子状态码 0 未执行  1执行中  2 执行成功  默认0',
  `result_code` int(5) NOT NULL DEFAULT '0' COMMENT '本次用例执行结果状态码   200执行成功  201执行失败  0未执行',
  `is_assert` int(2) NOT NULL DEFAULT '0' COMMENT '是否断言  0 不断言 1需要断言  默认0',
  `a_data` varchar(1000) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '断言数据',
  `a_mode` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '断言类型  >  =  <   >=   <=',
  `a_type` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据类型  例如  int   string  bool',
  `a_result_data` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '断言预期结果数据',
  `a_status` int(2) DEFAULT NULL COMMENT '断言结果  0失败  1成功',
  `is_rely_on` int(2) NOT NULL DEFAULT '0' COMMENT '是否依赖  0不依赖   1依赖 默认0',
  `header` text COLLATE utf8mb4_bin NOT NULL COMMENT '请求头',
  `request_data` text COLLATE utf8mb4_bin COMMENT '请求数据',
  `result_data` text COLLATE utf8mb4_bin COMMENT '返回数据',
  `group_id` int(11) NOT NULL COMMENT '所属分组id',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `modfiy_time` datetime DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`case_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

/* 测试用例分组表 */
CREATE TABLE `jk_cgroups` (
  `group_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '测试用例分组id',
  `group_name` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '测试用例分组名称',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `modfiy_time` datetime DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

/* 创建默认管理员用户 admin 12345678a */
INSERT INTO `user_info` (`u_id`, `u_name`, `u_password`, `u_salt`, `u_phone`, `is_admin`, `is_active`, `is_delete`, `create_time`, `modfiy_time`, `delete_time`) VALUES (10000, 'admin', 'e797802b23766c12f0d02c9ab6c63081d66e95e29e28af286d854a4013296d3e', 'f86c03a19b124b848b2eb481542080b7', '17700000000', 1, 1, 0, '2021-10-31 19:18:13', NULL, NULL);