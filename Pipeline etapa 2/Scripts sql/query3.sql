ALTER TABLE [dbo].[Producto_Unico]
DROP COLUMN Cod_Producto;

ALTER TABLE [dbo].[Producto_Unico]
ADD Cod_Producto INT NOT NULL IDENTITY(1,1);
