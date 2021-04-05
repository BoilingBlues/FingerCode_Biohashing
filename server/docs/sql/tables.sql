create table if not exists users (
    user_id int unsigned not null auto_increment,
    username varchar(20) not null unique,
    password char(64) not null,
    biocode text,
    primary key (user_id)
)engine = InnoDB auto_increment=100000 default charset=utf8mb4;

create table if not exists logs(
    log_id int unsigned not null auto_increment,
    user_id int unsigned not null,
    content text,
    createtime datetime DEFAULT CURRENT_TIMESTAMP,
    primary key(log_id),
    foreign key(user_id) references users (user_id)
)engine = InnoDB auto_increment=100000 default charset=utf8mb4;