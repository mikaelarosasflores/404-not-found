import os
import telebot
import groq
import time
from dotenv import load_dotenv

# ✅ Cargar tokens del .env
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN') 
GROQ_API_KEY = os.getenv('GROQ_API_KEY')      


# ✅ Inicialización
bot = telebot.TeleBot(TELEGRAM_TOKEN)

try:
    client = groq.Client(api_key=GROQ_API_KEY)
    groq_disponible = True
    print("✅ Groq inicializado - Análisis REAL de sentimiento")
except Exception as e:
    print(f"❌ Groq no disponible: {e}")
    groq_disponible = False
    client = None

user_context = {}

def analizar_mensaje_manual(texto):
    """Análisis COMPLETO de las 7 categorías de violencia - MEJORADO"""
    texto_lower = texto.lower()
    
    patrones_detectados = {}
    nivel_riesgo = 'bajo'
    puntuacion_riesgo = 0
    
    # 1️⃣ VIOLENCIA PSICOLÓGICA/EMOCIONAL - MEJORADO
    psicologica_palabras = [
        'inútil', 'estúpida', 'estúpido', 'no sirves', 'eres un', 'das lástima', 
        'muérete', 'idiota', 'incompetente', 'fracasada', 'fracasado', 'no vales nada',
        'burla', 'ridiculizar', 'ningunear', 'despreciar', 'humillar', 'criticar constantemente',
        'gaslighting', 'hacerte dudar', 'locura', 'exagerada', 'loca', 'celos excesivos',
        'acusar sin razón', 'desvalorizar', 'minimizar sentimientos', 'insultar', 'ofender'
    ]
    if any(palabra in texto_lower for palabra in psicologica_palabras):
        patrones_detectados['violencia_psicologica'] = True
        puntuacion_riesgo += 3
    
    # 2️⃣ VIOLENCIA FÍSICA - MEJORADO
    fisica_palabras = [
        'golpear', 'pegar', 'empujar', 'jalar', 'pellizcar', 'patear', 'abofetear',
        'tirar del pelo', 'ahogar', 'quemar', 'lastimar', 'herir', 'romper huesos',
        'usar armas', 'cuchillo', 'pistola', 'objeto contundente', 'zarandear', 'agredir',
        'violencia física', 'maltratar', 'abusar físicamente'
    ]
    if any(palabra in texto_lower for palabra in fisica_palabras):
        patrones_detectados['violencia_fisica'] = True
        puntuacion_riesgo += 4
    
    # 3️⃣ VIOLENCIA DIGITAL - MEJORADO
    digital_palabras = [
        'contraseñas', 'passwords', 'acceso a', 'cuentas', 'redes sociales', 'celular',
        'instagram', 'facebook', 'whatsapp', 'teléfono', 'dispositivo', 'revisar mensajes',
        'controlar redes', 'spyware', 'stalkear', 'sextorsión', 'difamar', 'fake profile',
        'suplantar identidad', 'onlyfans', 'deepfake', 'fotos íntimas', 'publicar fotos',
        'chantajear digital', 'extorsionar digital', 'revisar celular', 'mirar teléfono',
        'vigilar redes', 'controlar internet'
    ]
    if any(palabra in texto_lower for palabra in digital_palabras):
        patrones_detectados['violencia_digital'] = True
        puntuacion_riesgo += 3
    
    # 4️⃣ CONTROL Y AISLAMIENTO - MEJORADO (¡ESTE ERA EL PROBLEMA!)
    control_palabras = [
        'no salgas', 'no salga', 'dónde estás', 'con quién estás', 'debes hacer',
        'no hables con', 'no te vistas', 'controlar', 'vigilar', 'no veas a',
        'aislar', 'control económico', 'revisar tus mensajes', 'prohibir amistades',
        'control de redes sociales', 'pase contraseñas', 'pásame contraseñas',
        'dame contraseñas', 'acceso a tu celular', 'revisar tu celular',
        'controlar tu teléfono', 'vigilar tus movimientos', 'controlar horarios',
        'no me dejas ver', 'no me deja ver', 'prohibir salir', 'impedir ver',
        'controlar amistades', 'no permits ver', 'aislar de familia',
        'controlar con quién hablo', 'vigilar mis salidas'  # NUEVOS PATRONES
    ]
    if any(palabra in texto_lower for palabra in control_palabras):
        patrones_detectados['control_aislamiento'] = True
        puntuacion_riesgo += 3
    
    # 5️⃣ MANIPULACIÓN EMOCIONAL Y ABUSO PSICOLÓGICO - MEJORADO
    manipulacion_palabras = [
        'si me quisieras', 'eres egoísta', 'nadie te aguanta', 'por tu culpa',
        'sin mí no eres nada', 'nadie te va a querer', 'me debes', 'si no estás conmigo',
        'te voy a dejar si', 'nadie te querrá como yo', 'eres mi propiedad',
        'debes obedecerme', 'tienes que hacerme caso', 'si te vas me mato',
        'no puedo vivir sin ti', 'eres todo para mí', 'sin ti me muero',
        'love bombing', 'breadcrumbing', 'chantaje emocional', 'culpar', 'victimizarse',
        'hacerte sentir culpable', 'obligar a tener relaciones', 'presión sexual',
        'única razón para vivir', 'razón de vivir', 'sin ti no vivo'  # NUEVOS PATRONES
    ]
    if any(palabra in texto_lower for palabra in manipulacion_palabras):
        patrones_detectados['manipulacion_emocional'] = True
        puntuacion_riesgo += 3
    
    # 6️⃣ AMENAZAS Y ACOSO - MEJORADO (¡ESTE ERA EL PROBLEMA!)
    amenazas_palabras = [
        'matar', 'lastimar', 'hacer daño', 'te voy a', 'vas a pagar', 'acabar contigo',
        'eliminarte', 'romperte', 'destrozarte', 'te juro que', 'te aseguro que',
        'te voy a buscar', 'sé dónde vives', 'no te dejaré en paz', 'perseguir',
        'acosar', 'hostigar', 'estaré pendiente', 'vigilaré', 'esperar afuera',
        'seguirte', 'amenazar familia', 'amenazar mascotas', 'va a venir',
        'ir a tu casa', 'sabe dónde trabajo', 'conoce mi dirección',  # NUEVOS PATRONES
        'venir a buscarme', 'esperar en casa', 'vigilar trabajo',
        'amenazar con venir', 'ir a donde estés'
    ]
    if any(palabra in texto_lower for palabra in amenazas_palabras):
        patrones_detectados['amenazas_acoso'] = True
        puntuacion_riesgo += 4
    
    # 7️⃣ VIOLENCIA ECONÓMICA/PATRIMONIAL - MEJORADO (¡ESTE ERA EL PROBLEMA!)
    economica_palabras = [
        'dame dinero', 'págame', 'debes pagar', 'devuélveme', 'me debes plata',
        'si no me pagas', 'obligar a trabajar', 'control de sueldo', 'quitar tarjetas',
        'deudas forzadas', 'extorsión económica', 'no te doy dinero', 'controlar gastos',
        'prohibir trabajar', 'quitar propiedades', 'destruir documentos',
        'control patrimonial', 'impedir trabajo', 'sustraer bienes',
        'controla el dinero', 'dar mi sueldo', 'entregar salario',  # NUEVOS PATRONES
        'control financiero', 'manejar mi dinero', 'quitar ingresos',
        'obligar a dar dinero', 'controlar cuentas', 'prohibir trabajar'
    ]
    if any(palabra in texto_lower for palabra in economica_palabras):
        patrones_detectados['violencia_economica'] = True
        puntuacion_riesgo += 3  # Aumenté la puntuación
    
    # 🚨 DETECCIÓN DE SUICIDIO - PRIORIDAD MÁXIMA (YA FUNCIONABA BIEN)
    suicidio_palabras = ['suicidar', 'suicidio', 'matarme', 'acabar con todo', 'no quiero vivir']
    if any(palabra in texto_lower for palabra in suicidio_palabras):
        patrones_detectados['riesgo_suicida'] = True
        puntuacion_riesgo = 10  # Máxima prioridad
    
    # 📊 CALCULAR NIVEL DE RIESGO MEJORADO
    if puntuacion_riesgo >= 10:
        nivel_riesgo = 'crítico'
    elif puntuacion_riesgo >= 5:  # Bajé el threshold para ALTO
        nivel_riesgo = 'alto'
    elif puntuacion_riesgo >= 2:  # Bajé el threshold para MODERADO
        nivel_riesgo = 'moderado'
    else:
        nivel_riesgo = 'bajo'
    
    return {
        'nivel_riesgo': nivel_riesgo,
        'patrones_detectados': patrones_detectados,
        'puntuacion': puntuacion_riesgo
    }

