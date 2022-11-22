IF OBJECT_ID(N'dbo.Productos_Sucursales', N'U') IS NULL   
BEGIN
	CREATE TABLE Productos_Sucursales (
	Cod_Producto INT,
	Cod_Sucursal INT,
	Stock INT,
	Stock_Inicial INT,
	PRIMARY KEY(Cod_Producto,Cod_Sucursal));
END