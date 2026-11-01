![Economía del Conocimiento en Argentina – Equipo 3](assets/banner.svg)
# Economía del Conocimiento en Argentina – Análisis descriptivo

**Equipo 3 - PP1 - Economía del Conocimiento - 2C - 2026**
Prácticas Profesionalizantes 1 · Tecnicatura Superior en Ciencia de Datos e IA · Politécnico Malvinas Argentinas

## Integrantes del equipo
- Jordana Escalona – Analista de Datos / Documentadora
- José Luis Martín – Diseñador de Visualizaciones
- Alejandro Suarez – Encargado de Entrega / Comunicador
- David Moreira – Coordinador de Recursos / Calidad de Datos

---

## Descripción del proyecto
La Ley 27.506 de Economía del Conocimiento promueve actividades como el software y los servicios informáticos, la industria 4.0, la inteligencia artificial, la biotecnología y el audiovisual. Este proyecto realiza un **análisis descriptivo** con datos públicos para conocer el sector desde dos ejes:

1. **Talento:** cuánto cobran los puestos vinculados a datos e inteligencia artificial frente al resto de los puestos IT.
2. **Territorio:** cómo se distribuyeron entre las provincias los fondos de los programas de promoción (2020-2023) y si coinciden con el empleo en servicios informáticos.

El análisis es descriptivo: cuenta, resume y compara. No busca explicar causas ni medir el impacto de los programas.

---

