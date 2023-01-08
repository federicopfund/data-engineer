
# https://logging.apache.org/log4j/2.x/log4j-users-guide.pdf

class Log4j(object) -> logger:
    """
    Clase Wrapper para el objeto Log4j JVM.
    :param spark: objeto SparkSession.
    """
    def __init__(self, spark) -> LogManager:
         """ Obtener detalles de la aplicación Spark
              Contructor_
         """
        log4j = spark._jvm.org.apache.log4j
        conf = spark.sparkContext.getConf()
        app_id = conf.get('spark.app.id')
        app_name = conf.get("spark.app.name")
        message_pre  = '<' + app_name + ' ' + app_id + '>'
        self.logger = log4j.LogManager.getLogger(message_pre)

    def warn(self, message) -> None:
        """Registra una advertencia.
            :param: Mensaje de advertencia para escribir en el registro
            :Volver a la lista:
        """
        self.logger.warn(message)
        return None

    def info(self, message) -> None:
         """Información de registro.
                :param: Mensaje de información para escribir en el registro
                :Volver a la lista:
        """
        self.logger.info(message)
        return None

    def error(self, message) -> None:
        """Registra un error.
            :param: mensaje de error para escribir en el registro
            :Volver a la lista:
        """
        self.logger.error(message)
        return None

    def debug(self, message) -> None:
        self.logger.debug(message)
        return None
