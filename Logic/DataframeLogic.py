import pandas as pd

class DataframeLogic:
    
    @staticmethod
    def filterDataframes(df, df2):
        # Crea una columna unica con sucursal y stock
        df2['Sucursal_y_Stock'] = df2.apply(lambda row: {'Cod_Sucursal' : row['Cod_Sucursal'], 'Stock' : row['Stock']}, axis=1)
        # Colapsa las 10 filas por cada producto en una sola con un array de diccionarios
        suc_collapsed = df2[['Cod_Producto', 'Sucursal_y_Stock']].groupby('Cod_Producto').agg(lambda x: x.tolist())
        # Joinea los productos con stock
        join = df.set_index('Cod_Producto').join(suc_collapsed, on='Cod_Producto', how='inner')
        return join

    
    

