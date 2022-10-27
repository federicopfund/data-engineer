IF OBJECT_ID(N'dbo.Transformacion8', N'U') IS NULL   
BEGIN
    CREATE TABLE [dbo].[Transformacion8] (
		Cod_Producto VARCHAR(30) NOT NULL,
		Cod_Cliente VARCHAR(30) NOT NULL,
		Cod_Territorio VARCHAR(30) NOT NULL,
		NumeroOrden VARCHAR(30) NOT NULL,
		Cantidad VARCHAR(30) NOT NULL,
		PrecioUnitario VARCHAR(30) NOT NULL,
		CostoUnitario VARCHAR(30) NOT NULL,
		Impuesto VARCHAR(30) NOT NULL,
		Flete VARCHAR(30) NOT NULL,
		FechaOrden VARCHAR(30) NOT NULL,
		FechaEnvio VARCHAR(30) NOT NULL,
		FechaVencimiento VARCHAR(30) NOT NULL,
		Cod_Promocion VARCHAR(30) NOT NULL,
		Ingresos_Netos decimal(10,4) NOT NULL)
END