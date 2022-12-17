CREATE TABLE [dbo].[Mine] (
    [TruckID]       INT           NOT NULL,
    [Truck]         VARCHAR (65)  NULL,
    [ProjectID]     INT           NOT NULL,
    [Country]       NVARCHAR (50) NOT NULL,
    [OperatorID]    INT           NOT NULL,
    [FirstName]     NVARCHAR (50) NULL,
    [LastName]      NVARCHAR (50) NULL,
    [Age]           INT           NULL,
    [TotalOreMined] MONEY         NOT NULL,
    [TotalWasted]   MONEY         NOT NULL,
    [Date]          DATETIME      NULL
);

