# Databricks notebook source
import pyspark

spark = pyspark.sql.SparkSession.builder.master("local").appName("Transformacion 2").getOrCreate()

# COMMAND ----------

factmine_table = spark.read.load("Datasets\Tabla FactMine\FactMine.csv", format="csv", header=True, inferSchema=True)

# COMMAND ----------

factmine_table.printSchema()

# COMMAND ----------

factmine_table.show(5)

# COMMAND ----------

import pyspark.sql.functions as F
sumTotalOreMined = factmine_table.agg(F.sum("TotalOreMined").alias("Suma TotalOreMined"))
sumTotalOreMined.show()
