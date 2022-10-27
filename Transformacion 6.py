# Databricks notebook source
import pyspark

spark = pyspark.sql.SparkSession.builder.master("local").appName("Transformacion 6").getOrCreate()

# COMMAND ----------

producto_table =  spark.read.load("Datasets\Tabla Producto\Producto.csv" , format="csv", header=True, inferSchema=True)

# COMMAND ----------

import pyspark.sql.functions as F
tableSortedByDescCode = producto_table.sort(F.col("Cod_Producto").desc())
tableSortedByDescCode.show(truncate=False)
