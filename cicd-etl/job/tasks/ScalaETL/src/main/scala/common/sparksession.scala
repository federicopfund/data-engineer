package scala.common.sparkSession

import org.apache.spark.sql.SparkSession

object SparkSessionSingleton {

  @transient private var instance: SparkSession = _

  var absolutePath: String = _
  def getSparkSession: SparkSession = {
    if (instance == null) {
      synchronized {
        if (instance == null) {

         // val absolutePath =
           // new java.io.File("./src/main/resources/csv/transformed").getCanonicalPath
          // Builder base con Delta Lake + optimizaciones mínimas
          var builder = SparkSession.builder()
            .appName("SparkSessionExample")
              .config("spark.sql.warehouse.dir", "hdfs://localhost:9001/hive/warehouse/")
              .config("spark.hadoop.fs.defaultFS", "hdfs://localhost:9001")
              .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
              .config("spark.sql.shuffle.partitions", "8")
              .config("hive.metastore.uris", "")
              .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
              .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
              
          // Detectamos si spark-submit ya definió spark.master
          val masterFromSubmit = System.getProperty("spark.master", "")

          if (masterFromSubmit == "" || masterFromSubmit.startsWith("local")) {
            // Ejecutando desde sbt o modo local
            builder = builder.master("local[*]")
            println(">>> SparkSession ejecutándose en LOCAL (sbt run)")
          } else {
            // Ejecutando en cluster standalone
            println(s">>> SparkSession ejecutándose en CLUSTER: $masterFromSubmit")
          }

          instance = builder.getOrCreate()
        }
      }
    }
    instance
  }
}
