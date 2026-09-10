# Sistema de Debrief de Marca (investigación + trazabilidad + documento final)

Sistema modular, reutilizable para cualquier marca/producto/país, para construir
debriefs estratégicos de marca respaldados por investigación web verificable,
con separación explícita entre **hechos**, **interpretaciones** e **hipótesis**,
y trazabilidad completa (fuente, URL, fecha, confiabilidad) para cada afirmación.

Se entrega ya ejecutado para el caso solicitado: **Alpin Chocolate (Alpina) —
mercado Colombia**. El documento final está en `output/alpin_debrief.md`.

## 1. Arquitectura — decisiones y por qué

Antes de escribir código se resolvieron las 10 preguntas de diseño del brief:

1. **Herramientas de navegación disponibles para Claude Code en este entorno.**
   Se probaron `WebSearch` (búsqueda) y `WebFetch` (lectura directa de una URL).
   Resultado real, no teórico: `WebFetch` devolvió `EGRESS_BLOCKED` para **todos**
   los dominios probados (alpina.com, nestle.com.co, exito.com, larepublica.co,
   semana.com, trends.google.com, kantar.com, andi.com.co, elcolombiano.com,
   valoraanalitik.com, pulzo.com, e incluso en.wikipedia.org). `WebSearch` sí
   funcionó y fue la única vía real de investigación: devuelve fragmentos
   ("snippets") sintetizados de páginas indexadas, con su URL de origen. **Todo
   el sistema está diseñado asumiendo que la investigación la hace el propio
   agente de Claude Code con `WebSearch`**, y que el código Python es la capa de
   almacenamiento, verificación estructural, deduplicación y ensamblaje del
   documento — no un scraper autónomo. Esto también significa que **no se
   requiere ninguna API key de búsqueda**: la búsqueda la hace Claude Code
   directamente.

2. **Cómo se almacenan las fuentes.** JSON plano y versionable por marca:
   `research/<brand>/sources.json` (una fuente = una URL, con categoría,
   fecha de publicación si se conoce, fecha de consulta, `access_status` y
   nivel de confiabilidad) y `research/<brand>/evidence.json` (afirmaciones
   puntuales, tipadas HECHO/INTERPRETACION/HIPOTESIS, ligadas a 1+ fuentes).

3. **Cómo se hacen búsquedas múltiples.** No hay "motor de búsqueda" en el
   código: quien investiga (el agente) ejecuta múltiples `WebSearch`/`WebFetch`
   guiado por `config/brands/<brand>.yaml` (fuentes prioritarias + preguntas de
   investigación) y va registrando lo encontrado con `EvidenceStore` (vía CLI o
   como en este caso, vía un script de siembra, ver punto 9).

4. **Cómo se evita información duplicada.** Dos mecanismos en
   `src/brand_debrief/evidence_store.py`: (a) deduplicación de **fuentes** por
   URL normalizada (esquema+dominio+ruta, sin querystring ni slash final); (b)
   deduplicación aproximada de **evidencia** por similitud de texto
   (`difflib.SequenceMatcher`, umbral 0.88) para no repetir la misma afirmación
   redactada de dos formas distintas.

5. **Cómo se verifican fuentes.** No hay "verificación automática de verdad"
   (eso requeriría acceso a las páginas, que estaba bloqueado). Lo que sí se
   automatiza: (a) toda evidencia debe apuntar a una fuente que exista; (b) el
   nivel de confiabilidad se asigna con criterio explícito por tipo de fuente
   (oficial/informe corporativo > institucional > investigación de mercado >
   prensa especializada > retail/redes > blogs); (c) cuando el contenido viene
   solo de un snippet de búsqueda y no de lectura directa de la página, la
   confiabilidad se baja un nivel respecto a lo que tendría si se hubiera
   verificado línea por línea, y se anota explícitamente en `notes`.

6. **Cómo se generan las citas.** `src/brand_debrief/citations.py` construye,
   a partir del `EvidenceStore`, la sección `FUENTES` (agrupada por categoría)
   y la `MATRIZ DE EVIDENCIA` (afirmación · tipo · fuente · URL · fecha ·
   confiabilidad) de forma **mecánica**: si una afirmación no está en
   `evidence.json`, no puede aparecer citada en el documento final. Esto
   impide la "bibliografía genérica" que el brief pedía evitar.

