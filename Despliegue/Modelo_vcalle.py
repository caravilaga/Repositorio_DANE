'''
Importar librerías y definir directorios
'''
import pickle
import pandas as pd

data_path = r"D:\Despliegue\Proyecto HOP\Data\Vcalle/"
model_path = r"D:\Despliegue\Syntax\Modelado/"

'''
Importar modelos
'''
with open(model_path + "modelo_svc_optimizado_vcalle.pkl",'rb') as file:
    pipeline_vcalle = pickle.load(file)

'''
Importar data a predecir
'''
df = pd.read_csv(data_path + "02 - Intermedio/CENU_SIMULADO_modelo.csv")

'''
Realizar la predicción
'''
pred = pipeline_vcalle.predict(df)

'''
Adicionar columna con las predicciones
'''
df_final = df.copy()
df_final['Anomalia'] = pred

'''
Exportar
'''
df_final.to_csv(data_path + "03 - Final/Resultados_modelo.csv", index=True)
df_final.to_excel(data_path + "03 - Final/Resultados_modelo.xlsx", index=True)