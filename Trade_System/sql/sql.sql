CREATE TABLE buy_orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    price DECIMAL(10, 2) NOT NULL,            -- 买单价格
    amount DECIMAL(10, 2) NOT NULL,           -- 买单数量
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 创建时间
);


CREATE TABLE sell_orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    price DECIMAL(10, 2) NOT NULL,            -- 卖单价格
    amount DECIMAL(10, 2) NOT NULL,           -- 卖单数量
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 创建时间
);


CREATE TABLE trade_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    price DECIMAL(10, 2) NOT NULL,            -- 历史订单价格
    amount DECIMAL(10, 2) NOT NULL,           -- 历史订单数量
    type ENUM('buy', 'sell'),                 -- 买卖种类
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 创建时间
);
