import asyncio 

from pydantic import BaseModel, Field
from typing import Union

from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import json
import datetime
import random

from Logic.DataframeLogic import DataframeLogic
from Models.RequestItemModel import Item
from Models.BoughtItemModel import BoughtItem
from Models.AdditemModel import ItemAdd
from Data.DbContext import Context

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

dflogic = DataframeLogic()

with open("config.json") as file:
    config = json.load(file)

datalake_account_access_key = config['datalake']['datalake_account_access_key']
datalake_container = config['datalake']['datalake_container']
datalake_container2 = config['datalake']['datalake_container2']
datalake_account_name = config['datalake']['datalake_account_name']

context = Context(config['database']['server'], config['database']['database'], config['database']['username'], 
   config['database']['password'], config['database']['driver'])
cnxn = context.connect()

# Producto Unico
df_og = pd.read_csv(f'abfs://{datalake_container}@{datalake_account_name}.dfs.core.windows.net/Producto_Unico.csv',storage_options = {'account_key': datalake_account_access_key})
# Producto Sucursales
df2_og = pd.read_csv(f'abfs://{datalake_container}@{datalake_account_name}.dfs.core.windows.net/Producto_Sucursales.csv',storage_options = {'account_key': datalake_account_access_key})
# Ventas Producto Unico
df_ventas_og = pd.read_csv(f'abfs://{datalake_container}@{datalake_account_name}.dfs.core.windows.net/VentasInternet_Unico.csv',storage_options = {'account_key': datalake_account_access_key})
# Categoria
df_cat = pd.read_csv(f'abfs://{datalake_container}@{datalake_account_name}.dfs.core.windows.net/dboCategoria.csv',storage_options = {'account_key': datalake_account_access_key})
# Subcategoria
df_subcat = pd.read_csv(f'abfs://{datalake_container}@{datalake_account_name}.dfs.core.windows.net/dboSubCategoria.csv',storage_options = {'account_key': datalake_account_access_key})

@app.get("/productos")
async def getProductos(ignoreEmpty: bool = False):
    '''Devuelve todos los productos'''
    # Lee dataframes y variables 
    df = df_og.copy()

    # Si el query parameter ignoreEmpty es true entonces ignora las sucursales vacias
    if ignoreEmpty:
        df2 = df2_og[df2_og['Stock'] != 0].copy()
    else:
        df2 = df2_og.copy()
    
    # Devuelve dataframe filtrado
    join = dflogic.filterDataframes(df,df2)

    return json.loads(join.to_json(orient='records'))


@app.get("/producto/{id_producto}")
async def getProductoById(id_producto: int, response: Response, ignoreEmpty: bool = False):
    '''Devuelve el producto que tenga cierto ID'''
    # Lee dataframes
    df = df_og.copy()

    # Si el query parameter ignoreEmpty es true entonces ignora las sucursales vacias
    if ignoreEmpty:
        df2 = df2_og[df2_og['Stock'] != 0].copy()
    else:
        df2 = df2_og.copy()

    # Filtra por el producto pedido
    df = df.loc[df['Cod_Producto'] == id_producto]
    
    # Devuelve dataframe filtrado
    join = dflogic.filterDataframes(df,df2)

    if df.shape[0] != 0:
        return json.loads(join.to_json(orient='records'))
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error" : f"No existe el producto con id {id_producto}."}


@app.get('/categorias')
async def getCategorias():
    '''Devuelve todas las categorias'''
    # Lee dataframes y variables 
    df = df_cat.copy()

    return json.loads(df.to_json(orient='records'))


@app.get("/categoria/{id_categoria}")
async def getProductoByCategory(id_categoria: int, response: Response):
    '''Devuelve los productos bajo cierta categoria'''
    # Lee dataframes
    df = df_og.copy()
    df2 = df2_og.copy()
    # Filtra por la categoria pedida
    df = df.loc[df['Cod_Categoria'] == id_categoria]
    
    # Devuelve dataframe filtrado
    join = dflogic.filterDataframes(df,df2)

    if df.shape[0] != 0:
        return json.loads(join.to_json(orient='records'))
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error" : f"No existe la categoria con id {id_categoria}."}


@app.get('/subcategorias')
async def getSubcategorias():
    '''Devuelve todas las subcategorias'''
    # Lee dataframes y variables 
    df = df_subcat.copy()

    return json.loads(df.to_json(orient='records'))


