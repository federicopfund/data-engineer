-- Crear un esquema llamado "ecommerce"
CREATE SCHEMA IF NOT EXISTS ecommerce;

-- Cambiar al esquema "ecommerce"
SET search_path TO ecommerce;

-- Tabla para departamentos
CREATE TABLE departments (
  department_id SERIAL PRIMARY KEY,
  department_name VARCHAR(100) NOT NULL
);

-- Tabla para categorías
CREATE TABLE categories (
  category_id SERIAL PRIMARY KEY,
  category_name VARCHAR(100) NOT NULL,
  department_id INT NOT NULL,
  FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- Tabla para productos
CREATE TABLE products (
  product_id SERIAL PRIMARY KEY,
  product_name VARCHAR(255) NOT NULL,
  product_description TEXT,
  product_price DECIMAL(10, 2) NOT NULL,
  product_image_url VARCHAR(255),
  category_id INT NOT NULL,
  FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- Tabla para clientes
CREATE TABLE customers (
  customer_id SERIAL PRIMARY KEY,
  customer_fname VARCHAR(100) NOT NULL,
  customer_lname VARCHAR(100) NOT NULL,
  customer_email VARCHAR(255) NOT NULL,
  customer_password VARCHAR(255) NOT NULL,
  customer_street_address VARCHAR(255) NOT NULL,
  customer_city VARCHAR(100) NOT NULL,
  customer_state VARCHAR(100) NOT NULL,
  customer_zipcode VARCHAR(20) NOT NULL
);

-- Tabla para órdenes
CREATE TABLE orders (
  order_id SERIAL PRIMARY KEY,
  order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  customer_id INT NOT NULL,
  order_status VARCHAR(50) NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Tabla para elementos de orden
CREATE TABLE order_items (
  order_item_id SERIAL PRIMARY KEY,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL,
  subtotal DECIMAL(10, 2) NOT NULL,
  product_price DECIMAL(10, 2) NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);
