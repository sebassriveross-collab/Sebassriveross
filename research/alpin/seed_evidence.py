"""Script de siembra de evidencia para el debrief de Alpin Chocolate (Alpina).

Este script documenta, de forma reproducible y auditable, exactamente qué
se investigó y de dónde salió cada afirmación usada en el debrief. Se
ejecuta una sola vez (o cada vez que se amplía la investigación) y puebla
research/alpin/sources.json y research/alpin/evidence.json.

IMPORTANTE — limitación de acceso detectada durante la investigación:
en este entorno de ejecución, la herramienta de fetch directo de páginas
(WebFetch) devolvió EGRESS_BLOCKED para TODOS los dominios probados
(alpina.com, nestle.com.co, exito.com, larepublica.co, semana.com,
trends.google.com, kantar.com, andi.com.co, elcolombiano.com,
valoraanalitik.com, pulzo.com, en.wikipedia.org). La única herramienta de
navegación web que funcionó fue la búsqueda (WebSearch), que devuelve
fragmentos ("snippets") sintetizados a partir de las páginas indexadas,
con su URL de origen. Por lo tanto, TODA la evidencia de este debrief
proviene de snippets de búsqueda, no de lectura directa de la página
completa. Esto se registra explícitamente en cada fuente
(access_status="search_snippet") y se refleja en el nivel de
confiabilidad asignado (nunca "Alta" automática solo por tratarse de un
dominio oficial si el contenido no pudo verificarse línea por línea).

Ejecutar con:
    PYTHONPATH=src python3 research/alpin/seed_evidence.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from brand_debrief.evidence_store import EvidenceStore  # noqa: E402

store = EvidenceStore(ROOT / "research" / "alpin")

# ============================================================
# FUENTES
# ============================================================

S = {}  # mapa clave-legible -> Source

def src(key, **kwargs):
    S[key] = store.add_source(**kwargs)

# --- Alpina (oficial) ---
src("alpin_ficha", name="Alpina — Ficha de producto Alpin Chocolate Caja 200 ml",
    url="https://alpina.com/alpin-chocolate-caja-200-ml", category="alpina",
    access_status="search_snippet", reliability="Media",
    notes="Página oficial; contenido obtenido vía snippet de búsqueda (egress bloqueado para fetch directo).")

src("alpina_informes_gestion", name="Alpina — Informes de gestión (Corporativo/Inversionistas)",
    url="https://alpina.com/corporativo/inversionistas/informes/informes-de-gestion",
    category="alpina", access_status="search_snippet", reliability="Media",
    notes="URL oficial confirmada por buscador; el detalle financiero se corroboró vía prensa económica (ver fuentes secundarias).")

src("alpina_informes_sostenibilidad", name="Alpina — Informes de sostenibilidad",
    url="https://alpina.com/sostenibilidad/informes", category="alpina",
    access_status="search_snippet", reliability="Media")

# --- Competencia (oficial y prensa) ---
src("milo_nestle_brand", name="Nestlé Colombia — Página de marca Milo",
    url="https://www.nestle.com.co/brands/milo", category="competencia",
    access_status="search_snippet", reliability="Media",
    notes="Snippet de tagline: 'Energía y Nutrición para campeones'.")

src("milo_sitio", name="Milo Colombia — Sitio oficial (milo.com.co)",
    url="https://www.milo.com.co/", category="competencia",
    access_status="search_snippet", reliability="Media",
    notes="Tagline: 'Energía nutritiva para campeones'.")

src("milo_sostenibilidad", name="Milo Colombia — Sección Sostenibilidad (Escuela del Reciclaje)",
    url="https://www.milo.com.co/sostenibilidad", category="competencia",
    access_status="search_snippet", reliability="Media")

src("nesquik_nestle_brand", name="Nestlé Colombia — Página de marca Nesquik",
    url="https://www.nestle.com.co/brands/nesquik", category="competencia",
    access_status="search_snippet", reliability="Media")

src("milo_elcolombiano_80", name="El Colombiano — 'Milo te da energía, la meta la pones tú': 80 años en Colombia",
    url="https://www.elcolombiano.com/negocios/bebida-milo-cumple-80-anos-como-obtuvo-su-exito-CH25554215",
    category="competencia", access_status="search_snippet", reliability="Alta", published_date="2024-10")

src("milo_eltiempo_80", name="El Tiempo — 'Milo cumple 80 años dándole energía y sabor al mundo'",
    url="https://www.eltiempo.com/cultura/gastronomia/milo-cumple-80-anos-dandole-energia-y-sabor-al-mundo-historia-de-una-marca-3365855",
    category="competencia", access_status="search_snippet", reliability="Alta")

src("milo_pym_promesas", name="Revista P&M — 'Promesas Milo': convocatoria a niños deportistas",
    url="https://www.revistapym.com.co/articulos/comunicacion/38190/promesas-milo-la-convocatoria-a-ninos-deportistas-para-ser-la-imagen-de-la-marca",
    category="competencia", access_status="search_snippet", reliability="Alta")

src("milo_solar_nestle", name="Nestlé Colombia — Milo interviene espacios deportivos con energía solar (80 años)",
    url="https://www.nestle.com.co/media/news/milo-intervendra-espacios-deportivos",
    category="competencia", access_status="search_snippet", reliability="Media")

src("milo_calzado_portafolio", name="Portafolio — Milo lanzó línea de calzado en Colombia: balance de campaña",
    url="https://www.portafolio.co/negocios/empresas/milo-lanzo-linea-de-calzado-edicion-especial-balance-de-la-campana-640107",
    category="competencia", access_status="search_snippet", reliability="Alta")

src("milo_comite_olimpico", name="El Marketing Deportivo — Milo y el Comité Olímpico Colombiano buscan promesas del deporte",
    url="https://elmarketingdeportivo.com/milo-y-el-comite-olimpico-colombiano-buscan-las-promesas-del-deporte-en-colombia/",
    category="competencia", access_status="search_snippet", reliability="Media")

src("milo_tetrapak_empaque", name="El Empaque — Nestlé lanza nueva presentación de Milo en caja individual (Tetra Pak)",
    url="https://www.elempaque.com/temas/Lanzamiento-de-Nestle-en-Colombia,-nuevo-actor-en-mercado-de-bebidas-lacteas-saborizadas+107689",
    category="competencia", access_status="search_snippet", reliability="Alta")

src("milo_oxxo", name="OXXO Colombia — Milo Activ-Go Tetra Pak 180 ml (listado retail)",
    url="https://colombia.oxxodomicilios.com/product-details/milo-activgo-tetra-pak-180-ml/01GQJFVW9B6JK33P5Q7988QGPN",
    category="competencia", access_status="search_snippet", reliability="Media")

src("chocolisto_pulzo", name="Pulzo — Chocolatina Jet, Chocolisto y Jumbo cambian de dueño en Colombia (Nutresa/Gilinski)",
    url="https://www.pulzo.com/economia/chocolatinas-jet-chocolisto-jumbo-nutresa-ahora-grupo-gilinski-PP3442829",
    category="competencia", access_status="search_snippet", reliability="Alta")

src("chocolisto_semana_historia", name="Semana — 'Chocolisto... y listo' (historia de la marca)",
    url="https://www.semana.com/home/articulo/chocolisto-listo/164054/",
    category="competencia", access_status="search_snippet", reliability="Alta",
    notes="Chocolisto nació en 1961 como el primer chocolate en polvo del país, de Compañía Nacional de Chocolates.")

src("chocolisto_exito_tarro", name="Éxito — Bebida achocolatada Chocolisto en polvo, tarro 1000 g (listado retail)",
    url="https://www.exito.com/bebida-chocolatada-en-tarro-x-1000-gr-181271/p",
    category="competencia", access_status="search_snippet", reliability="Media")

src("chocolisto_makro_bolsa", name="Makro — Chocolisto bolsa 200 g (listado retail)",
    url="https://tienda.makro.com.co/p/chocolisto-bolsa-200g-158894",
    category="competencia", access_status="search_snippet", reliability="Media")

src("nesquik_jumbo_doypack", name="Jumbo Colombia — Nesquik chocolate Doy Pack 900 g (listado retail)",
    url="https://www.jumbocolombia.com/nesquik-chocolate-doy-pack-x-900g/p",
    category="competencia", access_status="search_snippet", reliability="Media")

src("chocolate_mesa_luker", name="Listado comercial — Casa Luker, chocolate de mesa (formato barra para chocolate caliente)",
    url="https://www.amazon.com/LUKER-Chocolate-Mesa-Azucar-Morena/dp/B07JHM4BLX",
    category="competencia", access_status="search_snippet", reliability="Baja",
    notes="Fuente comercial de bajo peso; se usa solo para confirmar el formato 'chocolate de mesa', no para datos de mercado.")

# --- Investigación de mercado ---
src("kantar_evoluciona_2025", name="Kantar — El consumidor colombiano evoluciona: más estratégico, omnicanal y consciente (2025)",
    url="https://www.kantar.com/latin-america/inspiracion/consumidor/2025/el-consumidor-colombiano-evoluciona",
    category="investigacion_mercado", access_status="search_snippet", reliability="Alta", published_date="2025")

src("kantar_tendencias_2025", name="Kantar Worldpanel — Aprendizajes y tendencias 2025 del consumo masivo colombiano",
    url="https://www.kantar.com/latin-america/inspiracion/consumidor/2024-worldpanel-colombia-aprendizajes-y-tendencias-2025-del-mercado-de-consumo-masivo",
    category="investigacion_mercado", access_status="search_snippet", reliability="Alta")

src("kantar_forbes_2025", name="Forbes Colombia — Consumo masivo Colombia 2025 según Kantar",
    url="https://forbes.co/2025/06/11/economia-y-finanzas/consumo-masivo-colombia-2025-segun-kantar",
    category="investigacion_mercado", access_status="search_snippet", reliability="Alta", published_date="2025-06-11")

src("nielseniq_semana_2025", name="Semana — Estudio de NielsenIQ revela claves del consumo masivo en Colombia 2025",
    url="https://www.semana.com/economia/empresas/articulo/estudio-de-nielsen-revela-las-claves-del-consumo-masivo-en-colombia-en-2025-entre-la-cautela-y-el-regreso-del-optimismo-para-las-empresas/202505/",
    category="investigacion_mercado", access_status="search_snippet", reliability="Alta")

src("nielseniq_valorydinero", name="Valor y Dinero — Las bebidas representan el 55% del consumo masivo en Colombia (NielsenIQ)",
    url="https://valorydinero.com/2024/10/09/las-bebidas-representan-el-55-del-sector-de-consumo-masivo-en-colombia-liderando-el-crecimiento-en-2024/",
    category="investigacion_mercado", access_status="search_snippet", reliability="Alta", published_date="2024-10-09")

src("euromonitor_milk_co", name="Euromonitor — Drinking Milk Products in Colombia (ficha de informe de mercado)",
    url="https://www.euromonitor.com/drinking-milk-products-in-colombia/report",
    category="investigacion_mercado", access_status="search_snippet", reliability="Alta")

# --- Institucionales ---
src("dane_ipc_ago2025", name="DANE — Comunicado de prensa IPC agosto 2025",
    url="https://www.dane.gov.co/files/operaciones/IPC/ago2025/cp-IPC-ago2025.pdf",
    category="institucional", access_status="search_snippet", reliability="Alta", published_date="2025-09-05")

src("andi_camara_alimentos", name="ANDI — Cámara de la Industria de Alimentos",
    url="https://www.andi.com.co/home/camara/16-industria-de-alimentos",
    category="institucional", access_status="search_snippet", reliability="Alta")

src("andi_valoraanalitik_produccion", name="Valora Analitik — Producción de alimentos en Colombia crece 7,5% en 2025",
    url="https://www.valoraanalitik.com/produccion-alimentos-colombia-crece-2025/",
    category="institucional", access_status="search_snippet", reliability="Alta")

src("andi_infobae_produccion", name="Infobae — Producción de alimentos en Colombia crece 7,5% en 2025 pese al 'tsunami regulatorio'",
    url="https://www.infobae.com/colombia/2025/10/04/produccion-de-alimentos-en-colombia-crece-75-en-2025-pese-al-tsunami-regulatorio-que-enfrenta-la-industria/",
    category="institucional", access_status="search_snippet", reliability="Alta", published_date="2025-10-04")

# --- Secundarias (prensa sobre Alpina / mercado / campañas / redes) ---
src("alpina_semana_ventas2025", name="Semana — Alpina aumenta ventas en 2025 gracias a la recuperación del consumo",
    url="https://www.semana.com/economia/empresas/articulo/alpina-aumenta-ventas-en-2025-gracias-a-la-recuperacion-del-consumo-en-colombia/202545/",
    category="secundaria", access_status="search_snippet", reliability="Alta")

src("alpina_portafolio_q1_2025", name="Portafolio — Resultados financieros de Alpina, primer trimestre 2025",
    url="https://www.portafolio.co/negocios/empresas/resultados-financieros-de-alpina-durante-el-primer-trimestre-del-2025-630251",
    category="secundaria", access_status="search_snippet", reliability="Alta")

src("alpina_elespectador_h1_2025", name="El Espectador — Alpina crece 6,7% en ventas en el primer semestre de 2025",
    url="https://www.elespectador.com/especiales/alpina-crece-67-en-ventas-en-el-primer-semestre-de-2025/",
    category="secundaria", access_status="search_snippet", reliability="Alta")

src("alpina_valoraanalitik_h1_2025", name="Valora Analitik — Alpina aumentó 6,7% sus ingresos en primer semestre de 2025",
    url="https://www.valoraanalitik.com/alpina-aumento-67-sus-ingresos-en-primer-semestre-de-2025-estas-son-sus-proyecciones-para-final-de-ano/",
    category="secundaria", access_status="search_snippet", reliability="Alta")

src("alpina_larepublica_h1_2025", name="La República — Ventas de Alpina Colombia alcanzaron $1,1 billones en el primer semestre",
    url="https://www.larepublica.co/empresas/ventas-de-alpina-colombia-alcanzaron-1-1-billones-en-el-primer-semestre-del-ano-4193955",
    category="secundaria", access_status="search_snippet", reliability="Alta")

src("achocolatadas_semana_competencia", name="Semana — La competencia de las bebidas achocolatadas para conquistar el desayuno de los colombianos",
    url="https://www.semana.com/la-competencia-bebidas-achocolatadas-para-conquistar-desayuno-colombianos/215915/",
    category="secundaria", access_status="search_snippet", reliability="Alta",
    notes="Fuente clave para la clasificación de competidores y hábitos de consumo de bebidas achocolatadas en Colombia.")

src("alpina_ai_campana", name="ContextoGanadero — El salto de Alpina a la inteligencia artificial encendió las redes sociales",
    url="https://www.contextoganadero.com/tendencias/el-salto-de-alpina-a-la-inteligencia-artificial-encendio-redes-sociales-que-paso",
    category="secundaria", access_status="search_snippet", reliability="Media")

src("alpina_tia_clara", name="COPU — Alpina y Buentipo se unen para incentivar el consumo de lácteos ('La Tía Clara')",
    url="https://copu.media/alpina-y-buentipo-se-unen-para-incentivar-el-consumo-de-lacteos-en-colombia-en-su-nueva-campana/",
    category="secundaria", access_status="search_snippet", reliability="Media")

src("alpina_latinspots_avena", name="LatinSpots — 'Alto de la avena' (El Ojo 2024) - Alpina Colombia",
    url="https://www.latinspots.com/pieza/comercial/alto-de-la-avena-el-ojo-2024/46447",
    category="secundaria", access_status="search_snippet", reliability="Media", published_date="2024-11-16")

src("alpina_larepublica_ninos", name="La República — Alpina y Ramo son las marcas más reconocidas por los niños",
    url="https://www.larepublica.co/consumo/alpina-y-ramo-son-las-marcas-mas-reconocidas-por-los-ninos-2027136",
    category="secundaria", access_status="search_snippet", reliability="Alta")

src("alpina_produ_sostenibilidad", name="PRODU — Andrea Restrepo (Alpina): objetivo 2024 es una nutrición más sostenible",
    url="https://www.produ.com/mercadeo/noticias/andrea-restrepo-de-alpina-nuestro-objetivo-ms-importante-para-2024-es-seguir-llevando-una-nutricin-ms-sostenible/",
    category="secundaria", access_status="search_snippet", reliability="Media")

src("alpina_semana_alpilitro", name="Semana — 'Alpilitro': el impacto de influencers y redes sociales en hábitos alimenticios",
    url="https://www.semana.com/cocina/historias/articulo/alpilitro-el-impacto-que-tienen-los-influencers-y-las-redes-sociales-en-los-habitos-alimenticios/202320/",
    category="secundaria", access_status="search_snippet", reliability="Media",
    notes="Sobre Alpinito (producto hermano de Alpin, no el mismo producto): #Alpilitro/#Alpinito se volvieron tendencia y motivaron el lanzamiento de una presentación de 1 litro de Alpinito.")

src("alpina_comunicaciones_blog", name="Blog académico 'Alpina Comunicaciones' — Marca y Target",
    url="http://alpinacomunicaciones.blogspot.com/2018/04/marca-y-target.html",
    category="secundaria", access_status="search_snippet", reliability="Baja",
    notes="Blog no oficial de bajo respaldo editorial; solo se usa para plantear una HIPÓTESIS a validar, nunca como hecho.")

# Retail — presentaciones/precios de Alpin
src("alpin_exito_caja200", name="Éxito — Alpin Chocolate Caja 200 ml (listado retail)",
    url="https://www.exito.com/leche-saborizada-alpin-chocolate-en-caja-x-200-ml-290704/p",
    category="secundaria", access_status="search_snippet", reliability="Media")

src("alpin_exito_sixpack", name="Éxito — Alpin sabor a chocolate sixpack caja 200 ml (1200 ml)",
    url="https://www.exito.com/bebida-alpin-sabor-a-chocolate-sixpack-en-caja-x-200-ml-cu-952292/p",
    category="secundaria", access_status="search_snippet", reliability="Media",
    notes="Precio observado en snippet de búsqueda: $23.100 COP (sixpack 200 ml x6, snapshot puntual, puede variar por región/fecha).")

src("alpin_exito_botella300", name="Éxito — Alpin chocolate botella 300 ml (listado retail)",
    url="https://www.exito.com/leche-botella-entera-chocolate-alpina-300-ml-3022657/p",
    category="secundaria", access_status="search_snippet", reliability="Media")

src("alpin_jumbo_bolsa180", name="Jumbo Colombia — Leche Alpín chocolate bolsa x6 x180 ml",
    url="https://www.jumbocolombia.com/leche-alpina-alpin-chocolate-bolsa-x6undx180mlc-u/p",
    category="secundaria", access_status="search_snippet", reliability="Media")

store.save()
print(f"Fuentes registradas: {len(store.sources)}")

# ============================================================
# EVIDENCIA
# ============================================================

def ev(**kwargs):
    return store.add_evidence(**kwargs)

# --- Descripción de marca / propósito ---
ev(claim="El propósito declarado de Alpina es nutrir de forma más sostenible y 'darle sabor a la vida', con compromisos de carbono neutralidad y neutralidad plástica.",
   evidence_type="HECHO", topic="marca_alpina",
   source_ids=[S["alpina_produ_sostenibilidad"].id, S["alpina_informes_sostenibilidad"].id],
   reliability="Media", notes="Contenido vía snippet, no verificado línea por línea en el informe completo.")

ev(claim="Alpina ocupó el 2° lugar en el ranking Merco ESG en 2024, señal de reconocimiento externo a su gestión ambiental, social y de gobierno corporativo.",
   evidence_type="HECHO", topic="marca_alpina",
   source_ids=[S["alpina_produ_sostenibilidad"].id], reliability="Media")

ev(claim="Alpina y Ramo son percibidas como las marcas más reconocidas por los niños en Colombia, según cobertura de prensa económica.",
   evidence_type="HECHO", topic="marca_alpina",
   source_ids=[S["alpina_larepublica_ninos"].id], reliability="Alta")

ev(claim="Dentro del portafolio de Alpina, Alpinito (yogur/bebida láctea para niños) y Alpin (bebida láctea achocolatada lista para tomar, apta para lonchera) son productos DISTINTOS, ambos con foco en el consumo infantil/juvenil.",
   evidence_type="HECHO", topic="portafolio_alpina",
   source_ids=[S["alpina_semana_alpilitro"].id], reliability="Media")

ev(claim="El fenómeno viral #Alpilitro/#Alpinito (tendencia en redes) impulsó a Alpina a lanzar una presentación de 1 litro de Alpinito, no de Alpin.",
   evidence_type="HECHO", topic="portafolio_alpina",
   source_ids=[S["alpina_semana_alpilitro"].id], reliability="Media")

ev(claim="Alpina implementó en 2025 una campaña con inteligencia artificial generativa, siendo señalada como una de las pioneras en Colombia en usar esta tecnología en publicidad.",
   evidence_type="HECHO", topic="comunicacion_alpina",
   source_ids=[S["alpina_ai_campana"].id], reliability="Media")

ev(claim="Alpina lanzó en 2024 la campaña 'La Tía Clara' junto con el estudio Buentipo para incentivar el consumo de lácteos en Colombia.",
   evidence_type="HECHO", topic="comunicacion_alpina",
   source_ids=[S["alpina_tia_clara"].id], reliability="Media")

ev(claim="La campaña 'Alto de la avena' de Alpina (DDB Colombia, dirigida por Gina Medina) fue publicada en noviembre de 2024 y participó en el festival El Ojo 2024.",
   evidence_type="HECHO", topic="comunicacion_alpina",
   source_ids=[S["alpina_latinspots_avena"].id], reliability="Media")

ev(claim="No se encontró evidencia suficiente para verificar que exista una campaña de comunicación reciente, sostenida y específicamente centrada en Alpin Chocolate (a diferencia de Alpinito, avena Alpina u otras líneas); la comunicación identificada corresponde a otras marcas del portafolio Alpina.",
   evidence_type="HECHO", topic="comunicacion_alpina",
   source_ids=[S["alpina_ai_campana"].id, S["alpina_tia_clara"].id, S["alpina_latinspots_avena"].id, S["alpina_semana_alpilitro"].id],
   reliability="Media", notes="Ausencia de evidencia, no evidencia de ausencia total: puede existir comunicación de Alpin no indexada o no encontrada con las búsquedas realizadas.")

# --- Producto Alpin ---
ev(claim="Alpin Chocolate está disponible en Colombia en al menos estas presentaciones: caja individual de 200 ml, sixpack de 200 ml (1200 ml), botella de 300 ml y bolsa x6 de 180 ml.",
   evidence_type="HECHO", topic="producto_alpin",
   source_ids=[S["alpin_exito_caja200"].id, S["alpin_exito_sixpack"].id, S["alpin_exito_botella300"].id, S["alpin_jumbo_bolsa180"].id],
   reliability="Alta")

ev(claim="Según el snippet de la ficha oficial de producto, Alpin es presentado como fuente de vitaminas A, B1, B2 y B3, fuente de proteína y calcio, y como un producto que no requiere refrigeración.",
   evidence_type="HECHO", topic="producto_alpin",
   source_ids=[S["alpin_ficha"].id], reliability="Media",
   notes="Contenido no verificado por lectura directa de la página completa (egress bloqueado); se toma del snippet indexado.")

ev(claim="El envase de Alpin (larga vida / no requiere refrigeración) es consistente con un producto UHT, lo que explica su distribución en punto de venta ambiente (no en cadena de frío) y su posicionamiento de practicidad/portabilidad (lonchera, 'para llevar').",
   evidence_type="INTERPRETACION", topic="producto_alpin",
   source_ids=[S["alpin_ficha"].id, S["alpin_exito_botella300"].id], reliability="Media")

ev(claim="Un precio observado (snapshot puntual, no serie histórica) para el sixpack de Alpin Chocolate de 200 ml (1200 ml totales) en Éxito fue de $23.100 COP.",
   evidence_type="HECHO", topic="producto_alpin",
   source_ids=[S["alpin_exito_sixpack"].id], reliability="Media",
   notes="Precio de un solo punto de venta en un momento dado; puede variar por región, canal y fecha. No se debe tratar como precio de lista nacional.")

ev(claim="No se encontró evidencia suficiente para verificar cifras de participación de mercado (market share) de Alpin Chocolate dentro de la categoría de bebidas achocolatadas en Colombia.",
   evidence_type="HECHO", topic="producto_alpin", source_ids=[S["euromonitor_milk_co"].id],
   reliability="Alta", notes="Los informes que sí contienen esa cifra (Euromonitor) están detrás de un muro de pago; solo se accedió a la ficha pública del informe.")

ev(claim="No se encontró evidencia suficiente para verificar el número de consumidores, edades exactas o cifras de ventas específicas de Alpin Chocolate.",
   evidence_type="HECHO", topic="producto_alpin", source_ids=[S["alpin_ficha"].id], reliability="Alta")

# --- Financiero Alpina (contexto corporativo, no específico de Alpin) ---
ev(claim="Alpina reportó ventas netas de aproximadamente $1,1 billones de pesos colombianos en el primer semestre de 2025, un crecimiento del 6,7% frente al mismo periodo de 2024, según coinciden Semana, El Espectador, Valora Analitik y La República.",
   evidence_type="HECHO", topic="financiero_alpina",
   source_ids=[S["alpina_semana_ventas2025"].id, S["alpina_elespectador_h1_2025"].id, S["alpina_valoraanalitik_h1_2025"].id, S["alpina_larepublica_h1_2025"].id],
   reliability="Alta", notes="Corroborado por cuatro medios económicos independientes con la misma cifra.")

ev(claim="Alpina reportó un EBITDA acumulado de aproximadamente $171.000 millones de pesos en el primer semestre de 2025, y proyectaba cerrar el año con ventas netas cercanas a $2,3 billones, EBITDA de $364.000 millones y utilidad neta cercana a $114.000 millones.",
   evidence_type="HECHO", topic="financiero_alpina",
   source_ids=[S["alpina_valoraanalitik_h1_2025"].id], reliability="Media",
   notes="Cifra de un solo medio (vía snippet); tratar como dato a corroborar si se usa para decisiones de alto impacto.")

ev(claim="Esta cifra de crecimiento corresponde a Alpina como compañía completa (todo su portafolio de lácteos, jugos, avenas, etc.), no específicamente a la línea Alpin Chocolate.",
   evidence_type="INTERPRETACION", topic="financiero_alpina",
   source_ids=[S["alpina_semana_ventas2025"].id], reliability="Alta")

# --- Mercado colombiano ---
ev(claim="Según cobertura de prensa que cita datos de mercado, el 87% de los hogares colombianos consume bebidas achocolatadas y el 71% repone su compra cada 15 días.",
   evidence_type="HECHO", topic="mercado_general",
   source_ids=[S["achocolatadas_semana_competencia"].id], reliability="Alta")

ev(claim="Las marcas líderes de bebidas achocolatadas identificadas en el mercado colombiano son Corona (Nutresa), Milo (Nestlé), Chocolisto (Nutresa), Nesquik (Nestlé) y Sol (Casa Luker).",
   evidence_type="HECHO", topic="mercado_general",
   source_ids=[S["achocolatadas_semana_competencia"].id], reliability="Alta",
   notes="Esta lista NO incluye a Alpin explícitamente entre las marcas líderes mencionadas por esta fuente, lo cual es en sí mismo un dato relevante para el diagnóstico de la marca.")

ev(claim="Alpin no aparece mencionado como marca líder en la nota de prensa especializada sobre la competencia de bebidas achocolatadas en Colombia, a diferencia de Milo, Chocolisto, Nesquik, Corona y Sol.",
   evidence_type="INTERPRETACION", topic="situacion_actual_alpin",
   source_ids=[S["achocolatadas_semana_competencia"].id], reliability="Media",
   notes="Una nota de prensa no es un estudio de participación de mercado; la ausencia de mención es indicio, no prueba de bajo posicionamiento.")

ev(claim="Dentro de la categoría de chocolate para consumo en el hogar, el consumo de chocolate de mesa (barra) cayó 2,6% mientras que los modificadores de leche en polvo (como Chocolisto) crecieron 1,9%.",
   evidence_type="HECHO", topic="mercado_general",
   source_ids=[S["achocolatadas_semana_competencia"].id], reliability="Alta")

ev(claim="El sector de alimentos en Colombia creció 7,51% a precios corrientes en el primer semestre de 2025, aportando un 21,5% al PIB manufacturero, y los lácteos crecieron 9,7% interanual a julio de 2025 según cifras DANE citadas por ANDI/prensa.",
   evidence_type="HECHO", topic="mercado_general",
   source_ids=[S["andi_valoraanalitik_produccion"].id, S["andi_infobae_produccion"].id], reliability="Alta")

ev(claim="El sector de alimentos colombiano está compuesto por cerca de 48.000 empresas (98% micro y pequeñas), con 86 grupos empresariales afiliados a la Cámara de la Industria de Alimentos de la ANDI que concentran el liderazgo de las principales categorías.",
   evidence_type="HECHO", topic="mercado_general",
   source_ids=[S["andi_valoraanalitik_produccion"].id, S["andi_camara_alimentos"].id], reliability="Alta")

ev(claim="Según Kantar, en 2024 el valor de la canasta de consumo masivo en Colombia creció 16,1% y el volumen 10,3%; la penetración del e-commerce en consumo masivo pasó de 1,2% en 2015 a 43% en 2024; los hogares compran en promedio 74 categorías al año (+15% desde 2015) pero hacen 7% menos actos de compra que en 2015.",
   evidence_type="HECHO", topic="mercado_kantar",
   source_ids=[S["kantar_tendencias_2025"].id, S["kantar_forbes_2025"].id], reliability="Alta")

ev(claim="Según Kantar, el consumidor colombiano de 2025 es descrito como más estratégico, omnicanal y consciente, con un consumo más racional y planificado.",
   evidence_type="HECHO", topic="mercado_kantar",
   source_ids=[S["kantar_evoluciona_2025"].id], reliability="Alta")

ev(claim="Según NielsenIQ, las bebidas representaron el 55% del sector de consumo masivo en Colombia en 2024 y aportaron el 69% del crecimiento del sector; las bebidas listas para tomar (RTD) fueron de las categorías de mayor crecimiento.",
   evidence_type="HECHO", topic="mercado_nielsen",
   source_ids=[S["nielseniq_valorydinero"].id], reliability="Alta")

ev(claim="Según NielsenIQ, más de la mitad de los consumidores colombianos estaría dispuesta a pagar más por productos más saludables o de mayor calidad, y la frescura es un atributo clave en las decisiones sobre lácteos.",
   evidence_type="HECHO", topic="mercado_nielsen",
   source_ids=[S["nielseniq_semana_2025"].id], reliability="Alta")

ev(claim="El segmento de bebidas achocolatadas listas para tomar (RTD, como Alpin y Milo Tetra Pak) se beneficia de la misma tendencia de crecimiento de bebidas RTD identificada por NielsenIQ para el consumo masivo colombiano en general.",
   evidence_type="INTERPRETACION", topic="mercado_nielsen",
   source_ids=[S["nielseniq_valorydinero"].id, S["achocolatadas_semana_competencia"].id], reliability="Media")

ev(claim="No se encontró evidencia suficiente (fuente pública, no bloqueada por muro de pago) para verificar el tamaño exacto en pesos o litros de la categoría de bebidas lácteas achocolatadas en Colombia.",
   evidence_type="HECHO", topic="mercado_general", source_ids=[S["euromonitor_milk_co"].id], reliability="Alta")

# --- Competencia: Milo ---
ev(claim="Milo llegó a Colombia en 1944 y en 2024 cumplió 80 años en el país, siendo posicionado históricamente como bebida de desayuno y lonchera infantil.",
   evidence_type="HECHO", topic="competencia_milo",
   source_ids=[S["milo_eltiempo_80"].id, S["milo_elcolombiano_80"].id], reliability="Alta")

ev(claim="El tagline identificado de Milo es 'Energía y Nutrición para campeones' / 'Energía nutritiva para campeones', y su comunicación se apoya fuertemente en el territorio de deporte y energía física.",
   evidence_type="HECHO", topic="competencia_milo",
   source_ids=[S["milo_nestle_brand"].id, S["milo_sitio"].id], reliability="Media")

ev(claim="Milo ejecuta la plataforma 'Promesas Milo' junto al Comité Olímpico Colombiano, dirigida a niños y adolescentes de 8 a 16 años con talento deportivo (fútbol, baloncesto, ciclismo, patinaje, atletismo), otorgando becas deportivas de 20 millones de pesos.",
   evidence_type="HECHO", topic="competencia_milo",
   source_ids=[S["milo_pym_promesas"].id, S["milo_comite_olimpico"].id], reliability="Alta")

ev(claim="Por su 80° aniversario, Milo intervino espacios deportivos públicos en Bogotá, Medellín y Cali con energía solar, y desarrolló una campaña de entrega de más de 100.000 pares de zapatillas deportivas.",
   evidence_type="HECHO", topic="competencia_milo",
   source_ids=[S["milo_solar_nestle"].id, S["milo_calzado_portafolio"].id], reliability="Alta")

ev(claim="Milo mantiene la plataforma de sostenibilidad 'Escuela del Reciclaje' desde 2022, incluyendo una cancha de voleibol hecha con Tetra Pak reciclado en Bogotá.",
   evidence_type="HECHO", topic="competencia_milo",
   source_ids=[S["milo_sostenibilidad"].id], reliability="Media")

ev(claim="Milo está disponible en Colombia en formato listo para tomar en Tetra Pak individual (ej. 180 ml, línea Activ-Go) y en presentaciones para lonchera (NUTRI-FIT).",
   evidence_type="HECHO", topic="competencia_milo",
   source_ids=[S["milo_tetrapak_empaque"].id, S["milo_oxxo"].id], reliability="Alta")

ev(claim="El territorio de marca de Milo combina de forma consistente: energía física, deporte/rendimiento, nutrición funcional y, más recientemente, sostenibilidad ambiental.",
   evidence_type="INTERPRETACION", topic="competencia_milo",
   source_ids=[S["milo_nestle_brand"].id, S["milo_pym_promesas"].id, S["milo_sostenibilidad"].id], reliability="Media")

# --- Competencia: Nesquik ---
ev(claim="Nesquik está disponible en Colombia tanto en polvo (presentaciones de 200 g, 400 g y 900 g, sabores chocolate/fresa/vainilla, incluida versión baja en azúcar) como en formato listo para tomar.",
   evidence_type="HECHO", topic="competencia_nesquik",
   source_ids=[S["nesquik_nestle_brand"].id, S["nesquik_jumbo_doypack"].id], reliability="Media")

ev(claim="No se encontró evidencia suficiente, con las búsquedas realizadas, sobre una campaña de comunicación local (Colombia) reciente y de alto perfil específica de Nesquik, en contraste con la actividad de comunicación encontrada para Milo y Alpina.",
   evidence_type="HECHO", topic="competencia_nesquik", source_ids=[S["nesquik_nestle_brand"].id], reliability="Media")

ev(claim="La menor presencia de comunicación reciente encontrada para Nesquik frente a Milo, sumado a no figurar entre las marcas líderes citadas por la prensa especializada junto a Corona/Milo/Chocolisto/Sol, sugiere que Nesquik ocupa un rol secundario en el mercado colombiano de bebidas achocolatadas frente a Milo y Chocolisto.",
   evidence_type="INTERPRETACION", topic="competencia_nesquik",
   source_ids=[S["achocolatadas_semana_competencia"].id, S["nesquik_nestle_brand"].id], reliability="Media")

# --- Competencia: Chocolisto ---
ev(claim="Chocolisto es una marca de Compañía Nacional de Chocolates, hoy parte de Grupo Nutresa; tras la adquisición de Nutresa por parte del Grupo Gilinski, su propiedad última pasó a este grupo.",
   evidence_type="HECHO", topic="competencia_chocolisto",
   source_ids=[S["chocolisto_pulzo"].id, S["chocolisto_semana_historia"].id], reliability="Alta")

ev(claim="CORRECCIÓN A LA CLASIFICACIÓN INICIAL: Chocolisto NO es una marca de Colombina, sino de Compañía Nacional de Chocolates / Grupo Nutresa. El brief original asumía una clasificación de competencia indirecta sin especificar dueño; la investigación encontró que además Chocolisto es citada junto con Milo como marca líder de la categoría, por lo que se reclasifica como competencia directa de facto.",
   evidence_type="INTERPRETACION", topic="competencia_chocolisto",
   source_ids=[S["chocolisto_pulzo"].id, S["achocolatadas_semana_competencia"].id], reliability="Alta")

ev(claim="Chocolisto nació en 1961 como el primer chocolate en polvo del país (Compañía Nacional de Chocolates).",
   evidence_type="HECHO", topic="competencia_chocolisto",
   source_ids=[S["chocolisto_semana_historia"].id], reliability="Alta")

ev(claim="Chocolisto está disponible en Colombia en presentaciones de polvo de 200 g (bolsa/doypack) y 1.000 g (tarro), fortificado con hierro, vitamina A, vitaminas B1/B2/B3, calcio y vitamina D3; se prepara mezclando con leche o agua, fría o caliente.",
   evidence_type="HECHO", topic="competencia_chocolisto",
   source_ids=[S["chocolisto_exito_tarro"].id, S["chocolisto_makro_bolsa"].id], reliability="Alta")

ev(claim="El territorio de marca de Chocolisto se apoya en tradición/nostalgia ('el primero del país' desde 1961) y en fortificación nutricional básica (vitaminas y minerales), más que en un territorio emocional de deporte o aventura como Milo.",
   evidence_type="INTERPRETACION", topic="competencia_chocolisto",
   source_ids=[S["chocolisto_semana_historia"].id, S["chocolisto_exito_tarro"].id], reliability="Media")

# --- Competencia: Corona / Sol (chocolate de mesa) ---
ev(claim="Corona (Nutresa) y Sol (Casa Luker) son chocolates de mesa (barra para preparar chocolate caliente), un formato y una ocasión de consumo distintos a la bebida achocolatada lista para tomar en frío como Alpin.",
   evidence_type="HECHO", topic="competencia_corona_sol",
   source_ids=[S["achocolatadas_semana_competencia"].id, S["chocolate_mesa_luker"].id], reliability="Media")

ev(claim="Corona y Sol compiten por la misma ocasión general de 'chocolate para el desayuno de los colombianos', pero no por el mismo momento de consumo específico (caliente/preparado en casa vs. frío/portátil) que Alpin, por lo que se consideran competencia tangencial, no directa.",
   evidence_type="INTERPRETACION", topic="competencia_corona_sol",
   source_ids=[S["achocolatadas_semana_competencia"].id], reliability="Media")

# --- Target / redes sociales ---
ev(claim="Una fuente de bajo respaldo editorial (blog académico no oficial) plantea que Alpina, en el imaginario de consumidores infantiles, puede funcionar casi como nombre genérico de categoría láctea, y que su línea Alpina Baby usa códigos visuales infantiles (colores pasteles, conejito) dirigidos también a los padres compradores.",
   evidence_type="HIPOTESIS", topic="target_alpina",
   source_ids=[S["alpina_comunicaciones_blog"].id], reliability="Por validar",
   notes="Fuente de baja confiabilidad (blog estudiantil); se presenta explícitamente como hipótesis a validar con investigación de consumidor, nunca como hecho.")

ev(claim="No se encontró evidencia verificable (de fuente confiable) sobre cifras exactas de seguidores, engagement o alcance de las cuentas oficiales de Alpina/Alpin, Milo Colombia, Nesquik o Chocolisto en redes sociales.",
   evidence_type="HECHO", topic="redes_sociales", source_ids=[S["alpina_ai_campana"].id], reliability="Alta")

ev(claim="El caso #Alpilitro muestra que Alpina (a través de Alpinito) ha demostrado capacidad de generar conversación viral orgánica en redes sociales impulsada por consumidores/influenciadores, no solo por pauta planeada.",
   evidence_type="HECHO", topic="redes_sociales",
   source_ids=[S["alpina_semana_alpilitro"].id], reliability="Media")

store.save()
print(f"Evidencia registrada: {len(store.evidence)}")
