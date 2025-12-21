package main

import scala.common.sparkSession.SparkSessionSingleton
import scala.ingest.hdfs
import scala.transform.funcTransform
import org.apache.spark.sql.SparkSession
import org.apache.log4j.PropertyConfigurator
import org.apache.hadoop.conf.Configuration
import sys.process._

object MainETL {

  def main(args: Array[String]): Unit = {
    PropertyConfigurator.configure(getClass.getResource("/log4j.properties"))

    val hdfsUriRoot = "hdfs://localhost:9001"
    val localCsvPath = "/home/fede/Documentos/data-engineer/cicd-etl/job/tasks/ScalaETL/src/main/resources/csv"
    

    // 1. Crear arquitectura del datalake
    hdfs.createDatalakeStructure(hdfsUriRoot)

    // 2. Subir archivos a RAW
    hdfs.uploadToRaw(hdfsUriRoot, localCsvPath)

    println("=== POC FINALIZADA ===")
    val archivos = Array("Categoria.csv", "FactMine.csv", "Mine.csv", "Producto.csv", "VentasInternet.csv")
    val spark = SparkSessionSingleton.getSparkSession
    // ETL Spark - Hadoop
    funcTransform.processFile(spark, archivos, hdfsUriRoot)
    spark.stop()
  }
}

