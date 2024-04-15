## Pre-installations
Before you begin working on this project, make sure you have the following software installed:

1. **Python**: You'll need Python installed on your system. If you haven't installed it yet, you can download and install it from the official Python website: [Python Official Website](https://www.python.org/)

2. **MySQL**: This project utilizes MySQL as the database. Install MySQL on your system by downloading it from the official website: [MySQL Official Website](https://dev.mysql.com/downloads/)

3. **MySQL Workbench**: MySQL Workbench is a visual database design tool that integrates SQL development, administration, design, creation, and maintenance into a single integrated development environment. You can download it from the official website: [MySQL Workbench Official Website](https://www.mysql.com/products/workbench/)

4. **PyCharm**: PyCharm is the Integrated Development Environment (IDE) used for this project. You can download it from JetBrains website: [PyCharm Official Website](https://www.jetbrains.com/pycharm/download/)

## Usage
 dawnload this zip file 
 and open this file in pycharm 
 install required lib 
 like flast ,  numpy etc 
modify database file 

 for database 
 
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
