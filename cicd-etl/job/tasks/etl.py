from pyspark.sql.types import IntegerType,DecimalType
import pyspark.sql.functions as function
from pyspark.sql import SparkSession
from collections import deque
import pandas as pd
import sys
import re

# Configuración del acceso a la storage account donde se encuentran los archivos CSV

storage_account_name = 'storagebasedatos2510'
storage_account_access_key = 'A2unit3rNXeeU445/ZoKWxti8RhVEH+RiRk4AXfiJHwHrbO1rGB4U0eWpedsV7mPyyIZqHvEXE2f+AStgBgCZw=='
spark.conf.set('fs.azure.account.key.' + storage_account_name + '.blob.core.windows.net', storage_account_access_key)
datalake_container = 'output'
datalake_storage_name = 'storagedatalake2510'
datalake_account_access_key = '2P0PSy5tfLMxuSwmFGk5ibSVXvRVaK7gWyn2bxD+fABrMfwlRejLOvxq2rpGtpZnPnSzQiC5mlHH+AStWVsSjA=='
# String de direcciones que vienen del Pipeline DataFactory
patterns = dbutils.widgets.get('parametro_direcciones')
# nombre del contenedor del Blob storage donde se encuentren los csv
blob_container = 'csv'

def main(Spark,patterns) -> None:
    '''Main ETL Script.
        Input : param spark :> Spark instancia.
        Output: return      :> None.
    '''
    transform = deque() # srendimiento O(1) en cualquier dirección. en el medio se relentiza. sacar de los extremos.
    FactMine       = re.compile(r'\bFactMine.csv\b')
    Categoria      = re.compile(r'\bCategoria.csv\b')
    Mine           = re.compile(r'\bMine.csv\b')
    Productos      = re.compile(r'\bProductos.csv\b')
    VentasInternet = re.compile(r'\bVentasInternet.csv\b')
    
    for Iter in patterns.split(","):
        match Iter:                                                          # Transformacion  | 1 |
            case Categoria.match(Iter).group():
                filePathstorage = "wasbs://" + blob_container \
                                             + "@" + storage_account_name \
                                             + f".blob.core.windows.net/{Categoria.search(Iter).group()}"
              # Spark DataFrame usando CSV Infiriendo el esquema y especificando que el archivo contiene encavezado,
                df_Categoria = (spark
                                    .read
                                        .format("csv")
                                            .option("header","true")
                                            .option("inferSchema","true")
                                                .load(filePathstorage,inferSchema = True, header = True, encoding="utf-8"))               
                
                CategoriaRename = (df_Categoria.withColumnRenamed('Categoria','Nombre_Categoria'))
                transform.append(CategoriaRename)
                return CategoriaRename         
                                                                             # Transformacion | 2 |
            case FactMine.match(Iter).group():
                filePathstorage = "wasbs://" + blob_container \
                                             + "@" + storage_account_name \
                                             + f".blob.core.windows.net/{FactMine.search(Iter).group()}"
                df_FactMine = (spark
                                    .read
                                        .format("csv")
                                            .option("header","true")
                                            .option("inferSchema","true")
                                                .load(filePathstorage,inferSchema = True, header = True, encoding="utf-8"))
                
                SumTotalOreMined = (df_FactMine.agg(function.round(function.sum("TotalOreMined"),4)
                                                                            .alias("Suma_TotalOreMined")))
                
                transform.append(SumTotalOreMined)
                
                return SumTotalOreMined
                                                                              # Transformaciones | 3 | 4 |    
            case Mine.match(Iter).group():                                   
                filePathstorage = "wasbs://" + blob_container \
                                             + "@" + storage_account_name \
                                             + f".blob.core.windows.net/{Mine.search(Iter).group()}"
                df_Mine = (spark
                            .read
                                .format("csv")
                                    .option("header","true")
                                    .option("inferSchema","true")
                                        .load(filePathstorage,inferSchema = True, header = True, encoding="utf-8"))
               
                SelectedColumns = (df_Mine.select("Country","FirstName","LastName","Age"))
                
                SumTotalWastedByCountry = (df_Mine
                                                .groupBy("Country")
                                                .agg(function.round(function.sum("TotalWasted"),4)
                                                .alias("Suma_TotalWasted")))
                
                transform.extend(SelectedColumns)
                
                transform.append(SumTotalWastedByCountry)
                
                return SelectedColumns, SumTotalWastedByCountry
                                                                                # Transformacion | 5 |
            case Productos.match(Iter).group():                               
                filePathstorage = "wasbs://" + blob_container \
                                             + "@" + storage_account_name \
                                             + f".blob.core.windows.net/{Productos.search(Iter).group()}"
                df_Productos = (spark
                                    .read
                                        .format("csv")
                                            .option("header","true")
                                            .option("inferSchema","true")
                                                .load(filePathstorage,inferSchema = True, header = True, encoding="utf-8"))
                
                ProductCount = (df_Productos.agg(function.count("Cod_Producto").alias("Cantidad_CodProducto")))
                
                ProductosCount_Cast = (ProductCount
                                            .withColumn("Cantidad_CodProducto" ,function.col("Cantidad_CodProducto")
                                            .cast(IntegerType())))
                
                transform.append(ProductCount)
                transform.append(ProductosCount_Cast)
                return ProductCount, ProductosCount_Cast
                                                                                # Transformaciones 6 | 7 | 8 | 9
            case VentasInternet.match(Iter).group():                     
                filePathstorage = "wasbs://" + blob_container \
                                             + "@" + storage_account_name \
                                             + f".blob.core.windows.net/{VentasInternet.search(Iter).group()}"
                df_VentasInternet = (park
                                        .read
                                            .format("csv")
                                                .option("header","true")
                                                .option("inferSchema","true")
                                                    .load(filePathstorage,inferSchema = True, header = True,encoding="utf-8"))
                
                TableSortedByDescCode = (df_VentasInternet.sort(function.col("Cod_Producto").desc()))
                
                SubcategoriaFiltered = (TableSortedByDescCode
                                                    .filter(TableSortedByDescCode['Cod_Categoria'] == 3))
                
                VentasWithNetIncome = (df_VentasInternet
                                                    .withColumn("Ingresos_Netos", function
                                                    .round(function.col("Cantidad")*function
                                                    .col("PrecioUnitario")-function
                                                    .col("CostoUnitario"),4)
                                                    .cast(DecimalType(10,4))))
                
                IngresosPorCodProducto = (VentasWithNetIncome
                                            .groupBy(function
                                                .col("Cod_Producto"))
                                                    .agg(function.round(function
                                                        .avg("Ingresos_Netos"),4)
                                                            .alias("Ingreso_Neto_Promedio"), function
                                                                .round(function.sum("Ingresos_Netos"),4)
                                                                .alias("Suma_Ingresos_Netos")))
                transform.append(TableSortedByDescCode)
                transform.append(SubcategoriaFiltered)
                transform.append(ventasWithNetIncome)
                transform.append(ingresosPorCodProducto)
                return TableSortedByDescCode, SubcategoriaFiltered, VentasWithNetIncome, IngresosPorCodProducto

    # Carga de las tablas transformadas en formato CSV en el Azure Data Lake Storage   
    for i in range(len(transform)-1):
        transform[i]
            .toPandas()
                .to_csv(f'abfs://{datalake_container}@{datalake_storage_name}.dfs.core.windows.net/transformacion{i+1}.csv',\
                        storage_options = {'account_key': datalake_account_access_key} ,index=False)

    return None

if __name__ == "__main__":
    if len(sys.argv) !=2:
        print(f"Uso: count <file>",file=sys.stderr)
        sys.exit(-1)
        Spark = (SparkSession.builder.appName("etl").getOrCreate()) #Cree una SparkSession utilizando las API SparkSession.
        main(Spark,patterns)                                        #Si no existe entonces cree una instancia.
        Spark.stop()                                                # Solo puede ser una Intancia por JVM.
        
                                                               
        
      

         





