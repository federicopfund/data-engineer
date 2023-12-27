import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.permission.FsPermission
import org.apache.hadoop.fs.{FileSystem, Path, FileStatus}

object HadoopConnectionExample extends App {

  // Configuración de Hadoop
  val hadoopConf = new Configuration()
  val Archivos = Array("Categoria.csv", "FactMine.csv","Subcategoria.csv", "Mine.csv", "Producto.csv", "VentasInternet.csv")

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
  if (!fs.exists(path)) {
    // Si no existe, crearlo
    fs.mkdirs(path)
    fs.setPermission(path, new FsPermission("777"))
    println(s"Directorio creado: $hdfsWorkingDir")
  } else {
    println(s"El directorio $hdfsWorkingDir ya existe.")
  }

  // Listar archivos en el directorio de trabajo
  listFiles(hdfsWorkingDir)

  // Iterar sobre las tablas y realizar operaciones
  Archivos.foreach { archivo =>
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

  // Cerrar la conexión al sistema de archivos HDFS
  fs.close()

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
