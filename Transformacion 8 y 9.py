# Databricks notebook source
import pyspark

spark = pyspark.sql.SparkSession.builder.master("local").appName("Transformacion 8 y 9").getOrCreate()

# COMMAND ----------

ventas_table = spark.read.load("Datasets\Tabla VentasInternet\VentasInternet.csv", format="csv", header=True, inferSchema=True)

# COMMAND ----------

ventas_table.printSchema()
ventas_table.show(5, truncate=True)

# COMMAND ----------

import pyspark.sql.functions as F
ventasWithNetIncome = ventas_table.withColumn("Ingresos Netos", F.col("Cantidad")*F.col("PrecioUnitario")-F.col("CostoUnitario"))
ventasWithNetIncome.show()

# COMMAND ----------

ingresosPorCodProducto = ventasWithNetIncome.groupBy(F.col("Cod_Producto")).agg(F.avg("Ingresos Netos").alias("Ingreso Neto Promedio"), F.sum("Ingresos Netos").alias("Suma Ingresos Netos"))
ingresosPorCodProducto.show()