@app.get("/subcategoria/{id_subcategoria}")
async def getProductoBySubcategory(id_subcategoria: int, response: Response):
    '''Devuelve los productos bajo cierta subcategoria'''
    # Lee dataframes
    df = df_og.copy()
    df2 = df2_og.copy()
    # Filtra por la subcategoria
    df = df.loc[df['Cod_Subcategoria'] == id_subcategoria]
    
    # Devuelve dataframe filtrado
    join = dflogic.filterDataframes(df,df2)
    
    if df.shape[0] != 0:
        return json.loads(join.to_json(orient='records'))
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error" : f"No existe subcategoria con id {id_subcategoria}."}


@app.get("/categoria/{id_categoria}/subcategoria/{id_subcategoria}")
async def getProductoByCategory(id_categoria: int, id_subcategoria: int, response: Response, ignoreEmpty: bool = False):
    '''Devuelve los productos bajo cierta categoria que corresponden a una subcategoria'''
    # Lee dataframes
    df = df_og.copy()

    # Si el query parameter ignoreEmpty es true entonces ignora las sucursales vacias
    if ignoreEmpty:
        df2 = df2_og[df2_og['Stock'] != 0].copy()
    else:
        df2 = df2_og.copy()

    # Filtra por la subcategoria y categoria pedida
    df = df.loc[(df['Cod_Categoria'] == id_categoria) & (df['Cod_Subcategoria'] == id_subcategoria)]
    
    # Devuelve dataframe filtrado
    join = dflogic.filterDataframes(df,df2)

    if df.shape[0] != 0:
        return json.loads(join.to_json(orient='records'))
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error" : f"La subcategoria {id_subcategoria} no pertenece a la categoria {id_categoria}, o alguna de estas dos no existe."}


@app.put('/producto/{id}')
async def create_item(id: int, item: Item, response: Response):
    if item.user == config['user1']['username'] and item.password == config['user1']['password']:
        
        global df2_og
        # Lee dataframes
        df = df_og.copy()
        df2 = df2_og.copy()

        df = df.loc[df['Cod_Producto'] == id]
        
        if df.shape[0] == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error":f"El producto con id {id} no se encuentra en la lista de productos."}
        
        df2 = DataframeLogic.stockUpItem(id, item.stock, df2)

        # Actualiza los valores en la base de datos
        with cnxn.cursor() as cursor:
            for index, row in df2.loc[df2['Cod_Producto'] == id].iterrows():
                cursor.execute("""
                    UPDATE dbo.Productos_Sucursales
                    SET Stock = ?
                    WHERE Cod_Producto = ? AND Cod_Sucursal = ?""", int(row['Stock']), id, int(row['Cod_Sucursal']))
        cnxn.commit()

        # Devuelve dataframe filtrado
        join = dflogic.filterDataframes(df,df2)

        df2_og = df2
        #guardo en otro container para no sobreescribir el anterior
        df2.to_csv(f'abfs://{datalake_container}@{datalake_account_name}.dfs.core.windows.net/Producto_Sucursales.csv',storage_options = {'account_key': datalake_account_access_key} ,index=False)

        return json.loads(join.to_json(orient='records'))
    
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"error":"El usuario o la contraseña no son validos"}


