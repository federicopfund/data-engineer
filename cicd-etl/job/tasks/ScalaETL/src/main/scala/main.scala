
package main

import scala.sparkSession.SparkSessionSingleton
import scala.transform.funcTranform
import org.apache.spark.sql.SparkSession



object MainETL {

  def main(args: Array[String]): Unit = {
    val archivos = Array("Categoria.csv", "FactMine.csv", "Mine.csv", "Producto.csv", "VentasInternet.csv")
    val spark = SparkSessionSingleton.getSparkSession
    funcTranform.processFile(spark, archivos)      
    spark.stop() 
  }
}