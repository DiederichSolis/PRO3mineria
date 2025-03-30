import pandas as pd
import os

carpeta_csv = "archivosCSV"
dataframes = []

# Definir todas las columnas que esperas tener en el unificado
columnas_objetivo = [
    'DEPREG', 'MUPREG', 'MESREG', 'AÑOREG', 'DIAOCU', 'MESOCU', 'AÑOOCU',
    'DEPOCU', 'MUPOCU', 'EDADHOM', 'EDADMUJ', 'PPERHOM', 'PPERMUJ',
    'NACHOM', 'NACMUJ', 'ESCHOM', 'ESCMUJ', 'CIUOHOM', 'CIUOMUJ'
]

print(f"📂 Archivos encontrados en '{carpeta_csv}':")
archivos = os.listdir(carpeta_csv)
print(archivos)

for archivo in archivos:
    if archivo.endswith(".CSV") or archivo.endswith(".csv"):
        ruta_completa = os.path.join(carpeta_csv, archivo)
        print(f"\n🔄 Leyendo: {archivo}")
        try:
            df = pd.read_csv(ruta_completa)

            # Renombrar columnas antiguas
            columnas_renombrar = {
                "PUEHOM": "PPERHOM",
                "PUEMUJ": "PPERMUJ"
            }
            df.rename(columns=columnas_renombrar, inplace=True)

            # Agregar columnas faltantes como NaN
            for col in columnas_objetivo:
                if col not in df.columns:
                    print(f"➕ Agregando columna faltante '{col}' en {archivo}")
                    df[col] = pd.NA

            # Reordenar columnas según el orden objetivo
            df = df[columnas_objetivo]
            dataframes.append(df)

        except Exception as e:
            print(f"❌ Error leyendo {archivo}: {e}")

# Unir todos los DataFrames ya estandarizados
if dataframes:
    df_unido = pd.concat(dataframes, ignore_index=True)
    df_unido.to_csv("unificado.csv", index=False)
    print(f"\n✅ Archivos combinados correctamente. Total de filas: {len(df_unido)}")
    print(f"📊 Total de columnas en 'unificado.csv': {len(df_unido.columns)}")
else:
    print("🚫 No se combinaron archivos válidos.")
