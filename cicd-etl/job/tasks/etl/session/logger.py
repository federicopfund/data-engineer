
# https://logging.apache.org/log4j/2.x/log4j-users-guide.pdf

class Log4j(object):
    """
    Clase Wrapper para el objeto Log4j JVM.
    :param spark: objeto SparkSession.
    """
    def __init__(self, spark):
        log4j = spark._jvm.org.apache.log4j
        conf = spark.sparkContext.getConf()
        app_id = conf.get('spark.app.id')
        app_name = conf.get("spark.app.name")
        message_pre  = '<' + app_name + ' ' + app_id + '>'
        self.logger = log4j.LogManager.getLogger(message_pre)

    def warn(self, message):
        """Registra una advertencia.
            :param: Mensaje de advertencia para escribir en el registro
            :Volver a la lista:
        """
        self.logger.warn(message)

    def info(self, message):
        self.logger.info(message)   
    
    def error(self, message):
        """Registra un error.
            :param: mensaje de error para escribir en el registro
            :Volver a la lista:
        """
        self.logger.error(message)
    

    def debug(self, message):
        self.logger.debug(message)