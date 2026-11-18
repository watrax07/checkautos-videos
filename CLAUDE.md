# CHECK AUTOS — taller de reels (sesiones en la nube)

Este repositorio edita reels verticales de CHECK AUTOS (revisión técnica vehicular, Perú) a partir de lo que el dueño
sube desde el teléfono. Se trabaja con HyperFrames (`/hyperframes`, `/media-use`, `/hyperframes-cli`).

## El pedido típico
"Edita entrada/vidN" → en `entrada/vidN/` hay una nota de voz de WhatsApp (.mp4/.opus/.m4a, el técnico narrando)
y fotos/videos del auto (a veces dentro de un .zip: extraerlo en una carpeta nueva, comprobando que no tenga rutas raras).
A veces no es una inspección sino un video del técnico hablando a cámara (sin nota de voz aparte).

## Antes de empezar
1. `bash tools/setup.sh` (instala ffmpeg y dependencias de Python si faltan).
2. Proyecto nuevo: `npx --yes hyperframes@0.8.186 init trabajo/vidN --example blank --resolution portrait --non-interactive --skill hyperframes`
   (con `HYPERFRAMES_SKIP_SKILLS=1`). `trabajo/` está en .gitignore.
3. Copia `tools/*.py` a `trabajo/vidN/_work/` y `assets/*` a `trabajo/vidN/assets/`.

## Voz (lo más importante para el cliente)
- Las notas de voz llegan SATURADAS casi siempre. Reparar con `tools/declip.py` (interpolación cúbica); adeclip de ffmpeg no sirve.
- Cadena: volume -9..-10 dB → highpass 85 Hz → afftdn MUY suave (nr 8) solo si hay ruido → -2 dB en 250 Hz → -1.5 dB en 3.2 kHz
  → highshelf 8 kHz -2 dB → deesser suave → compresión 2:1 → ganancia fija + alimiter a -1.5 dB, -16 LUFS. NUNCA subir agudos.
- Quitar "eh", repeticiones ("del… del"), alargamientos y silencios largos (`tools/edit_voice.py`, lista `cuts`; silencios a 0.15–0.32 s).
  Ubicar cada corte con `tools/contour.py` y verificar retranscribiendo POR TRAMOS (`tools/seg_transcribe.py`):
  Parakeet a veces se pasa al inglés con el audio limpio.
- Cabeza parlante: cortar video y audio juntos, alineados a fotograma (`tools/edit_talk.py`); zoom alterno 1.0/1.13 en cada corte.
- Música: `assets/music/the-corporate-upbeat.mp3` (CC BY 3.0, hay que dar crédito: `assets/music/CREDITOS.md`), a ~0.05 bajo la voz
  (voz ~20 dB sobre el fondo), sube solo al inicio y en el cierre. Efectos en `assets/sfx/` (Pixabay, sin crédito), 0.12–0.3.
- Entrega a -15 LUFS (ajustar con `-c:v copy -af volume=...` si sale más alto).

## Edición
- Plantillas: `plantillas/inspeccion/` (video 8: anotaciones a mano, medidor de fallas, dibujos) y `plantillas/cabeza-parlante/`
  (video 6: MITO/REALIDAD). Leer su SPEC/REVIEW. Cambiar un poco el estilo en cada video; no copiar idéntico.
- La plantilla de inspección usa una fuente "Marker" (assets/fonts/marker.ttf) que NO está en el repo (licencia de Windows):
  usar una fuente incluida en HyperFrames (Nunito 900, Poppins 800) o pedir al usuario un archivo con licencia libre.
- Gancho en los primeros 5 s; texto que aterriza en la palabra dicha; subtítulos palabra por palabra dentro de 168–1330 px.
- Mostrar cada falla con foco: círculos, flechas, etiquetas, dibujos generados cuando falte metraje.
- OCULTAR placas y números VIN/serie: revisar contact sheets de cada clip y no usar los tramos donde se lean.
- No inventar datos: si se agrega una referencia general (p. ej. "pintura normal ≈ 120 µm"), decirlo en la entrega.
- Marca: CHECK AUTOS, teléfono 959 365 374, logo en `assets/brand/logo.png`. Cierre con logo + teléfono ≥ 3 s.
- Siempre: `npx hyperframes check`, snapshots de cada escena, corregir y volver a mirar antes de renderizar.

## Entrega
1. `npx hyperframes render -o salida/CheckAutos_<Auto>.mp4 --quiet` y medir el audio.
2. Si pesa < 95 MB: `git add salida/<archivo>` y commit/push (para que el dueño lo descargue desde la app de GitHub).
   Si pesa más: re-encodar con `-crf 23` (sin tocar el audio) hasta quedar < 95 MB.
3. Opcional: `npx hyperframes publish` para un enlace compartible (pedir permiso: publica en internet).
4. No subir `entrada/` con material del cliente a otros lugares; no publicar en redes.
5. Responder en español, corto: qué se cortó de la voz, qué se mostró, qué datos se agregaron, qué hay que revisar.
