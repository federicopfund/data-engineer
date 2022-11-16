import asyncio 
from fastapi import FastAPI
import pandas as pd
import json

app = FastAPI()

# @app.get("/productos")
# async def getProductos():
#     '''Devuelve todos los productos'''
#     await asyncio.sleep(1)
#     df = pd.read_csv("Datasets locales/Producto_Unico.csv", index_col=0)
#     return {"dataframe" : json.loads(df.to_json(orient='records'))}

@app.get("/productos")
async def getProductos():
    '''Devuelve todos los productos'''
    # Lee dataframes y variables 
    datalake_account_access_key = 'tUkrsYf++bJtSl/fXv9rtVhvTxIxh+3pzuWgA41vR3LtnbCV9xefC4ImN8XVLmk5ZxphFCGfN9mY+AStxYp14A=='
    datalake_container = 'csv'
    datalake_account_name = 'datalake123cd4567'

    df = pd.read_csv(f'abfs://{datalake_container}@{datalake_account_name}.dfs.core.windows.net/Producto_Unico.csv',storage_options = {'account_key': datalake_account_access_key})
    df2 = pd.read_csv(f'abfs://{datalake_container}@{datalake_account_name}.dfs.core.windows.net/Producto_Sucursales.csv',storage_options = {'account_key': datalake_account_access_key})

    # Crea una columna unica con sucursal y stock
    df2['Sucursal_y_Stock'] = df2.apply(lambda row: {'Cod_Sucursal' : row['Cod_Sucursal'], 'Stock' : row['Stock']}, axis=1)
    # Colapsa las 10 filas por cada producto en una sola con un array de diccionarios
    suc_collapsed = df2[['Cod_Producto', 'Sucursal_y_Stock']].groupby('Cod_Producto').agg(lambda x: x.tolist())
    # Joinea los productos con stock
    join = df.set_index('Cod_Producto').join(suc_collapsed, on='Cod_Producto', how='inner')

    return {"dataframe" : json.loads(join.to_json(orient='records'))}


@app.get("/productos/{id_producto}")
async def getProductoById(id_producto: int):
    '''Devuelve el producto que tenga cierto ID'''
    # Lee dataframes
    datalake_account_access_key = 'tUkrsYf++bJtSl/fXv9rtVhvTxIxh+3pzuWgA41vR3LtnbCV9xefC4ImN8XVLmk5ZxphFCGfN9mY+AStxYp14A=='
    datalake_container = 'csv'
    datalake_account_name = 'datalake123cd4567'

    df = pd.read_csv(f'abfs://{datalake_container}@{datalake_account_name}.dfs.core.windows.net/Producto_Unico.csv',storage_options = {'account_key': datalake_account_access_key})
    df2 = pd.read_csv(f'abfs://{datalake_container}@{datalake_account_name}.dfs.core.windows.net/Producto_Sucursales.csv',storage_options = {'account_key': datalake_account_access_key})
    # Filtra por el producto pedido
    df = df.loc[df['Cod_Producto'] == id_producto]
    # Crea una columna unica con sucursal y stock
    df2['Sucursal_y_Stock'] = df2.apply(lambda row: {'Cod_Sucursal' : row['Cod_Sucursal'], 'Stock' : row['Stock']}, axis=1)
    # Colapsa las 10 filas por cada producto en una sola con un array de diccionarios
    suc_collapsed = df2[['Cod_Producto', 'Sucursal_y_Stock']].groupby('Cod_Producto').agg(lambda x: x.tolist())
    # Joinea los productos con stock
    join = df.set_index('Cod_Producto').join(suc_collapsed, on='Cod_Producto', how='inner')

    if df.shape[0] != 0:
        return {"dataframe" : json.loads(join.to_json(orient='records'))}
    else:
        return {"error" : f"No existe el producto con id {id_producto}"}


@app.get("/categorias/{id_categoria}")
async def getProductoByCategory(id_categoria: int):
    '''Devuelve los productos bajo cierta categoria'''
    # Lee dataframes
    datalake_account_access_key = 'tUkrsYf++bJtSl/fXv9rtVhvTxIxh+3pzuWgA41vR3LtnbCV9xefC4ImN8XVLmk5ZxphFCGfN9mY+AStxYp14A=='
    datalake_container = 'csv'
    datalake_account_name = 'datalake123cd4567'

    df = pd.read_csv(f'abfs://{datalake_container}@{datalake_account_name}.dfs.core.windows.net/Producto_Unico.csv',storage_options = {'account_key': datalake_account_access_key})
    df2 = pd.read_csv(f'abfs://{datalake_container}@{datalake_account_name}.dfs.core.windows.net/Producto_Sucursales.csv',storage_options = {'account_key': datalake_account_access_key})

    # Filtra por la categoria pedida
    df = df.loc[df['Cod_Categoria'] == id_categoria]
    # Crea una columna unica con sucursal y stock
    df2['Sucursal_y_Stock'] = df2.apply(lambda row: {'Cod_Sucursal' : row['Cod_Sucursal'], 'Stock' : row['Stock']}, axis=1)
    # Colapsa las 10 filas por cada producto en una sola con un array de diccionarios
    suc_collapsed = df2[['Cod_Producto', 'Sucursal_y_Stock']].groupby('Cod_Producto').agg(lambda x: x.tolist())
    # Joinea los productos con stock
    join = df.set_index('Cod_Producto').join(suc_collapsed, on='Cod_Producto', how='inner')

    if df.shape[0] != 0:
        return {"dataframe" : json.loads(join.to_json(orient='records'))}
    else:
        return {"error" : f"No existe la categoria con id {id_categoria}"}


