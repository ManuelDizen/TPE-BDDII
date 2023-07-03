create table if not exists banks(
    id serial primary key,
    code varchar(4) not null
);

create table if not exists bank_accounts(
    id serial primary key,
    balance integer not null,
    bank_id integer not null,
    cbu varchar not null,
    foreign key (bank_id) references banks(id)
);

create table if not exists users(
    id serial primary key,
    cuit varchar not null,
    name varchar not null,
    email varchar,
    phone varchar
);

create table if not exists user_to_banks(
    id serial primary key,
    user_id int not null,
    bank_id int not null,
    unique(user_id, bank_id)
);

INSERT INTO banks(id, code) SELECT 0, 'GAL' WHERE NOT EXISTS (SELECT 1 FROM banks WHERE id = 0);
INSERT INTO banks(id, code) SELECT 1, 'STD' WHERE NOT EXISTS (SELECT 1 FROM banks WHERE id = 1);
INSERT INTO banks(id, code) SELECT 2, 'FRA' WHERE NOT EXISTS (SELECT 1 FROM banks WHERE id = 2);