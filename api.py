import asyncio 
from fastapi import FastAPI
import pandas as pd
import json
from Logic.DataframeLogic import DataframeLogic

app = FastAPI()

dflogic = DataframeLogic()

with open("config.json") as file:
    config = json.load(file)

datalake_account_access_key = config['datalake']['datalake_account_access_key']
datalake_container = config['datalake']['datalake_container']
datalake_account_name = config['datalake']['datalake_account_name']

df_og = pd.read_csv(f'abfs://{datalake_container}@{datalake_account_name}.dfs.core.windows.net/Producto_Unico.csv',storage_options = {'account_key': datalake_account_access_key})
df2_og = pd.read_csv(f'abfs://{datalake_container}@{datalake_account_name}.dfs.core.windows.net/Producto_Sucursales.csv',storage_options = {'account_key': datalake_account_access_key})


@app.get("/productos")
async def getProductos():
    '''Devuelve todos los productos'''
    # Lee dataframes y variables 
    df = df_og.copy()
    df2 = df2_og.copy()
    
    # Devuelve dataframe filtrado
    join = dflogic.filterDataframes(df,df2)

    return {"dataframe" : json.loads(join.to_json(orient='records'))}


@app.get("/producto/{id_producto}")
async def getProductoById(id_producto: int):
    '''Devuelve el producto que tenga cierto ID'''
    # Lee dataframes
    df = df_og.copy()
    df2 = df2_og.copy()
    # Filtra por el producto pedido
    df = df.loc[df['Cod_Producto'] == id_producto]
    
    # Devuelve dataframe filtrado
    join = dflogic.filterDataframes(df,df2)

    if df.shape[0] != 0:
        return {"dataframe" : json.loads(join.to_json(orient='records'))}
    else:
        return {"error" : f"No existe el producto con id {id_producto}"}


@app.get("/categoria/{id_categoria}")
async def getProductoByCategory(id_categoria: int):
    '''Devuelve los productos bajo cierta categoria'''
    # Lee dataframes
    df = df_og.copy()
    df2 = df2_og.copy()
    # Filtra por la categoria pedida
    df = df.loc[df['Cod_Categoria'] == id_categoria]
    
    # Devuelve dataframe filtrado
    join = dflogic.filterDataframes(df,df2)

    if df.shape[0] != 0:
        return {"dataframe" : json.loads(join.to_json(orient='records'))}
    else:
        return {"error" : f"No existe la categoria con id {id_categoria}"}


@app.get("/categoria/{id_categoria}/subcategoria/{id_subcategoria}")
async def getProductoByCategory(id_categoria: int, id_subcategoria: int):
    '''Devuelve los productos bajo cierta categoria que corresponden a una subcategoria'''
    # Lee dataframes
    df = df_og.copy()
    df2 = df2_og.copy()
    # Filtra por la subcategoria y categoria pedida
    df = df.loc[(df['Cod_Categoria'] == id_categoria) & (df['Cod_Subcategoria'] == id_subcategoria)]
    
    # Devuelve dataframe filtrado
    join = dflogic.filterDataframes(df,df2)

    if df.shape[0] != 0:
        return {"dataframe": json.loads(join.to_json(orient='records'))}
    else:
        return {"error" : f"La subcategoria {id_subcategoria} no pertenece a la categoria {id_categoria}"}


@app.get("/subcategoria/{id_subcategoria}")
async def getProductoBySubcategory(id_subcategoria: int):
    '''Devuelve los productos bajo cierta subcategoria'''
    # Lee dataframes
    df = df_og.copy()
    df2 = df2_og.copy()
    # Filtra por la subcategoria
    df = df.loc[df['Cod_Subcategoria'] == id_subcategoria]
    
    # Devuelve dataframe filtrado
    join = dflogic.filterDataframes(df,df2)
    
    if df.shape[0] != 0:
        return {"dataframe" : json.loads(join.to_json(orient='records'))}
    else:
        return {"error" : f"No existe subcategoria con id {id_subcategoria}"}

@app.get('/test/{id_producto}')
async def sepaDios(id_producto: int):
    global df2_og
    # Lee dataframes
    df = df_og.copy()
    df2 = df2_og.copy()

    df2 = DataframeLogic.stockUpItem(1, 100, df2)

    df2_og = df2
    
    return {"dataframe": json.loads(df2.to_json(orient='records'))}
