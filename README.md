## Modernización de la infraestructura de inteligencia empresarial

Los almacenes de datos relacionales se encuentran en el centro de la mayoría de las soluciones de inteligencia empresarial (BI). Aunque los detalles específicos pueden variar entre implementaciones de almacenamiento de datos, un patrón común basado en un esquema desnormalizado y multidimensional ha surgido como el diseño estándar de un almacenamiento de datos relacional.


Al igual que todas las bases de datos relacionales, un almacenamiento de datos contiene tablas en las que se almacenan los datos que quiere analizar. Normalmente, estas tablas se organizan en un esquema optimizado para el modelado multidimensional, en el que las medidas numéricas asociadas a eventos conocidos como hechos se pueden agregar mediante los atributos de las entidades asociadas en varias dimensiones. 

### Descripción del proyecto:
>
 Proyecto integral orientado a la modernización de la infraestructura de Business Intelligence (BI). El objetivo principal del proyecto era construir un data warehouse a través de una tabla de hechos proporcionada por el cliente. Dicha tabla contenía toda la lógica de negocio integrada, lo que nos llevó a desarrollar ingeniería inversa para descubrir las dimensiones subyacentes.

Como resultado, se desarrollaron tablas multidimensionales centradas en eventos específicos del negocio, lo que nos permitió identificar nuevas oportunidades en logística y distribución de productos. A través de este análisis, logramos desarrollar una nueva algoritmia que permitía distribuir los productos en función de la demanda sectorial. Gracias a esto, la empresa experimentó una mejora significativa en la calidad del servicio de distribución.

Además, este proyecto sentó las bases para el desarrollo de una metodología que permitiría evaluar la eficacia operativa de cada sucursal en función de las ventas realizadas.

## Responsabilidades clave y logros:

### Transformación ETL con Apache Spark:

>Lideré el diseño e implementación de procesos de Extracción, Transformación, Carga (ETL) utilizando tecnologías Apache Spark. Aseguró una transformación perfecta de datos internos y externos, estructurados y no estructurados.

### Almacenamiento de datos con Apache Hadoop:
>Implementé Apache Hadoop como solución de almacenamiento principal, optimizando los procesos de almacenamiento y recuperación de datos. Colaboré con el equipo para diseñar una arquitectura de almacenamiento de datos eficiente dentro del marco de Hadoop.
### Integración del entorno de Databricks:
>Utilicé el entorno Databricks para mejorar las capacidades colaborativas de ingeniería y ciencia de datos. Aseguré la integración fluida de Databricks en el ecosistema de BI existente para flujos de trabajo optimizados.
### Automatización de fábrica de datos de Azure:
>Implementé Azure Data Factory para automatizar la ejecución de la canalización ETL sin problemas. Diseñé y orquesté cuadernos "Pipeline", optimizando el flujo de trabajo general de procesamiento de datos.

### Integración de Data Lake:
>Integró con éxito la salida de los procesos ETL en un DataLake centralizado. Se garantizó la coherencia, accesibilidad y seguridad de los datos dentro del entorno de DataLake.

### Power BI Visualizacion:
>Aprovechó Power BI para visualizar y presentar datos transformados. Desarrollé paneles de control interactivos y reveladores para facilitar la toma de decisiones basada en datos.
### Resultado del proyecto:
>El proyecto dio como resultado una infraestructura de BI robusta y escalable, capaz de manejar diversos tipos de datos y requisitos de procesamiento. Al incorporar Apache Spark, Hadoop, Databricks, Azure Data Factory y Power BI, logramos una canalización de datos perfecta de un extremo a otro. Los procesos automatizados no solo mejoraron la eficiencia sino que también permitieron obtener información en tiempo real a través de visualizaciones dinámicas de Power BI.

### Conclusiones clave:
>Este proyecto mostró mi capacidad para navegar e integrar varias tecnologías de vanguardia en el panorama de BI. La ejecución exitosa del proyecto resalta mi competencia en el diseño, implementación y optimización de soluciones de BI de un extremo a otro que satisfacen las necesidades cambiantes de las organizaciones basadas en datos.
# 


**Testing and releasing**
<details>
<summary>Comandos</summary>
<br />

```
git tag -a v<0.0.3> -m "Release tag for version <0.0.3>"
git push origin --tags
```
<br />
</details>
<br />

**Testing and releasing**
<details>
<summary>Integrantes </summary>
<br />


```
Integrantes
        root
            |-- Carlos Eduardo Denett: string (nullable = true)
            |-- Cecilia Marcela Espada : string (nullable = true)
            |-- Federico Pfund: string (nullable = true)
            |-- Juan Martín Elena: integer (nullable = true)
            |-- Agustín Fernández: string (nullable = true)
            |-- Patricio Perrone: integer (nullable = true)


```