def generar_acciones_recomendadas(patrones_detectados):
    """Recomendaciones ESPECÍFICAS para cada tipo de violencia"""
    
    acciones = ""
    
    # 🚨 PRIORIDAD MÁXIMA - RIESGO SUICIDA
    if 'riesgo_suicida' in patrones_detectados:
        acciones += "🚨🚨🚨 EMERGENCIA - RIESGO DE VIDA 🚨🚨🚨\n\n"
        acciones += "• 📞 Llama INMEDIATAMENTE a Línea 102 (Atención a niños, niñas y adolescentes)\n"
        acciones += "• 🏥 Ve a urgencias del hospital más cercano\n"
        acciones += "• 👥 Contacta a familiares o amigos de confianza\n"
        acciones += "• 🆘 Llama al 911 si es una emergencia inminente\n"
        acciones += "• 💬 Habla con un profesional de salud mental\n\n"
    
    # 1️⃣ VIOLENCIA PSICOLÓGICA
    if 'violencia_psicologica' in patrones_detectados:
        acciones += "💔 VIOLENCIA PSICOLÓGICA DETECTADA:\n"
        acciones += "• 🛡️ Tu salud mental es importante - busca apoyo profesional\n"
        acciones += "• 📝 Reconoce que el abuso verbal NO es normal\n"
        acciones += "• 🚶‍♀️ Aléjate de personas que te humillen o desvaloricen\n"
        acciones += "• 💪 Practica afirmaciones positivas diarias\n"
        acciones += "• 📞 Línea 141 - Apoyo en salud mental\n\n"
    
    # 2️⃣ VIOLENCIA FÍSICA
    if 'violencia_fisica' in patrones_detectados:
        acciones += "🚨 VIOLENCIA FÍSICA DETECTADA:\n"
        acciones += "• 🏥 Busca atención médica inmediata si hay lesiones\n"
        acciones += "• 📸 Documenta cualquier evidencia (fotos, videos)\n"
        acciones += "• 🚓 Denuncia ante autoridades inmediatamente\n"
        acciones += "• 🏠 Busca un lugar seguro lejos del agresor\n"
        acciones += "• 📞 Línea 144 - Violencia doméstica 24/7\n\n"
    
    # 3️⃣ VIOLENCIA DIGITAL
    if 'violencia_digital' in patrones_detectados:
        acciones += "📱 VIOLENCIA DIGITAL DETECTADA:\n"
        acciones += "• 🔑 Cambia TODAS tus contraseñas inmediatamente\n"
        acciones += "• ⚙️ Revisa configuraciones de privacidad en redes\n"
        acciones += "• 🚨 Reporta el contenido en las plataformas\n"
        acciones += "• 📸 Guarda capturas como evidencia\n"
        acciones += "• 👮 Denuncia ante autoridades cybernéticas\n\n"
    
    # 4️⃣ CONTROL Y AISLAMIENTO
    if 'control_aislamiento' in patrones_detectados:
        acciones += "🔐 CONTROL Y AISLAMIENTO DETECTADO:\n"
        acciones += "• 🗽 Mantén tu independencia y libertad personal\n"
        acciones += "• 🛑 Establece límites CLAROS sobre tu privacidad\n"
        acciones += "• 📱 Mantén contacto con tu red de apoyo\n"
        acciones += "• 💳 Ten acceso a tus propios recursos económicos\n"
        acciones += "• 🚫 NO cedas contraseñas o acceso personal\n\n"
    
    # 5️⃣ MANIPULACIÓN EMOCIONAL
    if 'manipulacion_emocional' in patrones_detectados:
        acciones += "🎭 MANIPULACIÓN EMOCIONAL DETECTADA:\n"
        acciones += "• 🔍 Reconoce los patrones de manipulación\n"
        acciones += "• 🧠 Confía en tu intuición y percepciones\n"
        acciones += "• 🚫 No cedas a culpas injustificadas\n"
        acciones += "• 💬 Busca perspectivas objetivas externas\n"
        acciones += "• 📚 Educate sobre relaciones saludables\n\n"
    
    # 6️⃣ AMENAZAS Y ACOSO
    if 'amenazas_acoso' in patrones_detectados:
        acciones += "👁️ AMENAZAS Y ACOSO DETECTADOS:\n"
        acciones += "• 📍 Varía tus rutinas diarias\n"
        acciones += "• 🏠 Asegura tu domicilio\n"
        acciones += "• 👥 Informa a personas de confianza\n"
        acciones += "• 🚔 Denuncia inmediatamente\n"
        acciones += "• 📱 Ten el 911 en marcación rápida\n\n"
    
    # 7️⃣ VIOLENCIA ECONÓMICA
    if 'violencia_economica' in patrones_detectados:
        acciones += "💰 VIOLENCIA ECONÓMICA DETECTADA:\n"
        acciones += "• 💳 Ten cuentas bancarias independientes\n"
        acciones += "• 📊 Lleva control de tus finanzas personales\n"
        acciones += "• 💼 Busca independencia laboral\n"
        acciones += "• 🚫 NO entregues dinero bajo presión\n"
        acciones += "• 📞 Línea 144 - Asesoramiento legal\n\n"
    
    if not acciones:
        acciones = "💡 PARA TU BIENESTAR:\n• 🧘‍♀️ Cuida tu salud mental\n• 🛑 Establece límites saludables\n• 👥 Mantén tu red de apoyo\n\n"
    
    # 📞 RECURSOS GENERALES
    acciones += "📞 RECURSOS DE AYUDA:\n"
    acciones += "• Línea 144 - Violencia 24/7\n"
    acciones += "• Línea 102 - Niños y adolescentes\n"
    acciones += "• Línea 137 - Violencia familiar/sexual\n"
    acciones += "• Línea 141 - Salud mental\n"
    acciones += "• 911 - Emergencias\n"
    
    return acciones

