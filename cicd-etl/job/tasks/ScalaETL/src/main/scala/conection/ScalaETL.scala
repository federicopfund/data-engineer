package Vortex.tranform

import org.apache.hadoop.fs.FsUrlStreamHandlerFactory
import java.nio.file.{Paths, Files}
import org.apache.spark.sql.{SparkSession, DataFrame,Row}
import org.apache.spark.sql.functions._
import scala.concurrent.{Future, Await}
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.duration._
import org.apache.spark.storage.StorageLevel
import scala.collection.JavaConverters._
import java.nio.file.attribute.BasicFileAttributes

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

    synchronized {
      try {
        new java.net.URL("file:/")
      } catch {
        case _: java.net.MalformedURLException =>
          java.net.URL.setURLStreamHandlerFactory(new org.apache.hadoop.fs.FsUrlStreamHandlerFactory())
      }
    }

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
      case _: Throwable => false
    }
  }

  def processPatternsParallel(spark: SparkSession, patterns: Array[String]): Unit = {
    val outputPath = "./src/main/resources/csv/transformed"
    deleteDirectory(outputPath)
    createDirectory(outputPath)
    val futures = patterns.map { pattern =>
      Future {
        pattern match {
          case "Categoria.csv" => transformCategoria(spark, pattern, outputPath)
          case "FactMine.csv" => transformFactMine(spark, pattern, outputPath)
          case "Mine.csv" => transformMine(spark, pattern, outputPath)
          case "Producto.csv" => transformProduct(spark, pattern, outputPath)
          case "VentasInternet.csv" => transformVentasInternet(spark, pattern, outputPath)
          case _ => throw new IllegalArgumentException(s"Archivo no reconocido: $pattern")
        }
      }
    }

    // Wait for all futures to complete
    Await.result(Future.sequence(futures.toList), Duration.Inf)
  }


  def transformCategoria(spark: SparkSession, pattern: String, outputPath: String): Unit = {

    val transformedFilePath = s"$outputPath/$pattern"

    if (!fileExists(transformedFilePath)) {
      val filePath = s"./src/main/resources/csv/$pattern"
      val dfCategoria = spark.read.option("header", "true").option("inferSchema", "true").csv(filePath)
      val dfFilteredCategoria = dfCategoria.na.drop().repartition(5) 
      val isCached: Boolean = isDataFrameCached(dfFilteredCategoria)

      if (!isCached) {
        dfFilteredCategoria.cache()
        dfFilteredCategoria.createOrReplaceTempView("dfCategoriaView")
        val transformations = List(
          "SELECT Categoria FROM dfCategoriaView",
          "SELECT Categoria AS Nombre_Categoria, * FROM dfCategoriaView")

        for ((transformation, index) <- transformations.zipWithIndex) {
          println(s"Aplicando transformación ${index + 1}: $transformation")
          val consulta: DataFrame = spark.sql(transformation).as("consulta")
          saveAndShow(consulta, outputPath, s"${pattern}_${index}")
        }
      }
      dfFilteredCategoria.unpersist()
    } else {
      println(s"La transformación para el patrón $pattern ya existe. No es necesario recalcular.")
    }
  }
  
    
  def transformFactMine(spark: SparkSession, pattern: String, outputPath: String): Unit = {
  
    val transformedFilePath = s"$outputPath/$pattern"
  
    if (!fileExists(transformedFilePath)) {
      val filePath = s"./src/main/resources/csv/$pattern"
      val dfFactMine = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(filePath)
      val dfFilteredFactMine = dfFactMine.na.drop().repartition(5) 
      val isCached: Boolean = isDataFrameCached(dfFilteredFactMine)
      
      if (!isCached) {
        dfFilteredFactMine.cache()
        dfFilteredFactMine.createOrReplaceTempView("dfFactMineView")
        val transformations = List(
           "SELECT TruckID, ProjectID, OperatorID, TotalOreMined FROM dfFactMineView",
            "SELECT ROUND(SUM(TotalOreMined), 4) AS Suma_TotalOreMined FROM dfFactMineView")
              
        for ((transformation, index) <- transformations.zipWithIndex) {
            println(s"Aplicando transformación ${index + 1}: $transformation")
            val consulta: DataFrame = spark.sql(transformation).as("consulta")
            saveAndShow(consulta, outputPath, s"${pattern}_${index}")
        }
        dfFilteredFactMine.unpersist()
        }
      } else {
        println(s"La transformación para el patrón $pattern ya existe. No es necesario recalcular.")
    }
  }
    
  def transformMine(spark: SparkSession, pattern: String, outputPath: String): Unit = {
   
    val transformedFilePath = s"$outputPath/$pattern"
   
    if (!fileExists(transformedFilePath)) {
      val filePath = s"./src/main/resources/csv/$pattern"
      val dfMine = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(filePath)
      val dfFilteredMine = dfMine.na.drop().repartition(5)
      val isCached: Boolean = isDataFrameCached(dfMine)
        if (!isCached) {
          dfFilteredMine.cache()
          dfFilteredMine.createOrReplaceTempView("dfView")
          val transformations = List(
            "SELECT Country, FirstName, LastName, Age FROM dfView",
            "SELECT DISTINCT FirstName, Country, LastName, Age FROM dfView",
            "SELECT DISTINCT FirstName, Country, LastName, Age  FROM dfView ORDER BY Age DESC",
            "SELECT Country, COUNT(*) AS PersonasPorPais FROM dfView GROUP BY Country")

          for ((transformation, index) <- transformations.zipWithIndex) {
            println(s"Aplicando transformación ${index + 1}: $transformation")
            val consulta: DataFrame = spark.sql(transformation).as("consulta")
            saveAndShow(consulta, outputPath, s"${pattern}_${index}")
          }
          dfFilteredMine.unpersist()
        }
      } else {
        println(s"La transformación para el patrón $pattern ya existe. No es necesario recalcular.")
    }
  }
  

  def transformProduct(spark: SparkSession, pattern: String, outputPath: String): Unit = {
    
    val transformedFilePath = s"$outputPath/$pattern"
   
    if (!fileExists(transformedFilePath)) {
      val filePath = s"./src/main/resources/csv/$pattern"
      val dfProductos = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(filePath)
      val dfFilteredProductos = dfProductos.na.drop().repartition(5) 
      val isCached: Boolean = isDataFrameCached(dfFilteredProductos)
      if (!isCached) {
        dfFilteredProductos.cache()
        dfFilteredProductos.createOrReplaceTempView("dfProductosView")
        val transformations = List(
             "SELECT Producto, Color FROM dfProductosView",
             "SELECT Color, COUNT(*) AS CantidadProductos FROM dfProductosView GROUP BY Color",
              "SELECT COUNT(Cod_Producto) AS Cantidad_CodProducto FROM dfProductosView")

        for ((transformation, index) <- transformations.zipWithIndex) {
          println(s"Aplicando transformación ${index + 1}: $transformation")
          val consulta: DataFrame = spark.sql(transformation).as("consulta")
          saveAndShow(consulta, outputPath, s"${pattern}_${index}")
        }
        dfFilteredProductos.unpersist()
      }
    } else {
     println(s"La transformación para el patrón $pattern ya existe. No es necesario recalcular.")
    }
  }
  

  def transformVentasInternet(spark: SparkSession, pattern: String, outputPath: String): Unit = {
    
    val transformedFilePath = s"$outputPath/$pattern"
   
    if (!fileExists(transformedFilePath)) {
      val filePath = s"./src/main/resources/csv/$pattern"
      val dfVentasInternet = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(filePath)
      val dfFilteredVentasInternet = dfVentasInternet.na.drop().repartition(5) 
      val isCached: Boolean = isDataFrameCached(dfFilteredVentasInternet)
      if (!isCached) {
        dfFilteredVentasInternet.cache()
        dfFilteredVentasInternet.createOrReplaceTempView("dfFilteredVentasInternet")
        val transformations = List(
           "SELECT * FROM dfFilteredVentasInternet ORDER BY Cod_Producto DESC",
            "SELECT * FROM dfFilteredVentasInternet WHERE Cod_Territorio >= 9",
             "SELECT *, ROUND((Cantidad * PrecioUnitario - CostoUnitario), 4) AS Ingresos_Netos FROM dfFilteredVentasInternet")

        for ((transformation, index) <- transformations.zipWithIndex) {
          println(s"Aplicando transformación ${index + 1}: $transformation")
          val consulta: DataFrame = spark.sql(transformation).as("consulta")
          saveAndShow(consulta, outputPath, s"${pattern}_${index}")
        }
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
  
  def createDirectory(directoryPath: String): Unit = {
    val path = Paths.get(directoryPath)
    if (!Files.exists(path)) {
      Files.createDirectories(path)
      println(s"Directorio creado: $directoryPath")
    }
  }

  def deleteDirectory(directoryPath: String): Unit = {
    val path = Paths.get(directoryPath)

    if (Files.exists(path)) {
      val files = Files.walk(path).iterator().asScala.toSeq.reverse
      files.foreach { filePath =>
        // Filtra la carpeta "transformed" del proceso de eliminación
        if (!filePath.toString.endsWith("transformed")) {
          Files.deleteIfExists(filePath)
          println(s"Archivo eliminado: $filePath")
        }
      }

      println(s"Directorio eliminado: $directoryPath")
      } else {
        println(s"El directorio $directoryPath no existe.")
        createDirectory(directoryPath)
    }
  }
}


