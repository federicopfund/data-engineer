# Utiliza una imagen base de Hadoop
FROM sequenceiq/hadoop-docker:latest


# Configura las variables de entorno para Hadoop
ENV HADOOP_HOME /usr/local/hadoop
ENV HADOOP_CONF_DIR /usr/local/hadoop/etc/hadoop

ENV PATH $PATH:$HADOOP_HOME/bin

# Copiar la configuración personalizada de Hadoop
COPY conf/core-site.xml $HADOOP_CONF_DIR/core-site.xml
COPY conf/hdfs-site.xml $HADOOP_CONF_DIR/hdfs-site.xml

#  Copiar la configuración personalizada de Hadoop
COPY conf/core-site.xml usr/local/hadoop/share/hadoop/common/templates/core-site.xml
COPY conf/hdfs-site.xml usr/local/hadoop/share/hadoop/hdfs/templates/hdfs-site.xml

# Formatear el sistema de archivos HDFS
RUN $HADOOP_HOME/bin/hdfs namenode -format