## Fuente de datos
| Dataset | Fuente | Uso |
|---|---|---|
| Encuesta de sueldos Sysarmy 2026.1 | [Sysarmy](https://sysarmy.com/blog/posts/resultados-de-la-encuesta-de-sueldos-2026-1/) | P1 |
| 9 programas de la Economía del Conocimiento (2020–2023) | [datos.gob.ar](https://datos.gob.ar) – Ministerio de Economía | P2, P3 |
| Puestos de trabajo por provincia y rama (CLAE 62) | [CEP XXI](https://datos.gob.ar/dataset/puestos-de-trabajo-por-departamento-partido-y-sector-de-actividad) | P3 |
| IPC | [INDEC](https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-31) | P2 (pesos de 2023) |
| Población por provincia | INDEC – Censo 2022 | P2 (monto por habitante) |
| Tipo de cambio A3500 | [BCRA](https://www.bcra.gob.ar/tipo-cambio-referencia-comunicacion-a-3500-tcnpm/) | P1 (contexto) |
| Grilla del convenio AGC (enero 2026) | [informaticos.ar](https://informaticos.ar/convenios/) | P1 (validación) |
| Honorarios recomendados (09-2026) | [CPCI Córdoba](https://cpcipc.org.ar/honorarios-recomendados/) | P1 (validación) |

El programa vigente KIT 4.0 no tiene datos abiertos: se pidieron por la Ley 27.275 (ver `solicitudes/`).
Detalle, enlaces de descarga y registros de cada archivo: [`data/raw/LEEME.md`](data/raw/LEEME.md).

---

## Objetivos del análisis
**Hilo conductor:** ¿Dónde está el trabajo en datos e inteligencia artificial, cuánto vale, y los fondos públicos de la Economía del Conocimiento acompañan esa distribución?

- **P1 – Perfiles laborales + territorio:** ¿Cuánto cobran los puestos de Datos e IA frente al resto de IT, y cómo cambia esa diferencia entre CABA y el resto del país?
- **P2 – Distribución territorial de fondos:** ¿Qué provincias concentran los fondos de los programas de la Economía del Conocimiento y cuántos beneficios recibió cada una?
- **P3 – Territorio + empleo registrado:** ¿Los fondos se distribuyen en proporción al empleo informático registrado de cada provincia?

El análisis es descriptivo y comparativo: muestra qué pasa en los datos, no sus causas.

---

## Herramientas utilizadas
- **Python** (pandas, matplotlib): EDA inicial (Sprint 1) y EDA Sprint 2, en notebooks ejecutables en Google Colab
- **OpenRefine**: limpieza de Sysarmy, programas y CPCI, con recetas JSON reproducibles – Sprint 2
- **Pentaho Data Integration**: unión de los 9 programas y transformación del CEP XXI – Sprint 2
- **Power BI**: modelo estrella con dim_provincia (Sprint 2) y dashboard interactivo final de 11 páginas (Sprint 3)
- Excel / CSV, Google Drive, Trello, GitHub y GitHub Desktop (ramas y pull requests), Google Meet y WhatsApp

---

## Proceso de análisis
- **Sprint 1 (completado):** organización del equipo, ficha de conocimiento del dominio, preguntas de análisis, diccionario de datos y EDA inicial sobre los datos originales.
- **Sprint 2 (completado):** limpieza y transformación (ETL) con OpenRefine y Pentaho según los problemas detectados en el EDA, integración por provincia (provincia_id), datasets complementarios, validación de salarios con tres fuentes, modelo base en Power BI, EDA Sprint 2 y reporte de insights.
- **Sprint 3 (completado):** dashboard interactivo en Power BI (11 páginas), 5 insights consolidados, data storytelling, presentación y exposición final, informe técnico, manual de usuario, diccionario de datos final y retrospectiva.

### Cómo reproducir el EDA
```bash
pip install -r requirements.txt
python analysis/eda_sprint1.py
```
Antes, copiar en `data/raw/` el archivo del CEP XXI, que no está en GitHub por su tamaño (ver [`data/raw/LEEME.md`](data/raw/LEEME.md)). El script genera `reports/sprint1/eda_resumen.xlsx` y los gráficos de `reports/sprint1/graficos/`.

**EDA Sprint 2:** [`analysis/eda_sprint2.ipynb`](analysis/eda_sprint2.ipynb) · [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1_4VTmtrcp5sCaBpBqJgX3_5VcBdsjKus)

Documento del EDA Sprint 2: [`reports/sprint2/PP1-S2-EDA-Sprint2.pdf`](reports/sprint2/PP1-S2-EDA-Sprint2.pdf) · Modelo de Power BI: [`reports/sprint2/EQ3_PP1_modelo.pbix`](reports/sprint2/EQ3_PP1_modelo.pbix)

---

## Entregables del Sprint 3
| Entregable | Archivo |
|---|---|
| Dashboard interactivo de Power BI | [`reports/sprint3/PP1-EQ3-Entrega_final_dashboard_interactivo.pbix`](reports/sprint3/PP1-EQ3-Entrega_final_dashboard_interactivo.pbix) · [PDF](reports/sprint3/PP1-S3-EQ3-Entrega_final_dashboard_interactivo.pdf) |
| Informe técnico | [`reports/sprint3/PP1-S3-Informe-Tecnico-Equipo3.pdf`](reports/sprint3/PP1-S3-Informe-Tecnico-Equipo3.pdf) |
| EDA final | [`reports/sprint3/PP1-S3-EDA-Final.pdf`](reports/sprint3/PP1-S3-EDA-Final.pdf) |
| Insights consolidados | [`reports/sprint3/PP1-S3-Insights-Consolidados.pdf`](reports/sprint3/PP1-S3-Insights-Consolidados.pdf) |
| Presentación (Data Storytelling) | [`reports/sprint3/PP1-S3-Presentacion-Data-Storytelling.pdf`](reports/sprint3/PP1-S3-Presentacion-Data-Storytelling.pdf) |
| Manual de usuario del dashboard | [`reports/sprint3/PP1-S3-Manual-de-Usuario-Tablero-Power-BI.pdf`](reports/sprint3/PP1-S3-Manual-de-Usuario-Tablero-Power-BI.pdf) |
| Diccionario de datos final | [`docs/PP1-S3-DiccionarioDatos-Final.xlsx`](docs/PP1-S3-DiccionarioDatos-Final.xlsx) |
| Retrospectiva del Sprint 3 | [`reports/sprint3/PP1-S3-Retrospectiva-Equipo3.pdf`](reports/sprint3/PP1-S3-Retrospectiva-Equipo3.pdf) |
| Video de la exposición | Se publicará en cuando esté en YouTube |

El dashboard tiene portada interactiva, navegación (Inicio, Anterior, Siguiente), filtros, botón Restablecer, un panel **Datasets** con las fuentes de cada página y un glosario. El detalle de cada página está en el manual de usuario.

---

## Resultados principales
*Resultados finales (Sprint 3) – 5 insights:*
- **P1 · Efecto composición:** en el total, Datos e IA cobra 8,8 % menos que el resto de IT ($3,10 M frente a $3,40 M), pero a igual seniority cobra igual o más (+20,9 % Junior, +15,8 % Semi-Senior). La diferencia se explica porque tiene menos personas Senior (39,8 % frente a 61,1 %). Las medianas de Datos e IA superan el piso del convenio AGC en todos los niveles.
- **P1 · No es solo CABA:** en el resto del país, Datos e IA cobra más en los tres niveles (+18 %, +19 % y +10 %). Fuera de CABA hay pocas respuestas: los valores son orientativos.
- **P2 · Por habitante:** Tierra del Fuego ($2.326), CABA ($1.188) y La Rioja ($1.000) superan el promedio nacional ($497); Buenos Aires, la que más recibió en total (29,3 %), queda por debajo ($399).
- **P2 · Tamaño de cada beneficio:** en las provincias con pocos beneficios, cada uno fue de más dinero: Chubut ($16,8 M), Río Negro ($14,8 M) y Entre Ríos ($14,7 M) frente a CABA ($9,9 M); el beneficio típico del país es de $10 M.
- **P3 · Fondos y empleo:** 22 de las 24 provincias reciben fondos por encima de su peso en el empleo informático; CABA concentra el 38,4 % del empleo y recibió el 16,5 % de los fondos (índice 0,43).

*Sprint 2 (datos limpios, indicadores relativos):*
- **P1:** a igual seniority, Datos e IA cobra igual o más que el resto de IT (+20,9 % Junior, +15,8 % Semi-Senior); la mediana total es menor por efecto composición. La ventaja se mantiene fuera de CABA.
- **P2:** por habitante (pesos de 2023), Tierra del Fuego ($2.326), CABA ($1.188) y La Rioja ($1.000) superan el promedio nacional ($497); Buenos Aires queda por debajo ($399).
- **P3:** 22 de las 24 provincias reciben fondos por encima de su peso en el empleo informático; solo CABA (índice 0,43) y Buenos Aires (0,78) reciben menos.

*Observaciones iniciales del Sprint 1:*
- Los puestos de datos e IA son el 8,9 % de las respuestas de Sysarmy. Su mediana salarial total es algo menor que la del resto ($3,10 M frente a $3,40 M, full-time), posiblemente porque el grupo tiene menos personas senior.
- Los 9 programas otorgaron 1.035 beneficios por $7.133 M (pesos corrientes) entre 2020 y 2023 y llegaron a las 24 jurisdicciones; Buenos Aires, CABA, Santa Fe y Córdoba reúnen cerca del 70 %.
- Las provincias con más fondos son también las de más empleo informático, pero las proporciones no coinciden: CABA y Buenos Aires tienen una parte del empleo mayor que su parte de los fondos.
- **Calidad de datos:** nombres de provincia y de columnas distintos entre archivos, montos en pesos de distintos años, valores protegidos (-99) en el CEP XXI y valores imposibles en algunas variables de Sysarmy. Se corrigieron en el ETL del Sprint 2.

---

## Visualizaciones

### Dashboard final (Sprint 3)

Todas las páginas del dashboard (portada, P1.1 a P3.2 y glosario): [**ver el PDF del dashboard**](reports/sprint3/PP1-S3-EQ3-Entrega_final_dashboard_interactivo.pdf).

### EDA Sprint 2

**P1 – Mediana del salario por seniority y piso del convenio AGC**
![Salarios por seniority](reports/sprint2/graficos/g1_salarios_seniority.png)

**P1 – Composición por seniority (efecto composición)**
![Composición por seniority](reports/sprint2/graficos/g2_composicion_seniority.png)

**P2 – Monto típico por beneficio**
![Monto típico por beneficio](reports/sprint2/graficos/g3_monto_tipico.png)

**P3 – Índice fondos / empleo informático**
![Índice fondos / empleo](reports/sprint2/graficos/g4_indice_fondos_empleo.png)

### EDA inicial (Sprint 1)
![Distribución del salario por grupo](reports/sprint1/graficos/G1_distribucion_salario_por_grupo.png)
![Monto adjudicado por provincia](reports/sprint1/graficos/G2_monto_por_provincia.png)
![Evolución del empleo en servicios informáticos](reports/sprint1/graficos/G3_evolucion_empleo_clae62.png)
![Fondos y empleo por provincia](reports/sprint1/graficos/G4_fondos_vs_empleo.png)

---

## Conclusiones
- A igual experiencia, los perfiles de datos e inteligencia artificial cobran igual o más que el resto de IT, también fuera de CABA. Comparar solo totales lleva a una conclusión equivocada por el efecto composición.
- Los fondos de los programas no siguen el tamaño de cada provincia ni su empleo informático: medidos por habitante y en proporción al empleo, se distribuyeron de forma más pareja entre provincias, y en las provincias con pocos beneficios cada beneficio fue más grande.
- Comparar a igual seniority, por habitante y en proporción al empleo muestra lo que los totales esconden.
- El análisis es descriptivo: muestra cómo se repartieron salarios y fondos, no explica por qué. Limitaciones: Sysarmy es una encuesta voluntaria; los programas llegan hasta 2023 (KIT 4.0 sin datos abiertos) y no se incluyen los beneficios impositivos del Régimen de Promoción (Ley 27.506).

---

## Estructura del repositorio
```
├── README.md
├── requirements.txt
├── data/
│   ├── raw/          → datos originales sin modificar (+ LEEME.md con las fuentes)
│   └── processed/    → datos limpios (Sprint 2)
├── analysis/
│   ├── eda_sprint1.py                     → script del EDA inicial
│   ├── eda_sprint2.ipynb                  → notebook del EDA Sprint 2
│   ├── unir_programas.ktr                 → Pentaho: unión de los 9 programas
│   ├── cep_empleo.ktr                     → Pentaho: empleo por provincia (CEP XXI)
│   ├── validacion_salarios_sysarmy.ipynb  → validación de salarios (CEP XXI y convenio AGC)
│   └── evidencia_comparativa_salarios.jpeg → gráfico de la validación de salarios
├── assets/
│   └── banner.svg    → banner del README
├── solicitudes/      → pedido de datos de KIT 4.0 (Ley 27.275)
|── docs/
│   ├── PP1-S1-Ficha-Conocimiento-del-Dominio.docx
│   ├── PP1-S1-Preguntas-de-analisis.docx
│   ├── PP1-S1-Diccionario-de-Datos.xlsx
│   ├── PP1-S2-Bitacora-ETL-Equipo3.csv
│   ├── PP1-S2-Check-Limpieza-Normalizacion.pdf
│   ├── PP1-S2-Registro-Errores-Herramienta.pdf
│   └── PP1-S3-DiccionarioDatos-Final.xlsx  → diccionario final (tablas, medidas DAX y uso por página)
└── reports/
    ├── sprint1/
    │   ├── PP1-S1-EDA-Inicial.docx
    │   ├── PP1-S1-Ficha-Seguimiento-Sprint.docx
    │   ├── eda_resumen.xlsx
    │   └── graficos/
    ├── sprint2/
    │   ├── PP1-S2-EDA-Sprint2.pdf
    │   ├── EQ3_PP1_modelo.pbix   → modelo base de Power BI
    │   └── graficos/             → gráficos del EDA Sprint 2
    └── sprint3/
        ├── PP1-EQ3-Entrega_final_dashboard_interactivo.pbix  → dashboard final
        ├── PP1-S3-EQ3-Entrega_final_dashboard_interactivo.pdf
        ├── PP1-S3-Informe-Tecnico-Equipo3.pdf
        ├── PP1-S3-EDA-Final.pdf
        ├── PP1-S3-Insights-Consolidados.pdf
        ├── PP1-S3-Presentacion-Data-Storytelling.pdf
        ├── PP1-S3-Manual-de-Usuario-Tablero-Power-BI.pdf
        └── PP1-S3-Retrospectiva-Equipo3.pdf
```
