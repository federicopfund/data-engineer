package vortex.exelstream

import org.apache.spark.sql.{SparkSession, DataFrame}
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types.{IntegerType, DecimalType}
import scala.concurrent.{Future, Await}
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.duration._


object SparkSessionSingleton {

  @transient private var instance: SparkSession = _

  def getSparkSession: SparkSession = {
    if (instance == null) {
      synchronized {
        if (instance == null) {
          instance = SparkSession.builder
              .appName("SparkSessionExample")
                .master("local[2]")
                  .config("spark.some.config.option", "config-value")
                  .config("spark.authenticate", "true")
                  .config("spark.authenticate.secret", "fede")
                  .config("spark.ssl.enabled", "true")
                  .config("spark.ssl.keyPassword", "fede")
                  .config("spark.ssl.keystore", "path/to/your/keystore")
                  .config("spark.executor.memory", "2g")
                  .config("spark.executor.cores", "3")
                  .config("spark.driver.memory", "1g")
                  .config("spark.driver.maxResultSize", "1g")
                  .config("spark.executor.instances", "2")
                  .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
                  .config("spark.default.parallelism", "4")
                  .config("spark.shuffle.compress", "true")
                  .config("spark.shuffle.manager", "tungsten-sort")
                  .config("spark.shuffle.file.buffer", "1m")
                  .config("spark.sql.shuffle.partitions", "8")
                  .config("spark.sql.autoBroadcastJoinThreshold", "10485760")
                  .config("spark.sql.inMemoryColumnarStorage.batchSize", "10000")
                  .config("spark.sql.inMemoryColumnarStorage.compressed", "true")
                  .config("spark.sql.broadcastTimeout", "300")
                  .config("spark.streaming.receiver.writeAheadLog.enable", "true")
                  .config("spark.sql.warehouse.dir", "file:./src/main/resources/csv/")
                .getOrCreate()
        }
      }
    }
    instance
  }

}


object MainETL {

  def main(args: Array[String]): Unit = {

    val spark = SparkSessionSingleton.getSparkSession
    try {
      processPatternsParallel(spark, Array("Categoria.csv", "FactMine.csv", "Mine.csv", "Producto.csv", "VentasInternet.csv"))
    } finally {
      spark.stop()
    }
  }

  def processPatternsParallel(spark: SparkSession, patterns: Array[String]): Unit = {
    val futures = patterns.map { pattern =>
      Future {
        pattern match {
          case "Categoria.csv" => transformCategoria(spark, pattern)
          case "FactMine.csv" => transformFactMine(spark, pattern)
          case "Mine.csv" => transformMine(spark, pattern)
          case "Producto.csv" => transformProduct(spark, pattern)
          case "VentasInternet.csv" => transformVentasInternet(spark, pattern)
          case _ => throw new IllegalArgumentException(s"Archivo no reconocido: $pattern")
        }
      }
    }

    // Wait for all futures to complete
    Await.result(Future.sequence(futures.toList), Duration.Inf)
  }

  def transformCategoria(spark: SparkSession, pattern: String): Unit = {
    val filePath = s"./src/main/resources/csv/$pattern"
    val dfCategoria = spark.read.option("header", "true").option("inferSchema", "true").csv(filePath)
    dfCategoria.cache()
    val CategoriaRename = dfCategoria.withColumnRenamed("Categoria", "Nombre_Categoria")
    saveToCSV(CategoriaRename, "./src/main/resources/csv/transformed", pattern)
    CategoriaRename.show()
    CategoriaRename.unpersist()
  }

  def transformFactMine(spark: SparkSession, pattern: String): Unit = {
    val filePath = s"./src/main/resources/csv/$pattern"
    val dfFactMine = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(filePath)
    dfFactMine.cache()
    val sumTotalOreMined = dfFactMine.agg(round(sum("TotalOreMined"), 4).alias("Suma_TotalOreMined"))
    sumTotalOreMined.explain()
    saveToCSV(sumTotalOreMined, "./src/main/resources/csv/transformed", pattern)
    val consulta = dfFactMine.select("TruckID", "ProjectID", "OperatorID", "TotalOreMined")
    saveToCSV(consulta, "./src/main/resources/csv/transformed", s"${pattern}_consulta")
    sumTotalOreMined.show()
    consulta.show()
    sumTotalOreMined.unpersist()
    consulta.unpersist()
  }

  def transformMine(spark: SparkSession, pattern: String): Unit = {
    val filePath = s"./src/main/resources/csv/$pattern"
    val dfMine = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(filePath)
    dfMine.cache()
    val selectedColumns = dfMine.select("Country", "FirstName", "LastName", "Age")
    saveToCSV(selectedColumns, "./src/main/resources/csv/transformed", pattern)
    val sumTotalWastedByCountry = dfMine.groupBy("Country").agg(round(sum("TotalWasted"), 4).alias("Suma_TotalWasted"))
    sumTotalWastedByCountry.explain()
    saveToCSV(sumTotalWastedByCountry, "./src/main/resources/csv/transformed", s"${pattern}_sum")
    selectedColumns.show()
    sumTotalWastedByCountry.show()
    selectedColumns.unpersist()
    sumTotalWastedByCountry.unpersist()
  }

  def transformProduct(spark: SparkSession, pattern: String): Unit = {
    val filePath = s"./src/main/resources/csv/$pattern"
    val df_Productos = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(filePath)
    df_Productos.cache()
    val result: DataFrame = df_Productos.agg(count("Cod_Producto").alias("Cantidad_CodProducto"))
    result.cache()
    saveToCSV(result, "./src/main/resources/csv/transformed", pattern)
    val ProductosCount_Cast = result.withColumn("Cantidad_CodProducto", col("Cantidad_CodProducto").cast(IntegerType))
    ProductosCount_Cast.explain()
    saveToCSV(ProductosCount_Cast, "./src/main/resources/csv/transformed", s"${pattern}_cast")
    result.show()
    ProductosCount_Cast.show()
    df_Productos.unpersist()
    result.unpersist()
  }

  def transformVentasInternet(spark: SparkSession, pattern: String): Unit = {
    val filePath = s"./src/main/resources/csv/$pattern"
    val df_VentasInternet = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(filePath)
    saveToCSV(df_VentasInternet, "./src/main/resources/csv/transformed", pattern)
 
  }

  def saveToCSV(df: DataFrame, outputPath: String, fileName: String): Unit = {
    df.coalesce(1).write.option("header", "true").csv(s"$outputPath/$fileName")
  }
}


