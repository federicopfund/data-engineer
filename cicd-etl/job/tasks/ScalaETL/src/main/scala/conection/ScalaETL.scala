package vortex.exelstream

import org.apache.spark.sql.{SparkSession, DataFrame}
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types.{IntegerType, DecimalType}
import scala.concurrent.{Future, Await}
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.duration._
import org.apache.spark.storage.StorageLevel

object SparkSessionSingleton {

  @transient private var instance: SparkSession = _
  
  def getSparkSession: SparkSession = {
    if (instance == null) {
      synchronized {
        if (instance == null) {
          val absolutePath = new java.io.File("./src/main/resources/csv").getCanonicalPath
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
                  .config("spark.sql.catalogImplementation", "in-memory")
                  .config("spark.sql.warehouse.dir", s"file:$absolutePath/")
                .getOrCreate()}
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

  def isDataFrameCached(df: DataFrame): Boolean = {
    try {
      df.storageLevel != org.apache.spark.storage.StorageLevel.NONE
    } catch {
      // Si hay una excepción, significa que el DataFrame no está en caché
      case _: Throwable => false
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
    val outputPath = "./src/main/resources/csv/transformed"
    val transformedFilePath = s"$outputPath/$pattern"
    if (!fileExists(transformedFilePath)) {
      val filePath = s"./src/main/resources/csv/$pattern"
      val dfCategoria = spark.read.option("header", "true").option("inferSchema", "true").csv(filePath)
      val dfFilteredCategoria = dfCategoria.na.drop()
      val isCached: Boolean = isDataFrameCached(dfFilteredCategoria)
      if (!isCached) {
        dfFilteredCategoria.cache()
        dfFilteredCategoria.createOrReplaceTempView("dfCategoriaView")
        val consulta = spark.sql("SELECT Categoria FROM dfCategoriaView")
        consulta.show()
      }

      val CategoriaRename = dfCategoria.withColumnRenamed("Categoria", "Nombre_Categoria")
      saveAndShow(CategoriaRename, outputPath, pattern)
      dfFilteredCategoria.unpersist()
    } else {
      println(s"La transformación para el patrón $pattern ya existe. No es necesario recalcular.")
    }
  }

  def transformFactMine(spark: SparkSession, pattern: String): Unit = {
    val outputPath = "./src/main/resources/csv/transformed"
    val transformedFilePath = s"$outputPath/$pattern"
    if (!fileExists(transformedFilePath)) {
      val filePath = s"./src/main/resources/csv/$pattern"
      val dfFactMine = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(filePath)
      val dfFilteredFactMine = dfFactMine.na.drop()
      val isCached: Boolean = isDataFrameCached(dfFilteredFactMine)
      if (!isCached) {
        dfFilteredFactMine.cache()
        dfFilteredFactMine.createOrReplaceTempView("dfFactMineView")
        val consulta = spark.sql("SELECT TruckID, ProjectID, OperatorID, TotalOreMined FROM dfFactMineView")
        consulta.show()
        dfFilteredFactMine.unpersist()
      }

      val sumTotalOreMined = dfFactMine.agg(round(sum("TotalOreMined"), 4).alias("Suma_TotalOreMined"))
      saveAndShow(sumTotalOreMined, outputPath, pattern)
    } else {
      println(s"La transformación para el patrón $pattern ya existe. No es necesario recalcular.")
    }
  }
    
  def transformMine(spark: SparkSession, pattern: String): Unit = {
    val outputPath = "./src/main/resources/csv/transformed"
    val transformedFilePath = s"$outputPath/$pattern"
    if (!fileExists(transformedFilePath)) {
      val filePath = s"./src/main/resources/csv/$pattern"
      val dfMine = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(filePath)
      val dfFilteredMine = dfMine.na.drop()
      val isCached: Boolean = isDataFrameCached(dfMine)
      if (!isCached) {
        dfFilteredMine.cache()
        dfFilteredMine.createOrReplaceTempView("dfMineView")
        val selectedColumns = spark.sql("SELECT Country, FirstName, LastName, Age FROM dfMineView")
        selectedColumns.show()
        dfFilteredMine.unpersist()
      }
     
      val sumTotalWastedByCountry = dfFilteredMine.groupBy("Country").agg(round(sum("TotalWasted"), 4).alias("Suma_TotalWasted"))
      saveAndShow(sumTotalWastedByCountry, outputPath, s"${pattern}_sum")
    } else {
      println(s"La transformación para el patrón $pattern ya existe. No es necesario recalcular.")
    }
  }



  def transformProduct(spark: SparkSession, pattern: String): Unit = {
    val outputPath = "./src/main/resources/csv/transformed"
    val transformedFilePath = s"$outputPath/$pattern"
    if (!fileExists(transformedFilePath)) {
      val filePath = s"./src/main/resources/csv/$pattern"
      val dfProductos = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(filePath)
      val dfFilteredProductos = dfProductos.na.drop()
      val isCached: Boolean = isDataFrameCached(dfFilteredProductos)
      if (!isCached) {
        dfFilteredProductos.cache()
        dfFilteredProductos.createOrReplaceTempView("dfProductosView")
        val selectedColumns = spark.sql("SELECT Producto, Color FROM dfProductosView")
        selectedColumns.show()
      }
     
      val result: DataFrame = dfFilteredProductos.agg(count("Cod_Producto").alias("Cantidad_CodProducto"))
      saveAndShow(result, outputPath, pattern)
      dfFilteredProductos.unpersist()
      val productosCountCast = result.withColumn("Cantidad_CodProducto", col("Cantidad_CodProducto").cast(IntegerType))
      saveAndShow(productosCountCast, outputPath, s"${pattern}_cast")
    } else {
      println(s"La transformación para el patrón $pattern ya existe. No es necesario recalcular.")
    }
  }


  def transformVentasInternet(spark: SparkSession, pattern: String): Unit = {
    val outputPath = "./src/main/resources/csv/transformed"
    val transformedFilePath = s"$outputPath/$pattern"
    if (!fileExists(transformedFilePath)) {
      val filePath = s"./src/main/resources/csv/$pattern"
      val dfVentasInternet = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(filePath)
      val dfFilteredVentasInternet = dfVentasInternet.na.drop()
      val isCached: Boolean = isDataFrameCached(dfFilteredVentasInternet)
      if (!isCached) {
        dfFilteredVentasInternet.cache()
        dfFilteredVentasInternet.createOrReplaceTempView("dfFilteredVentasInternet")
        dfFilteredVentasInternet.printSchema()
        dfFilteredVentasInternet.unpersist()
      }
    } else {
      println(s"La transformación para el patrón $pattern ya existe. No es necesario recalcular.")
    }
  }

  def saveAndShow(df: DataFrame, outputPath: String, fileName: String): Unit = {
    df.coalesce(1).write.option("header", "true").csv(s"$outputPath/$fileName")
    df.show()
  }

  def fileExists(filePath: String): Boolean = {
    // Lógica para verificar si el archivo existe
    // Puedes utilizar las utilidades de manejo de archivos de Scala o Java para esto.
    // Aquí, se utiliza java.nio.file.Files.exists para la verificación.
    java.nio.file.Files.exists(java.nio.file.Paths.get(filePath))
  }

}


