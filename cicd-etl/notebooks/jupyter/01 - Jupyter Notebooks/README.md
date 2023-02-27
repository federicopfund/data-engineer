# Jupyter Notebooks

Jupyter Notebooks es una aplicación web de código abierto que le permite crear y compartir código Python. Se utilizan con frecuencia para la ciencia de datos. Los ejemplos de código en este curso se completan usando Jupyter Notebooks que tienen una extensión de archivo . ipynb.

## Documentation

- [Jupyter](https://jupyter.org/) instalar Jupyter para que pueda ejecutar Jupyter Notebooks localmente en su computadora
- [Jupyter Notebook viewer](https://nbviewer.jupyter.org/)para ver Jupyter Notebooks en este repositorio de GitHub sin instalar Jupyter
- [Azure Notebooks](https://notebooks.azure.com/)  para crear una cuenta gratuita de Azure Notebooks para ejecutar Notebooks en la nube
- [Create and run a notebook](https://docs.microsoft.com/azure/notebooks/tutorial-create-run-jupyter-notebook?WT.mc_id=python-c9-niner) es un tutorial que te guía a través del proceso de uso de Azure Notebooks para crear un Jupyter Notebook completo que demuestra la regresión lineal
- [How to create and clone projects](https://docs.microsoft.com/azure/notebooks/create-clone-jupyter-notebooks?WT.mc_id=python-c9-niner) para crear un proyecto
- [Manage and configure projects in Azure Notebooks](https://docs.microsoft.com/azure/notebooks/configure-manage-azure-notebooks-projects?WT.mc_id=python-c9-niner) subir cuadernos a su proyecto

# pandas

[pandas](https://pandas/pydata.org​) is an open source Python library contains a number of high performance data structures and tools for data analysis.

## Documentation

- [Series](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html) stores one dimensional arrays
- [DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/frame.html) stores two dimensional arrays and can contain different datatypes

# Examining pandas DataFrame contents

The pandas [DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) is a structure for storing two-dimensional tabular data.

## Common functions

- [head](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.head.html) returns the first *n* rows from the DataFrame
- [tail](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.tail.html) returns the last *n* rows from the DataFrame
- [shape](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.shape.html) returns the dimensions of the DataFrame (e.g. number of rows and columns)
- [info](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.info.html) provides a summary of the DataFrame content including column names, their datatypes, and number of rows containing non-null values

# Query a pandas DataFrame

The pandas [DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)  is a structure for storing two-dimensional tabular data.

## Common properties

- [loc](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html) returns specific rows and columns by specifying column names
- [iloc](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iloc.html) returns specific rows and columns by specifying column positions

# CSV Files and Jupyter Notebooks

CSV files are comma separated variable file. CSV files are frequently used to store data. In order to access the data in a CSV file from a Jupyter Notebook you must upload the file. 

# Read and write CSV files from pandas DataFrames

You can populate a DataFrame with the data in a CSV file.

## Common functions and properties

- [read_csv](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html) reads a comma-separated values file into a DataFrame
- [to_csv](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html) writes contents of a DataFrame to a comma-separated values file
- [NaN](https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html) is the default representation of missing values

# Removing and splitting DataFrame columns

When preparing data for machine learning you may need to remove specific columns from the DataFrame.

## Common functions

- [drop](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop.html) deletes specified columns from a DataFrame

# Handling duplicates and rows with missing values

When preparing data for machine learning you need to remove duplicate rows and you may need to delete rows with missing values.

## Common functions

- [dropna](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.duplicated.html) removes rows with missing values
- [duplicated](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.duplicated.html) returns a True or False to indicate if a row is a duplicate of a previous row
- [drop_duplicates](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop_duplicates.html) returns a DataFrame with duplicate rows removed

# Splitting test and training data with scikit-learn

[scikit-learn](https://scikit-learn.org/) is a library of tools for predictive data analysis, which will allow you to prepare your data for machine learning and create models.

## Common functions

- [train_test_split](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html) splits arrays into random train and test subsets

# Train a linear regression model with scikit-learn

[Linear regression](https://en.wikipedia.org/wiki/Linear_regression) is a common algorithm for predicting values based on a given dataset.

## Common classes and functions

- [LinearRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html) fits a linear model
- [LinearRegression.fit](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html?highlight=linearregression#sklearn.linear_model.LinearRegression.fit) is used to fit the linear model based on training data

# Testing a model

Once a model is built it can be used to predict values. You can provide new values to see where it would fall on the spectrum, and test the generated model.

## Common classes and functions

- [LinearRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html) fits a linear model
- [LinearRegression.predict](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html?highlight=linearregression#sklearn.linear_model.LinearRegression.predict) is used to predict outcomes for new data based on the trained linear model


## Common functions

- [metrics](https://scikit-learn.org/stable/modules/classes.html?highlight=metrics#module-sklearn.metrics) includes functions and metrics that can be used for data science including measuring accuracy of models
- [mean_squared_error](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html#sklearn.metrics.mean_squared_error) returns the mean squared error, a measure used to measure accuracy of linear regression models
- [r2_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html#sklearn.metrics.r2_score) returns the R^2 regression score, a measure used to measure accuracy of linear regression models

## NumPy

[NumPy](https://numpy.org/) is a package for scientific computing with Python

### Common functions

- [sqrt](https://numpy.org/doc/1.18/reference/generated/numpy.sqrt.html?highlight=sqrt#numpy.sqrt) returns the square root of a value

### Common object

- [array](https://numpy.org/doc/1.18/reference/generated/numpy.array.html?highlight=array#numpy.array) creates an N-dimensional array object

## pandas

[pandas](https://pandas.pydata.org/) is a Python package for data analysis that includes a 1 dimensional and 2 dimensional array objects

### Common objects

- [Series](https://pandas.pydata.org/docs/reference/api/pandas.Series.html) stores a one dimensional array
- [DataFrame](https://pandas.pydata.org/docs/reference/frame.html) stores a two-dimensional array

# Visualizing data with Matplotlib

[Matplotlib](https://matplotlib.org/) gives you the ability to draw charts which can be used to visualize data.

## Common tools and functions

- [pyplot](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.html?highlight=pyplot#module-matplotlib.pyplot) provides the ability to draw plots similar to the MATLAB tool
- [pyplot.plot](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html#matplotlib.pyplot.plot) plots a graph
- [pyplot.show](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.show.html#matplotlib.pyplot.show) displays figures such as a graph
- [pyplot.scatter](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.scatter.html?highlight=scatter%20plot#matplotlib.pyplot.scatter) is used to draw scatter plots, a diagram that shows the relationship between two sets of data