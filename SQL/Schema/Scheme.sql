-- Crear un esquema llamado "ecommerce"
CREATE SCHEMA IF NOT EXISTS ecommerce;

-- Cambiar al esquema "ecommerce"
SET search_path TO ecommerce;

-- Tabla para productos
CREATE TABLE products (
  product_id SERIAL PRIMARY KEY,
  product_code VARCHAR(20) UNIQUE NOT NULL,
  product_name VARCHAR(255) NOT NULL,
  category_id INT NOT NULL,
  price DECIMAL(10, 2) NOT NULL,
  stock_quantity INT NOT NULL,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para categorías de productos
CREATE TABLE categories (
  category_id SERIAL PRIMARY KEY,
  category_name VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para subcategorías de productos
CREATE TABLE subcategories (
  subcategory_id SERIAL PRIMARY KEY,
  subcategory_code VARCHAR(50) COLLATE Modern_Spanish_CI_AS,
  subcategory_name VARCHAR(50) COLLATE Modern_Spanish_CI_AS,
  category_id INT NOT NULL,
  FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- Tabla para clientes
CREATE TABLE customers (
  customer_id SERIAL PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  address VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para pedidos
CREATE TABLE orders (
  order_id SERIAL PRIMARY KEY,
  customer_id INT NOT NULL,
  order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status VARCHAR(50) NOT NULL,
  total_amount DECIMAL(10, 2) NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Tabla para detalles de pedidos
CREATE TABLE order_details (
  order_detail_id SERIAL PRIMARY KEY,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL,
  unit_price DECIMAL(10, 2) NOT NULL,
  subtotal DECIMAL(10, 2) NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Tabla para promociones
CREATE TABLE promotions (
  promotion_id SERIAL PRIMARY KEY,
  promotion_code VARCHAR(20) UNIQUE NOT NULL,
  discount_percentage INT NOT NULL,
  start_date TIMESTAMP NOT NULL,
  end_date TIMESTAMP NOT NULL
);

-- Tabla para aplicar promociones a pedidos
CREATE TABLE order_promotions (
  order_id INT NOT NULL,
  promotion_id INT NOT NULL,
  PRIMARY KEY (order_id, promotion_id),
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (promotion_id) REFERENCES promotions(promotion_id)
);

-- Tabla para sucursales
CREATE TABLE branches (
  branch_id SERIAL PRIMARY KEY,
  branch_code VARCHAR(50) COLLATE Modern_Spanish_CI_AS,
  branch_code_pk INT COLLATE Modern_Spanish_CI_AS,
  branch_name VARCHAR(50) COLLATE Modern_Spanish_CI_AS,
  latitude FLOAT COLLATE Modern_Spanish_CI_AS,
  longitude FLOAT COLLATE Modern_Spanish_CI_AS
);

-- Tabla para subcategorías
CREATE TABLE subcategories (
  subcategory_id SERIAL PRIMARY KEY,
  subcategory_code VARCHAR(50) COLLATE Modern_Spanish_CI_AS,
  subcategory_name VARCHAR(50) COLLATE Modern_Spanish_CI_AS,
  category_id INT NOT NULL,
  FOREIGN KEY (category_id) REFERENCES categories(category_id)
);
-- Tabla para facturas de minería
CREATE TABLE fact_mine (
  truck_id INT NOT NULL,
  project_id INT NOT NULL,
  operator_id INT NOT NULL,
  total_ore_mined MONEY NOT NULL,
  total_wasted MONEY NOT NULL,
  date_mined DATETIME NULL,
  PRIMARY KEY (truck_id, project_id, operator_id),
  FOREIGN KEY (truck_id) REFERENCES trucks(truck_id),
  FOREIGN KEY (project_id) REFERENCES projects(project_id),
  FOREIGN KEY (operator_id) REFERENCES operators(operator_id)
);

-- Otras tablas del esquema...

-- Tabla para camiones
CREATE TABLE trucks (
  truck_id INT PRIMARY KEY,
  truck_name VARCHAR(65) NULL
);

-- Tabla para proyectos
CREATE TABLE projects (
  project_id INT PRIMARY KEY,
  project_name NVARCHAR(100) NOT NULL
);

-- Tabla para operadores
CREATE TABLE operators (
  operator_id INT PRIMARY KEY,
  first_name NVARCHAR(50) NULL,
  last_name NVARCHAR(50) NULL
);


-- Tabla para ventas por Internet
CREATE TABLE internet_sales (
  Cod_Producto VARCHAR(50) COLLATE Modern_Spanish_CI_AS,
  Cod_Cliente VARCHAR(50) COLLATE Modern_Spanish_CI_AS,
  Cod_Territorio VARCHAR(50) COLLATE Modern_Spanish_CI_AS,
  NumeroOrden INT COLLATE Modern_Spanish_CI_AS,
  Cantidad INT COLLATE Modern_Spanish_CI_AS,
  PrecioUnitario MONEY COLLATE Modern_Spanish_CI_AS,
  CostoUnitario MONEY COLLATE Modern_Spanish_CI_AS,
  Impuesto MONEY COLLATE Modern_Spanish_CI_AS,
  Flete REAL COLLATE Modern_Spanish_CI_AS,
  FechaOrden DATETIMEOFFSET COLLATE Modern_Spanish_CI_AS,
  FechaEnvio DATETIMEOFFSET COLLATE Modern_Spanish_CI_AS,
  FechaVencimiento DATETIMEOFFSET COLLATE Modern_Spanish_CI_AS,
);