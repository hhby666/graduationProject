drop database if exists face;
create database face;
use face;
create table if not exists face.`user`
(
    `id`          int(10) auto_increment comment '主键id',
    `sno`         varchar(10) unique not null COMMENT '学号',
    `name`        varchar(40)        not null COMMENT '姓名',
    `sex`         int(1)                      default 2 COMMENT '性别: 0: 男， 1: 女， 其他: 未知',
    `email`       varchar(40)        not null COMMENT '邮箱地址',
    `feature`     text               not null COMMENT '特征编码',
    `admin_id`    int(10)            not null COMMENT '归属管理员id',
    `create_time` datetime           not null default current_timestamp comment '创建时间',
    `update_time` timestamp          null     default current_timestamp on update current_timestamp comment '更新时间',
    primary key (`id`)
) engine = INNODB
  default charset = utf8 comment ='用户表';

create table if not exists face.`admin`
(
    `id`          int(10) auto_increment comment '主键id',
    `name`        varchar(40)  not null COMMENT '姓名',
    `user_name`   varchar(40)  not null unique COMMENT '用户名',
    `password`    varchar(100) not null COMMENT '密码',
    `email`       varchar(40)  not null COMMENT '邮箱地址',
    `create_time` datetime     not null default current_timestamp comment '创建时间',
    `update_time` timestamp    null     default current_timestamp on update current_timestamp comment '更新时间',
    primary key (`id`)
) engine = INNODB
  default charset = utf8 comment ='管理员表';

create table if not exists face.`activity`
(
    `id`          int(10) auto_increment comment '主键id',
    `name`        varchar(100) not null COMMENT '活动名',
    `admin_id`    int(10)      not null COMMENT '管理员id',
    `start_time`  datetime     not null COMMENT '签到开始时间',
    `end_time`    datetime     not null COMMENT '签到结束时间',
    `create_time` datetime     not null default current_timestamp comment '创建时间',
    `update_time` timestamp    null     default current_timestamp on update current_timestamp comment '更新时间',
    primary key (`id`)
) engine = INNODB
  default charset = utf8 comment ='活动表';

create table if not exists face.`sign`
(
    `user_id`     int(10)   not null comment '用户id',
    `activity_id` int(10)   not null COMMENT '活动id',
    `is_sign`     boolean            default false COMMENT '是否签到',
    `create_time` datetime  not null default current_timestamp comment '创建时间',
    `update_time` timestamp null     default current_timestamp on update current_timestamp comment '更新时间',
    primary key (`user_id`, `activity_id`)
) engine = INNODB
  default charset = utf8 comment ='签到表';

delimiter $
create trigger deleteUser
    after
        delete
    on user
    for each row
begin
    delete from sign where user_id = OLD.id;
end$
delimiter ;
delimiter $
create trigger deleteAdmin
    after
        delete
    on admin
    for each row
begin
    delete from activity where admin_id = OLD.id;
    delete from user where admin_id = OLD.id;
end$
delimiter ;
delimiter $
create trigger deleteAct
    after
        delete
    on activity
    for each row
begin
    delete from sign where sign.activity_id = OLD.id;
end$
delimiter ;