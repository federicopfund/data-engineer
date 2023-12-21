import sbt._
import sbtassembly.AssemblyPlugin.autoImport._

val sparkVersion = "2.4.8"

lazy val commonSettings = Seq(
  organization := "Vortex",
  scalaVersion := "2.12.13",
  version := "0.0.1"
)

lazy val libraryDeps = Seq(
  "org.apache.spark" %% "spark-core" % sparkVersion,
  "org.apache.spark" %% "spark-sql" % sparkVersion,
  "org.scalatest" %% "scalatest" % "3.2.9" % Test
)

// Configuración del proyecto
lazy val root = (project in file("."))
  .settings(
    commonSettings,
    libraryDependencies ++= libraryDeps,
    assembly / parallelExecution := true, // Habilitar la ejecución en paralelo
    assemblyExcludedJars := assemblyExcludedJars.value
  )
  .enablePlugins(AssemblyPlugin)
  .settings(
    assembly / parallelExecution := true
  )
Global / excludeLintKeys += root / assembly / parallelExecution
