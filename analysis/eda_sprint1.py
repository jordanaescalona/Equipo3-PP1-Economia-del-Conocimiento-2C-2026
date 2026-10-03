"""
EDA inicial – Sprint 1
Equipo 3 - PP1 - Economía del Conocimiento - 2C - 2026

Exploración inicial sobre los datos ORIGINALES (data/raw), sin limpieza previa.
La limpieza y transformación (ETL con Pentaho + MySQL) se hace en el Sprint 2.

Genera:
  reports/sprint1/eda_resumen.xlsx   -> tablas de perfil, calidad y resúmenes
  reports/sprint1/graficos/*.png     -> los 4 gráficos del documento EDA

Uso (desde la carpeta principal del repositorio):
  pip install -r requirements.txt
  python analysis/eda_sprint1.py

Nota: el archivo del CEP XXI (puestos_depto_priv_por_clae2.csv, ~95 MB) no está en
GitHub por su tamaño. Descargarlo de datos.gob.ar o de la carpeta de Drive y copiarlo
en data/raw/ (también acepta la versión comprimida .zip).
"""
from pathlib import Path
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

warnings.filterwarnings("ignore")
RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw"
SALIDA = RAIZ / "reports" / "sprint1"
GRAF = SALIDA / "graficos"
GRAF.mkdir(parents=True, exist_ok=True)

AZUL, GRIS, TINTA, SUAVE = "#2a78d6", "#b4b2a7", "#2b2b28", "#5f5e5a"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": TINTA, "axes.labelcolor": TINTA,
                     "xtick.color": TINTA, "ytick.color": TINTA})

# Códigos INDEC de provincia (iguales en los programas y en el CEP XXI)
PROVINCIAS = {2: "CABA", 6: "Buenos Aires", 10: "Catamarca", 14: "Córdoba", 18: "Corrientes", 22: "Chaco",
              26: "Chubut", 30: "Entre Ríos", 34: "Formosa", 38: "Jujuy", 42: "La Pampa", 46: "La Rioja",
              50: "Mendoza", 54: "Misiones", 58: "Neuquén", 62: "Río Negro", 66: "Salta", 70: "San Juan",
              74: "San Luis", 78: "Santa Cruz", 82: "Santa Fe", 86: "Santiago del Estero", 90: "Tucumán",
              94: "Tierra del Fuego"}

PUESTOS_IA = ["Data Scientist", "Data Engineer", "BI Analyst / Data Analyst", "AI Engineer",
              "AI / Prompt / Chatbots", "Data Governance / GRC"]


def a_numero(serie):
    """Convierte texto con coma decimal (ej. '3424985,22') a número."""
    return pd.to_numeric(serie.astype(str).str.replace(",", ".", regex=False), errors="coerce")


def limites_iqr(serie):
    q1, q3 = serie.quantile([0.25, 0.75])
    return q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)


def perfil(df, nombre):
    """Perfil de columnas: tipo, nulos, únicos, mínimo y máximo."""
    filas = []
    for c in df.columns:
        s = df[c]
        num = pd.api.types.is_numeric_dtype(s)
        filas.append({"dataset": nombre, "variable": c, "tipo_leido": str(s.dtype),
                      "nulos": int(s.isna().sum()), "pct_nulos": round(s.isna().mean() * 100, 1),
                      "valores_unicos": int(s.nunique()),
                      "minimo": s.min() if num else None, "maximo": s.max() if num else None,
                      "ejemplo": s.dropna().iloc[0] if s.notna().any() else None})
    return pd.DataFrame(filas)


def estilo(ax):
    for lado in ["top", "right", "left"]:
        ax.spines[lado].set_visible(False)
    ax.spines["bottom"].set_color("#d9d8d2")
    ax.tick_params(axis="y", length=0)
    ax.xaxis.grid(True, color="#ecebe6")
    ax.set_axisbelow(True)


tablas = {}

