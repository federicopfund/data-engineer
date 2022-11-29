import pyodbc

class Context:
    
    def __init__(self, server, database, username, password, driver):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.driver = driver
    

    def connect(self):
        return pyodbc.connect('DRIVER='+ self.driver +';SERVER=tcp:'+self.server +';PORT=1433;DATABASE='+self.database+
            ';UID='+self.username+';PWD='+ self.password)

    
    def cursor(self):
        return self.connect().cursor()