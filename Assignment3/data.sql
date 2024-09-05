CREATE DATABASE IF NOT EXISTS Trading_System;

USE Trading_System;

CREATE TABLE
    buy_orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        price DECIMAL(10, 2) NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE
    sell_orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        price DECIMAL(10, 2) NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE
    trade_history (
        id INT AUTO_INCREMENT PRIMARY KEY,
        price DECIMAL(10, 2) NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );