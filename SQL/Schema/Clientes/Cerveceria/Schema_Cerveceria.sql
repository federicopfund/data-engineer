

-- Tabla para almacenar información de las cervezas
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Cerveza')
BEGIN
    -- Crear la tabla Cervezas
    CREATE TABLE Cerveza (
        CervezaID INT PRIMARY KEY,
        Estilo VARCHAR(50) NOT NULL,
        GraduacionAlcoholica DECIMAL(3, 1),
        VolumenLitros DECIMAL(4, 2),
        Precio DECIMAL(5, 2) NOT NULL,
		Descripcion TEXT,
        IBU INT,
        SRM INT
    );
	
END

-- Tabla para almacenar información de los ingredientes de las cervezas
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Ingredientes')
BEGIN
    -- Crear la tabla Ingredientes
    CREATE TABLE Ingredientes (
        IngredienteID INT PRIMARY KEY,
        TipoIngrediente VARCHAR(50) NOT NULL,
		CantidadStok INT,
		CantUnidLitros DECIMAL(8, 4),
        Origen VARCHAR(50),
        Descripcion TEXT,
        FechaIngreso DATE,
        Proveedor VARCHAR(50),
        PrecioUnitario DECIMAL(8, 2),
        CervezaID INT,
        FOREIGN KEY (CervezaID) REFERENCES Cerveza(CervezaID)
    );
	
END


-- Tablas para la produccion de cerveza.
-- Tabla para almacenar información sobre la producción de cerveza
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'ProduccionCerveza')
BEGIN
    -- Crear la tabla ProduccionCerveza
    CREATE TABLE ProduccionCerveza (
        ProduccionID INT PRIMARY KEY,
        CervezaID INT,
        FechaProduccion DATE NOT NULL,
        CantidadProducida DECIMAL(8, 2) NOT NULL,
        Estado VARCHAR(50) NOT NULL,
        FOREIGN KEY (CervezaID) REFERENCES Cerveza(CervezaID)
    );
END

-- Tabla para almacenar información sobre los pasos de producción de cerveza
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'PasosProduccion')
BEGIN
    -- Crear la tabla PasosProduccion
    CREATE TABLE PasosProduccion (
        PasoID INT PRIMARY KEY,
        ProduccionID INT,
        Descripcion VARCHAR(100) NOT NULL,
        FechaPaso DATE NOT NULL,
        FOREIGN KEY (ProduccionID) REFERENCES ProduccionCerveza(ProduccionID)
    );

END


-- Tablas para el manejo de Stock
-- Tabla para almacenar información sobre el inventario de cervezas
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'InventarioCervezas')
BEGIN
    -- Crear la tabla InventarioCervezas
    CREATE TABLE InventarioCervezas (
        CervezaID INT PRIMARY KEY,
        CantidadStock DECIMAL(8, 2) NOT NULL,
        FOREIGN KEY (CervezaID) REFERENCES Cerveza(CervezaID)
    );
END
-- Tabla para almacenar información sobre los clientes
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Clientes')
BEGIN
    -- Crear la tabla Clientes
    CREATE TABLE Clientes (
        ClienteID INT PRIMARY KEY,
        Nombre VARCHAR(50) NOT NULL,
        Email VARCHAR(50),
        Telefono VARCHAR(15),
        Direccion VARCHAR(100),
        Ciudad VARCHAR(50),
        Pais VARCHAR(50),
        CodigoPostal VARCHAR(10)
    );
END


-- Tabla para almacenar información sobre las ventas de cervezas
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Orden')
BEGIN
    -- Crear la tabla Orden
    CREATE TABLE Orden (
        VentaID INT PRIMARY KEY,
        FechaVenta DATE NOT NULL,
        CervezaID INT,
        Cantidad DECIMAL(8, 2) NOT NULL,
        PrecioTotal DECIMAL(8, 2) NOT NULL,
        ClienteID INT,
        FOREIGN KEY (CervezaID) REFERENCES Cerveza(CervezaID),
        FOREIGN KEY (ClienteID) REFERENCES Clientes(ClienteID)
    );
END


-- Tablas para la distribucion

-- Tabla para almacenar información de las subcursales
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Subcursales')
BEGIN
    -- Crear la tabla Subcursales
    CREATE TABLE Subcursales (
        SubcursalID INT PRIMARY KEY,
        Nombre VARCHAR(50) NOT NULL,
        Direccion VARCHAR(100),
        Ciudad VARCHAR(50),
        Pais VARCHAR(50),
        CodigoPostal VARCHAR(10)
    );
END

-- Tabla para almacenar información de los productos en cada subcursal
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'InventarioSubcursal')
BEGIN
    -- Crear la tabla InventarioSubcursal
    CREATE TABLE InventarioSubcursal (
        SubcursalID INT,
        CervezaID INT,
        CantidadStock DECIMAL(8, 2) NOT NULL,
        PRIMARY KEY (SubcursalID, CervezaID),
        FOREIGN KEY (SubcursalID) REFERENCES Subcursales(SubcursalID),
        FOREIGN KEY (CervezaID) REFERENCES Cerveza(CervezaID)
    );
END

-- Tabla para almacenar información sobre las entregas a subcursales
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'EntregasSubcursales')
BEGIN
	CREATE TABLE EntregasSubcursales (
		EntregaID INT PRIMARY KEY,
		FechaEntrega DATE NOT NULL,
		SubcursalDestinoID INT,
		CervezaID INT,
		CantidadEntregada DECIMAL(8, 2) NOT NULL,
		PrecioTotalEntrega DECIMAL(8, 2) NOT NULL,
		FOREIGN KEY (SubcursalDestinoID) REFERENCES Subcursales(SubcursalID),
		FOREIGN KEY (CervezaID) REFERENCES Cerveza(CervezaID)
	);
END

-- Tabla para almacenar información sobre los proveedores
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Proveedores')
BEGIN
	CREATE TABLE Proveedores (
		ProveedorID INT PRIMARY KEY,
		Nombre VARCHAR(50) NOT NULL,
		Contacto VARCHAR(50),
		Telefono VARCHAR(15),
		Email VARCHAR(50)
	);
END
-- Tabla para almacenar información sobre los proveedores de las subcursales
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'ProveedoresSubcursales')
BEGIN
	CREATE TABLE ProveedoresSubcursales (
		SubcursalID INT,
		ProveedorID INT,
		PRIMARY KEY (SubcursalID, ProveedorID),
		FOREIGN KEY (SubcursalID) REFERENCES Subcursales(SubcursalID),
		FOREIGN KEY (ProveedorID) REFERENCES Proveedores(ProveedorID)
	);
END
