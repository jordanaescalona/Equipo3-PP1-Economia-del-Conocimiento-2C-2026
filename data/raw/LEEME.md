# Datos originales (sin modificar)

| Archivo | Fuente | Uso |
|---|---|---|
| `sysarmy_2026_1.csv` | Encuesta de sueldos Sysarmy 2026.1 – https://sueldos.openqube.io/encuesta-sueldos-2026.01/ | Pregunta 1 |
| `proyectos-aprobados-soluciona-012023.xlsx` | https://datos.gob.ar/dataset/programa-soluciona | Preguntas 2 y 3 |
| `proyectos-aprobados-solucionaii-012024.xlsx` | https://datos.gob.ar/dataset/programa-soluciona-ii | Preguntas 2 y 3 |
| `proyectos-aprobados-solucionaverde-012023.xlsx` | https://datos.gob.ar/dataset/programa-soluciona-verde | Preguntas 2 y 3 |
| `beneficios-otorgados-nodosii-edc-072023.xlsx` | https://datos.gob.ar/dataset/programa-nodos-de-la-economia-del-conocimiento | Preguntas 2 y 3 |
| `beneficios-otorgados-colaborativa-202401.xlsx` | https://datos.gob.ar/dataset/programa-produccion-colaborativa-de-economia-del-conocimiento | Preguntas 2 y 3 |
| `beneficios-aprobados-fortalecer-202301.xlsx` | https://datos.gob.ar/dataset/programa-fortalecer | Preguntas 2 y 3 |
| `proyectos-aprobados-satelital-012024.xlsx` | https://datos.gob.ar/dataset/programa-potenciar-satelital | Preguntas 2 y 3 |
| `proyectos-aprobados-vdj-012024.xlsx` | https://datos.gob.ar/dataset/programa-potenciar-industria-del-videojuego | Preguntas 2 y 3 |
| `proyectos-aprobados-capacitacion-gob-subnacionales-202307.xlsx` | https://datos.gob.ar/dataset/programa-capacitacion-4-0-y-economia-del-conocimiento-para-gobiernos-subnacionales | Pregunta 2 |
| `diccionario_cod_depto.csv`, `diccionario_clae2.csv` | CEP XXI – https://datos.gob.ar/dataset/puestos-de-trabajo-por-departamento-partido-y-sector-de-actividad | Pregunta 3 |
| `puestos_depto_priv_por_clae2.csv` (**no está en GitHub**) | CEP XXI – mismo enlace | Pregunta 3 |
| `ipc_api.csv` | INDEC – IPC nivel general nacional (base dic-2016 = 100), ene-2020 a dic-2023, vía API de Series de Tiempo de datos.gob.ar | Preguntas 2 y 3 (ajuste por inflación) |
| `tipo_cambio_api.csv` | BCRA – tipo de cambio de referencia Com. A3500, dic-2025 a feb-2026, vía API de Series de Tiempo de datos.gob.ar | Pregunta 1 (salarios en dólares) |

**Archivo pesado:** `puestos_depto_priv_por_clae2.csv` pesa unos 95 MB, por lo que se guarda en Google Drive (carpeta Sprint_1 / 02_Datos) y no en GitHub. Para ejecutar el script, descargarlo y copiarlo en esta carpeta.

**Nota:** `sysarmy_2026_1.csv` es la versión re-guardada por el equipo (separador `;`, codificación Windows-1252). El CSV original de Sysarmy usa `,`, UTF-8 y trae 9 filas vacías antes del encabezado. 
**Nota:** en `ipc_api.csv` la columna `indice_tiempo` quedó como número de serie de Excel (43831 = 01/01/2020). La versión limpia (`data/processed/ipc_mensual.csv`) tiene la fecha correcta.

## Fuentes usadas sin archivo en esta carpeta

| Dato | Fuente | Uso | Dónde está |
|---|---|---|---|
| Población por provincia | INDEC – Censo Nacional 2022 | Preguntas 2 y 3 | `data/processed/poblacion_provincia_2022.csv` |
| Piso salarial del convenio | AGC – CCT 1696/23, grillas 3T 2026 – https://informaticos.ar/convenios/ | Pregunta 1 y validación | Dentro de `analysis/validacion_salarios_sysarmy.ipynb` |
| Salario mediano y promedio por rama | CEP XXI – https://datos.gob.ar/dataset/produccion-salarios-promedio-mediano-por-sector-actividad | Validación | Consulta puntual (CLAE2 62, nov-2023) |