def detectar_emocion_rapida(texto):
    """Detección MEJORADA de emociones"""
    texto_lower = texto.lower().strip()
    
    emociones = {
        'enojo': ['enojada', 'enojado', 'enfadada', 'enfadado', 'rabia', 'molesta', 'molesto', 'furia'],
        'tristeza': ['triste', 'tristeza', 'deprimida', 'deprimido', 'mal', 'desanimada', 'desanimado', 'sola', 'soledad', 'aislada', 'aislado'],
        'miedo': ['asustada', 'asustado', 'miedo', 'preocupada', 'preocupado', 'ansiosa', 'ansioso'],
        'confusion': ['confundida', 'confundido', 'perdida', 'perdido', 'desorientada', 'desorientado'],
        'frustracion': ['frustrada', 'frustrado', 'desesperada', 'desesperado', 'impotente'],
        'ansiedad': ['ansiosa', 'ansioso', 'nerviosa', 'nervioso', 'intranquila', 'intranquilo'],
        'culpa': ['culpable', 'culpabilidad', 'arrepentida', 'arrepentido']
    }
    
    for emocion, palabras in emociones.items():
        for palabra in palabras:
            if palabra in texto_lower:
                return emocion
    return None

def generar_consejo_emocional(emocion):
    """Consejos para cada emoción"""
    consejos = {
        'enojo': "🔥 Detecto enojo...\n\n• 🌬️ Respira profundamente\n• 📝 Escribe y rompe el papel\n• 🚶‍♀️ Sal a caminar\n• ⏰ Espera antes de decidir\n\n¿Qué está causando este enojo?",
        'tristeza': "💙 Veo tristeza y soledad...\n\n• 🫂 Permítete sentir sin juicios\n• 👥 Habla con alguien de confianza\n• 🛁 Date un baño relajante\n• 📖 Recuerda momentos superados\n\n¿Quieres contarme más sobre lo que te tiene así?",
        'miedo': "🛡️ Siento miedo...\n\n• 🔍 Identifica específicamente qué te preocupa\n• 📋 Piensa en planes alternativos\n• 🌬️ Practica respiración profunda\n• 👥 Rodéate de personas seguras\n\n¿Qué te genera miedo?",
        'confusion': "💫 Entiendo confusión...\n\n• 🧠 Escribe todo sin filtrar\n• 📊 Haz lista de opciones\n• ⏳ Date tiempo\n• 🗣️ Habla con alguien objetivo\n\n¿Qué te confunde?",
        'frustracion': "🌪️ Detecto frustración...\n\n• 🛑 Date permiso de descansar\n• 🎉 Celebra pequeños progresos\n• 🔄 Cambia de actividad\n• 🤝 Pide ayuda\n\n¿Qué te frustra?",
        'ansiedad': "🌀 Percibo ansiedad...\n\n• 🌬️ Respiración 4-7-8\n• 🎯 Enfócate en el presente\n• 🚶‍♀️ Camina y siente el suelo\n• 📝 Escribe preocupaciones\n\n¿Qué te genera ansiedad?",
        'culpa': "⚖️ Siento culpa...\n\n• 🤔 Distingue responsabilidad vs culpa\n• 💝 Practica autoperdón\n• 📝 Escribe carta de perdón\n• 🎯 Enfócate en mejorar\n\n¿Qué te hace sentir culpa?"
    }
    return consejos.get(emocion, "🌻 Entiendo que estás en un momento difícil...\n\n¿Puedes contarme más específicamente cómo te sientes?")

