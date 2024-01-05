package scala.sparkSession

import org.apache.spark.sql.SparkSession
import java.nio.file.attribute.BasicFileAttributes
import java.nio.file.{Paths, Files}


object SparkSessionSingleton {

  @transient private var instance: SparkSession = _

  def getSparkSession: SparkSession = {
    if (instance == null) {
      synchronized {
        if (instance == null) {
          val absolutePath = new java.io.File("./src/main/resources/csv").getCanonicalPath
          instance = SparkSession.builder
                .appName("SparkSessionExample")
                    .master("local[2]")
                    .config("spark.some.config.option", "config-value")
                    .config("spark.authenticate", "true")
                    .config("spark.authenticate.secret", "fede")
                    .config("spark.ssl.enabled", "true")
                    .config("spark.ssl.keyPassword", "fede")
                    .config("spark.ssl.keystore", "path/to/your/keystore")
                    .config("spark.executor.memory", "2g")
                    .config("spark.executor.cores", "3")
                    .config("spark.driver.memory", "1g")
                    .config("spark.driver.maxResultSize", "1g")
                    .config("spark.executor.instances", "2")
                    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
                    .config("spark.default.parallelism", "4")
                    .config("spark.shuffle.compress", "true")
                    .config("spark.shuffle.manager", "tungsten-sort")
                    .config("spark.shuffle.file.buffer", "1m")
                    .config("spark.sql.shuffle.partitions", "8")
                    .config("spark.sql.autoBroadcastJoinThreshold", "10485760")
                    .config("spark.sql.inMemoryColumnarStorage.batchSize", "10000")
                    .config("spark.sql.inMemoryColumnarStorage.compressed", "true")
                    .config("spark.sql.broadcastTimeout", "300")
                    .config("spark.streaming.receiver.writeAheadLog.enable", "true")
                    .config("spark.sql.catalogImplementation", "in-memory")
                    .config("spark.sql.warehouse.dir", s"file:$absolutePath/")
                    .config("spark.dynamicAllocation.enabled", "true")
                    .config("spark.dynamicAllocation.initialExecutors", "2")
                    .config("spark.dynamicAllocation.minExecutors", "1")
                    .config("spark.dynamicAllocation.maxExecutors", "5")
                    .config("spark.executor.logs.rolling.maxRetainedFiles", "5")
                    .config("spark.executor.logs.rolling.strategy", "time")
                    .config("spark.executor.logs.rolling.time.interval", "daily")
                    .config("spark.executor.logs.rolling.maxSize", "100M")
                    .config("spark.sql.statistics.histogram.enabled", "true")
                    .config("spark.sql.statistics.histogram.bins", "100")
                .getOrCreate()
        }
      }
    }
    instance
  }
}
