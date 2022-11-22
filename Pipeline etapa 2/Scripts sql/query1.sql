IF OBJECT_ID(N'dbo.Producto_Unico', N'U') IS NULL   
BEGIN
	CREATE TABLE [dbo].[Producto_Unico] (
	Cod_Producto INT IDENTITY(1,1) PRIMARY KEY,
	Producto VARCHAR(50),
	Cod_Subcategoria INT,
	Cod_Categoria INT)
END