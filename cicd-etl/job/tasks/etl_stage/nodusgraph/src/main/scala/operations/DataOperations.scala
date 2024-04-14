package com.Vortex.etl.operations


abstract class DataOperation {
  def description: String
  def execute(): scala.util.Try[String]
}

class ExtractOperation(src: String) extends DataOperation {
  def description: String = s"Extract from $src"
  def execute(): scala.util.Try[String] = {
    println(s"Extracting data from $src...")
    scala.util.Success("Data extracted")
  }
}

class TransformOperation(transformation: String) extends DataOperation {
  def description: String = s"Transform using $transformation"
  def execute(): scala.util.Try[String] = {
    println(s"Applying transformation: $transformation...")
    scala.util.Success("Data transformed")
  }
}

class LoadOperation(dest: String) extends DataOperation {
  def description: String = s"Load into $dest"
  def execute(): scala.util.Try[String] = {
    println(s"Loading data into $dest...")
    scala.util.Success("Data loaded")
  }
}
