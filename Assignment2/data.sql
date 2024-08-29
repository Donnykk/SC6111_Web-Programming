CREATE DATABASE USER_SYSTEM;

USE USER_SYSTEM;

CREATE TABLE
    users (
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL
    );

CREATE TABLE
    sessions (
        session_id VARCHAR(255) PRIMARY KEY,
        user_id INT,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );