package scala.hadoop

import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.permission.FsPermission
import org.apache.hadoop.fs.{FileSystem, Path, FileStatus}

object HadoopConnection  extends App {

  val fileList = Array("Categoria.csv", "FactMine.csv", "Subcategoria.csv", "Mine.csv", "Producto.csv", "VentasInternet.csv")
  val hadoopConf = new Configuration()
  
    // Crear una instancia del sistema de archivos HDFS
  val fs = FileSystem.get(hadoopConf)
  
 
    // Ruta del sistema de archivos HDFS en el clúster Dockerizado
  val hdfsUri = "hdfs://172.19.0.2:9000"


    // Directorio de trabajo en HDFS
  val hdfsWorkingDir = "/user/fede/landing/csv"

  val path = new Path(hdfsWorkingDir)
    // hdfs url
  val pathhdfsString = "/user/fede/landing/csv/tranform"
  val pathhdfs: Path = new Path(pathhdfsString)
  createdirectory(pathhdfs)

    // Listar archivos en el directorio de trabajo
  listFiles(hdfsWorkingDir)

  fileList.foreach { archivo =>
    val filePath = s"./src/main/resources/csv/$archivo"
    val hdfsDestination = s"$hdfsWorkingDir/$archivo"

      // Subir un archivo al nuevo directorio
    uploadFile(filePath, hdfsDestination)

      // Listar archivos después de cargar el archivo
    listFiles(hdfsWorkingDir)

      // Descargar el archivo desde HDFS al sistema local
    val localDestination = s"./src/main/resources/hdfs/csv/$archivo"
    downloadFile(hdfsDestination, localDestination)
  }
   
  fs.close()
  
 
  def createdirectory(pathhdfs: Path): Unit = {
    if (!fs.exists(pathhdfs)) {
      fs.mkdirs(pathhdfs)
      fs.setPermission(pathhdfs, new FsPermission("777"))
      println(s"Directorio creado: $pathhdfs")
    } else {
      println(s"El directorio $pathhdfs ya existe.")
    }
  }

  def listFiles(directory: String): Unit = {
    val path = new Path(directory)
    val fileStatuses = fs.listStatus(path)
    println(s"Archivos en $directory:")
    fileStatuses.foreach(fileStatus => println(s" - ${fileStatus.getPath.getName}"))
  }

  def uploadFile(localPath: String, hdfsDestination: String): Unit = {
    val localFile = new Path(localPath)
    val hdfsFile = new Path(hdfsDestination)
    fs.copyFromLocalFile(localFile, hdfsFile)
    println(s"Archivo subido: $localPath -> $hdfsDestination")
  }

  def downloadFile(hdfsSource: String, localDestination: String): Unit = {
    val hdfsFile = new Path(hdfsSource)
    val localFile = new Path(localDestination)
    fs.copyToLocalFile(hdfsFile, localFile)
    println(s"Archivo descargado: $hdfsSource -> $localDestination")
  }
}
