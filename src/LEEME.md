# Fuentes del Simulador PER

`index.html` (en la raíz) es la app completa y la fuente de verdad: lleva dentro todas las preguntas.
Esta carpeta guarda las piezas con las que se generó, por si hay que rehacer algo.

- `preguntas_oficiales.json`: banco de preguntas (`Q`) y exámenes reales en orden (`T`).
- `parse_dgmm.py`: extrae las preguntas de los PDF de la DGMM y aplica las plantillas oficiales.
- `parse_andalucia.py` y `respuestas_andalucia/`: preguntas de Andalucía y sus respuestas resueltas.
- `luces_y_marcas_bank.js`: las 119 preguntas con figura de luces y marcas.
- `boyas.js`: fichas y generador de tests de la pestaña Boyas.
- `build_banco.py`: reconstruye el banco DGMM conservando los ids anteriores (para no perder el progreso).
- `and_convocatorias.py`: asigna a cada pregunta de Andalucía su convocatoria (campo `s`).

Cambios del 17/11/2026 en `parse_dgmm.py`: ya no se pierde la pregunta 1 (un número de página «1» la anulaba),
se detecta «(Con PNB Liberado)» en la línea siguiente al código de test, se separan opciones en una misma línea,
se salta una pregunta que falta en el texto y el «Código de Test 0» de febrero de 2021 es el Test 05 (comprobado por contenido).
- `mareas_ihm.json` y `mareas_preguntas.json`: datos de marea de cada pregunta (campo `m`), sacados de la API oficial del IHM
  (`https://ideihm.covam.es/api-ihm/getmarea?request=gettide&id=ID&date=AAAAMMDD`, horas UTC, alturas sobre la sonda de la carta).
  Comprobado: 26 de 27 respuestas oficiales coinciden; la de Santander (julio 2021, Test 02/04) no cuadra con la plantilla.
