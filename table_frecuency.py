import pandas as pd

def main():

    df = pd.read_excel("divorcios_guatemala.xlsx", sheet_name=0)
    df.dropna(how="all", inplace=True)

    df.columns = [
        "Etiqueta",
        "ColExtra1",
        "Menos20",
        "Edad20_24",
        "Edad25_29",
        "Edad30_34",
        "Edad35_39",
        "Edad40_44",
        "Edad45_49",
        "Edad50_54",
        "Edad55_59",
        "Edad60ymas",
        "Ignorado",
        "Año",
        "Menos15",
        "Edad15_19",
        "Edad18_19"
    ]

    cols_interes = [
        "Menos20", "Edad20_24", "Edad25_29", "Edad30_34",
        "Edad35_39", "Edad40_44", "Edad45_49",
        "Edad50_54", "Edad55_59", "Edad60ymas", "Ignorado"
    ]

    df_largo = df.melt(
        id_vars=["Año"],
        value_vars=cols_interes,
        var_name="GrupoEdad",
        value_name="Divorcios"
    )

    tabla_frecuencia = df_largo.groupby("GrupoEdad")["Divorcios"].sum().reset_index()

    print("===== TABLA DE FRECUENCIA POR GRUPO DE EDAD =====")
    print(tabla_frecuencia)

    tabla_frecuencia.to_excel("tabla_frecuencia_edad.xlsx", index=False)


if __name__ == "__main__":
    main()
