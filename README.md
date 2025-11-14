# 🟣 EVA_BOT – Módulo de Visión (OCR + Análisis de Violencia)

**Autora:** Gabriela Galarza  
**Proyecto:** Detección de violencia digital en imágenes (capturas de pantalla)  
**Integración:** Groq Vision · Tesseract · OpenCV · PyTelegramBotAPI  

---

## 📖 Índice

- [¿Qué es EVA_BOT?](#qué-es-evabot)
- [Módulos y funcionalidades](#módulos-y-funcionalidades)
- [Análisis: analyzers/vision.py](#21-analyzersvisionpy)
- [Integración con Telegram: main.py](#22-mainpy)
- [Tabla comparativa de severidades](#tabla-comparativa-de-severidades)
- [Respuestas empáticas automáticas](#respuestas-empáticas-automáticas)
- [Ejemplos reales](#ejemplos-reales)
- [Tecnologías utilizadas](#tecnologías-utilizadas)
- [Instalación](#instalación)
- [Archivo .env](#archivo-env)
- [Ejecución](#ejecución)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Notas importantes](#notas-importantes)
- [Autora](#autora)

---

## ❓ ¿Qué es EVA_BOT?

EVA_BOT es un módulo de análisis de imágenes diseñado para detectar **violencia digital** en capturas de pantalla de conversaciones (WhatsApp, Instagram, redes sociales, etc.).

El sistema combina:

- 🔍 **Groq Vision** para análisis visual inteligente  
- 🧠 **OCR local** (Tesseract + OpenCV) como respaldo  
- 🧹 **Preprocesamiento avanzado** de imagen  
- 🗂️ **Clasificación verbal de agresiones**  
- 🤖 **Integración con Telegram**  

Si la API externa falla, el sistema activa automáticamente un **fallback local** para mantener el análisis funcional.

---

## 🧩 Módulos y funcionalidades

- ✔️ Detección de violencia verbal en texto extraído de imágenes  
- ✔️ OCR + preprocesamiento (soporte para español e inglés)  
- ✔️ Análisis contextual mediante reglas simples  
- ✔️ Extracción de evidencias relevantes desde la imagen  
- ✔️ Clasificación por gravedad (**leve, media, alta**)  
- ✔️ Respuestas empáticas automáticas al usuario  
- ✔️ Sugerencia de recursos de ayuda según país  
- ✔️ Fallback local cuando Groq Vision no está disponible  

---

## 🔎 2.1. analyzers/vision.py

Este módulo se encarga del análisis principal de la imagen:

- Aplicación de **preprocesamiento** con OpenCV:
  - Reducción de ruido  
  - Aumento de contraste  
  - Binarización adaptativa / inteligente  
- Ejecución de **OCR** (Tesseract) en español e inglés  
- Limpieza y normalización del texto extraído  
- Búsqueda de insultos, agresiones y expresiones de violencia  
- Clasificación de la severidad según reglas:
  - Leve  
  - Media  
  - Alta  
- Sistema de respaldo:
  - Primero intenta con **Groq Vision**  
  - Si falla, utiliza **OCR local** como fallback  

---

## 🤖 2.2. main.py

Gestiona el flujo completo del bot de Telegram:

- Recepción de imágenes desde el chat  
- Validación básica de la imagen (peso, formato, etc.)  
- Envío de la imagen al analizador de visión  
- Construcción de la respuesta al usuario:
  - Resultado del análisis (violencia Sí/No)  
  - Severidad detectada  
  - Evidencias textuales  
  - Mensaje empático  
  - Recursos de ayuda según país (si corresponde)  

### Comandos disponibles

- `/start` – Mensaje de bienvenida e introducción a EVA_BOT  
- `/help` – Ayuda básica y explicación de uso  
- `/setcountry` – Configura el país para mostrar recursos locales  
- `/ping` – Verifica que el bot esté activo  

---

## 📊 Tabla comparativa de severidades

| Severidad | Descripción                          | Ejemplos detectados                  |
|----------|--------------------------------------|--------------------------------------|
| 🟢 Leve  | Lenguaje hiriente ocasional          | “callate”, “molestás”                |
| 🟡 Media | Agresiones verbales directas         | insultos, descalificaciones          |
| 🔴 Alta  | Violencia extrema o repetitiva       | amenazas, hostigamiento, humillación |

---

## 💬 Respuestas empáticas automáticas

Ejemplos de mensajes que el bot puede enviar:

- "Lamento que estés pasando por esto. No estás sola/o."  
- "Estoy acá para ayudarte, no es tu culpa."  
- "Podés borrar este chat cuando quieras; no guardo imágenes."  
- "Si querés, puedo darte recursos de apoyo confidenciales."  

---

## 🧪 Ejemplos reales

✔️ **1. Imagen con insultos detectados**  
- Violencia detectada: **Sí**  
- Categoría: **verbal**  
- Severidad: **media**  
- Evidencias: `"mierda"`, otras expresiones descalificadoras  
- Recomendación: bloquear, guardar evidencia, pedir ayuda si se repite  

---

✔️ **2. Imagen sin violencia**  
- Violencia detectada: **No**  
- Severidad: sin clasificación  
- Respuesta sugerida:  
  - Mensaje empático reforzando que no hay señales de violencia en el contenido analizado  

---

✔️ **3. Fallback activado (sin Groq Vision)**  
- ⚠️ API externa no disponible  
- Modo activo: **OCR local + reglas**  
- El bot informa al usuario que está usando el análisis local, pero mantiene la funcionalidad básica de detección.  

---

## 🛠️ Tecnologías utilizadas

| Tecnología        | Uso                                      |
|-------------------|-------------------------------------------|
| Python            | Lenguaje principal                        |
| OpenCV            | Preprocesamiento de imagen                |
| Tesseract OCR     | Lectura de texto (fallback local)         |
| Groq Vision API   | Análisis de imagen con IA                 |
| Pillow (PIL)      | Manipulación y carga de imágenes          |
| PyTelegramBotAPI  | Integración y manejo del bot de Telegram  |
| python-dotenv     | Manejo de variables de entorno            |

---

## 🐍 Crear entorno virtual

```bash
python -m venv .venv
source .venv/Scripts/activate
```

---

## 📦 Instalar dependencias

```bash
pip install -r requirements.txt
```

⚠️ Primera ejecución: descargará modelos (~500 MB).

---

## 🔐 Archivo .env

Crear un archivo llamado **.env** con:

```ini
TELEGRAM_BOT_TOKEN=tu_token
GROQ_API_KEY=tu_api_key
```

⚠️ **Nunca** subir este archivo al repositorio.  
Asegurate que `.gitignore` lo incluya.

---

## ▶️ Ejecución

```bash
python main.py
```

---

## 📂 Estructura del Proyecto

```bash
404-not-found/
│── legacy_modules/      
│── .gitignore
│── README.md            
│── main.py      
```

---

## ⚠️ Notas Importantes

- ❌ **No guarda imágenes ni datos privados.**
- 🔒 **Toda la información queda en la sesión del usuario.**
- 🔄 **Si la API externa falla → se activa el análisis local (fallback automático).**
- 🌱 **Proyecto desarrollado como parte del Módulo de Visión del bot EVA.**

---

## 👩‍💻 Autora

**Gabriela Galarza**  