7. **Cómo se manejan páginas que bloquean el scraping (o el egress del propio
   entorno).** Cada fuente tiene `access_status` (`ok` / `search_snippet` /
   `blocked` / `js_required` / `paywalled`). El documento final anota junto a
   cada fuente bloqueada: *"acceso directo bloqueado; información vía
   búsqueda/indexación"*. Nunca se presenta un dato de una página no leída
   directamente como si se hubiera verificado con el mismo nivel de certeza
   que una lectura completa.

8. **Cómo se maneja información contradictoria.**
   `src/brand_debrief/contradictions.py` agrupa la evidencia por `topic` y
   señala (a) contradicciones marcadas explícitamente (campo `contradicts` en
   una `Evidence`) y (b) casos donde dos afirmaciones del mismo tema contienen
   cifras numéricas distintas, para revisión manual — no resuelve solo cuál
   cifra es "la correcta".

9. **Cómo se guardan los resultados.** Todo bajo `research/<brand>/`:
   `sources.json`, `evidence.json`, y `sections/<NN>_<slug>.md` (la redacción
   humana/estratégica de cada uno de los 21 apartados del debrief, con citas
   inline `[Exxxxxxx]`). Para Alpin, además hay
   `research/alpin/seed_evidence.py`, un script reproducible que documenta
   exactamente qué se registró y con qué fuente — se puede volver a correr o
   auditar en cualquier momento.

10. **Cómo se genera el documento final.**
    `src/brand_debrief/document_builder.py` recorre la estructura genérica de
    21 secciones (`config/debrief_structure.yaml`), concatena el contenido de
    `research/<brand>/sections/*.md`, y le añade automáticamente (siempre al
    final, siempre generadas desde el store, nunca escritas a mano) las notas
    de contradicción, la Matriz de Evidencia y la sección de Fuentes.

### Por qué es reutilizable para otra marca

Lo único específico de Alpin es `config/brands/alpin.yaml` y el contenido de
`research/alpin/`. Para otra marca/producto/país:

```bash
cp config/brands/alpin.yaml config/brands/mi_marca.yaml
# editar: brand, product, country, category, competitors, priority_sources
mkdir -p research/mi_marca/sections
# investigar con WebSearch/WebFetch y registrar con el CLI (ver sección 3 abajo)
# escribir research/mi_marca/sections/01_punto_de_partida.md ... 21_conclusion_estrategica.md
PYTHONPATH=src python3 -m brand_debrief audit --brand mi_marca
PYTHONPATH=src python3 -m brand_debrief build --brand mi_marca
```

La estructura de 21 secciones (`config/debrief_structure.yaml`) también se
puede sustituir por otra si el proyecto lo requiere, sin tocar código.

## 2. Estructura de archivos

```
config/
  debrief_structure.yaml       # las 21 secciones del debrief, genérico/reutilizable
  brands/
    alpin.yaml                 # configuración específica de Alpin Chocolate / Alpina / Colombia
src/brand_debrief/
  models.py                    # Source, Evidence (dataclasses)
  evidence_store.py            # persistencia JSON + dedup + validación
  citations.py                 # genera sección FUENTES y MATRIZ DE EVIDENCIA
  contradictions.py            # detecta contradicciones explícitas y numéricas
  audit.py                     # auditoría estructural previa a la entrega
  document_builder.py          # ensambla el .md final
  cli.py / __main__.py         # interfaz de línea de comandos
research/
  alpin/
    seed_evidence.py           # script reproducible que registró toda la evidencia de Alpin
    sources.json               # 48 fuentes registradas
    evidence.json              # 50 afirmaciones tipadas y citadas
    sections/                  # 21 archivos .md, la redacción del debrief
output/
  alpin_debrief.md             # EL ENTREGABLE FINAL
```

## 3. Instalación

Requiere Python 3.9+ y la librería `PyYAML` (usada solo para leer los `.yaml`
de configuración):

```bash
pip install pyyaml
```

No se requiere ninguna otra dependencia ni ninguna API key: la investigación
web la realiza Claude Code con sus propias herramientas (`WebSearch`/`WebFetch`),
no el código Python.

## 4. Ejecución

