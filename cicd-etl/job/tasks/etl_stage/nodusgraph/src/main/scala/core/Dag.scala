package com.vortex.etl.core

class DAG[T] {
  var nodes: List[Node[T]] = Nil

  def addNode(node: Node[T]): Unit = {
    nodes = node :: nodes
  }

  def executeGraph(): Unit = {
    topologicalSort().foreach { node =>
      println(s"Executing operation at Node ${node.value}")
      node.operation.execute() match {
        case scala.util.Success(message) => println(message)
        case scala.util.Failure(exception) => println(s"Failed to execute operation: ${exception.getMessage}")
      }
    }
  }

  private def topologicalSort(): List[Node[T]] = {
    var result = List.empty[Node[T]]
    var tempMarked = scala.collection.mutable.Set.empty[Node[T]]
    var permMarked = scala.collection.mutable.Set.empty[Node[T]]

    def visit(n: Node[T]): Unit = {
      if (permMarked.contains(n)) return
      if (tempMarked.contains(n)) throw new RuntimeException("Cycle detected in DAG")
      tempMarked += n

      n.edges.foreach(visit)
      tempMarked -= n
      permMarked += n
      result = n :: result
    }

    nodes.foreach(visit)
    result.reverse
  }

  override def toString: String =
    nodes.map(node => s"${node.toString} -> ${node.edges.map(_.toString).mkString(", ")}").mkString("\n")
}



