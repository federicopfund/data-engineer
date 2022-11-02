# Login
$username = 'marconcz@21.edu.ar'
$password = 'myPassword15247'
$SecurePassword = ConvertTo-SecureString $password -AsPlainText -Force
$credentials = New-Object System.Management.Automation.PSCredential($username, $SecurePassword)
Login-AzAccount -Credential $credentials
# Set variables with your own values
$ResourceGroup = Get-AzResourceGroup -Name "Rgmarconcz"
$StorageAccountName = 'stoaccgrupo1'
$StorageBlobName = 'sourcegrupo1'
#$resourceGroupName = 'Rgmarconcz'

# Name of the data factory must be globally unique
$dataFactoryName = "dfgrupo1siglo21$(Get-Random)" 
$dataFactoryNameLocation = "East US"

# Configuracion AzSQLServer
$azureSqlServer = "grouponesqlserver-$(Get-Random)"
$azureSqlServerUser = "sqlgrupo1"
$azureSqlServerUserPassword = "Passwordgrupo1!"
$location = "westus3"
$startIp = "0.0.0.0"
$endIp = "0.0.0.0"
# Obtengo la ip publica para agregar al firewall desde una Api
$myPublicIp = (Invoke-WebRequest -Uri "http://ipinfo.io/ip" -UseBasicParsing).content

$StorageAccount = "stoaccgrupo1"
$azureStorageAccountKey = "<Az.Storage account key>"

# No need to change values for these variables
$azureSqlDatabaseLinkedService = "AzSqlDdbbLinkedService-$(Get-Random)"
$azureSqlDataWarehouseLinkedService = "AzureSqlDataWarehouseLinkedService"
$azureStorageLinkedService = "AzureStorageLinkedService"
$azureSqlDatabaseDataset = "AzureSqlDatabaseDataset"
$azureSqlDataWarehouseDataset = "AzureSqlDataWarehouseDataset"
$IterateAndCopySQLTablesPipeline = "IterateAndCopySQLTables"
$pipelineGetTableListAndTriggerCopyData = "GetTableListAndTriggerCopyData"


# create a data factory
#$df = Set-AzDataFactory -ResourceGroupName $resourceGroupName -Location $dataFactoryNameLocation -Name $dataFactoryName

# creo un storage account
$StorageAccount = New-AzStorageAccount -ResourceGroupName $ResourceGroup.ResourceGroupName `
  -Name $StorageAccountName `
  -Location eastus2 `
  -SkuName Standard_RAGRS `
  -Kind StorageV2

$ContainerName = $StorageBlobName
New-AzStorageContainer -Name $ContainerName -Context $StorageAccount.context -Permission Blob

# subo el .bacpac al blob
$Blob1HT = @{
  File             = "$(Get-Location)\dbRetail.bacpac"
  Container        = $ContainerName
  Blob             = "dbRetail.bacpac"
  Context          = $StorageAccount.context
  StandardBlobTier = 'Hot'
}
Set-AzStorageBlobContent @Blob1HT

# creo un AzSQLServer
Write-host "Se esta creando un Azure SQL Server...Espere"
$server = New-AzSqlServer -ResourceGroupName $ResourceGroup.ResourceGroupName `
-ServerName $azureSqlServer `
-Location $location `
-SqlAdministratorCredentials $(New-Object -TypeName System.Management.Automation.PSCredential `
-ArgumentList $azureSqlServerUser, $(ConvertTo-SecureString -String $azureSqlServerUserPassword -AsPlainText -Force))
$server

# configuro firewall del servidor 
Write-host "Configurando firewall Azure SQL Server...Espere"
$serverFirewallRule = New-AzSqlServerFirewallRule -ResourceGroupName $ResourceGroup.ResourceGroupName `
-ServerName $azureSqlServer `
-FirewallRuleName "AllowedIPs" -StartIpAddress $startIp -EndIpAddress $endIp
$serverFirewallRule

