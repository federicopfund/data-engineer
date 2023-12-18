import sbt._

val sparkVersion = "2.4.8"

lazy val root = (project in file("."))
  .settings(
    // Configuración básica del proyecto
    inThisBuild(List(
      organization := "Vortex",
      scalaVersion := "2.12.13"
    )),
    name := "tranform",
    version := "0.0.1",

    // Dependencias del proyecto
    libraryDependencies ++= Seq(
      "org.apache.spark" %% "spark-core" % sparkVersion,
      "org.apache.spark" %% "spark-sql" % sparkVersion,
      "org.apache.spark" %% "spark-kubernetes" % sparkVersion,
      "org.scalatest" %% "scalatest" % "3.2.9" % Test
    )
  )
