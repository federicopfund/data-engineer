// give the user a nice default project!

val sparkVersion = settingKey[String]("Spark version")

lazy val root = (project in file(".")).
  settings(
    inThisBuild(List(
      organization := "nodus",
      scalaVersion := "2.12.13"
    )),
    name := "nodusgraph",
    version := "0.0.1",

    sparkVersion := "3.3.0",


    libraryDependencies ++= Seq(
      "org.apache.spark" %% "spark-sql" % "3.3.0" % "provided",
      "com.snowflake" % "snowpark" % "1.11.0",
      "org.scalatest" %% "scalatest" % "3.2.2" % "test",
      "org.scalacheck" %% "scalacheck" % "1.15.2" % "test",
      "com.holdenkarau" %% "spark-testing-base" % "3.3.0_1.3.0" % "test"
    ),
    Global / excludeLintKeys += SettingKey[String]("sparkVersion")
  )
