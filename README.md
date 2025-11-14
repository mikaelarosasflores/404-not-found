🟣 EVA_BOT – Módulo de Visión (OCR + Análisis de Violencia)

Autora: Gabriela Galarza
Proyecto: Detección de violencia digital mediante análisis de imágenes
Integración: Groq Vision · Tesseract · OpenCV · PyTelegramBotAPI

📑 Índice

¿Qué es EVA_BOT?

Módulos y funcionalidades

2.1. analyzers/vision.py

2.2. main.py

Tabla comparativa de severidades

Respuestas empáticas automáticas

Ejemplos reales del funcionamiento

Tecnologías utilizadas

Instalación

Archivo .env

Ejecución

Estructura del proyecto

Notas importantes

Autora

## ¿Qué es EVA_BOT?

EVA_BOT es un módulo inteligente diseñado para detectar violencia digital en capturas de pantalla mediante:

Visión artificial

OCR optimizado

Análisis lingüístico

Mensajes empáticos y recursos de ayuda

Funciona procesando imágenes enviadas por los usuarios a través de un bot de Telegram, extrae texto, evalúa agresiones verbales y devuelve un análisis acompañado de recomendaciones.

El módulo incluye:

Groq Vision (si disponible)

OCR local (Tesseract + OpenCV)

Sistema de reglas de severidad

Clasificación automática

Respuestas empáticas

Recursos según país

## 2. Módulos y funcionalidades
### 2.1 analyzers/vision.py — Módulo de visión + OCR

Este archivo contiene el núcleo del análisis visual.

✔ Funciones principales

OCR con Tesseract (español + inglés)

Preprocesamiento avanzado con OpenCV

aumento de contraste

reducción de ruido

escala adaptativa

binarización Otsu

Tokenización y normalización del texto

Clasificación de agresiones verbales según listas:

insultos

manipulación

amenazas

Cálculo automático de severidad

Fallback automático:
Groq Vision → OCR local si hay error 401/403/timeout

✔ Configuración OCR
--oem 3 --psm 6 -l spa+eng

### 2.2 main.py — Integración con Telegram

El bot permite:

✔ Recibir imágenes

Cuando el usuario envía una foto:

Se analiza su resolución

Se extrae el texto

Se clasifica la severidad

Se genera un mensaje empático

Se brindan recursos locales (144, 911, etc.)

✔ Comandos disponibles

/start – Mensaje de bienvenida

/help – Guía de uso

/setcountry AR – Cambia país para mostrar recursos locales

/modo_cuidado on/off – Filtra lenguaje fuerte

/ping – Verifica conexión

## Tabla comparativa de severidades
Nivel	Criterios	Ejemplos detectados	Acción del bot
Baja	1 insulto aislado	“idiota”, “mierda”	Recomenda no responder y guardar evidencia
Media	manipulación emocional, 2–3 agresiones	“Todo es tu culpa”	Muestra recursos + alerta
Alta	amenazas directas	“Te voy a…”	Alerta + recursos urgentes (911)
Desconocida	texto vacío o inentendible	imágenes borrosas	Pide una foto mejor
## Respuestas empáticas automáticas

El bot integra un sistema emocional para acompañar al usuario:

Ejemplos:

“Lamento que estés pasando por esto. No es tu culpa.”

“Gracias por confiar en mí para compartir esta imagen.”

“Podés borrar este chat cuando quieras; no guardo nada.”

“Si querés, puedo ayudarte a decidir próximos pasos.”

## Ejemplos reales del funcionamiento
✔ Ejemplo 1 — Detecta insultos

Entrada: Captura con “gorda cerda”
Salida:

Violencia detectada: Sí
Categorías: verbal
Severidad: media
Evidencias: ['cerda', 'gorda']
Recomendaciones:
- No respondas
- Guardá evidencia
- Bloqueá a la persona

✔ Ejemplo 2 — Nada ofensivo

Entrada: Conversación normal
Salida:

Violencia detectada: No
Evidencias: (sin evidencias)
Recomendaciones: Estoy disponible si querés hablar o enviar otra imagen.

✔ Ejemplo 3 — API Groq no disponible

Salida:

Nota: análisis LLM no disponible (usando OCR local).

✔ Ejemplo 4 — Imagen borrosa

El bot responde:

La imagen es muy pequeña o borrosa y no se alcanzan a distinguir bien las letras.

Recomendación:
- Enviá una captura donde el texto ocupe buena parte de la pantalla.
- Resolución ideal: 600×600 px o más.

## Tecnologías utilizadas
Herramienta	Rol
Python	Lenguaje principal
PyTelegramBotAPI	Integración con Telegram
Groq Vision API	Análisis de imagen
Tesseract OCR	Lectura de texto local
OpenCV + NumPy	Preprocesamiento
Pillow	Manipulación de imágenes
dotenv	Variables de entorno
## Instalación
1. Crear entorno virtual
python -m venv .venv
source .venv/Scripts/activate

2. Instalar dependencias
pip install -r requirements.txt

## Archivo .env

El archivo NO debe subirse al repositorio.

Formato:

TELEGRAM_BOT_TOKEN=tu_token
GROQ_API_KEY=tu_api_key

## Ejecución
python main.py


Si está correcto, verás:

🤖 Bot iniciado…
📸 Esperando imágenes…

## Estructura del proyecto
/404-not-found
│── analyzers/
│     └── vision.py
│── bot/
│── core/
│── utils/
│── data/
│── .gitignore
│── main.py
│── README.md
│── requirements.txt

## Notas importantes

No se guardan las imágenes procesadas.

.env nunca debe subirse.

El bot no reemplaza atención profesional.

Usa fallback automático si Groq falla.

Toda la información se maneja localmente.

👩‍💻 Autora

Gabriela Galarza — Estudiante de Ciencias de Datos
Apasionada por la tecnología, IA y desarrollo con impacto social.