Desde la raíz del proyecto:

```bash
# Regenerar el debrief de Alpin a partir de la evidencia ya registrada:
PYTHONPATH=src python3 -m brand_debrief build --brand alpin

# Volver a poblar la evidencia desde cero (reproduce exactamente esta investigación):
PYTHONPATH=src python3 research/alpin/seed_evidence.py

# Auditar antes de entregar (chequeo estructural: fuentes válidas, tipos, secciones sin citar):
PYTHONPATH=src python3 -m brand_debrief audit --brand alpin

# Agregar nueva evidencia manualmente durante una futura investigación:
PYTHONPATH=src python3 -m brand_debrief add-source --brand alpin \
  --name "Nombre de la fuente" --url "https://..." --category competencia \
  --reliability Alta --access-status ok

PYTHONPATH=src python3 -m brand_debrief add-evidence --brand alpin \
  --claim "Afirmación puntual y verificable" --type HECHO --topic producto_alpin \
  --sources S1a2b3c4 --reliability Alta

# Listar todo lo registrado:
PYTHONPATH=src python3 -m brand_debrief list --brand alpin --what all
```

## 5. Formato de salida

Un único archivo Markdown (`output/<brand>_debrief.md`) con:
1–21. Las secciones del debrief (con citas inline `[Exxxxxxx]` que remiten a
la Matriz de Evidencia), incluyendo la Tabla de Competencia (Alpin/Milo/
Nesquik/Chocolisto) dentro de la sección 7 y el Mapa de Posicionamiento
Competitivo.
Luego, generadas automáticamente y no editables a mano: notas de
contradicción (si las hay), **MATRIZ DE EVIDENCIA** completa y **FUENTES**
agrupadas por categoría (Alpina / Competencia / Investigación de mercado /
Institucionales / Secundarias).

Markdown se eligió por ser el formato más simple de auditar línea por línea
(diff-able, sin dependencias de render) y fácilmente convertible a Word/PDF si
se necesita para presentación, sin acoplar el sistema a una herramienta de
oficina específica.

## 6. Qué encontró la investigación de Alpin (resumen para orientarse en el documento)

- **Chocolisto se reclasificó como competencia directa de facto** (no indirecta
  como asumía el brief original): aparece junto a Milo como marca líder de
  bebidas achocolatadas en Colombia, y su dueño real es Compañía Nacional de
  Chocolates/Grupo Nutresa, no Colombina.
- Se añadieron **Corona** y **Sol** (chocolate de mesa, Nutresa/Casa Luker)
  como competencia tangencial por ocasión de consumo.
- No se encontró evidencia de una promesa de marca propia ni de comunicación
  reciente específica de Alpin (a diferencia de Milo, Chocolisto, y de otras
  líneas de la propia Alpina como Alpinito o la avena).
- El "problema de comunicación" diagnosticado no es de producto ni de
  distribución, sino de ausencia de territorio y voz de marca propios.
- Todas las cifras de mercado (DANE, ANDI, Kantar, NielsenIQ) y de negocio
  (resultados financieros de Alpina) están citadas con su fuente exacta y su
  fecha de consulta en la Matriz de Evidencia; donde no se encontró un dato
  (participación de mercado de Alpin, Google Trends, cifras de redes
  sociales), el documento lo dice explícitamente en vez de inventarlo.

## 7. Limitaciones honestas (léase antes de usar el debrief para decisiones)

- La investigación se hizo 100% vía snippets de búsqueda, no lectura directa
  de páginas completas (limitación del entorno de ejecución, no del diseño
  del sistema). Si se corre este mismo pipeline desde un entorno sin ese
  bloqueo de red, se recomienda re-verificar las fuentes marcadas
  `access_status: search_snippet` con lectura directa.
- El target psicográfico, el perfil narrativo del consumidor y los insights
  (secciones 10–13 y 16) son **hipótesis razonadas**, no resultado de
  investigación cualitativa/cuantitativa con consumidores reales. Se
  recomienda validarlos antes de comprometer presupuesto de ejecución.
- No se tuvo acceso a los informes completos (de pago) de Kantar, NielsenIQ o
  Euromonitor sobre esta categoría específica; se usó únicamente lo publicado
  públicamente en sus sitios y en prensa que los cita.
