# Aplicación Spark – Procesamiento de Ventas Online

## Descripción del proyecto

El objetivo principal de este proyecto es la construcción de una **aplicación de procesamiento de datos basada en Apache Spark**, orientada al tratamiento de archivos en formato **CSV** que contienen información de **ventas online**.

A partir de una **tabla de hechos provista por el cliente**, el proyecto implementa un proceso de **normalización en dimensiones**, aplicando principios de modelado analítico con el fin de preparar los datos para su posterior consumo en herramientas de Business Intelligence.

La solución está diseñada bajo una arquitectura escalable, desacoplada y orientada a procesamiento distribuido, alineada con buenas prácticas de **Data Engineering**.

---

## Responsabilidades clave y logros

### Transformación ETL con Apache Spark

- Diseño e implementación de procesos de **Extracción, Transformación y Carga (ETL)** utilizando **Apache Spark**.
- Procesamiento eficiente de datos **estructurados y no estructurados**.
- Normalización de la tabla de hechos en dimensiones analíticas.
- Optimización de cargas mediante procesamiento distribuido.

---

### Almacenamiento de datos con Apache Hadoop

- Implementación de **Apache Hadoop (HDFS)** como solución de almacenamiento principal.
- Diseño de una arquitectura de almacenamiento eficiente y escalable.
- Optimización de procesos de escritura y lectura de datos dentro del ecosistema Hadoop.
- Integración de capas de datos alineadas a un enfoque de Data Lake.

---

### Integración del entorno Databricks

- Uso de **Databricks** como entorno colaborativo para ingeniería y ciencia de datos.
- Integración fluida con el ecosistema de BI existente.
- Ejecución y orquestación de notebooks Spark para procesamiento avanzado.
- Mejora de la productividad del equipo mediante capacidades colaborativas.

---

### Automatización con Azure Data Factory

- Implementación de **Azure Data Factory** para la automatización completa de la canalización ETL.
- Diseño y orquestación de pipelines para ejecución programada y controlada.
- Integración de notebooks y procesos Spark dentro de flujos automatizados.
- Optimización del flujo end-to-end de procesamiento de datos.

---

### Integración con Data Lake

- Integración de la salida de los procesos ETL en un **Data Lake centralizado**.
- Garantía de **consistencia, accesibilidad y seguridad** de los datos.
- Preparación de los datos para consumo analítico y reporting.
- Alineación con arquitecturas modernas de datos (Data Lake / Lakehouse).

---

### Visualización con Power BI

- Consumo de datos transformados desde el Data Lake en **Power BI**.
- Desarrollo de **dashboards interactivos** y orientados a negocio.
- Visualización de métricas clave para facilitar la toma de decisiones basada en datos.
- Habilitación de análisis exploratorio y reporting dinámico.

---

## Resultado del proyecto

El proyecto dio como resultado una **infraestructura de Business Intelligence robusta y escalable**, capaz de manejar distintos volúmenes y tipos de datos.

La integración de **Apache Spark, Hadoop, Databricks, Azure Data Factory y Power BI** permitió construir una **canalización de datos end-to-end**, completamente automatizada, desde la ingesta hasta la visualización.

Los procesos implementados:
- Mejoraron la eficiencia operativa.
- Reducieron la intervención manual.
- Permitieron obtener información casi en tiempo real mediante visualizaciones dinámicas.

---

## Conclusiones clave

Este proyecto demuestra la capacidad de:
- Diseñar arquitecturas modernas de datos.
- Integrar tecnologías de vanguardia dentro del ecosistema de BI.
- Implementar y optimizar soluciones de **Data Engineering de extremo a extremo**.

La ejecución exitosa del proyecto refleja experiencia en:
- Procesamiento distribuido.
- Modelado analítico.
- Automatización de pipelines.
- Visualización avanzada de datos.

---

## Testing y versionado

### Creación de tags de versión

<details>
<summary>Comandos</summary>
<br />

```bash
git tag -a v0.0.3 -m "Release versión 0.0.3"
git push origin --tags
