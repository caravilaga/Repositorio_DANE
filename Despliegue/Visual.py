import streamlit as st
import pandas as pd

data_path = r"D:\DANE - Contrato\2024\Operativo Barrido\Data\Despliegue prueba\Establecimientos/"

# Título de la aplicación
st.title("Seguimiento de los resultados del modelo de detección de anomalías")

# Lectura de la base de datos
data = pd.read_csv(data_path + "Intermedio/CENU_piloto_modelo.csv")
df = data[['UID_ENCUESTA','VA']]
df['Verificado'] = False

# Mostrar el DataFrame original
#st.write("DataFrame original:")
#st.write(df)

# Crear una lista de checkboxes para cada fila del DataFrame
# seleccionados = []

# for i in range(len(df)):
#     seleccionado = st.checkbox(f"Seleccionar {df['Nombre'][i]}", key=i)
#     seleccionados.append(seleccionado)

# # Actualizar la columna 'Seleccionado' en el DataFrame
# df["Seleccionado"] = seleccionados

def update(df, changes):
    for index, row in changes.iterrows():
        df.loc[index, 'Verificado'] = row['Verificado']
    return df

changes_df = df.copy()

changes = st.data_editor(
    changes_df,
    column_config= {
        "Verificado": st.column_config.CheckboxColumn(
            "¿Es un dato anómalo?",
            help = "Marque la casilla si el registro es anómalo",
            default= False
        )
    },
    disabled = ["widgets"],
    hide_index = True,
)

# Mostrar el DataFrame actualizado
#st.write("DataFrame actualizado:")
#st.write(df)


# Actualizar el Data frame final con los cambios
df_final = update(df.copy(), changes)

df_final.to_excel(data_path + "Prueba.xlsx")