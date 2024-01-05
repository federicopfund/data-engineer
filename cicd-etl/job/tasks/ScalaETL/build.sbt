import sbt._
import sbtassembly.AssemblyPlugin.autoImport._

val sparkVersion = "2.4.8"
val hadoopVersion = "3.0.0"

lazy val commonSettings = Seq(
  organization := "Vortex",
  scalaVersion := "2.12.13",
  version := "0.0.1"
)

lazy val libraryDeps = Seq(
  "org.apache.spark" %% "spark-core" % sparkVersion,
  "org.apache.spark" %% "spark-sql" % sparkVersion,
  "org.scalatest" %% "scalatest" % "3.2.9" % Test,
  "org.apache.hadoop" % "hadoop-client" % "2.2.0"
)

lazy val root = (project in file("."))
  .settings(
    commonSettings,
    libraryDependencies ++= libraryDeps,
    assembly / parallelExecution := true,
    assemblyExcludedJars := assemblyExcludedJars.value
  )
  .enablePlugins(AssemblyPlugin)
  .settings(
    assembly / parallelExecution := true
  )

lazy val transform = (project in file("src/main/scala/transform")).settings(name := "scala.transform")

lazy val sparksession = (project in file("src/main/scala/sparksession")).settings(name := "scala.sparkSession")

Global / excludeLintKeys += root / assembly / parallelExecution