@app.get("/categorias/{id_categoria}/subcategorias/{id_subcategoria}")
async def getProductoByCategory(id_categoria: int, id_subcategoria: int):
    '''Devuelve los productos bajo cierta categoria que corresponden a una subcategoria'''
    # Lee dataframes
    datalake_account_access_key = 'tUkrsYf++bJtSl/fXv9rtVhvTxIxh+3pzuWgA41vR3LtnbCV9xefC4ImN8XVLmk5ZxphFCGfN9mY+AStxYp14A=='
    datalake_container = 'csv'
    datalake_account_name = 'datalake123cd4567'

    df = pd.read_csv(f'abfs://{datalake_container}@{datalake_account_name}.dfs.core.windows.net/Producto_Unico.csv',storage_options = {'account_key': datalake_account_access_key})
    df2 = pd.read_csv(f'abfs://{datalake_container}@{datalake_account_name}.dfs.core.windows.net/Producto_Sucursales.csv',storage_options = {'account_key': datalake_account_access_key})

    # Filtra por la subcategoria y categoria pedida
    df = df.loc[(df['Cod_Categoria'] == id_categoria) & (df['Cod_Subcategoria'] == id_subcategoria)]
    # Crea una columna unica con sucursal y stock
    df2['Sucursal_y_Stock'] = df2.apply(lambda row: {'Cod_Sucursal' : row['Cod_Sucursal'], 'Stock' : row['Stock']}, axis=1)
    # Colapsa las 10 filas por cada producto en una sola con un array de diccionarios
    suc_collapsed = df2[['Cod_Producto', 'Sucursal_y_Stock']].groupby('Cod_Producto').agg(lambda x: x.tolist())
    # Joinea los productos con stock
    join = df.set_index('Cod_Producto').join(suc_collapsed, on='Cod_Producto', how='inner')

    if df.shape[0] != 0:
        return {"dataframe": json.loads(join.to_json(orient='records'))}
    else:
        return {"error" : f"La subcategoria {id_subcategoria} no pertenece a la categoria {id_categoria}"}


@app.get("/subcategorias/{id_subcategoria}")
async def getProductoByCategory(id_subcategoria: int):
    '''Devuelve los productos bajo cierta subcategoria'''
    # Lee dataframes
    datalake_account_access_key = 'tUkrsYf++bJtSl/fXv9rtVhvTxIxh+3pzuWgA41vR3LtnbCV9xefC4ImN8XVLmk5ZxphFCGfN9mY+AStxYp14A=='
    datalake_container = 'csv'
    datalake_account_name = 'datalake123cd4567'

    df = pd.read_csv(f'abfs://{datalake_container}@{datalake_account_name}.dfs.core.windows.net/Producto_Unico.csv',storage_options = {'account_key': datalake_account_access_key})
    df2 = pd.read_csv(f'abfs://{datalake_container}@{datalake_account_name}.dfs.core.windows.net/Producto_Sucursales.csv',storage_options = {'account_key': datalake_account_access_key})

    # Filtra por la subcategoria
    df = df.loc[df['Cod_Subcategoria'] == id_subcategoria]
    # Crea una columna unica con sucursal y stock
    df2['Sucursal_y_Stock'] = df2.apply(lambda row: {'Cod_Sucursal' : row['Cod_Sucursal'], 'Stock' : row['Stock']}, axis=1)
    # Colapsa las 10 filas por cada producto en una sola con un array de diccionarios
    suc_collapsed = df2[['Cod_Producto', 'Sucursal_y_Stock']].groupby('Cod_Producto').agg(lambda x: x.tolist())
    # Joinea los productos con stock
    join = df.set_index('Cod_Producto').join(suc_collapsed, on='Cod_Producto', how='inner')
    
    if df.shape[0] != 0:
        return {"dataframe" : json.loads(join.to_json(orient='records'))}
    else:
        return {"error" : f"No existe subcategoria con id {id_subcategoria}"}
