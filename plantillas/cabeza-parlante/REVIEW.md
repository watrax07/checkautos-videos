# Revisión — CHECK AUTOS · "Mitos vs Realidad: caja CVT" (video 6, cabeza parlante)

`npx hyperframes check`: 0 errores. Render `renders/checkautos-mitos-cvt.mp4` (1080x1920, 30 fps, 46 s);
entrega `vid6/CheckAutos_MitosCajaCVT_TikTok.mp4` con audio -2 dB: -15.1 LUFS, pico -3.3 dBFS (medido, no escuchado).

## Edición
- `_work/edit_talk.py`: los mismos cortes para video y audio, alineados a fotograma (1275 fotogramas = 42.5 s de audio exactos).
  46.5 s -> 42.5 s: se quitó el "¿sí?" de muletilla (34.3 s) y se acortaron 17 silencios/respiraciones a 0.10–0.22 s.
- Saltos de imagen disimulados con zoom alterno (1.0 / 1.13, centrado en la cara) en cada corte y con cortes a imágenes de apoyo.
- Audio original muy saturado (-9 LUFS, 2.7 % de muestras recortadas): picos reconstruidos (`declip.py`, aplanados 48 812 -> 18 377),
  paso alto, reducción de ruido suave (ruido del auto), sin realce de agudos, compresión 2:1, -16 LUFS. Música 0.05: voz 22.6 dB sobre el fondo.

## Visual
- Cara siempre visible arriba; tarjetas MITO (rojo, ✗) / REALIDAD (verde, ✔) a la altura del pecho; subtítulos debajo.
- Imágenes de apoyo reales de Check Autos (videos 3, 4 y 5): caja de cambios, motor, tablero, Colorado, Sentra.
- Gráficos generados: manual del fabricante (página que pasa), cuentakilómetros 80 000 -> 100 000 km, tanque que se drena y rellena,
  máquina de cambio de fluido, chips ¿Cuándo? / Fluido / Filtro / ¿Dónde lo haces?.

## A confirmar
- "la caja CVT": el reconocedor escuchó "se vete"; en el audio limpio se oye "CVT", que encaja con el tema. Confirmar.
- Las imágenes de apoyo son de otros autos inspeccionados (no del tema puntual del video).
