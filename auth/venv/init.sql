-- 1. Create user
CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Auth123';

-- 2. Create database
CREATE DATABASE auth;

-- 3. Grant privileges
GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';
FLUSH PRIVILEGES;

-- 4. Use the database
USE auth;

-- 5. Create table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO users (email, password) VALUES ('test123@example.com', 'password123');