# =====================================================================
# 1) SYSARMY – Pregunta 1
# =====================================================================
crudo = pd.read_csv(RAW / "sysarmy_2026_1.csv", sep=";", encoding="cp1252", low_memory=False)
# Si usan el CSV original descargado de Sysarmy: sep=",", encoding="utf-8", skiprows=9
sy = crudo.dropna(how="all").drop(columns=[c for c in crudo if crudo[c].isna().all()])
print(f"Sysarmy: {len(sy)} registros, {sy.shape[1]} variables "
      f"({len(crudo) - len(sy)} filas vacías y {crudo.shape[1] - sy.shape[1]} columnas vacías descartadas)")
tablas["Sysarmy_perfil"] = perfil(sy, "Sysarmy")

sy["salario_bruto"] = a_numero(sy["ultimo_salario_mensual_o_retiro_bruto_en_pesos_argentinos"])
sy["grupo_puesto"] = np.where(sy["trabajo_de"].isin(PUESTOS_IA), "Datos e IA", "Resto IT")
ft = sy[sy["dedicacion"] == "Full-Time"]
inf, sup = limites_iqr(ft["salario_bruto"])
tablas["Sysarmy_calidad"] = pd.DataFrame({
    "control": ["Filas duplicadas", "Salarios con coma decimal", "Salarios <= 0",
                "Atípicos altos (Full-Time, IQR)", "Límite superior IQR", "Edad > 90 (imposible)",
                "_sal igual al salario bruto (%)"],
    "resultado": [int(sy.drop(columns=["salario_bruto", "grupo_puesto"]).duplicated().sum()),
                  int(sy["ultimo_salario_mensual_o_retiro_bruto_en_pesos_argentinos"].astype(str).str.contains(",").sum()),
                  int((sy["salario_bruto"] <= 0).sum()), int((ft["salario_bruto"] > sup).sum()), round(sup),
                  int((sy["tengo_edad"] > 90).sum()),
                  round((sy["_sal"] == sy["ultimo_salario_mensual_o_retiro_bruto_en_pesos_argentinos"]).mean() * 100, 1)]})
tablas["Sysarmy_salario_grupo"] = (ft.groupby("grupo_puesto")["salario_bruto"]
                                  .describe().round(0).reset_index())

# Gráfico 1 – distribución del salario por grupo
fig, ax = plt.subplots(figsize=(7.5, 3.2))
datos = [ft.loc[ft.grupo_puesto == g, "salario_bruto"].dropna() for g in ["Datos e IA", "Resto IT"]]
bp = ax.boxplot(datos, vert=False, patch_artist=True, widths=0.5,
                flierprops=dict(marker="o", markersize=3, markerfacecolor=SUAVE, markeredgecolor="none", alpha=.4),
                medianprops=dict(color=TINTA, linewidth=2))
for caja, color in zip(bp["boxes"], [AZUL, GRIS]):
    caja.set_facecolor(color); caja.set_edgecolor(color); caja.set_alpha(.85)
ax.set_yticks([1, 2], ["Datos e IA", "Resto IT"]); ax.invert_yaxis()
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v/1e6:.0f} M"))
ax.set_xlabel("Salario bruto mensual (pesos)"); estilo(ax)
ax.set_title("Distribución del salario bruto: datos e IA frente al resto", loc="left", fontsize=11, fontweight="bold")
fig.text(0.01, 0.01, "Fuente: Encuesta de sueldos Sysarmy 2026.1. Solo full-time. Los puntos son valores atípicos.",
         fontsize=8, color=SUAVE)
plt.tight_layout(rect=(0, 0.05, 1, 1)); plt.savefig(GRAF / "G1_distribucion_salario_por_grupo.png", dpi=160); plt.close()

