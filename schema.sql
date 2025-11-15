-- SQLite DDL for the FOOD DELIVERY PLATFORM database 
-- Which includes: Customers, Restaurants, MenuItems and Orders tables
-- 
-- 
-- ensures foreign key constraints are enforced
PRAGMA foreign_keys = ON;

-- 
-- 
-- create tables for Customers, Restaurants, MenuItems and Orders
-- 
-- create Customers Table
CREATE TABLE
    IF NOT EXISTS Customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        membership_level TEXT CHECK (membership_level IN ('Bronze', 'Silver', 'Gold')),
        signup_year INTEGER,
        total_orders INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

--  Restaurants Table
CREATE TABLE
    IF NOT EXISTS Restaurants (
        restaurant_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        cuisine_type TEXT,
        rating INTEGER CHECK (rating BETWEEN 1 AND 5),
        established_year INTEGER,
        avg_price REAL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

--  MenuItems Table
CREATE TABLE
    IF NOT EXISTS MenuItems (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id INTEGER NOT NULL, -- foreign key to Restaurants table
        name TEXT NOT NULL,
        category TEXT,
        price REAL NOT NULL,
        calories REAL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (restaurant_id) REFERENCES Restaurants (restaurant_id) ON DELETE CASCADE ON UPDATE CASCADE
    );

-- 
--Orders Table
CREATE TABLE
    IF NOT EXISTS Orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL, -- foreign key to Customers 
        item_id INTEGER NOT NULL, -- foreign key to MenuItems 
        quantity INTEGER NOT NULL CHECK (quantity > 0),
        order_date DATE DEFAULT (DATE ('now')),
        delivery_time INTEGER,
        total_amount REAL NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES Customers (customer_id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (item_id) REFERENCES MenuItems (item_id) ON DELETE CASCADE ON UPDATE CASCADE
    );