import numpy as np
import pandas as pd

def extract_first_two_digits(x):
    '''
    Definición de una función para extraer los primeros dos dígitos del CIIU para obtener la división
    x: Columna a la que se le aplicará la columna 
    '''
    try:
        # Convert x to string, split at decimal point if present, and extract first two characters
        first_two_digits_str = str(x).split('.')[0][:2]
        # Convert the extracted string to an integer
        first_two_digits_int = int(first_two_digits_str)
        return first_two_digits_int
    except (ValueError, TypeError):
        # Return NaN (or any other value you prefer) if conversion fails
        return np.nan
    

# Función para verificar si '1' está presente en la cadena
def contain_one(value):
    '''
    Crear un vector de 1's y 0's con el objetivo crear la variable de Cámara de Comercio
    '''
    if pd.isna(value):
        return 0
    return 1 if '1' in value.split(',') else 0