import pandas as pd
from tabulate import tabulate
import tkinter as tk
from tkinter import ttk
import os
import numpy as np


# Debo cambiar el data frame de entrada
# Debo asignar True o False para la comparación

# Example DataFrame
data_path = r"D:\DANE - Contrato\2024\Operativo Barrido\Data\Resultados etapa 2"

df = pd.read_csv(os.path.join(data_path,"EMICRON_ATPCS.csv"),header = 0)
df['VA'] = df['VENTAS_MES_ANTERIOR'] - df['CYG']
df['C_V'] = df['CYG'] / (df['VENTAS_MES_ANTERIOR'] + 1)


def display_rows():
    selected_id_input = row_entry.get()
    selected_id = int(selected_id_input)
    
    selected_data = df[df['id'] == selected_id]

    # Si es vendedor de calle o establecimiento
    ubicacion = selected_data['UBICA'].iloc[0]

    # Características cualitativas para establecimientos
    rut = selected_data['IDRUT'].iloc[0]
    camara = selected_data['CAMCOMER'].iloc[0]
    depto = selected_data['COD_DEPTO'].iloc[0]
    reg_cont = selected_data['REG_CONT'].iloc[0]

    # Características de ambos grupos
    cpam = selected_data['CPAM'].iloc[0]
    sector = selected_data['GRUPOS4'].iloc[0]

    # Características cualitativas para vendedores de calle
    longevidad = selected_data['ANOS_ESPACIO'].iloc[0]
    sexo = selected_data['HOMBRE'].iloc[0]

    if ubicacion == 4:  # Vendedores de calle

        vars = ['VENTAS_MES_ANTERIOR','POTTOT','CYG','VA','C_V']

        filtered_prev = df[(df['UBICA']==ubicacion) & (df['CPAM']==cpam) & 
                        (df['GRUPOS4']==sector) & (df['ANOS_ESPACIO']==longevidad) & 
                        (df['HOMBRE']==sexo)]

        filtered = df[(df['UBICA']==ubicacion) & (df['CPAM']==cpam) & 
                        (df['GRUPOS4']==sector) & (df['ANOS_ESPACIO']==longevidad) & 
                        (df['HOMBRE']==sexo) & (df['ATPC']==False)]
        result =  filtered[vars].agg(['mean', 'std','sum'])
        new_row = result.loc['mean'] + 1.5 * result.loc['std']
        result.loc['sum'] = new_row
        result[['VENTAS_MES_ANTERIOR','CYG','VA']] = result[['VENTAS_MES_ANTERIOR','CYG','VA']]/1000

    elif ubicacion != 4: # Establecimientos
        
        vars = ['VENTAS_MES_ANTERIOR','CYG','POTTOT','REMUNERACION_TOTAL','ANIOS_OPERACION','VA','C_V']

        filtered_prev = df[(df['UBICA']==ubicacion) & (df['IDRUT']==rut) & 
                        (df['CAMCOMER']==camara) & (df['REG_CONT']==reg_cont) & 
                        (df['CPAM']==cpam) & (df['GRUPOS4']==sector) &
                        (df['OLA']==2022)]

        filtered = df[(df['UBICA']==ubicacion) & (df['IDRUT']==rut) & 
                        (df['CAMCOMER']==camara) & (df['REG_CONT']==reg_cont) & 
                        (df['CPAM']==cpam) & (df['GRUPOS4']==sector) &
                        (df['ATPC']==False) &
                        (df['OLA']==2022)]
        result =  filtered[vars].agg(['mean', 'std','sum'])
        new_row = result.loc['mean'] + 1.5 * result.loc['std']
        result.loc['sum'] = new_row
        result[['VENTAS_MES_ANTERIOR','CYG','REMUNERACION_TOTAL','VA']] = result[['VENTAS_MES_ANTERIOR','CYG','REMUNERACION_TOTAL','VA']]/1000
        
        
    dimensions_text = f"El número de combinaciones de las variables cualitativas en el dataframe es: {filtered_prev.shape[0]}\n\nVariables numéricas del grupo de control (mismas categorías pero no atípicos)\n\n"
    result_text.delete('1.0', tk.END)  # Clear previous results
    result_text.insert(tk.END, dimensions_text)

    # Display the table
    result_text.insert(tk.END, tabulate(result, headers='keys', tablefmt='fancy_grid'))

# Create main window
root = tk.Tk()
root.title("Data Viewer")

# Create frame for inputs
input_frame = ttk.Frame(root)
input_frame.pack(padx=10, pady=10)

# Label and entry widgets for row selection
row_label = ttk.Label(input_frame, text="id number:")
row_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

row_entry = ttk.Entry(input_frame, width=40)  # Define row_entry as a global variable
row_entry.grid(row=0, column=1, padx=5, pady=5)

# Button to display selected rows
show_button = ttk.Button(input_frame, text="Mostrar", command=display_rows)
show_button.grid(row=1, column=0, columnspan=2, pady=10)

# Frame for displaying results
result_frame = ttk.Frame(root)
result_frame.pack(padx=10, pady=10)


# Text widget for displaying results
result_text = tk.Text(result_frame, width=130, height=15, wrap=tk.WORD)
result_text.pack()

root.mainloop()