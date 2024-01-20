INSERT INTO Cerveza(CervezaID, Estilo, GraduacionAlcoholica, VolumenLitros, Precio, Descripcion, IBU, SRM)
VALUES 
(1, 'IPA', 6.5, 0.355, 7.99, 'Una IPA refrescante', 60, 10),
(2, 'Stout', 5.8, 0.473, 8.99, 'Cerveza oscura y tostada', 40, 30);

INSERT INTO Ingredientes(IngredienteID, TipoIngrediente, CantidadStok, CantUnidLitros, Origen, Descripcion, FechaIngreso, Proveedor, PrecioUnitario, CervezaID)
VALUES 
(1, 'L�pulo', 100, 0.5, 'EE. UU.', 'L�pulo arom�tico', '2023-01-15', 'ProveedorA', 5.99, 1),
(2, 'Malta', 200, 1.0, 'Canad�', 'Malta de cebada', '2023-02-20', 'ProveedorB', 3.99, 2);

-- ProduccionCerveza
INSERT INTO ProduccionCerveza (ProduccionID, CervezaID, FechaProduccion, CantidadProducida, Estado)
VALUES 
(1, 1, '2023-03-10', 100, 'En proceso'),
(2, 2, '2023-04-15', 80, 'Completada');

-- PasosProduccion
INSERT INTO PasosProduccion (PasoID, ProduccionID, Descripcion, FechaPaso)
VALUES 
(3, 1, 'Maceraci�n', '2023-03-10'),
(4, 1, 'Fermentaci�n', '2023-03-15');
-- Agrega m�s filas seg�n sea necesario

-- InventarioCervezas
INSERT INTO InventarioCervezas (CervezaID, CantidadStock)
VALUES 
(1, 100),
(2, 50);

-- Clientes
INSERT INTO Clientes (ClienteID, Nombre, Email, Telefono, Direccion, Ciudad, Pais, CodigoPostal)
VALUES 
(1, 'Juan Perez', 'juan@example.com', '123-456-7890', 'Calle Principal 123', 'Ciudad A', 'Pais A', '12345'),
(2, 'Ana Rodriguez', 'ana@example.com', '987-654-3210', 'Avenida Secundaria 456', 'Ciudad B', 'Pais B', '67890');
-- Agrega m�s filas seg�n sea necesario

-- Orden
INSERT INTO Orden (VentaID, FechaVenta, CervezaID, Cantidad, PrecioTotal, ClienteID)
VALUES 
(1, '2023-03-20', 1, 5, 39.95, 1),
(2, '2023-04-05', 2, 3, 26.97, 2);
-- Puedes agregar m�s filas seg�n sea necesario

-- Subcursales
INSERT INTO Subcursales (SubcursalID, Nombre, Direccion, Ciudad, Pais, CodigoPostal)
VALUES 
(1, 'Subcursal A', 'Avenida Principal 789', 'Ciudad C', 'Pais C', '54321'),
(2, 'Subcursal B', 'Calle Secundaria 012', 'Ciudad D', 'Pais D', '98765');
-- Agrega m�s filas seg�n sea necesario

-- InventarioSubcursal
INSERT INTO InventarioSubcursal (SubcursalID, CervezaID, CantidadStock)
VALUES 
(1, 1, 20),
(1, 2, 10),
(2, 1, 15);
-- Puedes agregar m�s filas seg�n sea necesario

-- EntregasSubcursales
INSERT INTO EntregasSubcursales (EntregaID, FechaEntrega, SubcursalDestinoID, CervezaID, CantidadEntregada, PrecioTotalEntrega)
VALUES 
(1, '2023-03-25', 1, 1, 10, 79.90),
(2, '2023-04-10', 2, 2, 5, 44.95);
-- Puedes agregar m�s filas seg�n sea necesario

-- Proveedores
INSERT INTO Proveedores (ProveedorID, Nombre, Contacto, Telefono, Email)
VALUES 
(1, 'Proveedor A', 'Contacto A', '111-222-3333', 'proveedorA@example.com'),
(2, 'Proveedor B', 'Contacto B', '444-555-6666', 'proveedorB@example.com');
-- Agrega m�s filas seg�n sea necesario

-- ProveedoresSubcursales
INSERT INTO ProveedoresSubcursales (SubcursalID, ProveedorID)
VALUES 
(1, 1),
(2, 2);
-- Puedes agregar m�s filas seg�n sea necesario







