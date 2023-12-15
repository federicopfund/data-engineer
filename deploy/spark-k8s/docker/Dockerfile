# Labels
LABEL maintainer="Federico Pfund <federicopfund@email.com>"
LABEL description="Imagen de Apache Spark 3.2.0 con Hadoop 3.3.1 y configuraciones personalizadas."

# Base image
FROM openjdk:11

# Define Spark and Hadoop versions
ENV SPARK_VERSION=3.2.0
ENV HADOOP_VERSION=3.3.1

# Download and install Hadoop
RUN mkdir -p /opt && \
    cd /opt && \
    curl http://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz | \
        tar -zx hadoop-${HADOOP_VERSION}/lib/native && \
    ln -s hadoop-${HADOOP_VERSION} hadoop && \
    echo "Hadoop ${HADOOP_VERSION} native libraries installed in /opt/hadoop/lib/native"

# Download and install Spark
RUN mkdir -p /opt && \
    cd /opt && \
    curl http://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop2.7.tgz | \
        tar -zx && \
    ln -s spark-${SPARK_VERSION}-bin-hadoop2.7 spark && \
    echo "Spark ${SPARK_VERSION} installed in /opt"


ADD spark-master /app/spark-master
ADD spark-worker /app/spark-worker
ADD spark-defaults.conf /opt/spark/conf/spark-defaults.conf
ENV PATH $PATH:/opt/spark/bin

# Additional configurations in spark-defaults.conf
RUN echo "# Configuraciones Avanzadas" >> /opt/spark/conf/spark-defaults.conf \
    && echo "spark.executor.extraJavaOptions -Dsome.property=value" >> /opt/spark/conf/spark-defaults.conf \
    && echo "spark.sql.shuffle.partitions 200" >> /opt/spark/conf/spark-defaults.conf \
    && echo "spark.streaming.receiver.writeAheadLog.enable true" >> /opt/spark/conf/spark-defaults.conf



