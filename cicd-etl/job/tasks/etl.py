from pyspark.sql.types import IntegerType,DecimalType
import pyspark.sql.functions as function
from pyspark.sql import SparkSession
from session.logger import Log4j
from collections import deque
#import pandas as pd
import sys
import re


def main(spark,patterns,storage_name,key_blobs,datalake_name,key_datalake):
    '''Main ETL Script.
        Input : param spark :> Spark instancia.
        Output: return      :> None.
    '''
   
    datalake_container = 'output'
    blob_container = 'csv'
    transform = deque()
    spark.conf.set('fs.azure.account.key.' + storage_name + '.blob.core.windows.net', key_blobs)
    for Iter in patterns:
        print(f'|--------------------------------------> Matcheando tablas:{Iter} <---------------------------------------|')
        match Iter:                                      
            case "Categoria.csv":                          # Transformacion   |1|
                print(f"|---------------------------> Comensaremos con etl en la tabla {Iter} <---------------------------|")
                if len(sys.argv) == 0:
                    filePaths = "wasbs://" + blob_container \
                                             + "@" + storage_name \
                                             + f".blob.core.windows.net/Categoria.csv"
                else:
                    filePaths = f'file:/opt/spark/spark-warehouse/csv/Categoria.csv' 
                    print("|----------------------------------> Crea DataFrame <-----------------------------------------|")
                    # Spark DataFrame Infiriendo el esquema y especificando que el archivo contiene encavezado,
                    df_Categoria = (spark
                                    .read
                                        .format("csv")
                                            .option("header","true")
                                            .option("inferSchema","true")
                                                .load(filePaths,inferSchema = True, \
                                                    header = True, encoding="utf-8"))   
                    df_Categoria.printSchema()            
                    print("|----------------------------------> Categoria <---------------------------------------------|")
                    # tranformacion 1
                    CategoriaRename = (df_Categoria.withColumnRenamed('Categoria','Nombre_Categoria'))
            
                    # Visualiza-
                    CategoriaRename.show()
                
                    # Construimos la URL con el Nombre de la Transformacion Especifica.
                    filePathDataLake=f'abfs://{datalake_container}@{datalake_name}.\
                                                                dfs.core.windows.net/CategoriaRename.csv'
                    # Tranforma DataFrame Spark a Dataframe Pandas luego a csv.
                    # Escribe en el contenedor de un data lake.                
                    """(CategoriaRename
                            .toPandas()
                                    .to_csv(filePathDataLake, storage_options = {'account_key': key_datalake} ,index=False))"""
                    transform.append(CategoriaRename)
                continue       
                                             # Transformacion | 2 |
            case "FactMine.csv":
                print(f"|----------------------> Comenzamos con el etl en la tabla:{Iter}<-----------------------------|")
                if len(sys.argv) == 0:
                    filePaths = "wasbs://" + blob_container \
                                             + "@" + storage_name \
                                             + f".blob.core.windows.net/FactMine.csv"
                else:
                    filePaths = f'file:/opt/spark/spark-warehouse/csv/FactMine.csv'
                                   
              
                    # Spark DataFrame Infiriendo el esquema y especificando que el archivo contiene encavezado.
                    df_FactMine = (spark
                                    .read
                                        .format("csv")
                                            .option("header","true")
                                            .option("inferSchema","true")
                                                .load(filePaths,inferSchema = True, \
                                                                header = True, encoding="utf-8"))
                    # Visualiza Schema:
                    df_FactMine.printSchema()

                    SumTotalOreMined = (df_FactMine.agg(function.round(function.sum("TotalOreMined"),4)
                                                                                       .alias("Suma_TotalOreMined")))
                    
                    # Visualiza display:
                    SumTotalOreMined.show()
                    # Crea tabla Temporal
                    df_FactMine.createOrReplaceTempView("SumTotalOreMinedTemporal")
                    # Query
                    SumTotalOreMinedTemporalQuery = spark.sql("select TruckID ,ProjectID, OperatorID \
                                                                                        from SumTotalOreMinedTemporal")
                    # Visualiza
                    SumTotalOreMined.show()
                    # Construimos la URL con el Nombre de la Transformacion Especifica.
                    filePathDataLake=f'abfs://{datalake_container}@{datalake_name}.\
                                                                dfs.core.windows.net/SumTotalOreMined.csv'
                    # Tranforma DataFrame Spark a Dataframe Pandas.
                    # luego a csv y escribe en el contenedor de un data lake.
                    """(SumTotalOreMined
                                .toPandas()
                                        .to_csv(filePathDataLake,\
                                            storage_options = {'account_key': key_datalake} \
                                            ,index=False))"""
                    transform.append(SumTotalOreMined)
                continue 
                                               # Transformaciones | 3 | 4 |    
            case "Mine.csv":
                print(f'|----------------> Comienzan las transformaciones en la tabla:{Iter}<----------------------|')
                if len(sys.argv) == 0:
                    filePaths = "wasbs://" + blob_container \
                                             + "@" + storage_name \
                                             + f".blob.core.windows.net/Mine.csv"
                else:
                    filePaths = f'file:/opt/spark/spark-warehouse/csv/Mine.csv'
                    df_Mine = (spark
                                    .read
                                        .format("csv")
                                            .option("header","true")
                                            .option("inferSchema","true")
                                                .load(filePaths,inferSchema = True, header = True, \
                                                                                     encoding="utf-8"))
                    # Visualizamos Schema del DataFrame
                    df_Mine.printSchema()
                    
                    # Query
                    print("|---------------------------------> Query Select a Mine <-------------------------------|")
                    SelectedColumns = (df_Mine.select("Country","FirstName","LastName","Age"))
                    # Visualizamos Schema del DataFrame
                    SelectedColumns.show()
                    # Crea tabla Temporal
                    SelectedColumns.createOrReplaceTempView("SelectedColumnsTemporal")
                    # Query
                    SelectedColumnsTemporalQuery = spark.sql("select Country, FirstName,Age from SelectedColumnsTemporal")
                    # Visualiza
                    SelectedColumnsTemporalQuery.show()
                    # Construimos la URL con el Nombre de la Transformacion Especifica.
                    filePathDataLake=f'abfs://{datalake_container}@{datalake_name}.\
                                                            dfs.core.windows.net/SelectedColumns.csv'
                    # Tranforma DataFrame Spark a Dataframe Pandas luego a csv.
                    # Luego escribe en el contenedor de un data lake.
                    """SelectedColumns
                                .toPandas()
                                        .to_csv(filePathDataLake,\
                                            storage_options = {'account_key': key_datalake}\
                                            ,index=False)"""
                    transform.append(SelectedColumns)
                    print(f"|------------- ---------> Dataframe SumTotalWastedByCountry <--------------------------|")
                    SumTotalWastedByCountry = (df_Mine
                                                .groupBy("Country")
                                                    .agg(function.round(function.sum("TotalWasted"),4)
                                                        .alias("Suma_TotalWasted")))
                     
                    transform.append(SumTotalWastedByCountry)
                     # Visualizamos Schema del DataFrame
                    SumTotalWastedByCountry.printSchema()
                    print("|----------------------------------> View <-------------------------------------------|")
                    # Crea tabla Temporal
                    SumTotalWastedByCountry.createOrReplaceTempView("SumTotalWastedByCountryTemporal")
                    # Query
                    SumTotalWastedByCountryQuery = spark.sql("select Country from SumTotalWastedByCountryTemporal")
                    # Visualiza
                    SumTotalWastedByCountryQuery.show()  
                
                    # Construimos la URL con el Nombre de la Transformacion Especifica.
                    filePathDataLake=f'abfs://{datalake_container}@{datalake_name}.\
                                                            dfs.core.windows.net/SumTotalWastedByCountry.csv'
                        
                    # Tranforma DataFrame Spark a Dataframe Pandas luego a csv.
                    # Escribe en el contenedor de un data lake.
                    """(SumTotalWastedByCountry
                                        .toPandas()
                                            .to_csv(filePathDataLake,\
                                                storage_options = {'account_key': key_datalake} \
                                                ,index=False))"""
                continue 
                                                    
                                                    # Transformacion | 5 |
            case "Producto.csv":
                print(f"|------------------> Comienzan las tranformaciones en la tabla:{Iter} <-------------------|")
                if len(sys.argv) == 0:
                    filePaths = "wasbs://" + blob_container \
                                             + "@" + storage_name \
                                             + f".blob.core.windows.net/Producto.csv"
                else:
                    filePaths = f'file:/opt/spark/spark-warehouse/csv/Producto.csv'
                    df_Productos = (spark
                                        .read
                                            .format("csv")
                                                .option("header","true")
                                                .option("inferSchema","true")
                                                    .load(filePaths,inferSchema = True, \
                                                        header = True, encoding="utf-8"))
                    # Visualizamos Schema del DataFrame Producto
                    df_Productos.printSchema()
                    # Query al Schema df_Productos
                    ProductCount = (df_Productos.agg(function.count("Cod_Producto").alias("Cantidad_CodProducto")))
                    # Visualizamos Schema del DataFrame ProductoCount
                    ProductCount.show()
                    print("|----------------------------------> View <-------------------------------------------|")
                    # Crea tabla Temporal
                    ProductCount.createOrReplaceTempView("ProductCountTemporal")
                    # Query
                    ProductCountTemporalQuery = spark.sql("select * from ProductCountTemporal")
                 
                    # Visualiza 
                    ProductCountTemporalQuery.show()  
              
                    filePathDataLake=f'abfs://{datalake_container}@{datalake_name}.\
                                                        dfs.core.windows.net/ProductCount.csv'
                    # Tranforma DataFrame Spark a Dataframe Pandas luego a csv.
                    # Escribe en el contenedor de un data lake.
                    """ProductCount
                            .toPandas()
                                .to_csv(filePathDataLake,\
                                            storage_options = {'account_key': key_datalake}\ 
                                            ,index=False)"""
                
                    ProductosCount_Cast = (ProductCount
                                                .withColumn("Cantidad_CodProducto" \
                                                ,function.col("Cantidad_CodProducto")
                                                 .cast(IntegerType())))
                    transform.append(ProductosCount_Cast)
                    # Visualizamos el Schema.
                    ProductosCount_Cast.printSchema()

                    filePathDataLake=f'abfs://{datalake_container}@{datalake_name}.\
                                                                    dfs.core.windows.net/ProductosCount_Cast.csv'
                    # Tranforma DataFrame Spark a Dataframe Pandas luego a csv.
                    # y escribe en el contenedor de un data lake.
                    """ProductosCount_Cast
                                    .toPandas()
                                        .to_csv(filePathDataLake,\
                                                storage_options = {'account_key': key_datalake}\
                                                 ,index=False)"""
                    
                continue
                                               # Transformaciones 6 | 7 | 8 | 9
            
            case "VentasInternet.csv":
                print(f"|------------->Comienzan las Tranformaciones en la tabla: {Iter}<----------------------|")
                if len(sys.argv) == 0:
                    filePaths = "wasbs://" + blob_container \
                                             + "@" + storage_name \
                                             + f".blob.core.windows.net/VentasInternet.csv"
                
                else:
                    filePaths = f'file:/opt/spark/spark-warehouse/csv/VentasInternet.csv'
                                           
                    # DataFrame df_VentasInternet
                    df_VentasInternet = (spark
                                            .read
                                            .format("csv")
                                                .option("header","true")
                                                .option("inferSchema","true")
                                                    .load(filePaths,inferSchema = True, header = True,\
                                                                                        encoding="utf-8"))
                    print("|--------------------->   Schema de Ventas Internet <------------------------------|")
                    # Visualizamos Schema
                    df_VentasInternet.printSchema()
                    
                    TableSortedByDescCode = (df_VentasInternet.sort(function.col("Cod_Producto").desc()))
                    # Visualizamos la tabla.
                    transform.append(TableSortedByDescCode)
                    print("|-------------------->Visualizamos tabla TableSortedByDescCode<--------------------|")
                    TableSortedByDescCode.show()
                    # Crea tabla Temporal
                    TableSortedByDescCode.createOrReplaceTempView("TableSortedByDescCodeTemporal")
                    # Query
                    TableSortedByDescCodeTemporalQuery = spark.sql("select Cod_Territorio,Cod_Cliente,Cod_Producto \
                                                                                    from TableSortedByDescCodeTemporal")
                    # Visualiza
                    TableSortedByDescCodeTemporalQuery.show() 
                    # Construimos la URL con el Nombre de la Transformacion Especifica.
                    filePathDataLake=f'abfs://{datalake_container}@{datalake_name}\
                                                            .dfs.core.windows.net/TableSortedByDescCode.csv'
                    # Tranforma DataFrame Spark a Dataframe Pandas luego a csv.
                    # y escribe en el contenedor de un data lake
                    """TableSortedByDescCode
                                    .toPandas()
                                        .to_csv(filePathDataLake,\
                                                storage_options = {'account_key': key_datalake} 
                                                ,index=False)"""

                    SubcategoriaFiltered = TableSortedByDescCode.filter(TableSortedByDescCode['Cod_Territorio']>=9)
                    transform.append(SubcategoriaFiltered)
                    # Visualizamos la tabla
                    SubcategoriaFiltered.show()
                    # Crea tabla Temporal
                    SubcategoriaFiltered.createOrReplaceTempView("SubcategoriaFilteredTemporal")
                    # Query
                    SubcategoriaFilteredTemporalQuery = spark.sql("select PrecioUnitario,CostoUnitario,Impuesto \
                                                                                from SubcategoriaFilteredTemporal")
                    # Visualiza
                    SubcategoriaFilteredTemporalQuery.show()

                    # Construimos la URL con el Nombre de la Transformacion Especifica.
                    filePathDataLake=f'abfs://{datalake_container}@{datalake_name}.\
                                                            dfs.core.windows.net/SubcategoriaFiltered.csv'
                    # Tranforma DataFrame Spark a Dataframe Pandas luego a csv 
                    # y escribe en el contenedor de un data lake
                    """SubcategoriaFiltered
                                    .toPandas()
                                        .to_csv(filePathDataLake,\
                                            storage_options = {'account_key': key_datalake} 
                                            ,index=False)"""
                
                    VentasWithNetIncome = (df_VentasInternet
                                                    .withColumn("Ingresos_Netos", function
                                                        .round(function.col("Cantidad")*function
                                                            .col("PrecioUnitario")-function
                                                                .col("CostoUnitario"),4)     
                                                                .cast(DecimalType(10,4))))
                    transform.append(VentasWithNetIncome)
                    # Visualizamos el Schema
                    VentasWithNetIncome.show()
                    # Crea tabla Temporal
                    VentasWithNetIncome.createOrReplaceTempView("VentasWithNetIncomeTemporal")
                    # Query
                    VentasWithNetIncomeTemporalQuery = spark.sql("select PrecioUnitario,Cod_Producto,Ingresos_Netos > 17\
                                                                                    from VentasWithNetIncomeTemporal")
                    # Visualiza
                    VentasWithNetIncomeTemporalQuery.show()  
                 
                    # Construimos la URL con el Nombre de la Transformacion Especifica.
                    filePathDataLake=f'abfs://{datalake_container}@{datalake_name}.\
                                                            dfs.core.windows.net/VentasWithNetIncome.csv'
                      # Tranforma DataFrame Spark a Dataframe Pandas luego a csv
                      # y escribe en el contenedor de un data lake
                    """VentasWithNetIncome
                                .toPandas()
                                    .to_csv(filePathDataLake,\
                                            storage_options = {'account_key': key_datalake} \
                                            ,index=False)"""

                    IngresosPorCodProducto = (VentasWithNetIncome
                                                .groupBy(function
                                                    .col("Cod_Producto"))
                                                    .agg(function.round(function
                                                        .avg("Ingresos_Netos"),4)
                                                            .alias("Ingreso_Neto_Promedio"), function
                                                                .round(function.sum("Ingresos_Netos"),4)
                                                                .alias("Suma_Ingresos_Netos")))
                    
                    transform.append(IngresosPorCodProducto)
                    # Visualizamos la tabla
                    IngresosPorCodProducto.show()
                    # Crea tabla Temporal
                    IngresosPorCodProducto.createOrReplaceTempView("IngresosPorCodProductoTemporal")
                    # Query
                    IngresosPorCodProductoTemporalQuery = spark.sql("select Ingreso_Neto_Promedio,Cod_Producto >473 \
                                                                                from IngresosPorCodProductoTemporal")
                    # Visualiza
                    IngresosPorCodProductoTemporalQuery.show() 
                    # Construimos la URL con el Nombre de la Transformacion Especifica.
                    filePathDataLake=f'abfs://{datalake_container}@{datalake_name}.\
                                                                    dfs.core.windows.net/IngresosPorCodProducto.csv'
                    # Tranforma DataFrame Spark a Dataframe Pandas luego a csv 
                    # y escribe en el contenedor de un data lake
                    """IngresosPorCodProducto
                                .toPandas()
                                    .to_csv(filePathDataLake,\
                                            storage_options = {'account_key': key_datalake} 
                                            ,index=False)"""
                continue 
            case _:
                raise ValueError("No se encuenta el Arcvhivo.")
    return None

if __name__ == "__main__":
    # Import 
    import dotenv
    import sys
    import os
    # cargamos las variables de entorno
    dotenv.load_dotenv()
    storage_name = 'storagebasedatos2510'
    key_blobs = os.getenv('KEY_BLOBS')
    datalake_name = 'storagedatalake2510'
    key_datalake = os.getenv('KEY_DATALAKE')
    # Nombre del contenedor del Blob storage donde se encuentren los csv
    # Cree una SparkSession utilizando las API SparkSession.
    # Si no existe entonces cree una instancia.
    # Solo puede ser una Intancia por JVM.
    spark = SparkSession.builder.master("local[3]").appName("etl").getOrCreate()
    # Patterns = dbutils.widgets.get('parametro_direcciones').split(",")
    patterns= sys.argv[1:]
    print(patterns)
    if len(patterns) > 0: 
        logger = Log4j(spark)
        main(spark,patterns,storage_name,key_blobs,datalake_name,key_datalake)                                       
        spark.stop()                                              
    else:
        logger = Log4j(spark)
        main(spark,patterns,storage_name,key_blobs,datalake_name,key_datalake)                                       
        spark.stop()  