package scala.transform


import java.nio.file.attribute.BasicFileAttributes
import org.apache.hadoop.fs.FsUrlStreamHandlerFactory
import org.apache.spark.sql.{DataFrame,Row}
import org.apache.spark.sql.functions._
import scala.concurrent.{Future, Await}
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.duration._
import org.apache.spark.storage.StorageLevel
import scala.collection.JavaConverters._
import org.apache.spark.sql.SparkSession
import java.nio.file.{Files, Path, Paths}
import java.util.stream.Collectors
import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.{FileSystem}


object funcTransform {
 
 

  // Variables globales
  var raw: String = _
  var bronze: String = _
  var silver: String = _
  var gold: String = _
  

  def processFile(spark: SparkSession, patterns: Array[String], hdfsUriRoot: String): Unit = {
    // Resources Local
    //val outputPath = "./src/main/resources/csv/transformed"
    //deleteDirectory(outputPath)
    //createDirectory(outputPath)
    // Resouce HDFS
    val hdfsUrlRoot = "hdfs://localhost:9001/hive/warehouse"
    val hdfsUrl = s"$hdfsUrlRoot/datalake"
    val raw     = s"$hdfsUrl/raw"
    val bronze  = s"$hdfsUrl/bronze"
    val silver  = s"$hdfsUrl/silver"
    val gold    = s"$hdfsUrl/gold"
    
    val futures = patterns.map { pattern =>
      Future {
        pattern match {
          case "Categoria.csv" => transformCategoria(spark, pattern, raw, bronze)
          case "FactMine.csv" => transformFactMine(spark, pattern, raw, bronze)
          case "Mine.csv" => transformMine(spark, pattern, raw, bronze)
          case "Producto.csv" => transformProduct(spark, pattern, raw, bronze)
          case "VentasInternet.csv" => transformVentasInternet(spark, pattern, raw, bronze)
          case _ => throw new IllegalArgumentException(s"Archivo no reconocido: $pattern")
        }
      }
    }

    Await.result(Future.sequence(futures.toList), Duration.Inf)
  }


  def transformCategoria(spark: SparkSession, pattern: String, loadFile: String, outputPath: String): Unit = {
    val WirteFileTransformPath = s"$outputPath/${pattern.stripSuffix(".csv")}"
    if (!fileExists(WirteFileTransformPath)) {
      val filePath = s"$loadFile/$pattern"
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
          saveAndShow(consulta, WirteFileTransformPath, s"${pattern.stripSuffix(".csv")}_${index}")
        }
      }
      dfFilteredCategoria.unpersist()
    } else {
      println(s"La transformación para el patrón $pattern ya existe. No es necesario recalcular.")
    }
  }
  
    
  def transformFactMine(spark: SparkSession, pattern: String,loadFile: String, outputPath: String): Unit = {
    val WirteFileTransformPath =  s"$outputPath/${pattern.stripSuffix(".csv")}"
    if (!fileExists(WirteFileTransformPath)) {
      val filePath = s"$loadFile/$pattern"
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
            saveAndShow(consulta, WirteFileTransformPath, s"${pattern.stripSuffix(".csv")}_${index}")
        }
        dfFilteredFactMine.unpersist()
        }
      } else {
        println(s"La transformación para el patrón $pattern ya existe. No es necesario recalcular.")
    }
  }
    

  def transformMine(spark: SparkSession, pattern: String, loadFile: String, outputPath: String): Unit = {
    val WirteFileTransformPath =  s"$outputPath/${pattern.stripSuffix(".csv")}"
    if (!fileExists(WirteFileTransformPath)) {
      val filePath = s"$loadFile/$pattern"
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
          saveAndShow(consulta, WirteFileTransformPath, s"${pattern.stripSuffix(".csv")}_${index}")
        }
        dfFilteredMine.unpersist()
        }
      } else {
      println(s"La transformación para el patrón $pattern ya existe. No es necesario recalcular.")
    }
  }
  

  def transformProduct(spark: SparkSession, pattern: String, loadFile: String, outputPath: String): Unit = {
    val WirteFileTransformPath =  s"$outputPath/${pattern.stripSuffix(".csv")}"
    if (!fileExists(WirteFileTransformPath)) {
      val filePath = s"$loadFile/$pattern"
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
          saveAndShow(consulta, WirteFileTransformPath, s"${pattern.stripSuffix(".csv")}_${index}")
        }
        dfFilteredProductos.unpersist()
      }
    } else {
    println(s"La transformación para el patrón $pattern ya existe. No es necesario recalcular.")
    }
  }
  
  def transformVentasInternet(spark: SparkSession, pattern: String, loadFile: String, outputPath: String): Unit = {
    val WirteFileTransformPath =  s"$outputPath/${pattern.stripSuffix(".csv")}"
    if (!fileExists(WirteFileTransformPath)) {
      val filePath = s"$loadFile/$pattern"
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
          saveAndShow(consulta, WirteFileTransformPath, s"${pattern.stripSuffix(".csv")}_${index}")
        }
        dfFilteredVentasInternet.unpersist()
      }
    } else {
    println(s"La transformación para el patrón $pattern ya existe. No es necesario recalcular.")
    }
  }  

  def saveAndShow(df: DataFrame, outputPath: String, fileName: String): Unit = {
    df.write.mode("overwrite").parquet(s"$outputPath/$fileName")
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

    if (Files.exists(path) && !Files.isDirectory(path)) {
      Files.delete(path)
    }

    if (!Files.exists(path)) {
      Files.createDirectories(path)
      println(s"Directorio creado: $directoryPath")
    }
  }


  def isDataFrameCached(df: DataFrame): Boolean = {
    try {
      df.storageLevel != org.apache.spark.storage.StorageLevel.NONE
    } catch {
      case _: Throwable => false
    }
  }
  def readCsv(spark: SparkSession, fullPath: String): DataFrame = {
    spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(fullPath)
  }

 
  def deleteDirectory(directoryPath: String): Unit = {
    val root: Path = Paths.get(directoryPath)

    if (!Files.exists(root)) {
      println(s"El directorio $directoryPath no existe.")
      createDirectory(directoryPath)
      return
    }

    val transformedDir: Path = root.resolve("transformed").toAbsolutePath

    // Obtener todos los paths usando solo APIs Java
    val stream = Files.walk(root)
    val allPaths = try {
      stream.collect(Collectors.toList[Path])
    } finally {
      stream.close()
    }

    // Ordenar de mayor a menor longitud → archivos primero, luego carpetas
    val sortedPaths = allPaths.toArray(new Array[Path](allPaths.size()))
      .sortWith(_.toString.length > _.toString.length)

    sortedPaths.foreach { filePath =>
      val abs = filePath.toAbsolutePath

      // Evitar eliminar la carpeta "transformed" y su contenido
      if (!abs.startsWith(transformedDir)) {
        try {
          Files.deleteIfExists(filePath)
          println(s"Eliminado: $filePath")
        } catch {
          case ex: Exception =>
            println(s"ERROR eliminando $filePath: ${ex.getMessage}")
        }
      }
    }

    println(s"Directorio procesado (excepto 'transformed'): $directoryPath")
  }
}



