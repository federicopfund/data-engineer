package scala.transform

import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.permission.FsPermission
import org.apache.hadoop.fs.{FileSystem, Path, FileStatus, FileUtil}
import org.apache.log4j.{Level, Logger}


object hdfs {
  
  private val logger = Logger.getLogger(getClass.getName)
  private var fs: FileSystem = _

  def initFileSystem(hadoopConf: Configuration, hdfsUri: String): Unit = {
    hadoopConf.set("fs.defaultFS", hdfsUri)
    fs = FileSystem.get(hadoopConf)
  }

  def runloadinHdfs(hadoopConf: Configuration, archivos: Array[String], hdfsUri: String, hdfsWorkingDir: String): Unit = {

    initFileSystem(hadoopConf, hdfsUri)

    // Configuración de la URI del sistema de archivos HDFS
    hadoopConf.set("fs.defaultFS", hdfsUri)
    
    // Crear una instancia del sistema de archivos HDFS
    val path = new Path(hdfsWorkingDir)

    // Establecer permisos en el directorio
    val permission = new FsPermission("777")
    fs.setPermission(path, permission)

    try {
      if (!fs.exists(path)) {
        // Si no existe, crearlo
        fs.mkdirs(path)
      } else {
        logger.info(s"El directorio $hdfsWorkingDir ya existe.")
        listFiles(fs, hdfsWorkingDir)
      }

      // Iterate over the tables and perform operations
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
    } catch {
      case e: Exception =>
        logger.error(s"Error en la ejecución: ${e.getMessage}")
    } finally {
      closeFileSystem()      
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
  
  def closeFileSystem(): Unit = {
    if (fs != null) {
      fs.close()
    }
  }
}
