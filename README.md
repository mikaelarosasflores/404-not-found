# 🟣 EVA_BOT – Módulo de Visión (OCR + Análisis de Violencia)

🔍 Sistema inteligente para detectar violencia digital en capturas de pantalla  
📱 WhatsApp · Instagram · Chat Apps · Redes Sociales  
💜 Hecho por: **Gabriela Galarza**

---

## 📘 Descripción General

EVA_BOT analiza imágenes para identificar **violencia digital**, como:

- insultos  
- manipulación emocional  
- agresiones verbales  
- lenguaje hiriente o descalificador  

Combina IA, visión artificial y análisis contextual para ofrecer un resultado empático, seguro y útil para la persona usuaria.

---

# 📑 Tabla de Contenidos

- 👉 [¿Qué desarrollé?](#qué-desarrollé)
- 👉 [Módulos y Funcionalidades](#módulos-y-funcionalidades)
  - 📌 [analyzers/vision.py](#21-analyzersvisionpy)
  - 📌 [main.py](#22-mainpy)
- 👉 [Tabla Comparativa de Severidades](#tabla-comparativa-de-severidades)
- 👉 [Respuestas Empáticas Automáticas](#respuestas-empáticas-automáticas)
- 👉 [Ejemplos Reales del Funcionamiento](#ejemplos-reales-del-funcionamiento)
- 👉 [Tecnologías Utilizadas](#tecnologías-utilizadas)
- 👉 [Instalación](#instalación)
- 👉 [Archivo .env](#archivo-env)
- 👉 [Ejecución](#ejecución)
- 👉 [Estructura del Proyecto](#estructura-del-proyecto)
- 👉 [Notas Importantes](#notas-importantes)
- 👉 [Autora](#autora)

---

# 🎯 ¿Qué desarrollé?

Diseñé un **módulo completo de análisis de imágenes** para detectar violencia digital presente en chats o publicaciones.  

🎛️ El sistema combina:

- 🧠 Modelos de visión IA (Groq Vision)  
- 📝 OCR local (Tesseract + OpenCV) como respaldo  
- 🚦 Clasificación de severidad (baja, media, alta)  
- 🧹 Limpieza y normalización avanzada del texto  
- ✨ Preprocesamiento profesional de imágenes  
- 🤖 Integración total con Telegram Bot  
- 🔄 Modo fallback automático si falla la API externa  
- 🛟 Respuestas empáticas y guía de ayuda para la persona usuaria  

---

# 🧩 Módulos y Funcionalidades

## 2.1. **analyzers/vision.py**

Incluye funcionalidades de análisis visual:

### 🔍 OCR + Visión Híbrida
- Extracción de texto en **spa+eng**  
- Aumento de contraste  
- Reducción de ruido  
- Binarización automática  
- Reescalado si la imagen es pequeña  

### ⚠ Detección de violencia verbal
- insultos → severidad baja  
- manipulación → severidad media  
- amenazas → severidad alta  

### 🎚 Clasificador de gravedad
Basado en cantidad, tipo e intensidad del texto detectado.

### 🛡 Modo seguro / fallback
Si Groq Vision falla → OCR local + reglas contextuales.

---

## 2.2. **main.py**

Controla:

✔ Recepción de imágenes  
✔ Ejecución del análisis  
✔ Respuestas empáticas  
✔ Recursos de ayuda  
✔ Comandos del bot  
✔ Modo cuidado  

### 🧵 Comandos disponibles

| Comando | Función |
|--------|---------|
| `/start` | Bienvenida |
| `/help` | Guía de uso |
| `/setcountry AR` | Cambiar país |
| `/modo_cuidado on/off` | Minimizar insultos |
| `/ping` | Prueba de vida |

---

# 🧨 Tabla Comparativa de Severidades

| Severidad | Descripción | Recomendación |
|----------|-------------|---------------|
| 🟢 **Baja** | Insultos aislados | Guardar evidencia |
| 🟡 **Media** | Manipulación emocional | No responder + bloquear |
| 🔴 **Alta** | Amenazas o daño directo | 144 / 911 |

---

# 💬 Respuestas Empáticas Automáticas

El bot acompaña emocionalmente al usuario:

- “Lamento que estés pasando por esto. No estás sola/solo.”  
- “Pedir ayuda es un acto de fortaleza.”  
- “No guardo tus imágenes, tu privacidad es prioridad.”  
- “Si querés, puedo ayudarte a pensar próximos pasos.”  

Incluye recursos por país (Argentina por defecto).

---

# 📸 Ejemplos Reales del Funcionamiento

## ✔ Caso 1 — Violencia verbal detectada

Violencia detectada: Sí
Categoría: Verbal
Severidad: Media
Evidencias: "cerda", "mierda"
Recomendación: Bloquear + guardar evidencia

shell
Copiar código

## ✔ Caso 2 — Imagen borrosa o muy pequeña

La imagen que enviaste es muy pequeña o borrosa.
Por favor enviá una captura donde el texto ocupe más espacio.

graphql
Copiar código

## ✔ Caso 3 — Fallback por API no disponible

Análisis realizado con OCR local (sin modelo LLM).

yaml
Copiar código

---

# 🛠 Tecnologías Utilizadas

| Herramienta | Uso |
|-------------|-----|
| Python | Lenguaje base |
| Groq Vision API | Modelos de visión |
| Tesseract OCR | OCR local |
| OpenCV | Preprocesamiento |
| Pillow | Imágenes |
| PyTelegramBotAPI | Bot de Telegram |
| python-dotenv | Variables de entorno |

---

# ⚙ Instalación

### 1️⃣ Crear entorno virtual

```bash
python -m venv .venv
source .venv/Scripts/activate
2️⃣ Instalar dependencias
bash
Copiar código
pip install -r requirements.txt
🔐 Archivo .env
ini
Copiar código
TELEGRAM_BOT_TOKEN=tu_token
GROQ_API_KEY=tu_api_key
⚠ Nunca subirlo al repositorio.

▶ Ejecución
bash
Copiar código
python main.py
🗂 Estructura del Proyecto
bash
Copiar código
404-not-found/
│── analyzers/
│   └── vision.py
│── core/
│── utils/
│── bot/
│── main.py
│── README.md
│── requirements.txt
│── .env  (local)
⚠ Notas Importantes
❌ No guarda imágenes ni datos privados.

🔒 Toda la información queda en la sesión del usuario.

🔄 Si la API externa falla → fallback local automático.

🧩 Proyecto desarrollado como parte del Módulo de Visión del bot EVA.

👩‍💻 Autora
Gabriela Galarza
Desarrolladora · Ciencia de Datos · IA para impacto social

