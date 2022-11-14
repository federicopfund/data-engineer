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
    df = pd.read_csv("Datasets locales/Producto_Unico.csv")
    df2 = pd.read_csv('Datasets locales/Producto_Sucursales.csv')

    df2['Sucursal_y_Stock'] = df2.apply(lambda row: {'Cod_Sucursal' : row['Cod_Sucursal'], 'Stock' : row['Stock']}, axis=1)
    suc_collapsed = df2[['Cod_Producto', 'Sucursal_y_Stock']].groupby('Cod_Producto').agg(lambda x: x.tolist())
    join = df.set_index('Cod_Producto').join(suc_collapsed, on='Cod_Producto', how='inner')

    return {"dataframe" : json.loads(join.to_json(orient='records'))}

@app.get("/productos/{id_producto}")
async def getProductoById(id_producto: int):
    '''Devuelve el producto que tenga cierto ID'''
    df = pd.read_csv("Datasets locales/Producto_Unico.csv")
    df2 = pd.read_csv('Datasets locales/Producto_Sucursales.csv')

    df = df.loc[df['Cod_Producto'] == id_producto]
    df2['Sucursal_y_Stock'] = df2.apply(lambda row: {'Cod_Sucursal' : row['Cod_Sucursal'], 'Stock' : row['Stock']}, axis=1)
    suc_collapsed = df2[['Cod_Producto', 'Sucursal_y_Stock']].groupby('Cod_Producto').agg(lambda x: x.tolist())
    join = df.set_index('Cod_Producto').join(suc_collapsed, on='Cod_Producto', how='inner')

    return {"dataframe" : json.loads(join.to_json(orient='records'))}

@app.get("/categorias/{id_categoria}")
async def getProductoByCategory(id_categoria: int):
    '''Devuelve los productos bajo cierta categoria'''
    df = pd.read_csv("Datasets locales/Producto_Unico.csv")
    df2 = pd.read_csv('Datasets locales/Producto_Sucursales.csv')

    df = df.loc[df['Cod_Categoria'] == id_categoria]
    df2['Sucursal_y_Stock'] = df2.apply(lambda row: {'Cod_Sucursal' : row['Cod_Sucursal'], 'Stock' : row['Stock']}, axis=1)
    suc_collapsed = df2[['Cod_Producto', 'Sucursal_y_Stock']].groupby('Cod_Producto').agg(lambda x: x.tolist())
    join = df.set_index('Cod_Producto').join(suc_collapsed, on='Cod_Producto', how='inner')

    return {"dataframe" : json.loads(join.to_json(orient='records'))}

@app.get("/categorias/{id_categoria}/subcategorias/{id_subcategoria}")
async def getProductoByCategory(id_categoria: int, id_subcategoria: int):
    '''Devuelve los productos bajo cierta categoria que corresponden a una subcategoria'''
    df = pd.read_csv("Datasets locales/Producto_Unico.csv")
    df2 = pd.read_csv('Datasets locales/Producto_Sucursales.csv')

    df = df.loc[(df['Cod_Categoria'] == id_categoria) & (df['Cod_Subcategoria'] == id_subcategoria)]
    df2['Sucursal_y_Stock'] = df2.apply(lambda row: {'Cod_Sucursal' : row['Cod_Sucursal'], 'Stock' : row['Stock']}, axis=1)
    suc_collapsed = df2[['Cod_Producto', 'Sucursal_y_Stock']].groupby('Cod_Producto').agg(lambda x: x.tolist())
    join = df.set_index('Cod_Producto').join(suc_collapsed, on='Cod_Producto', how='inner')

    if df.shape[0] != 0:
        return {"dataframe": json.loads(join.to_json(orient='records'))}
    else:
        return {"error" : f"La subcategoria {id_subcategoria} no pertenece a la categoria {id_categoria}"}

@app.get("/subcategorias/{id_subcategoria}")
async def getProductoByCategory(id_subcategoria: int):
    '''Devuelve los productos bajo cierta subcategoria'''
    df = pd.read_csv("Datasets locales/Producto_Unico.csv")
    df2 = pd.read_csv('Datasets locales/Producto_Sucursales.csv')

    df = df.loc[df['Cod_Subcategoria'] == id_subcategoria]
    df2['Sucursal_y_Stock'] = df2.apply(lambda row: {'Cod_Sucursal' : row['Cod_Sucursal'], 'Stock' : row['Stock']}, axis=1)
    suc_collapsed = df2[['Cod_Producto', 'Sucursal_y_Stock']].groupby('Cod_Producto').agg(lambda x: x.tolist())
    join = df.set_index('Cod_Producto').join(suc_collapsed, on='Cod_Producto', how='inner')
    
    return {"dataframe" : json.loads(join.to_json(orient='records'))}