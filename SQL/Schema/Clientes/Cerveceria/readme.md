>Cervezas:

    CervezaID: Identificador único de la cerveza (clave primaria).

    EstiloID: Clave foránea que referencia el ID del estilo de cerveza.

    Nombre: Nombre de la cerveza.

    GraduacionAlcoholica: Graduación alcohólica de la cerveza.

    VolumenLitros: Volumen de la cerveza en litros.

    Precio: Precio de la cerveza.

>Ingredientes:

    IngredienteID: Identificador único del ingrediente (clave primaria).

    Nombre: Nombre del ingrediente.

    Tipo: Tipo de ingrediente.
    
    Origen: Origen del ingrediente.
    
    Descripcion: Descripción del ingrediente.
    
    FechaIngreso: Fecha de ingreso del ingrediente.
    
    Proveedor: Proveedor del ingrediente.
    
    PrecioUnitario: Precio unitario del ingrediente.
    
    EstiloID: Clave foránea que referencia el ID del estilo de cerveza al que pertenece el ingrediente.

>EstilosCerveza:

    EstiloID: Identificador único del estilo de cerveza (clave primaria).
    
    Nombre: Nombre del estilo de cerveza.

    Descripcion: Descripción del estilo.
    
    IBU: Unidades Internacionales de Amargor.
    
    SRM: Índice de Color (Standard Reference Method).
    
    RangoAlcohol: Rango de graduación alcohólica.
    
    Comentarios: Comentarios adicionales sobre el estilo.

>ProduccionCerveza:

    ProduccionID: Identificador único de la producción de cerveza (clave primaria).

    CervezaID: Clave foránea que referencia el ID de la cerveza producida.

    FechaProduccion: Fecha de producción.

    CantidadProducida: Cantidad de cerveza producida.

    Estado: Estado de la producción (por ejemplo, "En proceso", "Listo para embotellar").

>PasosProduccion:

    PasoID: Identificador único del paso de producción (clave primaria).

    ProduccionID: Clave foránea que referencia el ID de la producción de cerveza a la que pertenece el paso.

    Descripcion: Descripción del paso de producción.
    
    FechaPaso: Fecha en que se realizó el paso.

>InventarioCervezas:

    CervezaID: Identificador único de la cerveza en el inventario (clave primaria).

    CantidadStock: Cantidad en stock de la cerveza.

>Orden:

    VentaID: Identificador único de la venta (clave primaria).
    
    FechaVenta: Fecha de la venta.
    
    CervezaID: Clave foránea que referencia el ID de la cerveza vendida.
    
    Cantidad: Cantidad de cerveza vendida.
    
    PrecioTotal: Precio total de la venta.
    
    ClienteID: Clave foránea que referencia el ID del cliente que realizó la compra.
    
>Clientes:

    ClienteID: Identificador único del cliente (clave primaria).

    Nombre: Nombre del cliente.

    Email: Dirección de correo electrónico del cliente.

    Telefono: Número de teléfono del cliente.

    Direccion: Dirección del cliente.

    Ciudad: Ciudad del cliente.

    Pais: País del cliente.

    CodigoPostal: Código postal del cliente.

>Subcursales:

    SubcursalID: Identificador único de la subcursal (clave primaria).

    Nombre: Nombre de la subcursal.
    
    Direccion: Dirección de la subcursal.
    
    Ciudad: Ciudad de la subcursal.
    
    Pais: País de la subcursal.
    
    CodigoPostal: Código postal de la subcursal.

>InventarioSubcursal:

    SubcursalID: Clave foránea que referencia el ID de la subcursal.

    CervezaID: Clave foránea que referencia el ID de la cerveza en el inventario de la subcursal.

    CantidadStock: Cantidad en stock de la cerveza en la subcursal.

>EntregasSubcursales:

    EntregaID: Identificador único de la entrega a subcursal (clave primaria).

    FechaEntrega: Fecha de la entrega.

    SubcursalDestinoID: Clave foránea que referencia el ID de la subcursal de destino.

    CervezaID: Clave foránea que referencia el ID de la cerveza entregada.

    CantidadEntregada: Cantidad de cerveza entregada.
    
    PrecioTotalEntrega: Precio total de la entrega.

>ProveedoresSubcursales:
    
    SubcursalID: Clave foránea que referencia el ID de la subcursal.

    ProveedorID: Clave foránea que referencia el ID del proveedor.
    
>Proveedores:

    ProveedorID: Identificador único del proveedor (clave primaria).

    Nombre: Nombre del proveedor.

    Contacto: Persona de contacto en el proveedor.

    Telefono: Número de teléfono del proveedor.
    
    Email: Dirección de correo electrónico del proveedor.