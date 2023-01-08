# 
## 1) Instalacion de Java y Scala:

> Si no tienes instalado el jdk de java:
```bash
sudo apt update
sudo apt install openjdk=11.0.17 
java --version
```
#### Output
```bash
openjdk 11.0.17 2022-10-18
OpenJDK Runtime Environment (build 11.0.17+8-post-Ubuntu-1ubuntu222.04)
OpenJDK 64-Bit Server VM (build 11.0.17+8-post-Ubuntu-1ubuntu222.04, mixed mode, sharing)
```
> Instalar Scala:  
```bash
sudo apt install scala
scala -version
```
#### Output
```bash
Scala code runner version 2.11.12 -- Copyright 2002-2017, LAMP/EPFL
```

# Instalar Apache Spark
 
>Descargar la última versión.

[link](https://archive.apache.org/dist/spark/spark-3.3.1/)

```bash
cd /tmp
wget https://archive.apache.org/dist/spark/spark-3.3.1/spark-3.3.1-bin-hadoop3.tgz 
```

> Extraiga el archivo descargado y muévalo al /opt directorio, renombrado como spark e elimina de archivos temporales el relese.
```bash
tar -xvzf spark-3.3.1-bin-hadoop3.tgz 
sudo mv spark-3.3.1-bin-hadoop3.tgz /opt/spark
sudo rm -r spark-3.3.1-bin-hadoop3.tgz 
```
>Cree variables de entorno para poder ejecutar y ejecutar Spark:
```bash
nano ~/.bashrc
```
>Agregue las líneas en la parte inferior del archivo y guárdelo.
```bash
export SPARK_HOME=/opt/spark

export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
```
>Ejecute los siguientes comandos para aplicar los cambios de su entorno.
```bash
source ~/.bashrc
```
# Inicie Apache Spark.
>En este punto, Apache Spark está instalado y listo para usar. 
> Ejecute los siguientes comandos para iniciarlo.
```bash
cd /opt/spark

./sbin/start-master.sh
```
>Inicie el proceso de trabajo de Spark ejecutando los siguientes comandos.
```
./sbin/start-slave.sh spark://localhost:7077
```
>Puede reemplazar el host localhost con el nombre de host del servidor o la dirección IP.
```
http://localhost:8080
```

>Si deseas conectarse a Spark a través de su shell de comandos, ejecute los siguientes comandos:
```
./sbin/spark-shell
```
# Run ETL
>Run Spark App si el clon fuen en Documents.

```
./bin/spark-submit \
                --master spark://fede:7077 \
                 $HOME/Documents/notebooks/cicd-etl/job/tasks/etl.py

```

>### Testing and releasing 


```
git tag -a v<your-project-version> -m "Release tag for version <your-project-version>"
git push origin --tags
```
