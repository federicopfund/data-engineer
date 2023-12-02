
from ast import List
import pyodbc 
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port

server = 'tcp:miservidors.database.windows.net,1433' 
database = 'miBaseDeDatosDeEjemplo' 
username = 'db' 

# Specifying the ODBC driver, server name, database, etc. directly


## Obtener la información de conexión

def conectaAK47(server,database,username,password):
    with pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
        ## hacemos la primer consulta
            cursor.execute('''SELECT TOP 20 pc.Name as CategoryName, p.name as ProductName
                            FROM SalesLT.ProductCategory pc
                            JOIN SalesLT.Product p
                            ON pc.productcategoryid = p.productcategoryid;''')
        
            row = cursor.fetchone()
            while row:
                print('name:', row[1])   # access by column index (zero-based)

                print (str(row[0]) + " " + str(row[1]))
                
                if not row:
                    break
            else:
                print(row)
                print(f"podemos acceder a los nombre: {row[0]}")
                
def conecta(server,database,username,password):
    conentado = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)              
    # Create a cursor from the connection
    cursor = conentado.cursor()
    return cursor
  
    
    
def consultaSQL(consulta):
    cursor = conecta(server,database,username,password)
    cursor.execute(consulta)
    contador=0
    ##print(help(cursor)) Te sera de mucha ayuda para ver las entrañas de la clase!!
    while True:
        contador +=1
       ## 'fetchone()':
       #   -  devuelve none cuando se recuperan todas las columnas
        row = cursor.fetchone() 
        if not row:
            break
        print(f"Consulta {contador}° : {row}")
    #print(help(on))

        
consulta1='''SELECT TOP 20 pc.Name as CategoryName, p.name as ProductName
                            FROM SalesLT.ProductCategory pc
                            JOIN SalesLT.Product p
                            ON pc.productcategoryid = p.productcategoryid;'''

consulta='''SELECT ProductID, Name, Color,	
            ListPrice,ProductNumber,
            StandardCost FROM SalesLT.Product;'''
            
consulta3='''SELECT  Name FROM SalesLT.ProductModel;'''
consulta4='''SELECT  UnitPrice FROM SalesLT.SalesOrderDetail;'''
consultaConClausula='''SELECT  * FROM SalesLT.SalesOrderDetail WHERE UnitPrice>356.8980 ;'''
consultaConClausula2='''SELECT  TOP 20 Name, ListPrice, StandardCost FROM SalesLT.Product WHERE StandardCost >= 400 and StandardCost <= 1000;'''
consultaConClausulaOR2='''SELECT  TOP 20 Name, ListPrice, StandardCost FROM SalesLT.Product WHERE StandardCost < 800 OR StandardCost > 870;'''
#consultaSQL(consultaConClausulaOR2)

def insertaData():
    cursor = conecta(server,database,username,password)
    cursor.execute(consulta)
    
insertaData("insert into products(id, name), values (pyodbc awesomelibrary")