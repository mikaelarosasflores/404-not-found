# 🤖 Bot de Apoyo Emocional con IA - Detección de Violencia

> **Sistema de análisis en tiempo real con Transformers para detectar 7 categorías de violencia y 13 emociones**

---

## 📋 Tabla de Contenidos

- [¿Qué desarrollé?](#-qué-desarrollé)
- [Instalación Paso a Paso](#-instalación-paso-a-paso)
- [Configuración de Tokens](#-configuración-de-tokens)
- [Cómo Usar el Bot](#-cómo-usar-el-bot)
- [Ejemplos Probados](#-ejemplos-probados)
- [Detección de Violencia y Emociones](#-detección-de-violencia-y-emociones)
- [Solución de Problemas](#-solución-de-problemas)

---

## 🎯 ¿Qué desarrollé?

Un **sistema funcional de análisis** centrado en la detección de patrones de violencia con **Inteligencia Artificial**, probado y operativo.

### Módulos Funcionales

#### 📁 **bot_test.py** - Sistema Principal
- ✅ Chatbot operativo con análisis en tiempo real
- ✅ Integración completa con analizadores de IA
- ✅ Detección automática de patrones y emociones
- ✅ **Funciona perfectamente**

#### 📁 **analyzers/sentiment_analyzer.py** - Analizador con IA
- 🤖 **Integración completa con Transformers**
- 📊 Modelos de IA para español:
  - `pysentimiento/robertuito-sentiment-analysis`
  - `finiteautomata/beto-emotion-analysis`
- 🔍 **7 categorías de violencia detectables**
- 💭 **13 emociones identificables**
- 📈 **3 niveles de riesgo** (Alto, Moderado, Leve)

#### 📁 **analyzers/security_analyzer_poo.py** - Sistema POO Avanzado
- 🛡️ Sistema orientado a objetos
- 🔍 Detección especializada de patrones
- 📊 Análisis de riesgo multicapa
- 💬 Respuestas contextuales automáticas

### Resultado Comprobado

✅ **Sistema híbrido IA + Reglas** que detecta violencia en tiempo real  
✅ **Análisis emocional avanzado** con modelos Transformers  
✅ **Integrado en chatbot** de Telegram funcional  
✅ **280+ patrones específicos** de detección

---

## ⭐ Características Principales

### 🎭 Doble Sistema de Análisis

#### 1. Análisis de Seguridad con IA
- Detecta **7 tipos de violencia** en mensajes
- Usa **Transformers** para análisis contextual
- **Scoring inteligente** de patrones
- Combina IA + reglas para mayor precisión

#### 2. Análisis de Sentimiento con IA
- Identifica **13 emociones** en español
- Modelos especializados (RoBERTuito, BETO)
- Cálculo de **intensidad emocional**
- Apoyo personalizado según estado emocional

---

## 🚀 Instalación Paso a Paso

### Paso 1: Descargar Python

1. Descargar de [python.org](https://www.python.org/downloads/)
2. **Versión:** 3.8 o superior (recomendado: 3.10)
3. ⚠️ **Marcar "Add Python to PATH"** durante instalación

### Paso 2: Preparar archivos

```bash
# Clonar o descargar el proyecto
git clone 

### Paso 3: Crear entorno virtual

**Windows:**
```bash
python -m venv chatbot_env
chatbot_env\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv chatbot_env
source chatbot_env/bin/activate
```

✅ Verás `(chatbot_env)` al inicio

### Paso 4: Instalar dependencias

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar todo
pip install -r requirements.txt
```

⚠️ **Primera ejecución:** Descargará modelos de IA (~500MB). Solo ocurre una vez.

---

## 🔑 Configuración de Tokens

### 1. Crear archivo .env

En la carpeta principal, crear archivo `.env`

### 2. Agregar token

```env
TELEGRAM_TOKEN=tu_token_aqui
```

### 3. Conseguir token de Telegram

1. Buscar `@BotFather` en Telegram
2. Enviar `/newbot`
3. Seguir instrucciones
4. Copiar token y pegar en `.env`

**Ejemplo:**
```env
TELEGRAM_TOKEN=7123456789:AAHdqTcvbXYZ1234567890abcdefGHIJKLM
```

---

## 📱 Cómo Usar el Bot

### Iniciar el Bot

```bash
python bot_test.py
```

**Salida esperada:**
```
🔄 Inicializando SecurityAnalyzer...
🤖 Cargando modelos de IA...
Device set to use cpu
✅ Modelo de emociones cargado
✅ Modelos de IA cargados exitosamente
✅ Bot listo - Detección completa de 7 categorías
```

### Comandos

#### Iniciar:
```
/start
/help
hola
```

#### Analizar (usar "analiza:"):
```
analiza: mi novio me controla el celular
analiza: me amenaza con publicar fotos
analiza: me insultan constantemente
analiza: me pega y tengo moretones
```

#### Expresar emociones:
```
me siento triste
tengo mucho miedo
estoy muy enojada
me siento agobiada
```

#### Cerrar:
```
no gracias
adiós
gracias
```

---

## ✅ Ejemplos Probados

### Ejemplo 1: Violencia Digital
```
👤 Usuario: analiza: mi ex quiere mis contraseñas de Instagram

🤖 Bot:
🟡 RIESGO MODERADO
📱 Violencia Digital
🚫 Control y Aislamiento

⚠️ Estos patrones pueden escalar
🔒 Cambia tus contraseñas inmediatamente
📞 144 - Asesoramiento
```

### Ejemplo 2: Violencia Física
```
👤 Usuario: analiza: me pegó y tengo moretones

🤖 Bot:
🔴 RIESGO ALTO
⚠️ VIOLENCIA FÍSICA DETECTADA

🚨 NECESITAS AYUDA INMEDIATA
📞 911 - Emergencias
🏥 Ve a urgencias
📸 Documenta lesiones
```

### Ejemplo 3: Análisis Emocional
```
👤 Usuario: me siento muy triste y asustada

🤖 Bot con IA:
💭 Emociones: Tristeza, Miedo
📊 Intensidad: Alta (0.85/1.00)

💙 Veo que estás triste...
🛡️ Y también tienes miedo...

Consejos personalizados + apoyo
📞 144 - Apoyo emocional 24/7
```

### Ejemplo 4: Emergencia
```
👤 Usuario: quiero morirme

🤖 Bot:
🚨🚨 EMERGENCIA - AYUDA INMEDIATA 🚨🚨
📞 LLAMA AHORA:
• 911 - Emergencias
• 144 - Crisis 24/7
• Línea de la Vida: 800 911 2000
💖 Tu vida es valiosa
```

---

## 🔍 Detección de Violencia y Emociones

### 7 Categorías de Violencia

| Categoría | Palabras Clave | Nivel |
|-----------|---------------|-------|
| 🔴 **Violencia Física** | golpes, pegar, moretones, lastimar | ALTO |
| 😔 **Violencia Psicológica** | insultos, gritar, humillar, gaslighting | ALTO |
| 🚫 **Control y Aislamiento** | celos, revisar celular, prohibir | MODERADO |
| ⚠️ **Amenazas y Acoso** | amenazar, perseguir, acosar | ALTO |
| 🔞 **Violencia Sexual** | forzar, obligar, presionar | ALTO |
| 📱 **Violencia Digital** | hackear, contraseñas, stalkear | MODERADO |
| 💔 **Manipulación Emocional** | chantaje, culpa, sin mí no eres nada | MODERADO |
| 💰 **Violencia Económica** | controlar dinero, no me deja trabajar | MODERADO |

### 13 Emociones Detectables

| Emoción | Respuesta del Bot |
|---------|-------------------|
| 😢 Tristeza | Consejos + apoyo emocional |
| 🔥 Enojo | Técnicas de respiración |
| 😨 Miedo | Evaluación de seguridad |
| 😰 Agobio | Manejo del estrés |
| 😕 Confusión | Clarificación + decisiones |
| 😔 Impotencia | Empoderamiento |
| 😊 Felicidad | Refuerzo positivo |
| 🤔 Soledad | Redes de apoyo |
| 💭 Culpa | Auto-perdón |
| 😳 Vergüenza | Normalización |
| 😰 Ansiedad | Relajación |
| 💢 Frustración | Ajuste expectativas |
| 🌟 Esperanza | Establecer metas |

---

## 📞 Líneas de Ayuda

### 🚨 Emergencias
- **911** - Emergencias
- **144** - Violencia 24/7
- **Línea de la Vida** - 800 911 2000
- **SAPTEL** - 55 5259 8121

### 📞 Orientación
- **141** - Orientación mujeres
- **137** - Víctimas violencia
- **089** - Denuncia anónima

---

## 🛠️ Solución de Problemas

### ❌ Error: "Module not found"

```bash
# Verificar entorno activo (debe verse (chatbot_env))
# Reinstalar
pip install -r requirements.txt
```

---

### ❌ Error: "Bot token is not defined"

**Solución:**
1. Crear archivo `.env` en carpeta raíz
2. Agregar: `TELEGRAM_TOKEN=tu_token_real`
3. Guardar sin espacios extras

---

### ❌ Modelos de IA no cargan

**Mensaje:**
```
⚠️ No se pudieron cargar los modelos de IA
⚠️ Se usará análisis basado en reglas
```

**Solución:**
```bash
pip install transformers==4.35.0 torch==2.1.0
```

**Nota:** Primera ejecución descarga modelos (~500MB)

---

### ❌ Bot no responde

**Verificar:**
1. ✅ Bot corriendo: `python bot_test.py`
2. ✅ Mensaje "Escuchando mensajes..."
3. ✅ Token correcto en `.env`
4. ✅ Bot activo en @BotFather

---

### ⚠️ Advertencias TensorFlow (NORMAL)

Estos mensajes son normales:
```
WARNING:tensorflow:...
I tensorflow/core/util/port.cc:113...
```

Para desactivarlos, agregar en `.env`:
```env
TF_ENABLE_ONEDNN_OPTS=0
```

---

### 🐧 Windows: Error PowerShell

Usar **Command Prompt (CMD)**:
```bash
chatbot_env\Scripts\activate.bat
python bot_test.py
```

---

## 📁 Estructura del Proyecto

```
bot-apoyo-emocional/
│
├── bot_test.py                 # Bot principal
│
├── analyzers/
│   ├── sentiment_analyzer.py  # Analizador IA (Transformers)
│   └── security_analyzer_poo.py # Sistema POO avanzado
│
├── requirements.txt            # Dependencias
├── .env                        # Tokens (NO SUBIR)
├── .gitignore                 
│
├── README.md                   # Esta documentación
└── chatbot_env/               # Entorno virtual (NO SUBIR)
```

---

## 📦 requirements.txt

```txt
# Bot de Telegram
pyTelegramBotAPI==4.15.2
python-dotenv==1.0.0

# Transformers y modelos de IA
transformers==4.35.0
torch==2.1.0
tensorflow==2.15.0
sentencepiece==0.1.99

# Utilidades
numpy==1.24.3
scipy==1.11.3
```

---

## 🔒 Seguridad

⚠️ **IMPORTANTE:**
- ❌ **NUNCA** compartas `.env`
- ❌ **NO** subas `.env` a GitHub
- ✅ Agrega `.env` a `.gitignore`
- ✅ Análisis local, no guarda conversaciones

El bot es confidencial pero **NO reemplaza ayuda profesional**.

---

## 📝 Notas Importantes

1. **Primera ejecución:** Descarga modelos (~500MB, solo una vez)
2. **Sin IA:** Funciona con análisis basado en reglas
3. **Privacidad:** Todo local, no almacena conversaciones
4. **Profesional:** NO reemplaza ayuda psicológica
5. **Actualizado:** Líneas de ayuda México 2024

---

## 🌟 Agradecimientos

Gracias a todas las personas que luchan contra la violencia. Este proyecto es un granito de arena en esa lucha.

**¡Tu seguridad y bienestar importan!** 💜

---

**By Frida** 🌸
