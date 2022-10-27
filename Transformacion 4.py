# Databricks notebook source
import pyspark

spark = pyspark.sql.SparkSession.builder.master("local").appName("Transformacion 4").getOrCreate()

# COMMAND ----------

mine_table =  spark.read.load("Datasets\Tabla Mine\Mine.csv" , format="csv", header=True, inferSchema=True)

# COMMAND ----------

mine_table.printSchema()
mine_table.show(5)

# COMMAND ----------

import pyspark.sql.functions as F
sumTotalWastedByCountry = mine_table.groupBy("Country").agg(F.sum("TotalWasted").alias("Suma TotalWasted"))
sumTotalWastedByCountry.show()
