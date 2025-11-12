<h1 align="center">🩷 EVA_BOT – Módulo de Visión (OCR + Empatía)</h1>
<p align="center">
  <b>Proyecto de detección de violencia digital mediante análisis de imágenes</b><br/>
  Por <b>Gabriela Galarza</b> · Integración con Groq Vision, Tesseract y respuestas empáticas
</p>

---

## 🌸 ¿Qué desarrollé?
Implementé un sistema funcional de **análisis de imágenes** enfocado en la **detección de patrones de violencia digital**  
(insultos, agresiones verbales o contenido sensible).  
El sistema combina **visión artificial (GROQ)**, **OCR local (Tesseract + OpenCV)** y **reglas contextuales**,  
integrándose con el chatbot principal de Telegram.

---

## 🧩 Módulos desarrollados y funcionalidades principales

### 1️⃣ `analyzers/vision.py`
Sistema de análisis visual y OCR (en español e inglés).

- 🧠 Detección de insultos o frases agresivas mediante texto extraído de imágenes.  
- 🔎 Clasificación de severidad: **leve**, **media**, **alta**.  
- 🧱 Fallback inteligente: si no hay acceso a modelos de visión (GROQ), usa OCR local con **OpenCV y PyTesseract**.  
- 🧬 Detección experimental de **manipulación digital** (bordes, distorsión, contraste).  

**Preprocesamiento de imágenes (OpenCV):**
- Escalado a 1200 px  
- Binarización  
- Contraste aumentado  
- Reducción de ruido  
- Configuración OCR: `--oem 3 --psm 6 -l spa+eng`

---

### 2️⃣ `main.py`
Bot de Telegram completamente funcional integrado con el analizador de visión.

- 💬 Implementación de **mensajes empáticos** y **recursos de ayuda** según país.  
- ⚙️ Comandos implementados:
  - `/start` → mensaje de bienvenida  
  - `/help` → guía de uso  
  - `/setcountry AR` → cambia país (por ISO-2)  
  - `/ping` → prueba de conexión  

El bot interpreta los resultados del analizador y devuelve:
- Categorías de violencia detectadas  
- Nivel de severidad  
- Evidencias (palabras o frases extraídas)  
- Recomendaciones y recursos de ayuda (ej. Línea 144, ONU Mujeres)  
- Nota de privacidad y cierre empático 💌  

---

## 💫 Resultado comprobado
✅ El sistema procesa correctamente capturas de chat (WhatsApp, IG, etc.)  
✅ Clasifica insultos por tipo y severidad  
✅ Devuelve evidencias y recomendaciones adaptadas al país  
✅ Ofrece respuestas empáticas automáticas con privacidad protegida  

---

## 🧠 Mensajes empáticos automáticos
> “Lamento que estés lidiando con esto. No estás sola/o: estoy para ayudarte. No es tu culpa.”  
> “Podés borrar este chat cuando quieras; no guardo tus imágenes.”  
> “Si querés, puedo buscar más recursos o pensar junt@s próximos pasos.”

---

## 🛠️ Tecnologías utilizadas

| Herramienta / Librería | Función |
|------------------------|----------|
| 🐍 **Python** | Base del proyecto |
| 🤖 **PyTelegramBotAPI** | Interacción con Telegram |
| 👁️ **Groq API** | Análisis con visión artificial (modelo `llama-3.2-vision-preview`) |
| 🧩 **Tesseract OCR + OpenCV + NumPy** | OCR local (fallback) y preprocesamiento |
| 🧾 **python-dotenv** | Carga segura de claves y variables de entorno |
| 🖼️ **Pillow** | Manipulación de imágenes |

---

## ⚙️ Configuración

1. Crear un entorno virtual:
```bash
python -m venv .venv
source .venv/Scripts/activate