# =====================================================================
# 2) PROGRAMAS – Pregunta 2
# =====================================================================
anio_resolucion = lambda s: s.astype(str).str.extract(r"(20\d\d)")[0].astype(float)
PROGRAMAS = [  # archivo, programa, tipo de beneficiario, columna beneficiario, monto, año
    ("proyectos-aprobados-soluciona-012023.xlsx", "SOLUCIONA", "Empresa", "beneficiario_razón_social",
     lambda d: d.monto_aprobado, lambda d: d.partida_presupuestaria),
    ("proyectos-aprobados-solucionaii-012024.xlsx", "SOLUCIONA II", "Empresa", "beneficiario_razón_social",
     lambda d: d.monto_aprobado, lambda d: d.partida_presupuestaria),
    ("proyectos-aprobados-solucionaverde-012023.xlsx", "SOLUCIONA VERDE", "Empresa", "beneficiario_razon_social",
     lambda d: d.monto_aprobado, lambda d: d.partida_presupuestaria),
    ("beneficios-otorgados-nodosii-edc-072023.xlsx", "NODOS", "Polo/Clúster", "organismo_nombre_o_razon_social",
     lambda d: d.anr_aprobado, lambda d: anio_resolucion(d.resolucion_numero)),
    ("beneficios-otorgados-colaborativa-202401.xlsx", "Producción Colaborativa", "Empresa", "beneficiario_razon_social",
     lambda d: d.anr_abonado.fillna(0) + d.subsidio_tasa_credito.fillna(0), lambda d: anio_resolucion(d.resolucion)),
    ("beneficios-aprobados-fortalecer-202301.xlsx", "FORTALECER", "Empresa", "organismo_nombre_o_razon_social",
     lambda d: d.anr_aprobado, lambda d: anio_resolucion(d.resolucion_numero)),
    ("proyectos-aprobados-satelital-012024.xlsx", "POTENCIAR Satelital", "Empresa/Institución",
     "organismo_nombre_o_razon_social", lambda d: d.anr_aprobado, lambda d: anio_resolucion(d.resolucion_numero)),
    ("proyectos-aprobados-vdj-012024.xlsx", "POTENCIAR Videojuego", "Empresa", "organismo_nombre_o_razon_social",
     lambda d: d.anr_aprobado, lambda d: anio_resolucion(d.resolucion_numero)),
    ("proyectos-aprobados-capacitacion-gob-subnacionales-202307.xlsx", "Capacitación 4.0", "Gobierno",
     "organismo_nombre", lambda d: d.anr_aprobado, lambda d: d.convocatoria),
]
partes, perfiles, resumen_archivos = [], [], []
for archivo, prog, tipo, col_benef, f_monto, f_anio in PROGRAMAS:
    d = pd.read_excel(RAW / archivo)
    perfiles.append(perfil(d, prog))
    resumen_archivos.append({"programa": prog, "archivo": archivo, "registros": len(d), "variables": d.shape[1],
                             "duplicados": int(d.duplicated().sum()), "nulos_totales": int(d.isna().sum().sum())})
    partes.append(pd.DataFrame({"programa": prog, "tipo_beneficiario": tipo,
                                "beneficiario": d[col_benef].astype(str).str.strip(),
                                "provincia_id": d["provincia_id"], "anio": f_anio(d), "monto": f_monto(d)}))
prog = pd.concat(partes, ignore_index=True)
prog["provincia"] = prog["provincia_id"].map(PROVINCIAS)
tablas["Programas_archivos"] = pd.DataFrame(resumen_archivos)
tablas["Programas_perfil"] = pd.concat(perfiles, ignore_index=True)
tablas["Programas_unificados"] = prog
inf, sup = limites_iqr(prog["monto"])
print(f"Programas: {len(prog)} beneficios, ${prog.monto.sum()/1e6:,.0f} M, "
      f"{prog.provincia.nunique()} provincias, {(prog.monto > sup).sum()} montos atípicos altos")

def ranking(df):
    r = (df.groupby("provincia").agg(monto=("monto", "sum"), beneficios=("monto", "size"))
         .sort_values("monto", ascending=False))
    r["pct"] = r["monto"] / r["monto"].sum() * 100
    return r

r_todos = ranking(prog)
tablas["Programas_por_provincia"] = r_todos.round(2).reset_index()
tablas["Programas_por_programa"] = (prog.groupby("programa")["monto"]
                                    .agg(["size", "sum", "median", "min", "max"]).round(0).reset_index())

