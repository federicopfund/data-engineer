package com.vortex.etl.core

class Node[T](val value: T, val operation: com.mycompany.etl.operations.DataOperation) {
  var edges: List[Node[T]] = Nil
  var level: Int = 0  // Hierarchical level in the DAG

  def connectTo(node: Node[T]): Unit = {
    if (!edges.exists(_ == node) && node != this && !hasPathTo(node)) {
      edges = node :: edges
      node.level = Math.max(node.level, this.level + 1)
    }
  }

  def hasPathTo(target: Node[T]): Boolean =
    edges.contains(target) || edges.exists(_.hasPathTo(target))

  override def toString: String =
    s"Node(${value.toString}, Level $level, Operation ${operation.description})"
}
