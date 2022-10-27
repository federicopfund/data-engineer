# Databricks notebook source
import pyspark

spark = pyspark.sql.SparkSession.builder.master("local").appName("Transformacion 3").getOrCreate()

# COMMAND ----------

mine_table = spark.read.load("Datasets\Tabla Mine\Mine.csv", format="csv", header=True, inferSchema=True)

# COMMAND ----------

mine_table.printSchema()

# COMMAND ----------

mine_table.show(5)

# COMMAND ----------

selectedColumns = mine_table.select("Country","FirstName","LastName","Age")
selectedColumns.show()
