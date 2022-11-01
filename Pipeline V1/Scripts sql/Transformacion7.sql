IF OBJECT_ID(N'dbo.Transformacion7', N'U') IS NULL   
BEGIN
    CREATE TABLE [dbo].[Transformacion7] (
		Cod_SubCategoria VARCHAR(5) NOT NULL,
		SubCategoria VARCHAR(20) NOT NULL,
		Cod_Categoria VARCHAR(5) NOT NULL)
END