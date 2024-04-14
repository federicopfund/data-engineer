package main

object etlStateGraph extends App {
  val dag = new com.vortex.etl.core.DAG[String]

  val node1 = new com.vortex.etl.core.Node("1", new com.Vortex.etl.operations.ExtractOperation("DataSource1"))
  val node2 = new com.vortex.etl.core.Node("2", new com.Vortex.etl.operations.TransformOperation("Filter and clean"))
  val node3 = new com.vortex.etl.core.Node("3", new com.Vortex.etl.operations.LoadOperation("DataWarehouse"))

  node1.connectTo(node2)
  node2.connectTo(node3)

  dag.addNode(node1)
  dag.addNode(node2)
  dag.addNode(node3)

  println("DAG Operations Plan:")
  println(dag)

  println("\nTopological Sorting and Execution:")
  dag.executeGraph()
}
