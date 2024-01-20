-- Tabla para almacenar informaci�n de las cervezas
CREATE TABLE Cervezas (
    CervezaID INT PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Estilo VARCHAR(50),
    GraduacionAlcoholica DECIMAL(3, 1),
    VolumenLitros DECIMAL(4, 2),
    Precio DECIMAL(5, 2) NOT NULL
);

-- Tabla para almacenar informaci�n de los ingredientes de las cervezas
CREATE TABLE Ingredientes (
    IngredienteID INT PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Tipo VARCHAR(50) NOT NULL
);

-- Tabla de relaci�n entre cervezas e ingredientes (relaci�n muchos a muchos)
CREATE TABLE CervezaIngredientes (
    CervezaID INT,
    IngredienteID INT,
    PRIMARY KEY (CervezaID, IngredienteID),
    FOREIGN KEY (CervezaID) REFERENCES Cervezas(CervezaID),
    FOREIGN KEY (IngredienteID) REFERENCES Ingredientes(IngredienteID)
);

-- Tabla para almacenar informaci�n sobre el inventario de cervezas
CREATE TABLE InventarioCervezas (
    CervezaID INT PRIMARY KEY,
    CantidadStock DECIMAL(8, 2) NOT NULL,
    FOREIGN KEY (CervezaID) REFERENCES Cervezas(CervezaID)
);

-- Resto de las tablas se mantienen igual

-- Tabla para almacenar informaci�n sobre las ventas de cervezas
CREATE TABLE Ventas (
    VentaID INT PRIMARY KEY,
    FechaVenta DATE NOT NULL,
    CervezaID INT,
    Cantidad DECIMAL(8, 2) NOT NULL,
    PrecioTotal DECIMAL(8, 2) NOT NULL,
    FOREIGN KEY (CervezaID) REFERENCES Cervezas(CervezaID)
);

-- Tabla para almacenar informaci�n sobre los clientes
CREATE TABLE Clientes (
    ClienteID INT PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Email VARCHAR(50),
    Telefono VARCHAR(15)
);
