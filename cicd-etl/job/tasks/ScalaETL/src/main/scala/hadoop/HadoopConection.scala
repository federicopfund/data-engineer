package scala.hadoop

import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.permission.FsPermission
import org.apache.hadoop.fs.{FileSystem, Path, FileStatus}

object Hadoop extends App {

  def main(fileList: Array[String]): Unit = {
    val hadoopConf = new Configuration()
    val fs = FileSystem.get(hadoopConf)
    val hdfsWorkingDir = "/user/fede/landing/csv"
    val transformDir = "/user/fede/landing/csv/transform"
    val transformPath: Path = new Path(transformDir)

    createDirectory(transformPath)
    listFiles(hdfsWorkingDir)

    fileList.foreach { archivo =>
      val filePath = s"./src/main/resources/csv/$archivo"
      val hdfsDestination = s"$hdfsWorkingDir/$archivo"

      uploadFile(filePath, hdfsDestination)
      listFiles(hdfsWorkingDir)

      val localDestination = s"./src/main/resources/hdfs/csv/$archivo"
      downloadFile(hdfsDestination, localDestination)
    }

    fs.close()
  }

  def createDirectory(path: Path): Unit = {
    val fs = FileSystem.get(new Configuration())
    if (!fs.exists(path)) {
      fs.mkdirs(path)
      fs.setPermission(path, new FsPermission("777"))
      println(s"Directorio creado: $path")
    } else {
      println(s"El directorio $path ya existe.")
    }
    fs.close()
  }

  def listFiles(directory: String): Unit = {
    val fs = FileSystem.get(new Configuration())
    val path = new Path(directory)
    val fileStatuses = fs.listStatus(path)
    println(s"Archivos en $directory:")
    fileStatuses.foreach(fileStatus => println(s" - ${fileStatus.getPath.getName}"))
    fs.close()
  }

  def uploadFile(localPath: String, hdfsDestination: String): Unit = {
    val fs = FileSystem.get(new Configuration())
    val localFile = new Path(localPath)
    val hdfsFile = new Path(hdfsDestination)
    fs.copyFromLocalFile(localFile, hdfsFile)
    println(s"Archivo subido: $localPath -> $hdfsDestination")
    fs.close()
  }

  def downloadFile(hdfsSource: String, localDestination: String): Unit = {
    val fs = FileSystem.get(new Configuration())
    val hdfsFile = new Path(hdfsSource)
    val localFile = new Path(localDestination)
    fs.copyToLocalFile(hdfsFile, localFile)
    println(s"Archivo descargado: $hdfsSource -> $localDestination")
    fs.close()
  }
}
