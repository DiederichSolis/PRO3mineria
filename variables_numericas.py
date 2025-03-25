import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar archivo
archivo = "divorcios_guatemala.xlsx"
df = pd.read_excel(archivo, sheet_name="Grupos edad hombre y mujer")

# Limpiar columnas: eliminar columnas no numéricas irrelevantes
df_clean = df.drop(columns=["Unnamed: 0", "Unnamed: 1", "Año"], errors='ignore')

# Asegurarse de que todos los datos sean numéricos
df_clean = df_clean.apply(pd.to_numeric, errors='coerce')

# Eliminar filas con valores nulos en todas las columnas
df_clean = df_clean.dropna(how='all')

# Transponer para trabajar por grupo de edad
df_trans = df_clean.T
print(df_trans.columns.tolist())

df_trans = df_trans.dropna()

# --- Estadísticas Descriptivas ---
print("===== Estadísticas Generales =====")
print(df_clean.describe())

# --- Visualización: Gráfico de caja (boxplot) ---
plt.figure(figsize=(12, 6))
sns.boxplot(data=df_clean)
plt.title("Distribución de divorcios por grupo de edad")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --- Visualización: Histograma ---
plt.figure(figsize=(12, 6))
df_clean.sum().plot(kind='bar')
plt.title("Cantidad total de divorcios por grupo de edad")
plt.ylabel("Cantidad")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --- Correlación (opcional si hay suficientes datos) ---
plt.figure(figsize=(10, 8))
sns.heatmap(df_clean.corr(), annot=True, cmap="Blues")
plt.title("Mapa de calor de correlaciones entre grupos de edad")
plt.show()
