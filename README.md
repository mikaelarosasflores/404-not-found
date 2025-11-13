# EVA_BOT – Módulo de Visión (OCR + Análisis de Violencia)

**Autora:** Gabriela Galarza  
**Proyecto:** Detección de violencia digital mediante análisis de imágenes  
**Integración:** Groq Vision · Tesseract · OpenCV · PyTelegramBotAPI

---

## 1. ¿Qué desarrollé?

Implementé un módulo completo de análisis de imágenes para detectar patrones de violencia digital presentes en capturas de pantalla (WhatsApp, Instagram, redes sociales, etc.).

El sistema combina:

- Análisis con modelos de visión artificial (Groq Vision)
- OCR local como alternativa (Tesseract + OpenCV)
- Reglas contextuales para clasificar insultos y agresiones
- Preprocesamiento avanzado para mejorar el texto extraído
- Integración con el bot principal de Telegram

El módulo funciona como un analizador autónomo, con fallback automático si la API de visión no está disponible.

---

## 2. Módulos y funcionalidades principales

### 2.1. `analyzers/vision.py` – Análisis de visión y OCR

Incluye:

- OCR en español e inglés (`spa+eng`)
- Detección de insultos, agresiones verbales y contenido sensible
- Clasificación por severidad (leve, media, alta)
- Fallback automático (Groq Vision → Tesseract)
- Detección básica de manipulación digital (contraste, bordes)
- Limpieza y normalización del texto detectado

#### Preprocesamiento con OpenCV

- Escalado a 1200 px  
- Binarización  
- Aumento de contraste  
- Reducción de ruido  

#### Configuración OCR utilizada

--oem 3 --psm 6 -l spa+eng

yaml
Copiar código

---

## 3. `main.py` – Integración con Telegram

El bot recibe una imagen del usuario y devuelve:

- Si se detectó violencia digital
- Categorías identificadas
- Nivel de severidad
- Evidencias (texto extraído)
- Recomendaciones y recursos por país
- Nota de privacidad
- Mensaje empático de acompañamiento

### Comandos disponibles

/start → Mensaje de bienvenida
/help → Guía de uso
/setcountry → Cambiar país según código ISO-2
/ping → Prueba de conexión

yaml
Copiar código

---

## 4. Mensajes empáticos automáticos

El sistema devuelve respuestas empáticas para acompañar al usuario:

> “Lamento que estés pasando por esto. No estás solo/a.”  
> “Puedes borrar este chat cuando quieras; no guardo tus imágenes.”  
> “Si querés, puedo buscar más recursos o ayudarte con próximos pasos.”

---

## 5. Ejemplos de funcionamiento

### Ejemplo 1 — Insultos detectados
**Entrada:** captura con frases agresivas.  
**Salida:**  
- Violencia detectada: Sí  
- Categorías: verbal  
- Severidad: media  
- Evidencias: insultos extraídos  
- Recomendación: no responder, bloquear, guardar evidencia  

### Ejemplo 2 — Sin violencia detectada
**Entrada:** captura sin contenido ofensivo.  
**Salida:**  
- Violencia detectada: No  
- Evidencias: texto neutral  
- Recomendación: mensaje empático y de disponibilidad  

### Ejemplo 3 — API Groq no disponible (modo fallback)
**Entrada:** imagen borrosa  
**Salida:**  
- Análisis realizado con OCR local  
- Advertencia: análisis sin LLM  
- Evidencias extraídas parcialmente  

---

## 6. Tecnologías utilizadas

| Herramienta / Librería        | Función |
|-------------------------------|---------|
| Python                        | Lenguaje principal |
| PyTelegramBotAPI              | Interacción con Telegram |
| Groq Vision API               | Análisis de visión artificial |
| Tesseract OCR + OpenCV + NumPy| OCR local y preprocesamiento |
| python-dotenv                 | Manejo de variables de entorno |
| Pillow                        | Manipulación de imágenes |

---

 