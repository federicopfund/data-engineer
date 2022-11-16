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

    @staticmethod
    def stockUpItem(id, stock, df2):
        # Subdataframe del producto
        stock_proporcional = df2[df2['Cod_Producto'] == id]
        # Stock total del producto
        sumStockOriginal = stock_proporcional.loc[:, 'Stock'].sum()
        # Reemplazo los stocks por sus proporciones
        stock_proporcional.loc[:, 'Stock'] /= sumStockOriginal
        # Agrego stock sin ajustar
        stock_proporcional.loc[:, 'Stock'] = round(stock*stock_proporcional.loc[:, 'Stock'], 0)
        stock_proporcional.loc[:, 'Stock'] = stock_proporcional.loc[:, 'Stock'].apply(lambda x: int(x))
        # Nuevo stock total
        sumStockNew = stock_proporcional.loc[:, 'Stock'].sum()

        # Ajusto stock en la tabla
        if sumStockNew > stock:
            for index, row in stock_proporcional['Stock'].sort_values(ascending=False).iloc[:(stock-sumStockNew)].items():
                #print(index, row)
                stock_proporcional.loc[index, 'Stock'] -=1
        elif sumStockNew < stock:
            for index, row in stock_proporcional['Stock'].sort_values(ascending=False).iloc[:(stock-sumStockNew)].items():
                #print(index, row)
                stock_proporcional.loc[index, 'Stock'] +=1

        # Cargo stock en la tabla final
        for index, row in df2.loc[df2['Cod_Producto'] == id, 'Stock'].items():
            df2.loc[index, 'Stock'] = stock_proporcional.loc[index, 'Stock']
        
        return df2