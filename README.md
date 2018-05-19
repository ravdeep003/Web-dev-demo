# Web-dev-demo

## Requirements:
* Flask
* Python-pip
* MySql

## Install Dependencies
  `pip install -r requirement.txt`
  
  
## How to run 
   `python app.py`

## Installing MySql
    sudo apt-get install mysql-server libmysqlclient-dev
    
## Creating Databases
    CREATE DATABASE testing;
    use testing
    
## Creating Tables
       CREATE TABLE user(id INT(5) AUTO_INCREMENT PRIMARY KEY, username VARCHAR(20), password VARCHAR(100), email VARCHAR(100), joined_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
       CREATE TABLE article(id INT(5) AUTO_INCREMENT PRIMARY KEY, author VARCHAR(20), title VARCHAR(200), content TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
