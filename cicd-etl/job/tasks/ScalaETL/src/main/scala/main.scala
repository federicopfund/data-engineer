package main

import scala.sparkSession.SparkSessionSingleton
import scala.transform.{funcTransform,hdfs}
import org.apache.spark.sql.SparkSession
import org.apache.log4j.PropertyConfigurator
import org.apache.hadoop.conf.Configuration


object MainETL {

  def main(args: Array[String]): Unit = {
    PropertyConfigurator.configure(getClass.getResource("/log4j.properties"))
    val hadoopConf = new Configuration()
    val archivos = Array("Categoria.csv", "FactMine.csv", "Mine.csv", "Producto.csv", "VentasInternet.csv")
    val hdfsUri = "hdfs://172.19.0.5:9000"
    val hdfsWorkingDir = "/user/fede/landing/csv"

    // Call the method from the Hdfs object
    hdfs.runloadinHdfs(hadoopConf, archivos, hdfsUri, hdfsWorkingDir)

    // Get SparkSession using the SparkSessionSingleton
    val spark = SparkSessionSingleton.getSparkSession

    // Process files using Spark
    funcTransform.processFile(spark, archivos)

    // Stop SparkSession
    spark.stop()
  }
}
