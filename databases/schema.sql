DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS order_history;
DROP TABLE IF EXISTS products;

CREATE TABLE users (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   username TEXT NOT NULL,
   password TEXT NOT NULL,
   securityQ1 TEXT NOT NULL,
   securityQ2 TEXT NOT NULL,
   securityQ3 TEXT NOT NULL,
   securityA1 TEXT NOT NULL,
   securityA2 TEXT NOT NULL,
   securityA3 TEXT NOT NULL,
   address TEXT NOT NULL,
   phone_number INTEGER NOT NULL,
   picture TEXT NOT NULL,
   role INTEGER NOT NULL,
   attempts INTEGER NOT NULL,
   last_attempt REAL
);

CREATE TABLE roles (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   role INTEGER NOT NULL,
   description TEXT NOT NULL
);

CREATE TABLE order_history (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   order_id INTEGER NOT NULL,
   product_id INTEGER NOT NULL,
   user_id INTEGER NOT NULL,
   quantity INTEGER NOT NULL,
   price REAL NOT NULL,
   order_date TEXT NOT NULL
);

CREATE TABLE products (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   name TEXT NOT NULL,
   description TEXT NOT NULL,
   dimensions TEXT,
   weight REAL,
   unit TEXT NOT NULL,
   price REAL NOT NULL,
   stock_level INTEGER NOT NULL,
   category TEXT NOT NULL,
   image TEXT NOT NULL
);