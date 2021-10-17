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


CREATE TABLE `jk_vgroups` (
  `group_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '分组id',
  `group_name` varchar(255) NOT NULL COMMENT '分组名称',
  `status` int(10) NOT NULL DEFAULT '0' COMMENT '是否启用 1启用 0禁用',
  `create_time` datetime NOT NULL,
  `modfiy_time` datetime DEFAULT NULL,
  PRIMARY KEY (`group_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8mb4;


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