# Fuentes del Simulador PER

`index.html` (en la raíz) es la app completa y la fuente de verdad: lleva dentro todas las preguntas.
Esta carpeta guarda las piezas con las que se generó, por si hay que rehacer algo.

- `preguntas_oficiales.json`: banco de preguntas (`Q`) y exámenes reales en orden (`T`).
- `parse_dgmm.py`: extrae las preguntas de los PDF de la DGMM y aplica las plantillas oficiales.
- `parse_andalucia.py` y `respuestas_andalucia/`: preguntas de Andalucía y sus respuestas resueltas.
- `luces_y_marcas_bank.js`: las 119 preguntas con figura de luces y marcas.
- `boyas.js`: fichas y generador de tests de la pestaña Boyas.
