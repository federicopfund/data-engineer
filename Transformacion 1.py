# Databricks notebook source
# El hostname se obtiene en la seccion overview del sqlserver
jdbcHostname = "sqlserverjme123.database.windows.net"
# Nombre de la db
jdbcDatabase = "dbRetail"
# Siempre es este puerto
jdbcPort = 1433

jdbcUrl = f"jdbc:sqlserver://{jdbcHostname}:{jdbcPort};database={jdbcDatabase}"
print(jdbcUrl)

# COMMAND ----------

# Credenciales de acceso a sqlserver
user = "serveradmin"
password = "Password123."

# COMMAND ----------

# Lectura de la tabla dbo.Categoria
categoria_table = (spark.read
  .format("jdbc")
  .option("url", jdbcUrl)
  .option("dbtable", "dbo.Categoria")
  .option("user", user)
  .option("password", password)
  .load()
)

# COMMAND ----------

categoria_table.printSchema()

# COMMAND ----------

display(categoria_table)

# COMMAND ----------

# Transformacion 1: renombrar el campo Categoria a Nombre_Categoria
categoria_table = categoria_table.withColumnRenamed("Categoria", "Nombre_Categoria")

# COMMAND ----------

display(categoria_table)
