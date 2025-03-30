import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt

# --- 1. Cargar Datos ---
try:
    # Intentar leer con codificación UTF-8 (común)
    df = pd.read_csv('unificado.csv', low_memory=False)
except UnicodeDecodeError:
    try:
        # Intentar con latin1 si UTF-8 falla
        df = pd.read_csv('Proyecto3MineriaDatos/unificado.csv', encoding='latin1', low_memory=False)
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        # Salir si no se puede leer el archivo
        exit()
except FileNotFoundError:
    print("Error: El archivo 'Proyecto3MineriaDatos/unificado.csv' no se encontró.")
    exit()

print("Columnas originales:", df.columns.tolist())
print("Primeras filas:\n", df.head())
print("\nInformación del DataFrame:")
df.info()

# --- 2. Seleccionar Variables para Clustering ---
# Nos enfocaremos en edad, escolaridad y año de ocurrencia
# Asegurémonos de que los nombres de columna coinciden exactamente
# Usaremos los nombres que parecen más probables basados en el PDF y la salida de df.info()
# Si 'ESCMUJ' no existe o tiene otro nombre, ajustar aquí.
# Asumiremos que ESCHOM/ESCMUJ existen y son numéricos representando niveles.
numerical_features = ['EDADHOM', 'EDADMUJ', 'ESCHOM', 'ESCMUJ', 'AÑOOCU']

# Verificar si todas las columnas seleccionadas existen
missing_cols = [col for col in numerical_features if col not in df.columns]
if missing_cols:
    print(f"\nError: Las siguientes columnas no se encontraron en el CSV: {missing_cols}")
    # Intentar con nombres alternativos o eliminar de la lista
    # Por ejemplo, si ESCMUJ no está, podríamos quitarla:
    # numerical_features.remove('ESCMUJ')
    # O si sospechamos un error tipográfico, corregirlo.
    # Por ahora, detendremos la ejecución si faltan columnas clave.
    exit()

# Seleccionar solo las columnas relevantes
df_cluster = df[numerical_features].copy()

# --- 3. Preprocesamiento ---
# Convertir columnas a numéricas, forzando errores a NaN
for col in numerical_features:
    df_cluster[col] = pd.to_numeric(df_cluster[col], errors='coerce')

# Manejar valores faltantes (NaN) - Usaremos imputación con la media
print(f"\nValores faltantes antes de imputar:\n{df_cluster.isnull().sum()}")
imputer = SimpleImputer(strategy='mean')
df_cluster_imputed = imputer.fit_transform(df_cluster)
df_cluster_imputed = pd.DataFrame(df_cluster_imputed, columns=numerical_features)
print(f"\nValores faltantes después de imputar:\n{df_cluster_imputed.isnull().sum()}")


# Escalar las variables
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_cluster_imputed)

# --- 4. Determinar Número de Clusters (k) - Método del Codo ---
print("\nCalculando WCSS para el método del codo...")
wcss = [] # Within-Cluster Sum of Squares
k_range = range(1, 11) # Probar de 1 a 10 clusters

for k in k_range:
    kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42, n_init=10) # n_init para estabilidad
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_) # inertia_ es el WCSS

# Graficar el método del codo
plt.figure(figsize=(10, 6))
plt.plot(k_range, wcss, marker='o', linestyle='--')
plt.title('Método del Codo para Determinar k Óptimo')
plt.xlabel('Número de Clusters (k)')
plt.ylabel('WCSS (Inertia)')
plt.xticks(k_range)
plt.grid(True)
plt.show()

# --> ¡INTERPRETACIÓN DEL GRÁFICO DEL CODO REQUERIDA AQUÍ! <--
# Observar el gráfico y elegir 'k' donde la curva empieza a aplanarse.
# Supongamos que el codo sugiere k=4 (esto es una suposición, ajustar según el gráfico real)
optimal_k = 4
print(f"\nBasado en el método del codo (inspección visual), elegimos k = {optimal_k}")

# --- 5. Aplicar K-Means ---
print(f"Aplicando K-Means con k = {optimal_k}...")
kmeans_final = KMeans(n_clusters=optimal_k, init='k-means++', random_state=42, n_init=10)
clusters = kmeans_final.fit_predict(X_scaled)

# Añadir la asignación de clusters al DataFrame original (con datos imputados)
df_cluster_imputed['Cluster'] = clusters
# También añadir al DataFrame original para análisis con otras variables
# Asegurarse de que los índices coincidan si hubo eliminaciones por NaN antes
df_analysis = df.loc[df_cluster_imputed.index].copy() # Usar índice de datos imputados
df_analysis['Cluster'] = clusters

# --- 6. Interpretar Clusters ---
print(f"\n--- Análisis de los {optimal_k} Clusters ---")

# Calcular centroides (promedios por cluster) en la escala original
centroids_scaled = kmeans_final.cluster_centers_
centroids_original = scaler.inverse_transform(centroids_scaled)
centroids_df = pd.DataFrame(centroids_original, columns=numerical_features)
print("\nCentroides de los Clusters (Promedios en escala original):")
print(centroids_df)

# Analizar tamaño y características de cada cluster
print("\nCaracterísticas promedio y tamaño por cluster:")
cluster_summary = df_cluster_imputed.groupby('Cluster').mean()
cluster_summary['Size'] = df_cluster_imputed['Cluster'].value_counts()
print(cluster_summary)

# Analizar la distribución de variables categóricas (como Ocupación) por cluster
# Asegurarse de que las columnas de ocupación existan
occupation_cols = ['OCUHOM', 'OCUMUJ']
existing_occ_cols = [col for col in occupation_cols if col in df_analysis.columns]

# Analizar la distribución de Ubicación (Departamento) por cluster
if 'DEPOCU' in df_analysis.columns:
    print("\nDistribución de Departamentos de Ocurrencia (Top 5) por Cluster:")
    df_analysis['DEPOCU'] = df_analysis['DEPOCU'].astype('category')
    dep_dist = df_analysis.groupby('Cluster')['DEPOCU'].apply(lambda x: x.value_counts().head(5))
    print(dep_dist)
else:
    print("\nNo se encontró la columna 'DEPOCU' para analizar por cluster.")
