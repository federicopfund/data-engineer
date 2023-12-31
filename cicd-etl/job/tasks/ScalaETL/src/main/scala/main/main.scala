import org.apache.spark.sql.SparkSession
import scala.sparkSession.SparkSessionSingleton
import scala.etl.Functions_etl
import scala.hadoop.HadoopConnection


object MainETL {


  def main(args: Array[String]): Unit = {
   
    val archivos = Array("Categoria.csv", "FactMine.csv", "Mine.csv", "Producto.csv", "VentasInternet.csv")
    val spark = SparkSessionSingleton.getSparkSession

    try {
      
      Functions_etl.processPatternsParallel(spark, archivos)
    } finally {
      spark.stop()
    }
  }
}
