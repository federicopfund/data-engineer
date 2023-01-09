# 
## 1) Instalacion de `Java` y `Scala`:

> Si no tienes instalado el jdk de java:
```bash
sudo apt update
sudo apt install openjdk=11.0.17 
java --version
```
#### `Output:`
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
#### `Output:`
```bash
Scala code runner version 2.11.12 -- Copyright 2002-2017, LAMP/EPFL
```

# Instalar `Apache Spark`
 
>Descargar la última versión.

[link](https://archive.apache.org/dist/spark/spark-3.3.1/)

```bash
cd /tmp
wget https://archive.apache.org/dist/spark/spark-3.3.1/spark-3.3.1-bin-hadoop3.tgz 
```

> Extraiga el archivo descargado y muévalo al `/opt` directorio, renombrado como `spark` e elimina de archivos temporales el relese.
```bash
tar -xvzf spark-3.3.1-bin-hadoop3.tgz 
sudo mv spark-3.3.1-bin-hadoop3.tgz /opt/spark
sudo rm -r spark-3.3.1-bin-hadoop3.tgz 
```
>Cree variables de entorno para poder ejecutar y ejecutar `Spark`:
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
# Inicie Apache `Spark`.
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
# Path de data:
> Ahora Moveremos la careta data al lugar indicado: seguramente te encuentras en el `path:`  /opt/spark:
> Pocisionate en la carpeta donde esta data Osea:

```
cd --
cd Documents/notebooks
```
>Es posible que veas la carpeta data:
>Ahora mueve esa carpeta a: `opt/spark/spark-warehouse.`

```
mv data ../../../../opt/spark/spark-warehouse
```
>Ahora  vuelve a: `opt/spark`:
```
cd /opt/spark
```
>Analiza el directorio, veras las carpeta `csv` dentro de `spark-warehouse.` con todos los archivos a tranformar. asegurate que se encuentre dicha carpeta. recuerda la carpeta csv dentro de   `spark-warehouse.`.

```
ls -l
```

# Run `ETL`
>Run Spark App si el clon fuen en Documents.

```
./bin/spark-submit \
                --master spark://localhost:7077 \
                 $HOME/Documents/notebooks/cicd-etl/job/tasks/etl.py

```
>En mi caso solo para el archivo VentasInternet.csv:
```
./bin/spark-submit \
                --master spark://fede:7077 \
                 $HOME/Documents/notebooks/cicd-etl/job/tasks/etl.py VentasInternet.csv

```
> Si quiere ejecutar todas las tranformaciones con el siguiente comando:

```
./bin/spark-submit --master spark://fede:7077 \
                    $HOME/Documents/notebooks/cicd-etl/job/tasks/etl.py\
                     VentasInternet.csv \
                     Categoria.csv \
                     FactMine.csv \
                     Producto.csv \
                     MIne.csv

```
> Recuerda tienes que estar parado en el directorio ```/opt/spark ```y tener la carpeta de ```csv``` proveniente de ```data``` en 
```spark-warehouse```.
> Tiempo de ejucion total: ```36.316101``` ms.  tranquilo bucaremos mayor eficiencia.

>### Testing and releasing 


```
git tag -a v<0.0.3> -m "Release tag for version <0.0.3>"
git push origin --tags
```
