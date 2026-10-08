# Encuadres y planimetría — vocabulario y notación

## Tamaños de plano

| Abrev. | Nombre | Encuadra | Función habitual |
|---|---|---|---|
| GPG | Gran plano general | Paisaje, personaje diminuto o ausente | Ubicar, aislar, escala |
| PG | Plano general | Personaje entero con mucho entorno | Relación personaje–espacio |
| PE | Plano entero | Cuerpo completo, de pies a cabeza | Acción física, vestuario |
| PA | Plano americano | Hasta las rodillas | Grupos, tensión física |
| PM | Plano medio | Hasta la cintura | Conversación, gesto |
| PMC | Plano medio corto | Hasta el pecho | Diálogo con más cercanía |
| PP | Primer plano | Rostro y hombros | Emoción |
| PPP / GPP | Primerísimo / gran primer plano | Parte del rostro | Máxima intensidad |
| PD | Plano detalle | Objeto o parte del cuerpo | Información, símbolo |

Combinados: **plano de escorzo / over the shoulder (OTS)**, **plano subjetivo (POV)**, **two shot / plano de dos**, **plano máster**, **plano de reacción**, **plano recurso / inserto**.

## Ángulos y alturas
- **Normal / eye level** — neutralidad, igualdad.
- **Picado** (cámara arriba, mira abajo) — empequeñece, vulnerabilidad, vigilancia.
- **Contrapicado** (cámara abajo, mira arriba) — poder, amenaza, monumentalidad.
- **Cenital** — mirada externa, patrón, destino.
- **Nadir** — extrañeza, extremo del contrapicado.
- **Holandés / aberrante** — desequilibrio; úsalo con moderación.
- **Altura de cadera, de suelo, de hombro** — matizan sin el peso simbólico de un picado o contrapicado marcado.

## Movimientos
| Término | Qué hace la cámara |
|---|---|
| Fijo | No se mueve |
| Panorámica (pan) | Gira en horizontal sobre su eje |
| Tilt | Gira en vertical sobre su eje |
| Travelling / dolly | Se desplaza (lateral, in, out) |
| Push-in / pull-out | Se acerca / aleja lentamente del sujeto |
| Grúa / jib | Sube o baja desplazándose |
| Cámara en mano | Inestabilidad orgánica, presencia |
| Steadicam / gimbal | Desplazamiento fluido siguiendo la acción |
| Zoom | Cambia la focal, no la perspectiva |
| Rack focus | Cambia el foco entre términos |
| Barrido (whip pan) | Panorámica rápida que difumina |

## Reglas de continuidad
- **Eje de acción / 180°**: línea imaginaria entre los personajes (o en la dirección del movimiento). Todas las cámaras de la escena quedan en un mismo lado.
- **Regla de 30°**: entre dos planos consecutivos del mismo sujeto, cambia el ángulo al menos ~30° o el tamaño de forma clara, para evitar el salto (jump cut) no deseado.
- **Raccord de mirada**: si A mira a la derecha del cuadro, B debe mirar a la izquierda.
- **Raccord de dirección**: un personaje que sale por la derecha entra por la izquierda en el plano siguiente.

## Notación de planimetría

```
Leyenda

  ( M )>      Personaje M mirando en la dirección de ">"
  M1 ····> M2 Recorrido de M desde la posición 1 a la 2
  [C 1A]      Cámara del plano 1A
   \   /      Cono de visión (más abierto = focal más corta)
  [C]====>[C] Movimiento de cámara (dolly/travelling)
  - - - - -   Eje de acción (no se cruza)
  ☀ / ◉       Luz / práctica
  ▭           Mueble · ┃ pared · ⌒ puerta · ═ ventana
```

### Ejemplo ASCII (escena de cocina, dos personajes)

```
 ┃══════ ventana ══════════════════════════┃
 ┃                                         ┃
 ┃   ▭ fregadero        (M)>               ┃
 ┃                       ·                 ┃
 ┃- - - - - - - - - - - -·- - - - - - - - -┃  eje M–D
 ┃                       ·                 ┃
 ┃                     <(D)                ┃
 ┃                                         ⌒ puerta
 ┃      [C 1A]  50mm           [C 1B] 50mm ┃
 ┃        \ /                     \ /      ┃
 ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃
 Ambas cámaras del mismo lado del eje.
```

### Planimetría en SVG
Cuando generes un SVG:
- Vista cenital, fondo claro, líneas de pared gruesas, mobiliario en gris.
- Personajes como círculos con inicial y un pequeño triángulo indicando la mirada.
- Cámaras como rectángulo + triángulo (objetivo) con el número de plano al lado; cono de visión semitransparente.
- Recorridos de actores en línea continua de color; movimientos de cámara en línea discontinua con flecha.
- Eje de acción en línea punteada roja.
- Leyenda en una esquina y título "Esc. N – Planimetría" con la escala aproximada.
- Usa la misma numeración de planos que la shot list.

## Focal y cono de visión (referencia aproximada en full frame / super 35)
| Focal FF | Equiv. S35 aprox. | Ángulo horizontal FF aprox. | Sensación |
|---|---|---|---|
| 18–24 mm | 12–16 mm | 90–74° | Amplio, espacio, distorsión cerca |
| 35 mm | 24 mm | 54° | Natural con contexto |
| 50 mm | 35 mm | 40° | Neutro, cercano a la mirada |
| 85 mm | 55 mm | 24° | Retrato, separa del fondo |
| 135 mm + | 90 mm + | ≤ 15° | Compresión, observación a distancia |
