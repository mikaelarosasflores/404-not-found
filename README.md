🧠 Análisis de Imágenes y Detección de Violencia
📍 Proyecto: EVA_BOT – Módulo de Visión (por Gabriela Galarza)
🔍 ¿Qué desarrollé?

Implementé un sistema funcional de análisis de imágenes enfocado en la detección de patrones de violencia digital (insultos, agresiones verbales y contenido sensible).
El sistema combina visión artificial (GROQ), OCR local (Tesseract) y reglas contextuales, integrándose con el chatbot principal.

🧩 Módulos desarrollados y funcionalidades principales

1. 🖼️ analyzers/vision.py

Sistema de análisis visual y OCR (en español e inglés).

Detección de insultos o frases agresivas mediante texto extraído de imágenes.

Clasificación de severidad: leve, media y alta.

Fallback inteligente: si no hay acceso a modelos de visión (GROQ), usa OCR local con OpenCV y Pytesseract.

Detección experimental de manipulación digital (bordes, distorsión, contraste).

2. 🤖 main.py

Bot funcional de Telegram integrado con el analizador.

Implementación completa de mensajes empáticos y recursos de ayuda según país.

Comandos implementados:

/start – Mensaje de bienvenida.

/help – Guía de uso.

/setcountry – Cambia país de referencia (por ISO-2).

/ping – Prueba de conexión.

Sistema de respuestas contextualizadas con tono humano y mensaje de contención.

3. ⚙️ core/recommender.py

Repositorio de recursos locales de ayuda (144, 911, ONU Mujeres).

Se adapta dinámicamente al país del usuario.

Prioriza recomendaciones claras y accesibles.

💡 Mejoras técnicas implementadas

Reestructuración completa del proyecto en arquitectura modular (OOP).

OCR local optimizado:

Preprocesamiento con OpenCV (escala, binarización, contraste, reducción de ruido).

Configuración --oem 3 --psm 6 -l spa+eng.

Respuestas empáticas automatizadas: mensajes de apoyo, privacidad y cuidado.

Control de errores robusto: mensajes claros si falta token, modelo o conexión.

.env aislado para seguridad.

Integración total con el chatbot principal del equipo.

🧪 Resultados comprobados

✔ Detección exitosa de frases agresivas en capturas de WhatsApp y redes sociales.
✔ Clasificación de violencia verbal y recomendación de recursos de ayuda.
✔ Funcionamiento estable en Telegram con mensajes claros, cálidos y empáticos.

🧰 Tecnologías utilizadas

Python 3.10

Telebot (PyTelegramBotAPI)

Pytesseract + OpenCV + NumPy

Groq API (llama-3.2-vision-preview)

Pillow

Dotenv

🌍 Impacto del módulo

El sistema busca detectar, contener y orientar ante posibles situaciones de violencia digital, cuidando la privacidad y ofreciendo recursos útiles y humanos.

"No se trata solo de analizar imágenes, sino de acompañar con empatía." 💛