# Gráfico 2 – monto por provincia
r = r_todos.iloc[::-1].copy(); r["mill"] = r["monto"] / 1e6
fig, ax = plt.subplots(figsize=(7.5, 6.2))
ax.barh(r.index, r["mill"], color=[AZUL if p in r_todos.index[:3] else GRIS for p in r.index], height=.7)
for y, (v, n, p) in enumerate(zip(r["mill"], r["beneficios"], r["pct"])):
    ax.text(v + r["mill"].max() * .01, y,
            f"{v:,.0f}".replace(",", ".") + f" M  ({p:.1f}".replace(".", ",") + f" %; {n} benef.)",
            va="center", fontsize=8)
estilo(ax); ax.set_xlim(0, r["mill"].max() * 1.32); ax.tick_params(labelsize=8.5)
ax.set_xlabel("Monto adjudicado total (millones de pesos corrientes)", fontsize=9)
top3 = r_todos["pct"].iloc[:3].sum()
fig.suptitle(f"Tres jurisdicciones concentran el {top3:.0f} % de los fondos\nde los programas de Economía del Conocimiento (2020-2023)",
             x=.02, ha="left", fontsize=11.5, fontweight="bold")
ax.set_title("Suma de los 9 programas, pesos corrientes de cada año. Etiqueta: millones, % del total y beneficiarios.",
             fontsize=8, loc="left", color=SUAVE)
fig.tight_layout(); fig.savefig(GRAF / "G2_monto_por_provincia.png", dpi=160); plt.close()

# =====================================================================
# 3) CEP XXI – Pregunta 3
# =====================================================================
cep_csv = RAW / "puestos_depto_priv_por_clae2.csv"
cep_zip = RAW / "puestos_depto_priv_por_clae2.zip"
if not cep_csv.exists() and not cep_zip.exists():
    print("AVISO: falta el archivo del CEP XXI en data/raw/. Se omite la pregunta 3.")
