package scala.transform

import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.permission.FsPermission
import org.apache.hadoop.fs.{FileSystem, Path, FileStatus, FileUtil}
import org.apache.log4j.{Level, Logger}

object Hdfs {

  // Verificar si el directorio ya existe en HDFS

  def runloadinHdfs(archivos: Array[String]): Unit = {
    // Configuración de Hadoop
    val hadoopConf = new Configuration()
    val logger = Logger.getLogger(getClass.getName)

    // Ruta del sistema de archivos HDFS en el clúster Dockerizado
    val hdfsUri = "hdfs://172.19.0.2:9000"

    // Configuración de la URI del sistema de archivos HDFS
    hadoopConf.set("fs.defaultFS", hdfsUri)

    // Directorio de trabajo en HDFS
    val hdfsWorkingDir = "/user/fede/landing/csv"

    // Crear una instancia del sistema de archivos HDFS
    val fs = FileSystem.get(hadoopConf)
    val path = new Path(hdfsWorkingDir)

    // Verificar si el directorio ya existe en HDFS
    try {
      if (!fs.exists(path)) {
        // Si no existe, crearlo
        fs.mkdirs(path)
        fs.setPermission(path, new FsPermission("777"))
         // Iterar sobre las tablas y realizar operaciones
        archivos.foreach { archivo =>
          val filePath = s"./src/main/resources/csv/$archivo"
          val hdfsDestination = s"$hdfsWorkingDir/$archivo"

          // Subir un archivo al nuevo directorio
          uploadFile(fs, filePath, hdfsDestination)

          // Listar archivos después de cargar el archivo
          listFiles(fs, hdfsWorkingDir)

          // Descargar el archivo desde HDFS al sistema local
          val localDestination = s"./src/main/resources/hdfs/csv/$archivo"
          downloadFile(fs, hdfsDestination, localDestination)
        logger.info(s"Directorio creado: $hdfsWorkingDir")
        }
      } else {
        logger.info(s"El directorio $hdfsWorkingDir ya existe.")
        listFiles(fs, hdfsWorkingDir)
      }
    } catch {
      case e: Exception =>
        logger.error(s"Error en la ejecución: ${e.getMessage}")
    } finally {
      // Cerrar la conexión al sistema de archivos HDFS
      if (fs != null) {
        fs.close()
      }
    }
  }

  def listFiles(fs: FileSystem, directory: String): Unit = {
    val path = new Path(directory)
    val fileStatuses = fs.listStatus(path)
    val logger = Logger.getLogger(getClass.getName)
    logger.info(s"Archivos en $directory:")
    fileStatuses.foreach(fileStatus => logger.info(s" - ${fileStatus.getPath.getName}"))
  }

  def uploadFile(fs: FileSystem, localPath: String, hdfsDestination: String): Unit = {
    val localFile = new Path(localPath)
    val hdfsFile = new Path(hdfsDestination)
    fs.copyFromLocalFile(localFile, hdfsFile)
    val logger = Logger.getLogger(getClass.getName)
    logger.info(s"Archivo subido: $localPath -> $hdfsDestination")
  }

  def downloadFile(fs: FileSystem, hdfsSource: String, localDestination: String): Unit = {
    val hdfsFile = new Path(hdfsSource)
    val localFile = new Path(localDestination)
    fs.copyToLocalFile(hdfsFile, localFile)
    val logger = Logger.getLogger(getClass.getName)
    logger.info(s"Archivo descargado: $hdfsSource -> $localDestination")
  }

  def deleteFile(fs: FileSystem, hdfsPath: String): Unit = {
    val fileToDelete = new Path(hdfsPath)
    if (fs.exists(fileToDelete)) {
      fs.delete(fileToDelete, true) // El segundo parámetro indica si se debe eliminar recursivamente si es un directorio
      val logger = Logger.getLogger(getClass.getName)
      logger.info(s"Archivo eliminado: $hdfsPath")
    } else {
      val logger = Logger.getLogger(getClass.getName)
      logger.info(s"El archivo $hdfsPath no existe en HDFS.")
    }
  }
}