def analizar_sentimiento_usuario(texto):
    """Analiza la emoción del USUARIO, no del mensaje agresor"""
    if not groq_disponible:
        return "No pude analizar"
    try:
        if len(texto) > 500:
            texto = texto[:500]
        
        prompt = f"""
        Analiza la emoción de la PERSONA que está contando esta situación. 
        Responde SOLO con una palabra: tristeza, enojo, miedo, frustracion, confusion, ansiedad, culpa, neutral
        
        Situación: "{texto}"
        """
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=10
        )
        sentimiento = response.choices[0].message.content.strip().lower()
        sentimientos_validos = ['tristeza', 'enojo', 'miedo', 'frustracion', 'confusion', 'ansiedad', 'culpa', 'neutral']
        return sentimiento if sentimiento in sentimientos_validos else "No pude analizar"
    except Exception as e:
        print(f"❌ Error en análisis Groq: {e}")
        return "No pude analizar"

# [EL RESTO DEL CÓDIGO PERMANECE IGUAL - desde @bot.message_handler hasta el final]
# ... (mantener todo el resto del código igual)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    user_text = message.text.strip()
    
    print(f"👤 Usuario {user_id}: {user_text}")
    
    # 🎯 DETECTAR DESPEDIDAS Y AGRADECIMIENTOS - SOLO CUANDO HAY CONTEXTO
    despedidas = ['no', 'nop', 'ya está', 'listo', 'ya', 'no gracias', 'adiós', 'chao', 'bye', 'gracias', 'thank you', 'thanks']
    if user_id in user_context and any(palabra in user_text.lower() for palabra in despedidas):
        bot.reply_to(message, "🌻 Hasta luego, cuídate mucho. Estaré aquí cuando me necesites. 💫")
        del user_context[user_id]
        return
    
    # 🎯 DETECTAR ANÁLISIS DE MENSAJE
    if any(user_text.lower().startswith(palabra) for palabra in ['analiza', 'analyze', 'analizar']):
        texto_analizar = user_text
        for palabra in ['analiza', 'analyze', 'analizar', ':', 'este', 'this', 'mensaje']:
            texto_analizar = texto_analizar.lower().replace(palabra, '')
        texto_analizar = texto_analizar.strip()
        
        if not texto_analizar:
            bot.reply_to(message, "🔍 ¿Qué mensaje quieres que analice?")
            return
        
        msg_analizando = bot.reply_to(message, "🔍 Analizando con cuidado... 🌸")
        time.sleep(1)
        
        try:
            # ANÁLISIS DE SEGURIDAD del mensaje agresor
            analysis = analizar_mensaje_manual(texto_analizar)
            
            # ANÁLISIS DE EMOCIÓN del USUARIO (no del mensaje)
            emocion_usuario = analizar_sentimiento_usuario(texto_analizar)
            
            respuesta = "💫 HE ANALIZADO EL MENSAJE CUIDADOSAMENTE\n\n"
            
            # Mostrar emoción detectada en el USUARIO
            if emocion_usuario != "No pude analizar":
                respuesta += f"📊 Detecto que tú te sientes: {emocion_usuario.upper()}\n\n"
            
            emoji_riesgo = {'crítico': '🔴🚨🚨', 'alto': '🔴🚨', 'moderado': '🟡⚠️', 'bajo': '🟢✅'}
            respuesta += f"🛡️ Evaluación de riesgo: {emoji_riesgo.get(analysis['nivel_riesgo'], '✅')} {analysis['nivel_riesgo'].upper()}\n\n"
            
            if analysis['patrones_detectados']:
                respuesta += "⚠️ COMPORTAMIENTOS PREOCUPANTES DETECTADOS:\n\n"
                for patron in analysis['patrones_detectados'].keys():
                    respuesta += f"• 🔍 {patron.replace('_', ' ').title()}\n"
                respuesta += "\n"
            
            acciones = generar_acciones_recomendadas(analysis['patrones_detectados'])
            respuesta += acciones + "\n\n"
            
            # MEJOR FLUJO: Preguntar directamente por emociones
            respuesta += "💬 ¿Puedes contarme cómo te sientes con esta situación?"
            
            user_context[user_id] = {
                'esperando_emocion': True,
                'ultimo_analisis': analysis
            }
            
            bot.edit_message_text(respuesta, chat_id=message.chat.id, message_id=msg_analizando.message_id)
            
        except Exception as e:
            print(f"❌ Error en análisis: {e}")
            bot.edit_message_text("❌ Lo siento, tuve un problema. ¿Podrías intentarlo de nuevo? 🌸", chat_id=message.chat.id, message_id=msg_analizando.message_id)
        return
    
    # 💬 DETECTAR EMOCIONES DIRECTAMENTE
    emocion_detectada = detectar_emocion_rapida(user_text)
    if emocion_detectada and user_id not in user_context:
        consejo = generar_consejo_emocional(emocion_detectada)
        bot.reply_to(message, consejo)
        user_context[user_id] = {'esperando_respuesta': True}
        return
    
    # 💬 MANEJO DE EMOCIONES DESPUÉS DE ANÁLISIS
    elif user_id in user_context and user_context[user_id].get('esperando_emocion'):
        emocion = detectar_emocion_rapida(user_text)
        if emocion:
            consejo = generar_consejo_emocional(emocion)
            bot.reply_to(message, consejo)
            # MANTENER CONVERSACIÓN ABIERTA
            user_context[user_id]['esperando_emocion'] = False
            user_context[user_id]['esperando_respuesta'] = True
        else:
            # Si no detecta emoción clara, preguntar de otra forma
            bot.reply_to(message, "💬 ¿Puedes describir cómo te sientes con esta situación?")
        return
    
    # 💬 RESPUESTA A "¿QUIERES HABLAR MÁS?"
    elif user_id in user_context and user_context[user_id].get('esperando_respuesta'):
        if any(palabra in user_text.lower() for palabra in ['sí', 'si', 'sip', 'claro', 'por supuesto', 'ok', 'sí quiero']):
            bot.reply_to(message, "💬 ¿Hay algo más en lo que pueda acompañarte? Puedes contarme cómo te sientes o si necesitas más orientación 🌸")
        else:
            # Solo cerrar si es claramente una despedida
            if any(palabra in user_text.lower() for palabra in ['no', 'nada más', 'eso es todo', 'adiós', 'chao']):
                bot.reply_to(message, "🌻 Hasta luego, cuídate mucho. Estaré aquí cuando me necesites. 💫")
                del user_context[user_id]
            else:
                # Si no es despedida clara, mantener conversación
                emocion = detectar_emocion_rapida(user_text)
                if emocion:
                    consejo = generar_consejo_emocional(emocion)
                    bot.reply_to(message, consejo)
                else:
                    bot.reply_to(message, "💬 ¿Hay algo más en lo que pueda apoyarte?")
        return
    
    # 👋 MENSAJE INICIAL
    elif user_text.lower() in ['hola', 'hi', 'hello', '/start']:
        bot.reply_to(message, 
            "🌻 ¡Hola! Soy tu asistente de apoyo emocional y seguridad.\n\n"
            "Puedo ayudarte a:\n\n"
            "🔍 Analizar mensajes preocupantes:\n"
            "Escribe: analiza: tu mensaje aquí\n\n"
            "💬 Apoyo emocional:\n" 
            "Puedes contarme cómo te sientes\n\n"
            "🛡️ Orientación en situaciones difíciles\n\n"
            "¿En qué puedo acompañarte hoy? 💫"
        )
        return
    
    # 🔍 DETECCIÓN AUTOMÁTICA DE MENSAJES PREOCUPANTES
    else:
        analisis_rapido = analizar_mensaje_manual(user_text)
        if analisis_rapido['nivel_riesgo'] in ['crítico', 'alto']:
            bot.reply_to(message,
                "🔍 Este mensaje parece preocupante. ¿Quieres que lo analice en detalle?\n\n"
                "Escribe: analiza: [tu mensaje aquí]\n\n"
                "O cuéntame cómo te sientes 💬"
            )
        else:
            emocion = detectar_emocion_rapida(user_text)
            if emocion:
                consejo = generar_consejo_emocional(emocion)
                bot.reply_to(message, consejo)
                user_context[user_id] = {'esperando_respuesta': True}
            else:
                bot.reply_to(message,
                    "🌻 Hola, ¿en qué puedo acompañarte?\n\n"
                    "Puedo ayudarte a:\n"
                    "• 🔍 Analizar mensajes preocupantes\n"  
                    "• 💬 Ofrecer apoyo emocional\n"
                    "• 🛡️ Orientarte en situaciones difíciles\n\n"
                    "Escribe 'analiza:' seguido del mensaje\n"
                    "O cuéntame cómo te sientes 💫"
                )

print("🤖 Asistente de Seguridad y Apoyo Emocional Iniciado")
print("🎯 Detección de 7 tipos de violencia MEJORADA")
print("📱 Escuchando mensajes...")
bot.polling()