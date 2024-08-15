import pandas as pd
import numpy as np
import seaborn as sns
#from statsmodels.stats.weightstats import DescrStatsW
from matplotlib import patheffects
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date, MetaData, Table, Numeric, Time
import sys
from urllib.request import urlopen
import json
import Funciones

## Definiendo conexión con la base de datos
host = "localhost"
database = "dane"
user = "postgres"
port = 5432
password = "1234"

data_path = r"D:\Despliegue\Proyecto HOP\Data\Vcalle/"
dicc_path = r"D:\Despliegue\Proyecto HOP\Data/"

connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
connection_string


## Conectándose con el motor e importando las tabñas
engine = create_engine(connection_string)
insp = inspect(engine)
insp.get_table_names()


sql = 'SET SEARCH_PATH TO public, data_cruda, data_intermedia; SELECT * FROM v_calle;'

df = pd.DataFrame(pd.read_sql(sql, con = engine))


'''
Importar diccionarios para las variables de:
+ Ubicación
+ Actividad económica

Declarar los diccionarios para:
+ Departamento
+ GRUPOS12
+ Escala Sí/No

Selección de variables para el operativo de Establecimientos
'''

rel_g12 = pd.read_excel(dicc_path + "Diccionario.xlsx", sheet_name="GRUPOS12")
rel_sex = pd.read_excel(dicc_path + "Diccionario.xlsx", sheet_name="SEXO")
rel_anio = pd.read_excel(dicc_path + "Diccionario.xlsx", sheet_name="ANOS_ESPACIO")

dic_depto = {5:"Antioquia",8:"Atlántico",11:"Bogotá, D. C.",13:"Bolívar",15:"Boyacá",17:"Caldas",18:"Caquetá",
             19:"Cauca",20:"Cesar",23:"Córdoba",25:"Cundinamarca",27:"Chocó",41:"Huila",44:"La Guajira",47:"Magdalena",
             50:"Meta",52:"Nariño",54:"Norte De Santander",63:"Quindío",66:"Risaralda",68:"Santander",70:"Sucre",73:"Tolima",
             76:"Valle Del Cauca",88:"San Andrés"}

dic_sector = {2:"Industria",3:"Comercio",4:"Servicios"}

dic_rut = {1:"Sí",0:"No"}

dic_g12 = {3:"Industria",
           4:"Construcción",
           5:"Comercio",
           6:"Transporte y almacenamiento",
           7:"Alojamiento/servicios de comida",
           8:"Información y comunicaciones",
           9:"Actividades inmobiliarias",
           10:"Educación",
           11:"Actividades de salud humana",
           12:"Actividades artísticas",
}

dic_ANOS_ESPACIO = {1: "[0-1)", 
                    2: "[1-3)",
                    3: "[3-5)",
                    4: "[5-10)",
                    5: "x>=10"} 

var_mov = ['uid_encuesta','ventas','pottot','cyg','va','c_v','cod_dpto','cpam','grupos12','anos_espacio','hombre'] 

def fix_decoding(text):
    if text is None:
        return text
    return text.encode('latin1').decode('utf-8')


'''
Creación de variables
'''

# Crear la variable de Costos y Gastos agregada 
df['cyg'] = df[['gasto_tot','costos']].sum(axis=1)
df.loc[(df['gasto_tot'].isna()) & (df['costos'].isna()), 'cyg'] = np.nan

# Total Personal Ocupado
df['trabajsoc'] = pd.to_numeric(df['trabajsoc'], errors= 'coerce')
df['trabajpago'] = pd.to_numeric(df['trabajpago'], errors= 'coerce')
df['trabajfami'] = pd.to_numeric(df['trabajfami'], errors= 'coerce')

df['pottot'] = df[['trabajsoc','trabajpago','trabajfami']].sum(axis=1)
df.loc[(df['trabajsoc'].isna()) & (df['trabajpago'].isna()) & (df['trabajfami'].isna()), 'cyg'] = np.nan

# Ciudad Principal y Área Metropolitana
cpam = [11001,	5001,	5079,	5088,	5129,	5212,	5266,	5308,	5360,	5380,	5631,	76001,	76892,	8001,
        8758,	68001,	68276,	68307,	68547,	17001,	17873,	52001,	66001,	66170,	66400,	73001,	54001,	54874,
        54405,	54261,	50001,	23001,	13001,	15001,	18001,	19001,	20001,	27001,	41001,	44001,	47001,	63001,	
        70001,	88001]
df['cod_mpio'] = pd.to_numeric(df['cod_mpio'], errors= 'coerce')
df['cpam'] = (df['cod_mpio'].isin(cpam) & df['clase']==1).apply(lambda x: int(x))

# Actividad Económica
df['division'] = df['ciiu_4'].apply(Funciones.extract_first_two_digits)
df = pd.merge(df,rel_g12,on='division',how="left")

# Valor Agregado
df['va'] = df['ventas'] - df['cyg']

# Coeficiente técnico de costos y gastos sobre ingresos
df['c_v'] = df['cyg'] / (df['ventas'] + 1)

'''
Modificación de los labels de algunas variables
'''
# Antigüedad
df['anos_espacio'] = df['anos_espacio'].apply(fix_decoding)
df['anos_espacio'] = df['anos_espacio'].map(dict(zip(rel_anio['ANOS_ESPACIO'], rel_anio['Codigo'])))

# Sexo
df['sexo'] = df['sexo'].map(dict(zip(rel_sex['SEXO'], rel_sex['Codigo'])))
df.rename(columns = {'sexo' : 'hombre'}, inplace = True)


'''
Selección de las variables
'''
df_final = df[var_mov]


'''
Filtrado de las unidades económicas
'''
# Ubicación geográfica: departamentos
depto_emicron = [8, 13, 44, 47, 70, 20, 25, 11, 18, 41, 15, 68, 54, 76, 52, 19, 17, 63, 73, 66,  5, 23, 27, 50, 88]
df_final = df_final[df_final['cod_dpto'].isin(depto_emicron)]

# Descartar unidades económicas con algún NA o 99 dentro de sus registros
id_ig = df_final['uid_encuesta'][((df_final.isna()) | (df_final==99)).any(axis=1)]
df_final = df_final[~(df_final['uid_encuesta'].isin(id_ig))]

'''
Asignar labels
'''
df_final['cod_dpto'] = df_final['cod_dpto'].map(dic_depto)
df_final['cpam'] = df_final['cpam'].map(dic_rut)
df_final['grupos12'] = df_final['grupos12'].map(dic_g12)
df_final['hombre'] = df_final['hombre'].map(dic_rut)
df_final['anos_espacio'] = df_final['anos_espacio'].map(dic_ANOS_ESPACIO)

'''
Exportar
'''
df_final.to_csv(data_path + "02 - Intermedio/CENU_SIMULADO_modelo.csv", index=False)
df_final.to_excel(data_path + "02 - Intermedio/CENU_SIMULADO_modelo.xlsx", index=False)


#df_f.to_csv(data_path + "02 - Intermedio/FINAL.csv", index=False)