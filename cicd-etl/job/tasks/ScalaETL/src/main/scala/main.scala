package main

import scala.sparkSession.SparkSessionSingleton
import scala.transform.{funcTranform, Hdfs}
import org.apache.spark.sql.SparkSession
import org.apache.log4j.PropertyConfigurator

object MainETL {

  def main(args: Array[String]): Unit = {
    // Configure Log4j
    PropertyConfigurator.configure(getClass.getResource("/log4j.properties"))

    // Array of files to be processed
    val archivos = Array("Categoria.csv", "FactMine.csv", "Mine.csv", "Producto.csv", "VentasInternet.csv")

    // Run HDFS script to handle HDFS operations
    Hdfs.runloadinHdfs(archivos)

    // Get SparkSession using the SparkSessionSingleton
    val spark = SparkSessionSingleton.getSparkSession

    // Process files using Spark
    funcTranform.processFile(spark, archivos)

    // Stop SparkSession
    spark.stop()
  }
}
