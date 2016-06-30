drop table if exists user;
create table user (
    id integer primary key autoincrement,
    username text not null,
    password text not null
);

drop table if exists person;
create table person (
    id integer primary key autoincrement,
    first_name text not null,
    last_name text not null,
    family_name text,
    birth_year text,
    tree integer not null,
    foreign key(tree) references user(id)
);