Write-host "Configurando firewall para permitir todas las Ip de Azure...Espere"
$serverFirewallRule2 = New-AzSqlServerFirewallRule -ResourceGroupName $ResourceGroup.ResourceGroupName `
-ServerName $azureSqlServer -AllowAllAzureIPs
$serverFirewallRule2

Write-host "Configurando firewall para permitir mi Ip publica...Espere"
$serverFirewallRule = New-AzSqlServerFirewallRule -ResourceGroupName $ResourceGroup.ResourceGroupName `
-ServerName $azureSqlServer `
-FirewallRuleName "AllowMyPublicIP" -StartIpAddress $myPublicIP -EndIpAddress $myPublicIP
$serverFirewallRule


$serverName = $azureSqlServer
$databaseName = "groupOneSqlServerDatabase"

Write-host "Creando base de datos"
$database = New-AzSqlDatabase -ComputeGeneration Gen5 `
-DatabaseName $databaseName `
-Edition GeneralPurpose `
-ResourceGroupName $ResourceGroup.ResourceGroupName `
-ServerName $serverName `
-VCore 2
$database

Write-host "Importando BACPAC desde $StorageAccountName ..."
$importRequest = New-AzSqlDatabaseImport -ResourceGroupName $ResourceGroup.ResourceGroupName `
-ServerName $serverName -DatabaseName $databaseName `
-DatabaseMaxSizeBytes $database.MaxSizeBytes -StorageKeyType "StorageAccessKey" `
-StorageKey $(Get-AzStorageAccountKey -ResourceGroupName $ResourceGroup.ResourceGroupName -StorageAccountName $StorageAccountName).Value[0] `
-StorageUri "https://stoaccgrupo1.blob.core.windows.net/sourcegrupo1/dbRetail.bacpac" `
-Edition "Standard" -ServiceObjectiveName "P6" `
-AdministratorLogin $azureSqlServerUser `
-AdministratorLoginPassword $(ConvertTo-SecureString -String $azureSqlServerUserPassword -AsPlainText -Force)

$importStatus = Get-AzSqlDatabaseImportExportStatus -OperationStatusLink $importRequest.OperationStatusLink

[Console]::Write("Importando BACPAC..")
while ($importStatus.Status -eq "InProgress") {
    $importStatus = Get-AzSqlDatabaseImportExportStatus -OperationStatusLink $importRequest.OperationStatusLink
    [Console]::Write(".")
    Start-Sleep -s 10
}

[Console]::WriteLine("")
$importStatus


# creo un DF.V2
Write-host "Creando DataFactory V2..."
$df = Set-AzDataFactoryV2 -Location $location -Name $dataFactoryName -ResourceGroupName $ResourceGroup.ResourceGroupName

# creo un linked service para almacenar en un JSON
Write-host "Creando SQL DataBase Linked Service..."

$azureSQLDatabaseLinkedServiceDefinition = @"
{
    "name": "$azureSqlDatabaseLinkedService",
    "type": "Microsoft.DataFactory/factories/linkedservices",
    "properties": {
        "annotations": [],
        "type": "AzureSqlDatabase",
        "typeProperties": {
            "connectionString": "integrated security=False;encrypt=True;connection timeout=30;data source=$azureSqlServer.database.windows.net;initial catalog=$databaseName;user id=$azureSqlServerUser;password = $azureSqlServerUserPassword"
        }
    }
}
"@

# creo un archivo JSON con el SqlDatabase
$azureSQLDatabaseLinkedServiceDefinition | Out-File "$(Get-Location)\$azureSqlDatabaseLinkedService.json"
#$cred = New-AzDataFactoryV2LinkedServiceEncryptedCredential -DataFactoryName $dataFactoryName -ResourceGroupName $ResourceGroup.ResourceGroupName -IntegrationRuntimeName 'test-selfhost-ir' -DefinitionFile ".\azureSqlDatabaseLinkedService.json" > encryptedSQLServerLinkedService.json
# linkeo el SqlDatabase del JSON al DFV2
Write-host "Linkeando SQL DataBase Linked Service..."
Set-AzDataFactoryV2LinkedService -DataFactoryName $dataFactoryName -ResourceGroupName $ResourceGroup.ResourceGroupName -Name $azureSqlDatabaseLinkedService `
-File "$(Get-Location)\$azureSqlDatabaseLinkedService.json"

Read-Host -Prompt "Presione una tecla para cerrar..."