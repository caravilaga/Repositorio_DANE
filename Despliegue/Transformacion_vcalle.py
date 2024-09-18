'''
Importar librerías y definir directorios
'''
import pandas as pd
import numpy as np
import Funciones

#data_path = r"D:\Despliegue\Proyecto HOP\Data\Vcalle/"
#dicc_path = r"D:\Despliegue\Proyecto HOP\Data/"

data_path = r"D:\DANE - Contrato\2024\Operativo Barrido\Data\Despliegue prueba\Vcalle/"
dicc_path = r"D:\DANE - Contrato\2024\Operativo Barrido\Data/"

df = pd.read_csv(data_path + "01 - Crudo/DB_SIMULADA_VDC (2).csv", sep = ';')

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

var_mov = ['UID_ENCUESTA','VENTAS','POTTOT','CYG','VA','C_V','COD_DPTO','CPAM','GRUPOS12','ANOS_ESPACIO','HOMBRE'] 

'''
Creación de variables
'''

# Crear la variable de Costos y Gastos agregada 
df['CYG'] = df[['GASTO_TOT','COSTOS']].sum(axis=1)
df.loc[(df['GASTO_TOT'].isna()) & (df['COSTOS'].isna()), 'CYG'] = np.nan

# Total Personal Ocupado
df['TRABAJSOC'] = pd.to_numeric(df['TRABAJSOC'], errors= 'coerce')
df['TRABAJPAGO'] = pd.to_numeric(df['TRABAJPAGO'], errors= 'coerce')
df['TRABAJFAMI'] = pd.to_numeric(df['TRABAJFAMI'], errors= 'coerce')

df['POTTOT'] = df[['TRABAJSOC','TRABAJPAGO','TRABAJFAMI']].sum(axis=1)
df.loc[(df['TRABAJSOC'].isna()) & (df['TRABAJPAGO'].isna()) & (df['TRABAJFAMI'].isna()), 'POTTOT'] = np.nan

# Ciudad Principal y Área Metropolitana
cpam = [11001,	5001,	5079,	5088,	5129,	5212,	5266,	5308,	5360,	5380,	5631,	76001,	76892,	8001,
        8758,	68001,	68276,	68307,	68547,	17001,	17873,	52001,	66001,	66170,	66400,	73001,	54001,	54874,
        54405,	54261,	50001,	23001,	13001,	15001,	18001,	19001,	20001,	27001,	41001,	44001,	47001,	63001,	
        70001,	88001]
df['COD_MPIO'] = pd.to_numeric(df['COD_MPIO'], errors= 'coerce')
df['CPAM'] = (df['COD_MPIO'].isin(cpam) & df['CLASE']==1).apply(lambda x: int(x))

# Actividad Económica
# df['Division'] = df['CIIU_4'].apply(Funciones.extract_first_two_digits)
# df = pd.merge(df,rel_g12,on='Division',how="left")

## Versión 2.0
df['GRUPOS12'] = None

# Creación de la variable GRUPOS12 a partir de las respuestas del formulario
# df.loc[df['ACTIVIDAD'] == 1, 'Division'] = 47
# df.loc[df['SERVICIO'] == 1, 'Division'] = 56
# df.loc[df['SERVICIO'] == 2, 'Division'] = 38
# df.loc[df['SERVICIO'] == 3, 'Division'] = 92
# df.loc[df['SERVICIO'] == 4, 'Division'] = 45
# df.loc[df['SERVICIO'] == 5, 'Division'] = 95
# df.loc[df['SERVICIO'] == 6, 'Division'] = 96
# df.loc[df['PRODUCTO'].isin([1,2,3]) , 'Division'] = 32
# df.loc[df['PRODUCTO'] == 4 , 'Division'] = 15

df.loc[df['ACTIVIDAD'] == 1, 'GRUPOS12'] = 5
df.loc[df['SERVICIO'] == 1, 'GRUPOS12'] = 7
df.loc[df['SERVICIO'] == 2, 'GRUPOS12'] = 3
df.loc[df['SERVICIO'] == 3, 'GRUPOS12'] = 12
df.loc[df['SERVICIO'] == 4, 'GRUPOS12'] = 5
df.loc[df['SERVICIO'] == 5, 'GRUPOS12'] = 12
df.loc[df['SERVICIO'] == 6, 'GRUPOS12'] = 12
df.loc[df['PRODUCTO'].isin([1,2,3]) , 'GRUPOS12'] = 3
df.loc[df['PRODUCTO'] == 4 , 'GRUPOS12'] = 3


# Valor Agregado
df['VA'] = df['VENTAS'] - df['CYG']

# Coeficiente técnico de costos y gastos sobre ingresos
df['C_V'] = df['CYG'] / (df['VENTAS'] + 1)

'''
Modificación de los labels de algunas variables
'''
# Antigüedad
df['ANOS_ESPACIO'] = df['ANOS_ESPACIO'].map(dict(zip(rel_anio['ANOS_ESPACIO'], rel_anio['Codigo'])))

# Sexo
df['SEXO'] = df['SEXO'].map(dict(zip(rel_sex['SEXO'], rel_sex['Codigo'])))
df.rename(columns = {'SEXO' : 'HOMBRE'}, inplace = True)


'''
Selección de las variables
'''
df_final = df[var_mov]


'''
Filtrado de las unidades económicas
'''
# Ubicación geográfica: departamentos
depto_emicron = [8, 13, 44, 47, 70, 20, 25, 11, 18, 41, 15, 68, 54, 76, 52, 19, 17, 63, 73, 66,  5, 23, 27, 50, 88]
df_final = df_final[df_final['COD_DPTO'].isin(depto_emicron)]

# Descartar unidades económicas con algún NA o 99 dentro de sus registros
id_ig = df_final['UID_ENCUESTA'][((df_final.isna()) | (df_final==99)).any(axis=1)]
df_final = df_final[~(df_final['UID_ENCUESTA'].isin(id_ig))]

'''
Asignar labels
'''
df_final['COD_DPTO'] = df_final['COD_DPTO'].map(dic_depto)
df_final['CPAM'] = df_final['CPAM'].map(dic_rut)
df_final['GRUPOS12'] = df_final['GRUPOS12'].map(dic_g12)
df_final['HOMBRE'] = df_final['HOMBRE'].map(dic_rut)
df_final['ANOS_ESPACIO'] = df_final['ANOS_ESPACIO'].map(dic_ANOS_ESPACIO)


'''
Exportar
'''
df_final.to_csv(data_path + "02 - Intermedio/CENU_SIMULADO_modelo.csv", index=False)
df_final.to_excel(data_path + "02 - Intermedio/CENU_SIMULADO_modelo.xlsx", index=False)