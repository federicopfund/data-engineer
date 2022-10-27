IF OBJECT_ID(N'dbo.Transformacion4', N'U') IS NULL   
BEGIN
    CREATE TABLE [dbo].[Transformacion4] (
		Country VARCHAR(25) NOT NULL, 
		Suma_TotalWasted decimal(29,4) NOT NULL)
END