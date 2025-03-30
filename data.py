import pandas as pd
import os

carpeta_csv = "archivosCSV"
dataframes = []

# Verificar archivos dentro de la carpeta
print(f"📂 Archivos encontrados en '{carpeta_csv}':")
archivos = os.listdir(carpeta_csv)
print(archivos)

# Iterar sobre los CSV
for archivo in archivos:
    if archivo.endswith(".CSV") or archivo.endswith(".csv"):  # considerar mayúsculas
        ruta_completa = os.path.join(carpeta_csv, archivo)
        print(f"🔄 Leyendo: {archivo}")
        try:
            df = pd.read_csv(ruta_completa)
            print(f"✅ Columnas en {archivo}: {list(df.columns)}")

            if not dataframes or list(df.columns) == list(dataframes[0].columns):
                dataframes.append(df)
            else:
                print(f"⚠️ Columnas NO coinciden en {archivo}")
                print(f"➡️ Esperadas: {list(dataframes[0].columns)}")
                print(f"➡️ Encontradas: {list(df.columns)}")

        except Exception as e:
            print(f"❌ Error leyendo {archivo}: {e}")

# Unir si hay archivos válidos
if dataframes:
    df_unido = pd.concat(dataframes, ignore_index=True)
    df_unido.to_csv("unificado.csv", index=False)
    print(f"✅ Archivos combinados. Total de filas: {len(df_unido)}")
else:
    print("🚫 No se combinaron archivos válidos.")
