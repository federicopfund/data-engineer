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
    val hadoopConf = new Configuration()
    val archivos = Array("Categoria.csv", "FactMine.csv", "Mine.csv", "Producto.csv", "VentasInternet.csv")
    val containerName = "namenode"
    val command = Seq("sh", "-c", s"""docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $containerName""")
    val result = command.!!
    val numeros: Array[Int] = result.trim.split('.').map(_.toInt)
    val direccionIP: String = numeros.mkString(".")
    val hdfsUri: String = s"hdfs://$direccionIP:9000"
    val hdfsWorkingDir = "/user/fede/landing/csv"
    hdfs.runloadinHdfs(hadoopConf, archivos, hdfsUri, hdfsWorkingDir)
    val spark = SparkSessionSingleton.getSparkSession
    funcTransform.processFile(spark, archivos)
    spark.stop()
  }
}

