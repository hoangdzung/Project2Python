-- schema monitor

CREATE SCHEMA if not exists MONITOR default character set utf8
  collate utf8_general_ci;
use MONITOR;

-- table monitor.server
create table if not exists MONITOR.SERVER(
  id int not null auto_increment,
  NAME varchar(45) null,
  primary key (id),
  index NAME_IDX (NAME ASC)
)
ENGINE = InnoDB;

-- table MONITOR.USER
create table if not exists MONITOR.USER(
  id int not null auto_increment,
  UID int null,
  NAME varchar(45) null,
  SERVER varchar(45) null,
  primary key (id),
  unique index USER_IDX (UID ASC, NAME ASC),
  index SERVER_FK_IDX (SERVER ASC),
  constraint USER_SERVER_FK
    foreign key (SERVER)
    references MONITOR.SERVER (NAME)
    on delete no action
    on update no action
)
ENGINE = InnoDB;

-- table MONITOR.JOB
create table if not exists MONITOR.JOB(
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
    references MONITOR.USER (UID)
    on delete no action
    on update no action,
  constraint JOB_SERVER_FK
    foreign key (SERVER)
    references MONITOR.SERVER (NAME)
    on delete no action
    on update no action
)
ENGINE = InnoDB;

-- table MONITOR.jSAMPLE
create table if not exists MONITOR.jSAMPLE(
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
    references MONITOR.JOB (PID, UID, START_TIME)
    on delete no action
    on update no action
)
ENGINE = InnoDB;

-- table MONITOR.sSAMPLE
create table if not exists MONITOR.sSAMPLE(
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
    references MONITOR.SERVER (NAME)
    on delete no action
    on update no action
)
ENGINE = InnoDB;

-- table MONITOR.PREDICTION
create table if not exists MONITOR.PREDICTION(
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

grant all on MONITOR.* to vir@'%' identified by 'thanhdat97';


