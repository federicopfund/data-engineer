package main

import scala.sparkSession.SparkSessionSingleton
import scala.transform.{funcTransform,hdfs}
import org.apache.spark.sql.SparkSession
import org.apache.log4j.PropertyConfigurator
import org.apache.hadoop.conf.Configuration
import sys.process._

object MainETL {

  def main(args: Array[String]): Unit = {
    PropertyConfigurator.configure(getClass.getResource("/log4j.properties"))
    val archivos = Array("Categoria.csv", "FactMine.csv", "Mine.csv", "Producto.csv", "VentasInternet.csv")
    val spark = SparkSessionSingleton.getSparkSession
    funcTransform.processFile(spark, archivos)
    spark.stop()
  }
}

