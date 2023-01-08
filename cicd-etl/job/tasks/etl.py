from pyspark.sql.types import IntegerType,DecimalType
import pyspark.sql.functions as function
from pyspark.sql import SparkSession
from session import logger
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
# nombre del contenedor del Blob storage donde se encuentren los csv
blob_container = 'csv'

def main(spark,patterns) -> None:
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
                if sys.argv == 0:
                    filePaths = "wasbs://" + blob_container \
                                             + "@" + storage_account_name \
                                             + f".blob.core.windows.net/{Categoria.search(Iter).group()}"
                else:
                    filePaths = f'opt/spark/spark-warehouse/data/csv/{Categoria.search(Iter).group()}'
                    continue                 
                 # Spark DataFrame Infiriendo el esquema y especificando que el archivo contiene encavezado,
                df_Categoria = (spark
                                    .read
                                        .format("csv")
                                            .option("header","true")
                                            .option("inferSchema","true")
                                                .load(filePaths,inferSchema = True, \
                                                    header = True, encoding="utf-8"))               
                # tranformacion 1
                CategoriaRename = (df_Categoria.withColumnRenamed('Categoria','Nombre_Categoria'))
                # Crea tabla Temporal
                CategoriaRename.createOrReplaceTempView("CategoriaRename")
                # Query
                CategoriaRenameTemporal = spark.sql("select Nombre_Categoria")
                # Visualiza
                CategoriaRenameTemporal.show()
                
                # Construimos la URL con el Nombre de la Transformacion Especifica.
                filePathDataLake=f'abfs://{datalake_container}@{datalake_storage_name}.\
                                                                dfs.core.windows.net/CategoriaRename.csv'
                # Tranforma DataFrame Spark a Dataframe Pandas luego a csv.
                #  Escribe en el contenedor de un data lake.                
                """(CategoriaRename
                            .toPandas()
                                    .to_csv(filePathDataLake,\
                                        storage_options = {'account_key':\
                                             datalake_account_access_key} ,index=False))"""
                # Retornamos el DataFrame para posteriones usos
                return CategoriaRename         
                                                         # Transformacion | 2 |
            case FactMine.match(Iter).group():
                if sys.argv == 0:
                    filePaths = "wasbs://" + blob_container \
                                             + "@" + storage_account_name \
                                             + f".blob.core.windows.net/{FactMine.search(Iter).group()}"
                else:
                    filePaths = f'opt/spark/spark-warehouse/data/csv/{FactMine.search(Iter).group()}'
                    continue                 
              
                # Spark DataFrame Infiriendo el esquema y especificando que el archivo contiene encavezado.
                df_FactMine = (spark
                                    .read
                                        .format("csv")
                                            .option("header","true")
                                            .option("inferSchema","true")
                                                .load(filePaths,inferSchema = True, \
                                                                header = True, encoding="utf-8"))
                
                SumTotalOreMined = (df_FactMine.agg(function.round(function.sum("TotalOreMined"),4)
                                                                            .alias("Suma_TotalOreMined")))
                
                 # Crea tabla Temporal
                SumTotalOreMined.createOrReplaceTempView("SumTotalOreMinedTemporal")
                # Query
                SumTotalOreMinedTemporalQuery = spark.sql("select SumTotalOreMinedTemporal")
                # Visualiza
                SumTotalOreMinedTemporalQuery.show()
                 # Construimos la URL con el Nombre de la Transformacion Especifica.
                filePathDataLake=f'abfs://{datalake_container}@{datalake_storage_name}.\
                                                                dfs.core.windows.net/SumTotalOreMined.csv'
                # Tranforma DataFrame Spark a Dataframe Pandas.
                # luego a csv y escribe en el contenedor de un data lake.
                """(SumTotalOreMined
                            .toPandas()
                                    .to_csv(filePathDataLake,\
                                        storage_options = {'account_key': datalake_account_access_key} \
                                        ,index=False))"""
                

                # Retornamos el data frama para posteriones usos
                return SumTotalOreMined
                                                        # Transformaciones | 3 | 4 |    
            case Mine.match(Iter).group():
                if sys.argv == 0:
                    filePaths = "wasbs://" + blob_container \
                                             + "@" + storage_account_name \
                                             + f".blob.core.windows.net/{Mine.search(Iter).group()}"
                else:
                    filePaths = f'opt/spark/spark-warehouse/data/csv/{Mine.search(Iter).group()}'
                    continue                                      
                
                df_Mine = (spark
                            .read
                                .format("csv")
                                    .option("header","true")
                                    .option("inferSchema","true")
                                        .load(filePaths,inferSchema = True, header = True, \
                                                                                    encoding="utf-8"))
                 
                 # Construimos la URL con el Nombre de la Transformacion Especifica.
                
                SelectedColumns = (df_Mine.select("Country","FirstName","LastName","Age"))
                
                # Crea tabla Temporal
                SelectedColumns.createOrReplaceTempView("SelectedColumnsTemporal")
                # Query
                SelectedColumnsTemporalQuery = spark.sql("select SelectedColumnsTemporal")
                # Visualiza
                SelectedColumnsTemporalQuery.show()
                 # Construimos la URL con el Nombre de la Transformacion Especifica.
                filePathDataLake=f'abfs://{datalake_container}@{datalake_storage_name}.\
                                                            dfs.core.windows.net/SelectedColumns.csv'
                # Tranforma DataFrame Spark a Dataframe Pandas luego a csv.
                # Luego escribe en el contenedor de un data lake.
                """SelectedColumns
                            .toPandas()
                                    .to_csv(filePathDataLake,\
                                        storage_options = {'account_key': datalake_account_access_key}\
                                         ,index=False)"""
                
                SumTotalWastedByCountry = (df_Mine
                                                .groupBy("Country")
                                                    .agg(function.round(function.sum("TotalWasted"),4)
                                                        .alias("Suma_TotalWasted")))
                 # Crea tabla Temporal
                SumTotalWastedByCountry.createOrReplaceTempView("SumTotalWastedByCountryTemporal")
                # Query
                SumTotalWastedByCountryQuery = spark.sql("select SumTotalWastedByCountryTemporal")
                # Visualiza
                SumTotalWastedByCountryQuery.show()  
              
                 # Construimos la URL con el Nombre de la Transformacion Especifica.
                filePathDataLake=f'abfs://{datalake_container}@{datalake_storage_name}.\
                                                        dfs.core.windows.net/SumTotalWastedByCountry.csv'
                
                # Tranforma DataFrame Spark a Dataframe Pandas luego a csv.
                #  Escribe en el contenedor de un data lake.
                """(SumTotalWastedByCountry
                                     .toPandas()
                                        .to_csv(filePathDataLake,\
                                            storage_options = {'account_key': datalake_account_access_key} \
                                            ,index=False))"""
                
                return SelectedColumns, SumTotalWastedByCountry
                                                    
                                                       # Transformacion | 5 |
            case Productos.match(Iter).group():
                if sys.argv == 0:
                    filePaths = "wasbs://" + blob_container \
                                             + "@" + storage_account_name \
                                             + f".blob.core.windows.net/{Productos.search(Iter).group()}"
                else:
                    filePaths = f'opt/spark/spark-warehouse/data/csv/{Productos.search(Iter).group()}'
                    continue                                      
                
                df_Productos = (spark
                                    .read
                                        .format("csv")
                                            .option("header","true")
                                            .option("inferSchema","true")
                                                .load(filePaths,inferSchema = True, \
                                                    header = True, encoding="utf-8"))
                
                ProductCount = (df_Productos.agg(function.count("Cod_Producto").alias("Cantidad_CodProducto")))
                  # Construimos la URL con el Nombre de la Transformacion Especifica.
                 # Crea tabla Temporal
                ProductCount.createOrReplaceTempView("ProductCountTemporal")
                # Query
                ProductCountTemporalQuery = spark.sql("select ProductCountTemporal")
                # Visualiza
                ProductCountTemporalQuery.show()  
              
                filePathDataLake=f'abfs://{datalake_container}@{datalake_storage_name}.\
                                                        dfs.core.windows.net/ProductCount.csv'
                # Tranforma DataFrame Spark a Dataframe Pandas luego a csv.
                # Escribe en el contenedor de un data lake.
                """ProductCount
                            .toPandas()
                                .to_csv(filePathDataLake,\
                                            storage_options = {'account_key': datalake_account_access_key}\ 
                                            ,index=False)"""
                
                ProductosCount_Cast = (ProductCount
                                            .withColumn("Cantidad_CodProducto" ,function.col("Cantidad_CodProducto")
                                            .cast(IntegerType())))
                
                filePathDataLake=f'abfs://{datalake_container}@{datalake_storage_name}.\
                                                                    dfs.core.windows.net/ProductosCount_Cast.csv'
                # Tranforma DataFrame Spark a Dataframe Pandas luego a csv.
                # y escribe en el contenedor de un data lake.
                """ProductosCount_Cast
                                .toPandas()
                                    .to_csv(filePathDataLake,\
                                                storage_options = {'account_key': datalake_account_access_key}\
                                                 ,index=False)"""
                   # Crea tabla Temporal
                ProductProductosCount_Cast.createOrReplaceTempView("ProductosCount_CastTemporal")
                # Query
                ProductosCount_CastTemporalQuery = spark.sql("select ProductosCount_CastTemporal")
                # Visualiza
                ProductCountTemporalQuery.show()  

                return ProductCount, ProductosCount_Cast
                                                            # Transformaciones 6 | 7 | 8 | 9
            
            case VentasInternet.match(Iter).group():
                 if sys.argv == 0:
                    filePaths = "wasbs://" + blob_container \
                                             + "@" + storage_account_name \
                                             + f".blob.core.windows.net/{VentasInternet.search(Iter).group()}"
                else:
                    filePaths = f'opt/spark/spark-warehouse/data/csv/{VentasInternet.search(Iter).group()}'
                    continue                       
             
                df_VentasInternet = (spark
                                        .read
                                            .format("csv")
                                                .option("header","true")
                                                .option("inferSchema","true")
                                                    .load(filePaths,inferSchema = True, header = True,\
                                                    encoding="utf-8"))
                
                TableSortedByDescCode = (df_VentasInternet.sort(function.col("Cod_Producto").desc()))
                 # Crea tabla Temporal
                TableSortedByDescCode.createOrReplaceTempView("TableSortedByDescCodeTemporal")
                # Query
                TableSortedByDescCodeTemporalQuery = spark.sql("select TableSortedByDescCodeTemporal")
                # Visualiza
                TableSortedByDescCodeTemporalQuery.show() 
                  # Construimos la URL con el Nombre de la Transformacion Especifica.
                filePathDataLake=f'abfs://{datalake_container}@{datalake_storage_name}\
                                                            .dfs.core.windows.net/TableSortedByDescCode.csv'
                # Tranforma DataFrame Spark a Dataframe Pandas luego a csv.
                # y escribe en el contenedor de un data lake
                """TableSortedByDescCode
                                .toPandas()
                                    .to_csv(filePathDataLake,\
                                            storage_options = {'account_key': datalake_account_access_key} 
                                            ,index=False)"""

                SubcategoriaFiltered = (TableSortedByDescCode.filter(TableSortedByDescCode['Cod_Categoria'] == 3))
                # Crea tabla Temporal
                SubcategoriaFiltered.createOrReplaceTempView("SubcategoriaFilteredTemporal")
                # Query
                SubcategoriaFilteredTemporalQuery = spark.sql("select SubcategoriaFilteredTemporal")
                # Visualiza
                SubcategoriaFilteredTemporal.show() 

                
                 # Construimos la URL con el Nombre de la Transformacion Especifica.
                filePathDataLake=f'abfs://{datalake_container}@{datalake_storage_name}.\
                                                            dfs.core.windows.net/SubcategoriaFiltered.csv'
                # Tranforma DataFrame Spark a Dataframe Pandas luego a csv y escribe en el contenedor de un data lake
                """SubcategoriaFiltered
                                .toPandas()
                                    .to_csv(filePathDataLake,\
                                            storage_options = {'account_key': datalake_account_access_key} 
                                            ,index=False)"""
                
                VentasWithNetIncome = (df_VentasInternet
                                                    .withColumn("Ingresos_Netos", function
                                                        .round(function.col("Cantidad")*function
                                                            .col("PrecioUnitario")-function
                                                                .col("CostoUnitario"),4)
                                                                    .cast(DecimalType(10,4))))
                  # Crea tabla Temporal
                VentasWithNetIncome.createOrReplaceTempView("VentasWithNetIncomeTemporal")
                # Query
                VentasWithNetIncomeTemporalQuery = spark.sql("select VentasWithNetIncomeTemporal")
                # Visualiza
                VentasWithNetIncomeTemporalQuery.show() 
                
                # Construimos la URL con el Nombre de la Transformacion Especifica, para mayor interpretacion de tablas
                filePathDataLake=f'abfs://{datalake_container}@{datalake_storage_name}.\
                                                            dfs.core.windows.net/VentasWithNetIncome.csv'
                # Tranforma DataFrame Spark a Dataframe Pandas luego a csv y escribe en el contenedor de un data lake
                """VentasWithNetIncome
                                .toPandas()
                                    .to_csv(filePathDataLake,\
                                            storage_options = {'account_key': datalake_account_access_key} \
                                            ,index=False)"""

                IngresosPorCodProducto = (VentasWithNetIncome
                                            .groupBy(function
                                                .col("Cod_Producto"))
                                                    .agg(function.round(function
                                                        .avg("Ingresos_Netos"),4)
                                                            .alias("Ingreso_Neto_Promedio"), function
                                                                .round(function.sum("Ingresos_Netos"),4)
                                                                .alias("Suma_Ingresos_Netos")))
                   # Crea tabla Temporal
                IngresosPorCodProducto.createOrReplaceTempView("IngresosPorCodProductoTemporal")
                # Query
                IngresosPorCodProductoTemporalQuery = spark.sql("select IngresosPorCodProductoTemporal")
                # Visualiza
                IngresosPorCodProductoTemporalQuery.show() 
                 # Construimos la URL con el Nombre de la Transformacion Especifica.
                filePathDataLake=f'abfs://{datalake_container}@{datalake_storage_name}.\
                                                                dfs.core.windows.net/IngresosPorCodProducto.csv'
                # Tranforma DataFrame Spark a Dataframe Pandas luego a csv 
                # y escribe en el contenedor de un data lake
                """IngresosPorCodProducto
                                .toPandas()
                                    .to_csv(filePathDataLake,\
                                            storage_options = {'account_key': datalake_account_access_key} 
                                            ,index=False)"""
            
                return TableSortedByDescCode, SubcategoriaFiltered, VentasWithNetIncome, IngresosPorCodProducto
            
            case _:
                raise ValueError("No se encuenta el Arcvhivo")
      return None

if __name__ == "__main__":
#Cree una SparkSession utilizando las API SparkSession.
    #Si no existe entonces cree una instancia.
    # Solo puede ser una Intancia por JVM.
    spark = SparkSession.builder .master("local[3]").appName("etl").getOrCreate()
    if len(patterns) == 0:
        patterns = sys.argv     
        logger = Log4j(spark)
        main(spark,patterns)                                       
        spark.stop()                                              
    else:
        patterns = dbutils.widgets.get('parametro_direcciones')
        logger = Log4j(spark)
        main(spark,patterns)                                       
        spark.stop()  
        
      

         





