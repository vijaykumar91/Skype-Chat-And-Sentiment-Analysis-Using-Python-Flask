create table signup (
    id serial,
    name varchar,
    createdate timestamp,
    email varchar(200) NOT NULL,
    pasword_crypt varchar(200) NOT NULL,
    PRIMARY KEY (ID)
);