@app.put('/comprar/{id}')
async def buyItem(id: int, item: BoughtItem, response: Response):
    global df2_og
    global df_ventas_og

    df = df_og.copy()
    df2 = df2_og.copy()
    ventas = df_ventas_og.copy()

    df = df.loc[df['Cod_Producto'] == id]

    if df.shape[0] == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error":f"El producto con id {id} no se encuentra en la lista de productos."}
    
    df2 = DataframeLogic.buyProduct(id, item.Cantidad, item.Sucursal, df2)

    if df2 is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error":f"No se puede comprar una cantidad mayor al stock disponible."}

    with cnxn.cursor() as cursor:
            cursor.execute("""
                UPDATE dbo.Productos_Sucursales
                SET Stock = ?
                WHERE Cod_Producto = ? AND Cod_Sucursal = ?""", 
                int(df2.loc[(df2['Cod_Producto'] == id) & (df2['Cod_Sucursal'] == item.Sucursal), 'Stock']), id, item.Sucursal)
    cnxn.commit()
    
    #Devuelve dataframe filtrado
    join = dflogic.filterDataframes(df,df2)

    today = datetime.datetime.now()
    precio_unitario = random.random()*3578.27+3.99
    costo_unitario = precio_unitario * (ventas['CostoUnitario'] / ventas['PrecioUnitario']).agg('mean')

    # Agrego el registro de venta al df de ventas con datos que me saque principalmente de la galera
    ventas.loc[len(ventas)] = [id, ventas['Cod_Cliente'].max()+1, item.Sucursal, 
        f"SO{ventas['NumeroOrden'].apply(lambda x: int(x[2:])).max()+1}", item.Cantidad, 
        round(precio_unitario,2), round(costo_unitario,2), round(precio_unitario * 0.08,2), 
        round(precio_unitario * 0.025,2), today.strftime("%Y-%m-%d %H:%M:%S"), (today+datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S"), 
        (today+datetime.timedelta(days=12)).strftime("%Y-%m-%d %H:%M:%S"), 1]

    df2_og = df2
    df_ventas_og = ventas
    
    # Comento la subida del csv de ventas porque tarda demasiado (18 segundos en mi caso)
    #ventas.to_csv(f'abfs://{datalake_container}@{datalake_account_name}.dfs.core.windows.net/VentasInternet_Unico.csv',storage_options = {'account_key': datalake_account_access_key} ,index=False)
    df2.to_csv(f'abfs://{datalake_container}@{datalake_account_name}.dfs.core.windows.net/Producto_Sucursales.csv',storage_options = {'account_key': datalake_account_access_key} ,index=False)
    
    #return json.loads(join.to_json(orient='records'))
    return json.loads(ventas.loc[len(ventas)-1].to_json())



@app.post('/productos/')
async def create_item(item: ItemAdd, response: Response):
    global df2_og
    global df_og

    if item.user == config['user1']['username'] and item.password == config['user1']['password']:
        prod_suc_add = df2_og.copy()
        prod_unico_add = df_og.copy()

        #print(prod_unico_add.loc[prod_unico_add['Producto'] == item.name].shape[0])
        if prod_unico_add.loc[prod_unico_add['Producto'] == item.name].shape[0] > 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"error":f"El producto {item.name} ya se encuentra en la lista de productos."}

        prod_unico_add.loc[len(prod_unico_add)]=[1+len(prod_unico_add),str(item.name),item.subcat,item.cat]
        max = prod_suc_add['Cod_Producto'].max()

        for i in range(len(item.sucursales)):
            prod_suc_add.loc[len(prod_suc_add)]=[max+1,i+1,item.sucursales[i],item.sucursales[i],{'Cod_Sucursal': (i+1), 'Stock': (item.sucursales[i])}]

        df2_og = prod_suc_add
        df_og = prod_unico_add

        with cnxn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO dbo.Producto_Unico (Producto, Cod_Subcategoria, Cod_Categoria)
                VALUES (?, ?, ?)""", 
                item.name, item.subcat, item.cat)
            
            for index, row in prod_suc_add.loc[prod_suc_add['Cod_Producto'] == max+1].iterrows():
                cursor.execute("""
                    INSERT INTO dbo.Productos_Sucursales (Cod_Producto, Cod_Sucursal, Stock, Stock_Inicial)
                    VALUES (?, ?, ?, ?)""", 
                    int(row['Cod_Producto']), int(row['Cod_Sucursal']), int(row['Stock']), int(row['Stock_Inicial']))
        cnxn.commit()

        #Devuelve dataframe filtrado
        join = dflogic.filterDataframes(prod_unico_add.loc[prod_unico_add['Cod_Producto'] == len(prod_unico_add)], prod_suc_add)

        prod_suc_add.to_csv(f'abfs://{datalake_container}@{datalake_account_name}.dfs.core.windows.net/Producto_Sucursales.csv',storage_options = {'account_key': datalake_account_access_key},index=False,encoding='utf-8')
        prod_unico_add.to_csv(f'abfs://{datalake_container}@{datalake_account_name}.dfs.core.windows.net/Producto_Unico.csv',storage_options = {'account_key': datalake_account_access_key},index=False,encoding='utf-8')

        return json.loads(join.to_json(orient='records'))
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"error":"El usuario o la contraseña no son validos"}
    