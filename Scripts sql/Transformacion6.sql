IF OBJECT_ID(N'dbo.Transformacion6', N'U') IS NULL   
BEGIN
    CREATE TABLE [dbo].[Transformacion6] (
			Cod_Producto VARCHAR(20) NOT NULL,
			Producto VARCHAR(50) NOT NULL,
			Cod_SubCategoria VARCHAR(20) NOT NULL,
			Color VARCHAR(20) NOT NULL)
END