# Utiliza una imagen base de Hadoop
FROM sequenceiq/hadoop-docker:latest


# Configura las variables de entorno para Hadoop
ENV HADOOP_HOME /usr/local/hadoop
ENV HADOOP_CONF_DIR /usr/local/hadoop/etc/hadoop

ENV PATH $PATH:$HADOOP_HOME/bin

# Copiar la configuración personalizada de Hadoop
COPY conf/core-site.xml $HADOOP_CONF_DIR/core-site.xml
COPY conf/hdfs-site.xml $HADOOP_CONF_DIR/hdfs-site.xml

# Formatear el sistema de archivos HDFS
RUN $HADOOP_HOME/bin/hdfs namenode -format


# Crear un directorio en el contenedor
RUN mkdir -p $HADOOP_HOME/sourcecontainer

COPY csv/Categoria.csv $HADOOP_HOME/sourcecontainer/Categoria.csv
COPY csv/FactMine.csv $HADOOP_HOME/sourcecontainer/FactMine.csv
COPY csv/Mine.csv $HADOOP_HOME/sourcecontainer/Mine.csv
COPY csv/Subcategoria.csv $HADOOP_HOME/sourcecontainer/Subcategoria.csv
COPY csv/Sucursales.csv $HADOOP_HOME/sourcecontainer/Sucursales.csv
COPY csv/Ventasinternet.csv $HADOOP_HOME/sourcecontainer/Ventasinternet.csv

