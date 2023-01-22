
CREATE TABLE [dbo].[VentasInternet] (
    [Cod_Producto]     VARCHAR (50) COLLATE Modern_Spanish_CI_AS NULL,
    [Cod_Cliente]      VARCHAR (50) COLLATE Modern_Spanish_CI_AS NULL,
    [Cod_Territorio]   VARCHAR (50) COLLATE Modern_Spanish_CI_AS NULL,
    [NumeroOrden]      INT COLLATE Modern_Spanish_CI_AS NULL,
    [Cantidad]         INT COLLATE Modern_Spanish_CI_AS NULL,
    [PrecioUnitario]   MONEY COLLATE Modern_Spanish_CI_AS NULL,
    [CostoUnitario]    MONEY COLLATE Modern_Spanish_CI_AS NULL,
    [Impuesto]         MONEY COLLATE Modern_Spanish_CI_AS NULL,
    [Flete]            REAL COLLATE Modern_Spanish_CI_AS NULL,
    [FechaOrden]       DATETIMEOFFSET COLLATE Modern_Spanish_CI_AS NULL,
    [FechaEnvio]       DATETIMEOFFSET COLLATE Modern_Spanish_CI_AS NULL,
    [FechaVencimiento] DATETIMEOFFSET COLLATE Modern_Spanish_CI_AS NULL,
    [Cod_Promocion]    VARCHAR (50) COLLATE Modern_Spanish_CI_AS NULL
);

