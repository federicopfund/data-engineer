
-- Tabla para almacenar informaci�n de las cervezas
CREATE TABLE Cervezas (
    CervezaID INT PRIMARY KEY,
	EstiloID INT,
    Nombre VARCHAR(50) NOT NULL,
    GraduacionAlcoholica DECIMAL(3, 1),
    VolumenLitros DECIMAL(4, 2),
    Precio DECIMAL(5, 2) NOT NULL,
	FOREIGN KEY (EstiloID) REFERENCES EstilosCerveza(EstiloID)
);

-- Tabla para almacenar informaci�n de los ingredientes de las cervezas
CREATE TABLE Ingredientes (
    IngredienteID INT PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Tipo VARCHAR(50) NOT NULL,
    Origen VARCHAR(50),
    Descripcion TEXT,
    FechaIngreso DATE,
    Proveedor VARCHAR(50),
    PrecioUnitario DECIMAL(8, 2),
	EstiloID INT, -- Nueva columna para el ID del estilo
    FOREIGN KEY (EstiloID) REFERENCES EstilosCerveza(EstiloID)
);
);

-- Tabla para almacenar informaion de los estilos de Cerveza
CREATE TABLE EstilosCerveza (
    EstiloID INT PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Descripcion TEXT,
    IBU INT, -- Unidades Internacionales de Amargor
    SRM INT, -- �ndice de Color (Standard Reference Method)
    RangoAlcohol DECIMAL(3, 1), -- Rango de Graduaci�n Alcoholica (por ejemplo, 4.0 - 6.0)
    Comentarios TEXT
);

-- Tablas para la produccion de cerveza.
-- Tabla para almacenar informaci�n sobre la producci�n de cerveza
CREATE TABLE ProduccionCerveza (
    ProduccionID INT PRIMARY KEY,
    CervezaID INT,
    FechaProduccion DATE NOT NULL,
    CantidadProducida DECIMAL(8, 2) NOT NULL,
    Estado VARCHAR(50) NOT NULL, -- Por ejemplo, "En proceso", "Listo para embotellar", etc.
    FOREIGN KEY (CervezaID) REFERENCES Cervezas(CervezaID)
);

-- Tabla para almacenar informaci�n sobre los pasos de producci�n de cerveza
CREATE TABLE PasosProduccion (
    PasoID INT PRIMARY KEY,
    ProduccionID INT,
    Descripcion VARCHAR(100) NOT NULL,
    FechaPaso DATE NOT NULL,
    FOREIGN KEY (ProduccionID) REFERENCES ProduccionCerveza(ProduccionID)
);

-- Tablas para el manejo de Stock
-- Tabla para almacenar informaci�n sobre el inventario de cervezas
CREATE TABLE InventarioCervezas (
    CervezaID INT PRIMARY KEY,
    CantidadStock DECIMAL(8, 2) NOT NULL,
    FOREIGN KEY (CervezaID) REFERENCES Cervezas(CervezaID)
);


-- Tabla para almacenar informaci�n sobre las ventas de cervezas
CREATE TABLE Orden (
    VentaID INT PRIMARY KEY,
    FechaVenta DATE NOT NULL,
    CervezaID INT,
    Cantidad DECIMAL(8, 2) NOT NULL,
    PrecioTotal DECIMAL(8, 2) NOT NULL,
    ClienteID INT, -- Nueva columna para el ID del cliente
    FOREIGN KEY (CervezaID) REFERENCES Cervezas(CervezaID),
    FOREIGN KEY (ClienteID) REFERENCES Clientes(ClienteID)
);

-- Tabla para almacenar informaci�n sobre los clientes
CREATE TABLE Clientes (
    ClienteID INT PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Email VARCHAR(50),
    Telefono VARCHAR(15),
    Direccion VARCHAR(100), -- Nueva columna para la direcci�n del cliente
    Ciudad VARCHAR(50), -- Nueva columna para la ciudad del cliente
    Pais VARCHAR(50), -- Nueva columna para el pa�s del cliente
    CodigoPostal VARCHAR(10) -- Nueva columna para el c�digo postal del cliente
);

-- Tablas para la distribucion

-- Tabla para almacenar informaci�n de las subcursales
CREATE TABLE Subcursales (
    SubcursalID INT PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Direccion VARCHAR(100),
    Ciudad VARCHAR(50),
    Pais VARCHAR(50),
    CodigoPostal VARCHAR(10)
);

-- Tabla para almacenar informaci�n de los productos en cada subcursal
CREATE TABLE InventarioSubcursal (
    SubcursalID INT,
    CervezaID INT,
    CantidadStock DECIMAL(8, 2) NOT NULL,
    PRIMARY KEY (SubcursalID, CervezaID),
    FOREIGN KEY (SubcursalID) REFERENCES Subcursales(SubcursalID),
    FOREIGN KEY (CervezaID) REFERENCES Cervezas(CervezaID)
);

-- Tabla para almacenar informaci�n sobre las entregas a subcursales
CREATE TABLE EntregasSubcursales (
    EntregaID INT PRIMARY KEY,
    FechaEntrega DATE NOT NULL,
    SubcursalDestinoID INT,
    CervezaID INT,
    CantidadEntregada DECIMAL(8, 2) NOT NULL,
    PrecioTotalEntrega DECIMAL(8, 2) NOT NULL,
    FOREIGN KEY (SubcursalDestinoID) REFERENCES Subcursales(SubcursalID),
    FOREIGN KEY (CervezaID) REFERENCES Cervezas(CervezaID)
);

-- Tabla para almacenar informaci�n sobre los proveedores de las subcursales
CREATE TABLE ProveedoresSubcursales (
    SubcursalID INT,
    ProveedorID INT,
    PRIMARY KEY (SubcursalID, ProveedorID),
    FOREIGN KEY (SubcursalID) REFERENCES Subcursales(SubcursalID),
    FOREIGN KEY (ProveedorID) REFERENCES Proveedores(ProveedorID)
);

-- Tabla para almacenar informaci�n sobre los proveedores
CREATE TABLE Proveedores (
    ProveedorID INT PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Contacto VARCHAR(50),
    Telefono VARCHAR(15),
    Email VARCHAR(50)
);
