drop table if exists `blocks`;
create table `blocks` (
    `id` integer primary key autoincrement,
    `version` integer not null default 0,
    `generator_id` integer not null,
    `track_id` integer not null,
    `length` integer not null,
    `range` integer not null,
    `offset` integer not null,
    `filename` string not null,
    `refcount` integer not null default 0,
    `notes` string null
);

