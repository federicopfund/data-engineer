
--Cervezas: Contiene información sobre las cervezas disponibles, como nombre, estilo, graduación alcohólica, precio y stock.

--Clientes: Almacena información sobre los clientes, como nombre, apellido, email y teléfono.

--Ordenes: Registra las órdenes realizadas por los clientes, incluyendo la fecha y el total.

--DetallesOrden: Almacena detalles de las órdenes, como la cerveza pedida, la cantidad, el precio unitario y el subtotal. Se establecen claves foráneas para mantener la integridad referencial.

-- Tabla para almacenar información de las cervezas
CREATE TABLE Cervezas (
    CervezaID INT PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Estilo VARCHAR(50),
    GraduacionAlcoholica DECIMAL(3, 1),
    VolumenLitros DECIMAL(4, 2),
    Precio DECIMAL(5, 2) NOT NULL
);

-- Tabla para almacenar información de los ingredientes de las cervezas
CREATE TABLE Ingredientes (
    IngredienteID INT PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Tipo VARCHAR(50) NOT NULL
);

-- Tabla de relación entre cervezas e ingredientes (relación muchos a muchos)
CREATE TABLE CervezaIngredientes (
    CervezaID INT,
    IngredienteID INT,
    PRIMARY KEY (CervezaID, IngredienteID),
    FOREIGN KEY (CervezaID) REFERENCES Cervezas(CervezaID),
    FOREIGN KEY (IngredienteID) REFERENCES Ingredientes(IngredienteID)
);

-- Tabla para almacenar información sobre la producción de cerveza
CREATE TABLE ProduccionCerveza (
    ProduccionID INT PRIMARY KEY,
    CervezaID INT,
    FechaProduccion DATE NOT NULL,
    CantidadProducida DECIMAL(8, 2) NOT NULL,
    Estado VARCHAR(50) NOT NULL, -- Por ejemplo, "En proceso", "Listo para embotellar", etc.
    FOREIGN KEY (CervezaID) REFERENCES Cervezas(CervezaID)
);

-- Tabla para almacenar información sobre los pasos de producción de cerveza
CREATE TABLE PasosProduccion (
    PasoID INT PRIMARY KEY,
    ProduccionID INT,
    Descripcion VARCHAR(100) NOT NULL,
    FechaPaso DATE NOT NULL,
    FOREIGN KEY (ProduccionID) REFERENCES ProduccionCerveza(ProduccionID)
);
-- Tabla para almacenar información sobre el inventario de cervezas
CREATE TABLE InventarioCervezas (
    CervezaID INT PRIMARY KEY,
    CantidadStock DECIMAL(8, 2) NOT NULL,
    FOREIGN KEY (CervezaID) REFERENCES Cervezas(CervezaID)
);

-- Resto de las tablas se mantienen igual

-- Tabla para almacenar información sobre las ventas de cervezas
CREATE TABLE Ventas (
    VentaID INT PRIMARY KEY,
    FechaVenta DATE NOT NULL,
    CervezaID INT,
    Cantidad DECIMAL(8, 2) NOT NULL,
    PrecioTotal DECIMAL(8, 2) NOT NULL,
    FOREIGN KEY (CervezaID) REFERENCES Cervezas(CervezaID)
);

-- Tabla para almacenar información sobre los clientes
CREATE TABLE Clientes (
    ClienteID INT PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Email VARCHAR(50),
    Telefono VARCHAR(15)
);
