
import scala.sparkSession.SparkSessionSingleton
import scala.etl.Functions_etl
import scala.hadoop.{Hadoop,DockerHadoop}
import org.apache.spark.sql.SparkSession



object MainETL {

  def main(args: Array[String]): Unit = {
    val archivos = Array("Categoria.csv", "FactMine.csv", "Mine.csv", "Producto.csv", "VentasInternet.csv")
    val spark = SparkSessionSingleton.getSparkSession
    Functions_etl.processPatternsParallel(spark, archivos)      
    spark.stop() 
  }
}