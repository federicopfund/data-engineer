IF OBJECT_ID(N'dbo.Transformacion9', N'U') IS NULL   
BEGIN
    CREATE TABLE [dbo].[Transformacion9] (
		Cod_Producto VARCHAR(5) NOT NULL,
		Ingreso_Neto_Promedio decimal(14,4) NOT NULL,
		Suma_Ingresos_Netos decimal(20,4) NOT NULL)
END