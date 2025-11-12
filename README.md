# 🔍 Analisis de Sentimiento - Resumen Breve

Que desarrolle?
Un sistema funcional de analisis centrado en la deteccion de patrones de violencia, probado y operativo a traves de mis modulos principales.

Mis Modulos Funcionales
----------------------

bot_test.py
- Sistema principal probado y funcionando
- Chatbot operativo con analisis en tiempo real
- Integracion completa con los analizadores
- Funciona perfectamente

Analizadores (Sistema Especializado)
- security_analyzer_poo.py - Sistema avanzado POO
- 7 categorias de violencia detectables
- 3 niveles de riesgo (Alto, Moderado, Leve)
- Respuestas contextuales automaticas
- sentiment_analyzer.py - Analisis emocional base

Resultado Comprobado
-------------------
Desarrolle y probe exitosamente un sistema de analisis que detecta patrones de violencia en tiempo real, integrado en un chatbot completamente funcional.

Doble Sistema de Analisis
------------------------
1. Analisis de Seguridad: Detecta patrones de violencia en mensajes
2. Analisis de Sentimiento: Identifica el estado emocional de la persona para dar apoyo personalizado

INSTALACION PASO A PASO
=======================

Paso 1: Descargar Python
------------------------
- Si no tienes Python, descargalo de python.org
- Version 3.8 o superior
- Durante instalacion, marcar "Add Python to PATH"

Paso 2: Preparar los archivos
-----------------------------
- Descargar todos los archivos del proyecto
- Ponerlos en una carpeta llamada "security-chatbot"
- Abrir terminal o command prompt en esa carpeta

Paso 3: Crear entorno virtual
-----------------------------
En la terminal, ejecutar:

Windows:
python -m venv chatbot_env
chatbot_env\Scripts\activate

Mac/Linux:
python3 -m venv chatbot_env
source chatbot_env/bin/activate

Deberias ver (chatbot_env) al inicio de la linea de comandos.

Paso 4: Instalar dependencias EXACTAS
-------------------------------------
Con el entorno virtual activado, ejecutar:

pip install pyTelegramBotAPI==4.15.2
pip install groq==0.9.0
pip install python-dotenv==1.0.0

Esperar a que termine cada instalacion.

Paso 5: Configurar tokens
-------------------------
1. Crear archivo .env en la misma carpeta
2. Abrir el archivo .env con bloc de notas
3. Pegar este contenido:

TELEGRAM_TOKEN=tu_token_de_telegram_aqui
GROQ_API_KEY=tu_api_key_de_groq_aqui

4. Guardar el archivo

Como conseguir los tokens:
- Token Telegram: Buscar @BotFather en Telegram, crear bot con /newbot
- API Key Groq: Registrarse en groq.com, ir a API Keys

Paso 6: Ejecutar el bot
-----------------------
En la terminal, con entorno virtual activado:

python bot_test.py

Si todo esta bien, deberias ver:
- Groq inicializado - Analisis REAL de sentimiento
- Asistente de Seguridad y Apoyo Emocional Iniciado
- Escuchando mensajes...

COMO USAR EL BOT
================

Frases para iniciar:
hola
hi
hello
/start

Para analizar mensajes (OBLIGATORIO usar "analiza:"):
analiza: mi novio me controla el celular
analiza: me amenazan con publicar fotos
analiza: no me dejan salir de casa
analiza: me insultan y humillan
analiza: me piden mis contraseñas

Para expresar emociones (el bot analiza tu estado de animo):
me siento triste
me siento asustada
me siento enojada
me siento confundida
estoy preocupada
tengo miedo
tengo ansiedad
me siento sola
estoy desesperada
tengo culpa

Para cerrar la conversacion:
no
no gracias
adiós
chao
bye
gracias
listo
ya está

EJEMPLOS QUE FUNCIONAN
=====================

Ejemplo 1: Analisis de violencia digital
Usuario: analiza: mi ex quiere mis contraseñas de Instagram
Bot: Detecta VIOLENCIA DIGITAL - Riesgo ALTO

Ejemplo 2: Analisis de control
Usuario: analiza: mi pareja no me deja ver a mis amigos
Bot: Detecta CONTROL Y AISLAMIENTO - Riesgo MODERADO

Ejemplo 3: Analisis de amenazas
Usuario: analiza: me amenaza con venir a mi casa
Bot: Detecta AMENAZAS Y ACOSO - Riesgo MODERADO

Ejemplo 4: Expresar emociones - ANALISIS DE SENTIMIENTO
Usuario: me siento triste y asustada
Bot: Detecta TRISTEZA y MIEDO - Ofrece consejos especificos para esas emociones

Ejemplo 5: Cerrar conversacion
Usuario: no, gracias
Bot: Se despide adecuadamente

QUE HACE EL BOT - DOBLE SISTEMA
==============================

Sistema 1: Analisis de Seguridad
- Analiza mensajes en busca de 7 tipos de violencia
- Evalua nivel de riesgo (Alto, Moderado, Leve)
- Ofrece recursos de ayuda especificos

Sistema 2: Analisis de Sentimiento
- Detecta emociones del usuario (tristeza, miedo, enojo, etc.)
- Analiza el estado emocional de la persona
- Ofrece consejos personalizados segun la emocion detectada
- Proporciona apoyo emocional contextual

TIPOS DE VIOLENCIA QUE DETECTA
=============================

1. Violencia Psicologica - insultos, humillaciones
2. Violencia Fisica - golpes, agresiones
3. Violencia Digital - control de redes, contraseñas
4. Control y Aislamiento - prohibir salidas, amistades
5. Manipulacion Emocional - chantaje, culpas
6. Amenazas y Acoso - persecucion, intimidacion
7. Violencia Economica - control de dinero, sueldo

EMOCIONES QUE DETECTA
====================

- Tristeza
- Miedo
- Enojo
- Confusion
- Frustracion
- Ansiedad
- Culpa

LINEAS DE AYUDA INCLUIDAS
========================

- Linea 144 - Violencia 24/7
- Linea 102 - Ninos y adolescentes
- Linea 137 - Violencia familiar y sexual
- Linea 141 - Salud mental
- 911 - Emergencias

SOLUCION DE PROBLEMAS
====================

Si sale error "Module not found":
- Verificar que el entorno virtual esta activado
- Revisar que se instalaron las 3 dependencias exactas

Si sale error de tokens:
- Verificar que el archivo .env esta en la carpeta correcta
- Confirmar que los tokens son validos

Si el bot no responde:
- Verificar que se ejecuto python bot_test.py
- Confirmar que aparece "Escuchando mensajes..."

Si no detecta patrones:
- Asegurarse de usar "analiza:" antes del mensaje
- Verificar que el mensaje contiene palabras clave

ARCHIVOS NECESARIOS
==================

- bot_test.py (archivo principal)
- requirements.txt (dependencias)
- .env (tokens - NO SUBIR A INTERNET)
- sentiment_analyzer.py (analizador base)
- security_analyzer_poo.py (analizador avanzado)

NOTAS IMPORTANTES
================

- Nunca compartas tu archivo .env
- El bot es confidencial pero no reemplaza ayuda profesional
- Funciona para cualquier genero
- Esta probado y funcionando correctamente
- Tiene doble sistema: seguridad + analisis emocional

By Frida
