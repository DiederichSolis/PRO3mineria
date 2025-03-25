import pandas as pd
import os
from glob import glob

# Configuración
input_folder = "input_xls"
output_file = "divorcios_guatemala.xlsx"
hojas_relevantes = [
    "Grupos edad hombre y mujer",
    "Pueblo del hombre y mujer",
    "Mes de registro y departamento",
    "Ocupaciones de mujer y hombre",
    "Mes ocurrencia y día"
]

# Mapeo de correcciones para columnas inconsistentes
correcciones = {
    "Xinca": "Xinka",
    "subgrupos ocupacionales": "grupos ocupacionales",
    "Ocupación  no especificada": "Ocupación no especificada"
}

# Procesar archivos
hojas_combinadas = {hoja: pd.DataFrame() for hoja in hojas_relevantes}

for archivo in glob(os.path.join(input_folder, "*.xls*")):
    try:
        # Extraer año del nombre del archivo
        año = os.path.basename(archivo).split(".")[0]
        
        # Leer archivo
        xls = pd.ExcelFile(archivo)
        
        for hoja in hojas_relevantes:
            # Saltar hojas con nombres ligeramente diferentes
            if hoja not in xls.sheet_names:
                print(f"Advertencia: {hoja} no encontrada en {archivo}")
                continue
            
            # Leer datos y limpiar encabezados
            df = pd.read_excel(xls, sheet_name=hoja, skiprows=2)
            df.columns = df.columns.str.strip()
            
            # Aplicar correcciones de nombres de columnas
            df.rename(columns=correcciones, inplace=True)
            
            # Añadir columna de año
            df["Año"] = año
            
            # Concatenar datos
            hojas_combinadas[hoja] = pd.concat([hojas_combinadas[hoja], df], ignore_index=True)

    except Exception as e:
        print(f"Error procesando {archivo}: {str(e)}")

# Guardar resultados
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    for hoja, datos in hojas_combinadas.items():
        datos.to_excel(writer, sheet_name=hoja, index=False)

print("¡Unificación exitosa! Archivo generado:", output_file)