-- Insertar datos en la tabla Ingredientes
MERGE INTO Ingredientes AS target
USING (VALUES
    (1, 'Lúpulo Cascade', 'Lúpulo'),
    (2, 'Malta Pale', 'Malta'),
    (3, 'Levadura Ale', 'Levadura'),
    (4, 'Lúpulo Amarillo', 'Lúpulo'),
    (5, 'Malta Munich', 'Malta'),
    (6, 'Levadura Lager', 'Levadura')
) AS source (IngredienteID, Nombre, Tipo)
ON target.IngredienteID = source.IngredienteID
WHEN MATCHED THEN
    UPDATE SET Nombre = source.Nombre, Tipo = source.Tipo
WHEN NOT MATCHED THEN
    INSERT (IngredienteID, Nombre, Tipo)
    VALUES (source.IngredienteID, source.Nombre, source.Tipo);

-- Insertar datos en la tabla Cervezas
MERGE INTO Cervezas AS target
USING (VALUES
    (1, 'IPA', 'India Pale Ale', 6.5, 0.355, 5.99),
    (2, 'Stout', 'Stout', 7.2, 0.473, 7.99),
    (3, 'Blonde Ale', 'Blonde Ale', 5.0, 0.5, 6.49),
    (4, 'Amber Lager', 'Amber Lager', 5.8, 0.355, 6.79),
    (5, 'Wheat Beer', 'Wheat Beer', 4.2, 0.5, 5.49)
) AS source (CervezaID, Nombre, Estilo, GraduacionAlcoholica, VolumenLitros, Precio)
ON target.CervezaID = source.CervezaID
WHEN MATCHED THEN
    UPDATE SET Nombre = source.Nombre, Estilo = source.Estilo, GraduacionAlcoholica = source.GraduacionAlcoholica,
               VolumenLitros = source.VolumenLitros, Precio = source.Precio
WHEN NOT MATCHED THEN
    INSERT (CervezaID, Nombre, Estilo, GraduacionAlcoholica, VolumenLitros, Precio)
    VALUES (source.CervezaID, source.Nombre, source.Estilo, source.GraduacionAlcoholica, source.VolumenLitros, source.Precio);

-- Insertar datos en la tabla CervezaIngredientes
MERGE INTO CervezaIngredientes AS target
USING (VALUES
    (1, 1), (1, 2), (1, 3),
    (2, 1), (2, 2), (2, 3),
    (3, 1), (3, 2), (3, 3),
    (4, 4), (4, 5), (4, 6),
    (5, 1), (5, 2), (5, 3)
) AS source (CervezaID, IngredienteID)
ON target.CervezaID = source.CervezaID AND target.IngredienteID = source.IngredienteID
WHEN NOT MATCHED THEN
    INSERT (CervezaID, IngredienteID)
    VALUES (source.CervezaID, source.IngredienteID);

-- Insertar datos en la tabla ProduccionCerveza
MERGE INTO ProduccionCerveza AS target
USING (VALUES
    (1, 1, '2024-01-01', 500, 'En proceso'),
    (2, 2, '2024-01-02', 300, 'Listo para embotellar'),
    (3, 3, '2024-01-03', 400, 'Listo para embotellar'),
    (4, 4, '2024-01-04', 200, 'En proceso'),
    (5, 5, '2024-01-05', 350, 'Listo para embotellar')
) AS source (ProduccionID, CervezaID, FechaProduccion, CantidadProducida, Estado)
ON target.ProduccionID = source.ProduccionID
WHEN MATCHED THEN
    UPDATE SET CervezaID = source.CervezaID, FechaProduccion = source.FechaProduccion,
               CantidadProducida = source.CantidadProducida, Estado = source.Estado
WHEN NOT MATCHED THEN
    INSERT (ProduccionID, CervezaID, FechaProduccion, CantidadProducida, Estado)
    VALUES (source.ProduccionID, source.CervezaID, source.FechaProduccion, source.CantidadProducida, source.Estado);

-- Insertar datos en la tabla PasosProduccion
MERGE INTO PasosProduccion AS target
USING (VALUES
    (1, 1, 'Maceración', '2024-01-01'),
    (2, 1, 'Cocción', '2024-01-02'),
    (3, 2, 'Fermentación', '2024-01-03'),
    (4, 2, 'Maduración', '2024-01-04'),
    (5, 3, 'Filtrado', '2024-01-05'),
    (6, 3, 'Carbonatación', '2024-01-06'),
    (7, 4, 'Clarificación', '2024-01-07'),
    (8, 5, 'Embotellado', '2024-01-08')
) AS source (PasoID, ProduccionID, Descripcion, FechaPaso)
ON target.PasoID = source.PasoID
WHEN MATCHED THEN
    UPDATE SET ProduccionID = source.ProduccionID, Descripcion = source.Descripcion, FechaPaso = source.FechaPaso
WHEN NOT MATCHED THEN
    INSERT (PasoID, ProduccionID, Descripcion, FechaPaso)
    VALUES (source.PasoID, source.ProduccionID, source.Descripcion, source.FechaPaso);

-- Insertar datos en la tabla InventarioCervezas
MERGE INTO InventarioCervezas AS target
USING (VALUES
    (1, 200),
    (2, 100),
    (3, 150),
    (4, 50),
    (5, 80)
) AS source (CervezaID, CantidadStock)
ON target.CervezaID = source.CervezaID
WHEN MATCHED THEN
    UPDATE SET CantidadStock = source.CantidadStock
WHEN NOT MATCHED THEN
    INSERT (CervezaID, CantidadStock)
    VALUES (source.CervezaID, source.CantidadStock);

-- Insertar datos en la tabla Ventas
MERGE INTO Ventas AS target
USING (VALUES
    (1, '2024-01-10', 1, 10, 59.90),
    (2, '2024-01-11', 2, 6, 47.94),
    (3, '2024-01-12', 3, 8, 51.92),
    (4, '2024-01-13', 4, 4, 27.16),
    (5, '2024-01-14', 5, 7, 38.43)
) AS source (VentaID, FechaVenta, CervezaID, Cantidad, PrecioTotal)
ON target.VentaID = source.VentaID
WHEN MATCHED THEN
    UPDATE SET FechaVenta = source.FechaVenta, CervezaID = source.CervezaID,
               Cantidad = source.Cantidad, PrecioTotal = source.PrecioTotal
WHEN NOT MATCHED THEN
    INSERT (VentaID, FechaVenta, CervezaID, Cantidad, PrecioTotal)
    VALUES (source.VentaID, source.FechaVenta, source.CervezaID, source.Cantidad, source.PrecioTotal);

-- Insertar datos en la tabla Clientes
MERGE INTO Clientes AS target
USING (VALUES
    (1, 'Juan Perez', 'juan@example.com', '123-456-7890'),
    (2, 'Maria Rodriguez', 'maria@example.com', '987-654-3210')
) AS source (ClienteID, Nombre, Email, Telefono)
ON target.ClienteID = source.ClienteID
WHEN MATCHED THEN
    UPDATE SET Nombre = source.Nombre, Email = source.Email, Telefono = source.Telefono
WHEN NOT MATCHED THEN
    INSERT (ClienteID, Nombre, Email, Telefono)
    VALUES (source.ClienteID, source.Nombre, source.Email, source.Telefono);
