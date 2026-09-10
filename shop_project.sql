-- @block
CREATE DATABASE IF NOT EXISTS shop;
USE shop;

-- @block
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price INT NOT NULL,
    kind VARCHAR(20) NOT NULL,          -- 'Clothing','Food','Tool','Thing'
    amount INT NOT NULL,
    vaild_date VARCHAR(20) NOT NULL,    -- stored as text "mm/dd/yy" (see DateEntry.get())
    size VARCHAR(20) NOT NULL,          -- 'Small','Medium','Big'
    added_date VARCHAR(20) NOT NULL     -- stored as text "mm/dd/yy"
);

-- @block
CREATE TABLE IF NOT EXISTS purchases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price INT NOT NULL,
    kind VARCHAR(20) NOT NULL,
    amount INT NOT NULL,
    vaild_date VARCHAR(20) NOT NULL,
    size VARCHAR(20) NOT NULL,
    purchased_date VARCHAR(20) NOT NULL
);

-- @block
CREATE TABLE IF NOT EXISTS my_variables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    value VARCHAR(50) NOT NULL          
);

-- @block
INSERT INTO my_variables (id, name, value) VALUES
    (1, 'total_sales', '0'),
    (2, 'total_money', '0');
	