some commands to create database
CREATE DATABASE parkingdetails;
use parkingdetails;
CREATE TABLE users (
   id INT AUTO_INCREMENT PRIMARY KEY,
   username VARCHAR(255) NOT NULL UNIQUE,
   email VARCHAR(255) NOT NULL UNIQUE,
   password VARCHAR(255) NOT NULL
);

INSERT INTO users (username, email, password) 
VALUES ('Ayaan','ayaanpatel81@gmail.com','Ayaan@2002');

use parkingdetails;

update users set email = 'ashpakpatel81@gmail.com' where id = 1;

ALTER TABLE users AUTO_INCREMENT = 1;

select * from users;

delete from users where id = 1;
