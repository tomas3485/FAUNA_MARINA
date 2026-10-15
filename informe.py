import sqlite3

import pandas as pd
from openpyxl.chart import BarChart, Reference

conn = sqlite3.connect("fauna_marina.db")
df = pd.read_sql("SELECT * FROM avistamientos", conn)

# Limpiar fechas: las que no se puedan interpretar se descartan
df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce", utc=True, format="mixed")
df = df.dropna(subset=["fecha"])
df["mes"] = df["fecha"].dt.strftime("%Y-%m")
df["fecha"] = df["fecha"].dt.tz_localize(None)  # Excel no admite zonas horarias

resumen = df.groupby("especie").size().reset_index(name="registros")
por_mes = df.groupby(["mes", "especie"]).size().reset_index(name="registros")

with pd.ExcelWriter("informe.xlsx", engine="openpyxl") as writer:
    resumen.to_excel(writer, sheet_name="Resumen", index=False)
    por_mes.to_excel(writer, sheet_name="Por mes", index=False)
    df.to_excel(writer, sheet_name="Datos", index=False)

    ws = writer.sheets["Resumen"]
    chart = BarChart()
    chart.title = "Registros por especie"
    datos = Reference(ws, min_col=2, min_row=1, max_row=len(resumen) + 1)
    categorias = Reference(ws, min_col=1, min_row=2, max_row=len(resumen) + 1)
    chart.add_data(datos, titles_from_data=True)
    chart.set_categories(categorias)
    ws.add_chart(chart, "E2")

print(f"Informe generado con {len(df)} registros válidos")