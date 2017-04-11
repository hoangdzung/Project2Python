-- schema monitor_test

CREATE SCHEMA if not exists MONITOR_TEST default character set utf8
  collate utf8_general_ci;
use MONITOR_TEST;

-- table monitor_test.server
create table if not exists MONITOR_TEST.SERVER(
  id int not null auto_increment,
  NAME varchar(45) null,
  primary key (id),
  index NAME_IDX (NAME ASC)
)
ENGINE = InnoDB;

-- table MONITOR_TEST.USER
create table if not exists MONITOR_TEST.USER(
  id int not null auto_increment,
  UID int null,
  NAME varchar(45) null,
  SERVER varchar(45) null,
  primary key (id),
  unique index USER_IDX (UID ASC, NAME ASC),
  index SERVER_FK_IDX (SERVER ASC),
  constraint USER_SERVER_FK
    foreign key (SERVER)
    references MONITOR_TEST.SERVER (NAME)
    on delete no action
    on update no action
)
ENGINE = InnoDB;

-- table MONITOR_TEST.JOB
create table if not exists MONITOR_TEST.JOB(
  id int not null auto_increment,
  PID int null,
  UID int null,
  START_TIME datetime null,
  CMD_NAME varchar(45) null,
  COMMAND tinytext null,
  SERVER varchar(45) null,
  primary key (id),
  unique index P_IDX (PID ASC, UID ASC, START_TIME ASC),
  index UID_FK_IDX (UID ASC),
  index SERVER_FK_IDX (SERVER ASC),
  constraint JOB_UID_FK
    foreign key (UID)
    references MONITOR_TEST.USER (UID)
    on delete no action
    on update no action,
  constraint JOB_SERVER_FK
    foreign key (SERVER)
    references MONITOR_TEST.SERVER (NAME)
    on delete no action
    on update no action
)
ENGINE = InnoDB;

-- table MONITOR_TEST.jSAMPLE
create table if not exists MONITOR_TEST.jSAMPLE(
  id int not null auto_increment,
  PID int null,
  UID int null,
  START_TIME datetime null,
  RUN_TIME timestamp null default current_timestamp,
  CPU decimal(6, 3) null,
  RAM decimal(6, 3) null,
  RAM_RSS int null,
  RAM_VMS int null,
  DISK_IN bigint null,
  DISK_OUT bigint null,
  primary key (id),
  constraint P_FK
    foreign key (PID, UID, START_TIME)
    references MONITOR_TEST.JOB (PID, UID, START_TIME)
    on delete no action
    on update no action
)
ENGINE = InnoDB;

-- table MONITOR_TEST.sSAMPLE
create table if not exists MONITOR_TEST.sSAMPLE(
  id int not null auto_increment,
  NAME varchar(45) null,
  TIMESTAMP timestamp null default current_timestamp,
  CPU decimal(6, 3) null,
  RAM decimal(6, 3) null,
  RAM_AVAILABLE int null,
  RAM_CACHED int null,
  DISK_IN bigint null,
  DISK_OUT bigint null,
  primary key (id),
  index SERVER_FK_IDX (NAME ASC),
  constraint sSAMPLE_SERVER_FK
    foreign key (NAME)
    references MONITOR_TEST.SERVER (NAME)
    on delete no action
    on update no action
)
ENGINE = InnoDB;

-- table MONITOR_TEST.PREDICTION
create table if not exists MONITOR_TEST.PREDICTION(
  id int not null auto_increment,
  UID int null,
  USER_NAME varchar(45) null,
  LAST_USED_SERVER varchar(45) null,
  LAST_LOGIN datetime,
  AVG_CPU decimal(6, 3),
  MAX_CPU decimal(6, 3),
  AVG_RAM decimal(6, 3),
  MAX_RAM decimal(6, 3),
  primary key (id)
)
ENGINE = InnoDB;

-- grant all on MONITOR_TEST.* to vir@'%' identified by 'thanhdat97';
