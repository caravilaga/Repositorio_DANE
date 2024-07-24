'''
Importar librerías y definir directorios
'''
import pandas as pd
import numpy as np
import Funciones

data_path = r"D:\DANE - Contrato\2024\Operativo Barrido\Data\Despliegue prueba\Establecimientos/"
dicc_path = r"D:\DANE - Contrato\2024\Operativo Barrido\Data/"

df = pd.read_csv(data_path + "Intermedio/CENU_SIMULADO.csv")
# df = pd.read_csv(data_path + "Intermedio/CENU.csv")

'''
Importar diccionarios para las variables de:
+ Registros Contables
+ Ubicación
+ Actividad económica

Declarar los diccionarios para:
+ Departamento
+ GRUPOS12
+ Escala Sí/No

Selección de variables para el operativo de Establecimientos
'''

rel_reg_con= pd.read_excel(dicc_path + "Diccionario.xlsx", sheet_name="REG_CONT")
rel_ubica= pd.read_excel(dicc_path + "Diccionario.xlsx", sheet_name="UBICA")
rel_g12 = pd.read_excel(dicc_path + "Diccionario.xlsx", sheet_name="GRUPOS12")
rel_rut = pd.read_excel(dicc_path + "Diccionario.xlsx", sheet_name="IDRUT")
rel_cam = pd.read_excel(dicc_path + "Diccionario.xlsx", sheet_name="CAM_COMER")


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

dic_regconta = {1: "Estado_PyG", 
                2: "Libros_Operaciones", 
                3: "Otro",  
                4:"No_lleva_registros" } 


dic_ubica = {1: "Establecimientos", 
             3: "VCAE"} 

var_estab = ['UID_ENCUESTA','ING_TOTAL','CYG','POTTOT','REMUNERACION_TOTAL','DPTO','CPAM','GRUPOS12','UBICA','IDRUT','CAMCOMER','REG_CONT','ANIOS_OPERACION','VA','C_V'] 

'''
Creación de variables
'''
# Agregar las variables de gastos (viviendas y locales)
df['GASTOS'] =  df[['GTOTAL_ANO','GTOTAL_ANOV']].sum(axis=1)
df.loc[(df['GTOTAL_ANOV'].isna()) & (df['GTOTAL_ANO'].isna()), 'GASTOS'] = np.nan

# Crear la variable de Costos y Gastos agregada 
df['CYG'] = df[['COSTO_TOTAL','GASTOS']].sum(axis=1)
df.loc[(df['GASTOS'].isna()) & (df['COSTO_TOTAL'].isna()), 'CYG'] = np.nan

# Crear remuneración total
df['REMUNERACION_TOTAL'] = (df[['SALFIJOH','SALFIJOM','SALPERMH','SALPERMM','SALTEMPH','SALTEMPM']].replace(99,np.nan).sum(axis=1))*df['MESOPA'].replace(99,np.nan)

# Ciudad Principal y Área Metropolitana
cpam = [11001,	5001,	5079,	5088,	5129,	5212,	5266,	5308,	5360,	5380,	5631,	76001,	76892,	8001,
        8758,	68001,	68276,	68307,	68547,	17001,	17873,	52001,	66001,	66170,	66400,	73001,	54001,	54874,
        54405,	54261,	50001,	23001,	13001,	15001,	18001,	19001,	20001,	27001,	41001,	44001,	47001,	63001,	
        70001,	88001, 1]

df['MPIO'] = pd.to_numeric(df['MPIO'], errors= 'coerce')
df['CPAM'] = (df['MPIO'].isin(cpam) & df['CLASE']==1).apply(lambda x: int(x))

# Actividad Económica
df['Division'] = df['CIIUSELECCIONADO'].apply(Funciones.extract_first_two_digits)
df = pd.merge(df,rel_g12,on='Division',how="left")

# Antigüedad
df['ANIOS_OPERACION'] = 2024 - df['IDAIO']

# Valor Agregado
df['VA'] = df['ING_TOTAL'] - df['CYG']

# Coeficiente técnico de costos y gastos sobre ingresos
df['C_V'] = df['CYG'] / (df['ING_TOTAL'] + 1)

'''
Modificación de los labels de algunas variables
'''
# Registros contables
df['REG_CONT'] = df['REG_CONT'].map(dict(zip(rel_reg_con['REG_CONT'], rel_reg_con['Codigo'])))

# Ubicación de la unidad económica
df['UBICA'] = df['UBICA'].map(dict(zip(rel_ubica['UBICA'], rel_ubica['Codigo'])))

# Tenencia de RUT
df['IDRUT'] = df['IDRUT'].map(dict(zip(rel_rut['IDRUT'], rel_rut['Codigo'])))

# Cámara de comercio
df['CAMCOMER'] = df['CAMCOMER'].map(dict(zip(rel_cam['CAMCOMER'], rel_cam['Codigo'])))
df['CAMCOMER'] = df['CAMCOMER'].fillna(0)
df.loc[df['CAMCOMER']==" ",'CAMCOMER'] = 0

'''
Selección de las variables
'''
df_final = df[var_estab]


'''
Filtrado de las unidades económicas
'''
# Ubicación geográfica: departamentos
depto_emicron = [8, 13, 44, 47, 70, 20, 25, 11, 18, 41, 15, 68, 54, 76, 52, 19, 17, 63, 73, 66,  5, 23, 27, 50, 88]
df_final = df_final[df_final['DPTO'].isin(depto_emicron)]

# Seleccionar unidades económicas ubicadas en vivienda o establecimiento fijo (1 y 3)
df_final = df_final[df_final['UBICA'].isin([1,3])]

# Descartar unidades económicas con algún NA o 99 dentro de sus registros
id_ig = df_final['UID_ENCUESTA'][((df_final.isna()) | (df_final==99)).any(axis=1)]
df_final = df_final[~(df_final['UID_ENCUESTA'].isin(id_ig))]


'''
Asignar labels
'''

df_final['DPTO'] = df_final['DPTO'].map(dic_depto)
df_final['CPAM'] = df_final['CPAM'].map(dic_rut)
df_final['IDRUT'] = df_final['IDRUT'].map(dic_rut)
df_final['CAMCOMER'] = df_final['CAMCOMER'].map(dic_rut)
df_final['GRUPOS12'] = df_final['GRUPOS12'].map(dic_g12)
df_final['REG_CONT'] = df_final['REG_CONT'].map(dic_regconta)
df_final['UBICA'] = df_final['UBICA'].map(dic_ubica)


'''
Exportar
'''
df_final.to_csv(data_path + "Intermedio/CENU_SIMULADO_modelo.csv", index=False)
df_final.to_excel(data_path + "Intermedio/CENU_SIMULADO_modelo.xlsx", index=False)

# df_final.to_csv(data_path + "Intermedio/CENU_piloto_modelo.csv", index=False)
# df_final.to_excel(data_path + "Intermedio/CENU_piloto_modelo.xlsx", index=False)