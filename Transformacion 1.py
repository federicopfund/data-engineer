# Databricks notebook source
# El hostname se obtiene en la seccion overview del sqlserver
jdbcHostname = "grouponesqlserver-379320670.database.windows.net"
# Nombre de la db
jdbcDatabase = "groupOneSqlServerDatabase"
# Siempre es este puerto
jdbcPort = 1433

jdbcUrl = f"jdbc:sqlserver://{jdbcHostname}:{jdbcPort};database={jdbcDatabase}"
print(jdbcUrl)

# COMMAND ----------

# Credenciales de acceso a sqlserver
user = "sqlgrupo1"
password = "Passwordgrupo1!"

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
display(categoria_table)

# COMMAND ----------

# Transformacion 1: renombrar el campo Categoria a Nombre_Categoria
categoriaTransformada = categoria_table.withColumnRenamed("Categoria", "Nombre_Categoria")

# COMMAND ----------

display(categoriaTransformada)
categoriaTransformada.printSchema()

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS CategoriaTransformada;

# COMMAND ----------

categoriaTransformada.write.saveAsTable("CategoriaTransformada")

# COMMAND ----------

# Tabla local de databricks
createLocalTable = f'''
CREATE TABLE IF NOT EXISTS Transformacion
USING org.apache.spark.sql.jdbc
OPTIONS (
    url '{jdbcUrl}',
    dbtable '{"dbo.Transformacion1"}',
    user '{user}',
    password '{password}',
    loginTimeout = 120
    ) '''

#print(createLocalTable)
spark.sql(createLocalTable)

# COMMAND ----------

# MAGIC %sql
# MAGIC /* Simula truncar la tabla porque no se puede hacer TRUNCATE TABLE con external tables*/
# MAGIC INSERT OVERWRITE TABLE Transformacion SELECT * FROM Transformacion where 1=2;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO Transformacion
# MAGIC SELECT * FROM CategoriaTransformada;