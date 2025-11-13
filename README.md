EVA_BOT – Módulo de Visión (OCR + Análisis de Violencia)

Autora: Gabriela Galarza
Proyecto: Detección de violencia digital mediante análisis de imágenes
Integración: Groq Vision · OpenCV · Tesseract · PyTelegramBotAPI

1. ¿Qué desarrollé?

Implementé un módulo completo de análisis de imágenes para detectar patrones de violencia digital presentes en capturas de pantalla (WhatsApp, Instagram, etc.).

El sistema combina:

Análisis con modelos de visión (Groq Vision)

OCR local como alternativa (Tesseract + OpenCV)

Reglas contextuales para clasificar insultos

Preprocesamiento avanzado para mejorar el texto extraído

Conexión directa con el chatbot principal de Telegram

Mi módulo funciona como un analizador especializado dentro del bot EVA_BOT.

2. Módulos y funcionalidades principales
2.1 analyzers/vision.py – Módulo de visión y OCR

✔ OCR en español e inglés (spa+eng)
✔ Detección de insultos, agresiones verbales y contenido sensible
✔ Clasificación por severidad: leve, media, alta
✔ Preprocesamiento con OpenCV:

Escalado a 1200 px

Binarización

Aumento de contraste

Reducción de ruido
✔ Fallback inteligente:
Si Groq Vision no está disponible → usa OCR local automáticamente
✔ Detección experimental de manipulación digital (bordes, distorsión, contraste)

Configuración OCR utilizada:

--oem 3 
--psm 6 
-l spa+eng

2.2 main.py – Bot de Telegram integrado al analizador

Funcionalidades implementadas:

Interpretación completa de resultados del analizador de imágenes

Envío de recomendaciones según severidad

Recursos de ayuda según país (ej.: Línea 144 en AR)

Mensajes empáticos para acompañar al usuario

Comandos disponibles:

/start        → mensaje de bienvenida  
/help         → guía de uso  
/setcountry   → cambia país por ISO-2  
/ping         → prueba de conexión  


El bot devuelve:

Categorías detectadas

Nivel de severidad

Evidencias (frases extraídas)

Recomendaciones y recursos útiles

Nota de privacidad

3. Resultado comprobado

✔ Procesa correctamente capturas de chat
✔ Detecta insultos y agresiones verbales
✔ Clasifica severidad en 3 niveles
✔ Funciona incluso sin Groq (usa OCR local)
✔ Devuelve mensajes empáticos y profesionales
✔ No guarda imágenes → privacidad asegurada

4. Mensajes empáticos automáticos

El bot incluye mensajes diseñados para acompañar a la persona:

“Lamento que estés lidiando con esto. No estás solo/a: estoy para ayudarte. No es tu culpa.”
“Puedes borrar este chat cuando quieras; no guardo tus imágenes.”
“Si quieres, puedo buscar más recursos o pensar en los próximos pasos.”

5. Tecnologías utilizadas
Herramienta / Librería	Función
Python	Base del módulo
PyTelegramBotAPI	Interacción con Telegram
Groq API	Análisis con visión artificial
Tesseract OCR + OpenCV	OCR local y preprocesamiento
NumPy	Procesamiento de matrices
Pillow	Manipulación de imágenes
python-dotenv	Carga de claves y variables de entorno
6. Instalación del entorno
6.1 Crear entorno virtual
python -m venv .venv


Activar entorno:

source .venv/Scripts/activate   # Windows

6.2 Instalar dependencias
pip install -r requirements.txt

7. Configurar archivo .env

Este archivo NO debe subirse al repositorio.
Solo se documenta el formato requerido.

TELEGRAM_BOT_TOKEN=tu_token
GROQ_API_KEY=tu_api_key


Reemplazar por valores reales.

8. Ejecutar el bot
python main.py


Si todo está correctamente configurado, el bot quedará escuchando mensajes e imágenes.

9. Archivos necesarios

main.py

analyzers/vision.py

requirements.txt

.env (local, no subir)

10. Notas importantes

No guardar ni compartir el archivo .env

Este sistema no reemplaza ayuda profesional

Toda la información procesada se mantiene privada

El bot está probado en entorno real con capturas de chat

Este módulo se integra con otros analizadores del proyecto EVA_BOT

11. Estado actual

El módulo quedó funcional, probado e integrado al bot general del equipo.
Detecta insultos, clasifica severidad y devuelve recursos de ayuda y mensajes empáticos.
