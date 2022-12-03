import pandas as pd

class DataframeLogic:
    
    @staticmethod
    def filterDataframes(df, df2):
        # Crea una columna unica con sucursal y stock
        df2['Sucursal_y_Stock'] = df2.apply(lambda row: {'Cod_Sucursal' : row['Cod_Sucursal'], 'Stock' : row['Stock']}, axis=1)
        # Colapsa las 10 filas por cada producto en una sola con un array de diccionarios
        suc_collapsed = df2[['Cod_Producto', 'Sucursal_y_Stock']].groupby('Cod_Producto').agg(lambda x: x.tolist())
        # Joinea los productos con stock
        #print(suc_collapsed)
        join = df.join(suc_collapsed, on='Cod_Producto', how='inner')
        return join

    @staticmethod
    def stockUpItem(id, stock, df2):
        # Agrego un producto a cada sucursal si tenemos 10 o mas de stock
        #print(df2.loc[df2['Cod_Producto'] == id, 'Stock'].sum())
        if stock >= 10:
            #print(stock_proporcional, "antes")
            df2.loc[df2['Cod_Producto'] == id, 'Stock'] += 1
            #print(stock_proporcional, "despues")
            # Actualizo el stock
            stock -= 10
        
        # Subdataframe del producto
        stock_proporcional = df2[df2['Cod_Producto'] == id]
        #print(stock_proporcional['Stock'].sum())

        # Si la suma del stock es distinto de cero, usar las proporciones dadas
        if (stock_proporcional.loc[:, 'Stock'].sum() != 0):
            # Stock total del producto
            sumStockOriginal = stock_proporcional.loc[:, 'Stock'].sum()
            # Reemplazo los stocks por sus proporciones
            stock_proporcional.loc[:, 'Stock'] /= sumStockOriginal
            #print(stock_proporcional)
        # De lo contrario, usar las proporciones iniciales
        else:
            # Stock total del producto
            sumStockOriginal = stock_proporcional.loc[:, 'Stock_Inicial'].sum()
            # Reemplazo los stocks por sus proporciones
            stock_proporcional.loc[:, 'Stock'] = stock_proporcional.loc[:, 'Stock_Inicial'] / sumStockOriginal
        
        # Agrego stock sin ajustar
        stock_proporcional.loc[:, 'Stock'] = round(stock*stock_proporcional.loc[:, 'Stock'], 0)
        stock_proporcional.loc[:, 'Stock'] = stock_proporcional.loc[:, 'Stock'].apply(lambda x: int(x))
        # Nuevo stock total
        sumStockNew = stock_proporcional.loc[:, 'Stock'].sum()

        # Si no hay nada cargado o falla en cargar
        if sumStockNew == 0:
            for index, row in stock_proporcional.sort_values(by='Stock_Inicial', ascending=False)['Stock'].iloc[:(stock-sumStockNew)].items():
                stock_proporcional.loc[stock_proporcional['Cod_Sucursal'] == index, 'Stock'] +=1

        sumStockNew = stock_proporcional.loc[:, 'Stock'].sum()

        # Ajusto stock en la tabla
        #print(sumStockNew)
        if sumStockNew > stock:
            for index, row in stock_proporcional['Stock'].sort_values(ascending=False).iloc[:(sumStockNew-stock)].items():
                #print(index, row)
                stock_proporcional.loc[stock_proporcional['Cod_Sucursal'] == index, 'Stock'] -=1
        elif sumStockNew < stock:
            for index, row in stock_proporcional['Stock'].sort_values(ascending=False).iloc[:(stock-sumStockNew)].items():
                #print(index, row)
                stock_proporcional.loc[stock_proporcional['Cod_Sucursal'] == index, 'Stock'] +=1

        # Cargo stock en la tabla final
        for index, row in df2.loc[df2['Cod_Producto'] == id, 'Stock'].items():
            df2.loc[index, 'Stock'] += stock_proporcional.loc[index, 'Stock']
        
        #print(stock_proporcional['Stock'].sum())
        #print(df2.loc[df2['Cod_Producto'] == id, 'Stock'].sum())
        return df2

    @staticmethod
    def buyProduct(id, cantidad, sucursal, df2):
        stock = df2.loc[df2['Cod_Producto'] == id & df2['Cod_Sucursal'] == sucursal, 'Stock']

        if stock >= cantidad:
            df2.loc[['Cod_Producto'] == id & df2['Cod_Sucursal'] == sucursal, 'Stock'] -= cantidad

            return df2
        else:
            return None