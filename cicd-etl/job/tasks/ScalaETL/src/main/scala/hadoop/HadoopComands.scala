package scala.hadoop

import scala.sys.process._
import java.util.concurrent.TimeUnit


object DockerHadoop extends App {

  def main(args: Array[String]): Boolean = {
    start(args)
  }

  def start(args: Array[String]): Boolean = {
    if (!isNamenodeRunning()) {
      println("Los servicios en Docker Compose no están activos. Iniciando Docker Compose...")
      // Intentar iniciar Docker Compose
      
      if (!startDockerCompose()) {
        println("No se pudo iniciar Docker Compose. Saliendo del programa.")
        false
      } else {
        // Docker Compose iniciado correctamente, ejecutar comandos de Hadoop
        executeHadoopCommands()
        true
      }
    } else {
      // Los servicios ya están activos, ejecutar directamente comandos de Hadoop
      executeHadoopCommands()
      true
    }
  }

 
  def isNamenodeRunning(): Boolean = {
    // Obtener la ruta del directorio del usuario
    val userHome = System.getProperty("user.home")

    // Cambiar al directorio que contiene docker-compose.yml
    val changeDirectoryCmd = Seq("bash", "-c", s"cd $userHome/Documentos/data-engineer/deploy/hadoop")
    changeDirectoryCmd.!

    // Verificar si el servicio namenode está en ejecución
    val isNamenodeRunningCmd = Seq("docker-compose", "ps", "--quiet", "--filter", "status=running", "namenode")
    (isNamenodeRunningCmd #| Seq("grep", "-q", ".*")).! == 0
  }

  def executeHadoopCommands(): Unit = {
    // Definir los comandos de Hadoop con tiempos de espera (10 segundos en este ejemplo)
    val hadoopCommands = Seq(
      "docker exec -i namenode hadoop fs -mkdir /user",
      "docker exec -i namenode hadoop fs -mkdir /user/fede",
      "docker exec -i namenode hadoop fs -mkdir /user/fede/landing",
      "docker exec -i namenode hadoop fs -mkdir /user/fede/landing/csv",
      "docker exec -i namenode hadoop fs -mkdir /user/fede/landing/csv/transform",
      "docker exec -i namenode hadoop fs -chmod 777 /user/fede/landing/csv",
      "docker exec -i namenode hadoop fs -chown fede:hadoop /user/fede/landing/csv",
      "docker exec -i namenode hadoop fs -chmod 777 /user/fede/landing/csv/transform",
      "docker exec -i namenode hadoop fs -chown fede:hadoop /user/fede/landing/csv/transform",
      "docker exec -i namenode hdfs dfsadmin -report",
      "docker exec -i namenode hdfs dfsadmin -refreshNodes"
    )

    // Ejecutar los comandos de Hadoop
    hadoopCommands.foreach { command =>
      val processBuilder = Process(Seq("bash", "-c", command))
      val exitCode = processBuilder.!
      if (exitCode != 0) {
        println(s"Error al ejecutar el comando: $command")
      }
    }
  }

  def startDockerCompose(): Boolean = {
    // Obtener la ruta del directorio del usuario
    val userHome = System.getProperty("user.home")

    // Cambiar al directorio que contiene docker-compose.yml y ejecutar Docker Compose
    val dockerComposeUpCmd = Seq("docker-compose", "start")
    val processBuilder = Process(dockerComposeUpCmd, new java.io.File(s"$userHome/Documentos/data-engineer/deploy/hadoop"))
    val exitCode = processBuilder.!

    if (exitCode != 0) {
      println("Error al intentar iniciar Docker Compose.")
      false
    } else {
      true
    }
  }
}
