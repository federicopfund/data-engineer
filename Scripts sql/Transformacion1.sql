IF OBJECT_ID(N'dbo.Transformacion1', N'U') IS NULL   
BEGIN
    CREATE TABLE [dbo].[Transformacion1] (
		Cod_Categoria VARCHAR(10) PRIMARY KEY,
		Nombre_Categoria VARCHAR(20) NOT NULL)
END