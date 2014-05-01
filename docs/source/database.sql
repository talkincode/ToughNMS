-- create table oms_stat_load
create table oms_stat_load (
    host_name varchar(64) not null,
    avg_1 varchar(8) not null,
    avg_5 varchar(8) not null,
    avg_15 varchar(8) not null,
    check_time varchar(19) not null,
	primary key ( host_name,check_time )
);
-- create table oms_stat_traffic
create table oms_stat_traffic (
    host_name varchar(64) not null,
    traffic int(11) not null,
    check_time varchar(19) not null,
	primary key ( host_name,check_time )
);
