# Databricks notebook source
import pyspark

spark = pyspark.sql.SparkSession.builder.master("local").appName("Transformacion 5").getOrCreate()

# COMMAND ----------

producto_table =  spark.read.load("Datasets\Tabla Producto\Producto.csv" , format="csv", header=True, inferSchema=True)

# COMMAND ----------

producto_table.printSchema()
producto_table.show(5,truncate=False)

# COMMAND ----------

import pyspark.sql.functions as F
productCount = producto_table.agg(F.count("Cod_Producto").alias("Cantidad CodProducto"))
productCount.show()