else:
    cep = pd.read_csv(cep_csv if cep_csv.exists() else cep_zip)
    tablas["CEP_perfil"] = perfil(cep, "CEP XXI")
    tablas["CEP_calidad"] = pd.DataFrame({
        "control": ["Registros", "Filas duplicadas", "Filas sin departamento", "Filas con -99 (secreto estadístico)",
                    "Primer mes", "Último mes"],
        "resultado": [len(cep), int(cep.duplicated().sum()), int(cep.codigo_departamento_indec.isna().sum()),
                      int((cep.puestos == -99).sum()), cep.fecha.min(), cep.fecha.max()]})
    dicc = pd.read_csv(RAW / "diccionario_cod_depto.csv")
    c62 = cep[cep.clae2 == 62].merge(dicc[["codigo_departamento_indec", "id_provincia_indec"]]
                                    .rename(columns={"id_provincia_indec": "prov_dicc"}),
                                    on="codigo_departamento_indec", how="left")
    c62["puestos_validos"] = c62["puestos"].where(c62["puestos"] >= 0)   # -99 = dato protegido
    c62["anio"] = c62["fecha"].str[:4].astype(int)

    # Gráfico 3 – evolución del empleo CLAE 62 (total país)
    mensual = c62.groupby("fecha")["puestos_validos"].sum(); mensual.index = pd.to_datetime(mensual.index)
    tablas["CEP_clae62_anual"] = mensual.groupby(mensual.index.year).mean().round(0).rename("puestos_promedio").reset_index()
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    ax.plot(mensual.index, mensual / 1000, color=AZUL, lw=2)
    ax.axvspan(pd.Timestamp("2020-01-01"), pd.Timestamp("2023-12-31"), color="#ecebe6", zorder=0)
    ax.text(pd.Timestamp("2020-02-01"), mensual.max() / 1000 * .62, "Período de los\nprogramas (2020-2023)", fontsize=8, color=SUAVE)
    for lado in ["top", "right"]: ax.spines[lado].set_visible(False)
    ax.yaxis.grid(True, color="#ecebe6"); ax.set_axisbelow(True); ax.set_ylim(0, mensual.max() / 1000 * 1.1)
    ax.set_ylabel("Miles de puestos", fontsize=9)
    crec = (mensual.iloc[-1] / mensual.iloc[0] - 1) * 100
    fig.suptitle(f"El empleo en servicios informáticos creció {crec:.0f} % entre 2014 y 2023", x=.02, ha="left",
                 fontsize=11.5, fontweight="bold")
    ax.set_title("Puestos asalariados registrados del sector privado, CLAE 62, total país, mensual.", fontsize=8,
                 loc="left", color=SUAVE)
    fig.tight_layout(); fig.savefig(GRAF / "G3_evolucion_empleo_clae62.png", dpi=160); plt.close()

    # Empleo 2021 por provincia vs fondos (sin Capacitación 4.0, dirigido a gobiernos)
    x = c62[(c62.anio == 2021) & c62.prov_dicc.notna()]
    emp = x.groupby(["prov_dicc", "fecha"])["puestos_validos"].sum().groupby("prov_dicc").mean()
    emp.index = emp.index.astype(int).map(PROVINCIAS)
    fondos = ranking(prog[prog.tipo_beneficiario != "Gobierno"])["monto"]
    comp = pd.DataFrame({"fondos": fondos, "empleo_2021": emp}).fillna(0)
    comp["pct_fondos"] = comp.fondos / comp.fondos.sum() * 100
    comp["pct_empleo"] = comp.empleo_2021 / comp.empleo_2021.sum() * 100
    comp["ranking_fondos"] = comp.fondos.rank(ascending=False, method="min").astype(int)
    comp["ranking_empleo"] = comp.empleo_2021.rank(ascending=False, method="min").astype(int)
    comp = comp.sort_values("fondos", ascending=False)
    tablas["Fondos_vs_empleo"] = comp.round(2).reset_index(names="provincia")

    # Gráfico 4 – % fondos vs % empleo (misma escala)
    tt = comp[(comp.pct_fondos >= 1) | (comp.pct_empleo >= 1)].sort_values("pct_fondos")
    fig, ax = plt.subplots(figsize=(7.5, 6)); y = np.arange(len(tt)); h = .38
    ax.barh(y + h/2 + .01, tt.pct_fondos, h, color=AZUL, label="% de los fondos (sin Capacitación 4.0)")
    ax.barh(y - h/2 - .01, tt.pct_empleo, h, color=GRIS, label="% del empleo en servicios informáticos (CLAE 62, 2021)")
    for i, (a, b) in enumerate(zip(tt.pct_fondos, tt.pct_empleo)):
        ax.text(a + .4, i + h/2, f"{a:.1f}".replace(".", ","), va="center", fontsize=7.5)
        ax.text(b + .4, i - h/2, f"{b:.1f}".replace(".", ","), va="center", fontsize=7.5, color=SUAVE)
    ax.set_yticks(y, tt.index, fontsize=8.5); estilo(ax); ax.set_xlim(0, 44)
    ax.set_xlabel("Porcentaje del total nacional", fontsize=9); ax.legend(loc="lower right", frameon=False, fontsize=8)
    caba = comp.loc["CABA"]
    fig.suptitle(f"CABA reúne el {caba.pct_empleo:.0f} % del empleo informático pero solo el {caba.pct_fondos:.0f} % de los fondos;\n"
                 "las demás provincias recibieron más fondos que su peso en el empleo",
                 x=.02, ha="left", fontsize=11, fontweight="bold")
    ax.set_title("Provincias con al menos 1 % de los fondos o del empleo. Puestos asalariados registrados del sector privado.",
                 fontsize=8, loc="left", color=SUAVE)
    fig.tight_layout(); fig.savefig(GRAF / "G4_fondos_vs_empleo.png", dpi=160); plt.close()

# =====================================================================
with pd.ExcelWriter(SALIDA / "eda_resumen.xlsx") as w:
    for nombre, t in tablas.items():
        t.to_excel(w, sheet_name=nombre[:31], index=False)
print(f"Listo: {SALIDA / 'eda_resumen.xlsx'} y {len(list(GRAF.glob('*.png')))} gráficos en {GRAF}")
