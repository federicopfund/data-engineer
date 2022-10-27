# Databricks notebook source
import pyspark

spark = pyspark.sql.SparkSession.builder.master("local").appName("Transformacion 7").getOrCreate()

# COMMAND ----------

subcategoria_table = spark.read.load("Datasets\Tabla Subcategoria\Subcategoria.csv", format="csv", header=True, inferSchema=True)

# COMMAND ----------

subcategoria_table.printSchema()
subcategoria_table.show(5, truncate=False)

# COMMAND ----------

import pyspark.sql.functions as F
subcategoriaFiltered = subcategoria_table.filter(subcategoria_table['Cod_Categoria'] == 3)
subcategoriaFiltered.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Otras formas de filtrarlo

# COMMAND ----------

subcategoriaFiltered2 = subcategoria_table.filter(subcategoria_table.Cod_Categoria == 3)
subcategoriaFiltered2.show()

# COMMAND ----------

subcategoriaFiltered3 = subcategoria_table[subcategoria_table['Cod_Categoria'] == 3]
subcategoriaFiltered3.show()

# COMMAND ----------

subcategoriaFiltered4 = subcategoria_table.where(F.col("Cod_Categoria") == 3)
subcategoriaFiltered4.show()
