IF OBJECT_ID(N'dbo.Transformacion3', N'U') IS NULL   
BEGIN
    CREATE TABLE [dbo].[Transformacion3] (
			Country VARCHAR(25) NOT NULL,
			FirstName VARCHAR(25) NOT NULL,
			LastName VARCHAR(25) NOT NULL,
			Age INT NOT NULL)
END