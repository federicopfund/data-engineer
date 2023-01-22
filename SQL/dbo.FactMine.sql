CREATE TABLE [dbo].[FactMine] (
    [TruckID]       INT      NOT NULL,
    [ProjectID]     INT      NOT NULL,
    [OperatorID]    INT      NOT NULL,
    [TotalOreMined] MONEY    NOT NULL,
    [TotalWasted]   MONEY    NOT NULL,
    [Date]          DATETIME NULL
);

