"""
BOT DE APOYO EMOCIONAL - VERSIÓN MEJORADA CON DETECCIÓN COMPLETA
Detecta 7 categorías de violencia con patrones expandidos
"""

import telebot
import time
import os
import random
import re
from dotenv import load_dotenv
from analyzers.sentiment_analyzer import SecurityAnalyzer

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Inicializar analizador
analyzer = SecurityAnalyzer()
user_context = {}

print("🤖 Bot de Apoyo Emocional - Versión Mejorada")
print(f"🎯 {analyzer.version}")

# ==================== PATRONES EXPANDIDOS POR CATEGORÍA ====================
PATRONES_VIOLENCIA = {
    'violencia_fisica': {
        'patrones': [
            r'me\s+(pega|golpea|empuja|jala|avienta|sacude)',
            r'(pega|golpea|empuja|jala|avienta|sacude)\s+me',
            r'me\s+(dio|pego|golpeo|empujo)',
            r'me\s+puso\s+la\s+mano\s+encima',
            r'me\s+(lastim[óo]|hiri[óo])',
            r'me\s+tir[óo]\s+(algo|cosas)',
            r'me\s+(agarr[óo]|sujet[óo])\s+fuerte',
            r'me\s+zamarr(e|[óo])',
            r'me\s+jaloneó',
            r'me\s+da\s+(golpes|nalgadas|cachetadas|patadas)',
            r'me\s+amenaza\s+con\s+pegar',
            r'levanta\s+la\s+mano',
            r'rompe\s+cosas\s+cuando\s+se\s+enoja',
            r'tira\s+cosas',
            r'me\s+ha\s+dejado\s+(moretones|marcas|heridas)',
            r'fuerza\s+f[íi]sica',
            r'violencia\s+f[íi]sica'
        ],
        'nivel_base': 'alto',
        'icono': '🔴'
    },
    
    'violencia_psicologica': {
        'patrones': [
            r'me\s+(grita|insulta|humilla|menosprecia|degrada)',
            r'me\s+hace\s+sentir\s+(mal|in[úu]til|tonta?|est[úu]pida?|fea)',
            r'me\s+dice\s+(in[úu]til|tonta?|est[úu]pida?|idiota|basura)',
            r'me\s+(critica|juzga|ofende)\s+todo\s+el\s+tiempo',
            r'se\s+burla\s+de\s+(m[íi]|mis)',
            r'me\s+(ridiculiza|averg[üu]enza)',
            r'me\s+compara\s+con',
            r'me\s+ignora\s+(completamente|por\s+d[íi]as)',
            r'ley\s+del\s+hielo',
            r'tratamiento\s+silencioso',
            r'me\s+hace\s+(dudar|sentir\s+loca)',
            r'gaslighting',
            r'luz\s+de\s+gas',
            r'niega\s+lo\s+que\s+(dijo|hizo|pas[óo])',
            r'distorsiona\s+(la\s+realidad|mis\s+recuerdos)',
            r'me\s+minimiza',
            r'mis\s+sentimientos\s+no\s+importan',
            r'exagero\s+todo',
            r'muy\s+sensible',
            r'dram[áa]tica'
        ],
        'nivel_base': 'alto',
        'icono': '😔'
    },
    
    'control_aislamiento': {
        'patrones': [
            r'se\s+enoja\s+(cuando|si)\s+(hablo|salgo|veo)',
            r'se\s+molesta\s+(cuando|si)\s+(hablo|salgo|veo)',
            r'celos\s+(de|por|cuando)\s+(hablo|salgo|veo|mis)',
            r'celoso\s+(de|por|cuando)\s+(hablo|salgo|veo|mis)',
            r'no\s+me\s+deja\s+(salir|ver|hablar|tener)',
            r'proh[íi]be\s+(salir|ver|hablar|tener)',
            r'controla\s+(mis\s+)?amigos?',
            r'controla\s+(mis\s+)?amistades',
            r'controla\s+con\s+qui[ée]n\s+(hablo|salgo|veo)',
            r'aisla\s+de\s+(mi\s+)?familia',
            r'no\s+quiere\s+que\s+(vea|hable|salga)',
            r'revisa\s+(mi|mis)\s+(mensajes|celular|tel[ée]fono|redes)',
            r'quiere\s+saber\s+(todo|donde|con\s+qui[ée]n)',
            r'me\s+(llama|escribe|busca)\s+todo\s+el\s+tiempo',
            r'controla\s+mi\s+ubicaci[óo]n',
            r'quiere\s+(contrase[ñn]as|claves)',
            r'se\s+pone\s+(celoso|celosa)\s+por\s+todo',
            r'no\s+puedo\s+(salir|tener)\s+amigos',
            r'me\s+aleja\s+de',
            r'tengo\s+que\s+(pedir\s+permiso|avisarle)',
            r'me\s+(vigila|persigue|espía|acecha)',
            r'stalking',
            r'acoso'
        ],
        'nivel_base': 'moderado',
        'icono': '🚫'
    },
    
    'amenazas_intimidacion': {
        'patrones': [
            r'me\s+amenaza\s+con',
            r'amenaza\s+con\s+(matarme|hacerme\s+da[ñn]o|lastimar)',
            r'amenaza\s+con\s+(suicidarse|irse|dejarme)',
            r'amenaza\s+(a\s+)?mi\s+familia',
            r'me\s+(intimida|asusta|aterroriza)',
            r'me\s+da\s+miedo',
            r'tengo\s+miedo\s+(de\s+)?[ée]l',
            r'dice\s+que\s+me\s+va\s+a',
            r'va\s+a\s+(matarme|hacerme)',
            r'te\s+voy\s+a',
            r'chantaje\s+(emocional|con)',
            r'si\s+(me\s+dejas|te\s+vas)',
            r'amenaza\s+con\s+(quitarme|llevarse)',
            r'dice\s+que\s+(se\s+mata|se\s+suicida)',
            r'me\s+extorsiona',
            r'dice\s+que\s+va\s+a\s+difundir',
            r'amenaza\s+con\s+(fotos|videos|ex)',
            r'revenge\s+porn',
            r'porno\s+venganza'
        ],
        'nivel_base': 'alto',
        'icono': '⚠️'
    },
    
    'violencia_sexual': {
        'patrones': [
            r'me\s+(fuerza|obliga)\s+a',
            r'me\s+presiona\s+para',
            r'no\s+acepta\s+un\s+no',
            r'insiste\s+(aunque|cuando)\s+(digo|le\s+digo)\s+no',
            r'me\s+toca\s+sin\s+(permiso|consentimiento)',
            r'no\s+respeta\s+mi\s+(cuerpo|espacio)',
            r'me\s+(acosa|hostiga)\s+sexualmente',
            r'comentarios\s+sexuales\s+inc[óo]modos',
            r'me\s+hace\s+sentir\s+inc[óo]moda?\s+sexualmente',
            r'abuso\s+sexual',
            r'violaci[óo]n',
            r'me\s+oblig[óo]\s+a\s+tener',
            r'no\s+respeta\s+mi\s+no',
            r'me\s+grab[óo]\s+sin\s+permiso',
            r'comparti[óo]\s+(fotos|videos)\s+[íi]ntimos',
            r'sexting\s+no\s+consensuado',
            r'me\s+env[íi]a\s+(fotos|mensajes)\s+sexuales',
            r'dick\s+pics',
            r'no\s+ped[íi]\s+(fotos|videos)'
        ],
        'nivel_base': 'alto',
        'icono': '🔞'
    },
    
    'violencia_digital': {
        'patrones': [
            r'revisa\s+mi\s+(celular|tel[ée]fono|whatsapp)',
            r'espía\s+mis\s+(mensajes|redes|conversaciones)',
            r'hackea|hackeo',
            r'entr[óo]\s+a\s+mi\s+(cuenta|perfil)',
            r'public[óo]\s+(fotos|videos)\s+sin\s+permiso',
            r'me\s+etiqueta\s+en',
            r'cre[óo]\s+perfil\s+falso',
            r'se\s+hace\s+pasar\s+por',
            r'me\s+(acosa|hostiga)\s+por\s+(redes|internet|l[íi]nea)',
            r'cyberbullying',
            r'ciberacoso',
            r'me\s+manda\s+mensajes\s+(obsesivos|constantes)',
            r'bombardeo\s+de\s+mensajes',
            r'me\s+stalkea\s+en\s+redes',
            r'revisa\s+mis\s+redes\s+sociales',
            r'me\s+bloque[óo]\s+de\s+todo',
            r'control\s+digital',
            r'me\s+obliga\s+a\s+(compartir|dar)\s+(ubicaci[óo]n|contrase[ñn]as)',
            r'gps\s+localizador',
            r'app\s+esp[íi]a'
        ],
        'nivel_base': 'moderado',
        'icono': '📱'
    },
    
    'manipulacion_emocional': {
        'patrones': [
            r'me\s+(culpa|responsabiliza)\s+(de|por)',
            r'(culpa|es\s+mi\s+culpa)\s+de\s+todo',
            r'me\s+hace\s+sentir\s+culpable',
            r'chantaje\s+emocional',
            r'se\s+hace\s+(la\s+)?v[íi]ctima',
            r'manipula\s+(mis\s+)?sentimientos',
            r'juega\s+con\s+mis\s+emociones',
            r'me\s+confunde',
            r'hot\s+and\s+cold',
            r'fr[íi]o\s+y\s+caliente',
            r'dice\s+una\s+cosa\s+y\s+hace\s+otra',
            r'promesas\s+vac[íi]as',
            r'nunca\s+cumple',
            r'me\s+enga[ñn]a',
            r'mentiras\s+constantes',
            r'doble\s+vida',
            r'infiel',
            r'me\s+usa\s+emocionalmente',
            r'love\s+bombing',
            r'bombardeo\s+de\s+amor',
            r'ciclo\s+de\s+(abuso|violencia)',
            r'luna\s+de\s+miel',
            r'pide\s+perd[óo]n\s+pero\s+vuelve',
            r'promete\s+cambiar\s+pero\s+no'
        ],
        'nivel_base': 'moderado',
        'icono': '💔'
    },
    
    'violencia_economica': {
        'patrones': [
            r'controla\s+(mi|mis)\s+(dinero|finanzas|gastos|ingresos)',
            r'no\s+me\s+deja\s+trabajar',
            r'proh[íi]be\s+(trabajar|estudiar)',
            r'sabotea\s+mi\s+(trabajo|empleo|carrera)',
            r'me\s+quita\s+(el\s+)?dinero',
            r'me\s+obliga\s+a\s+(dar|entregarle)',
            r'tengo\s+que\s+pedir(le)?\s+dinero',
            r'controla\s+todos\s+los\s+gastos',
            r'no\s+puedo\s+(comprar|gastar)',
            r'me\s+(niega|quita)\s+recursos',
            r'dependencia\s+econ[óo]mica',
            r'abuso\s+econ[óo]mico',
            r'me\s+hace\s+firmar',
            r'deudas\s+a\s+mi\s+nombre',
            r'usa\s+mis\s+tarjetas',
            r'gasta\s+mi\s+dinero',
            r'no\s+me\s+da\s+para',
            r'me\s+mantiene\s+sin\s+dinero',
            r'explotaci[óo]n\s+econ[óo]mica'
        ],
        'nivel_base': 'moderado',
        'icono': '💰'
    }
}

# ==================== ANÁLISIS MEJORADO ====================
def _analizar_completo(texto):
    """Análisis completo con todas las categorías"""
    texto_lower = texto.lower()
    
    categorias_detectadas = {}
    nivel_riesgo_max = 'bajo'
    
    # Evaluar cada categoría
    for categoria, config in PATRONES_VIOLENCIA.items():
        for patron in config['patrones']:
            if re.search(patron, texto_lower):
                categorias_detectadas[categoria] = {
                    'nivel': config['nivel_base'],
                    'icono': config['icono']
                }
                
                # Actualizar nivel máximo de riesgo
                if config['nivel_base'] == 'alto' and nivel_riesgo_max != 'alto':
                    nivel_riesgo_max = 'alto'
                elif config['nivel_base'] == 'moderado' and nivel_riesgo_max == 'bajo':
                    nivel_riesgo_max = 'moderado'
                break
    
    # Ajustar nivel si hay múltiples categorías
    if len(categorias_detectadas) >= 3:
        nivel_riesgo_max = 'alto'
    elif len(categorias_detectadas) >= 2 and nivel_riesgo_max == 'bajo':
        nivel_riesgo_max = 'moderado'
    
    # Casos especiales - palabras de emergencia
    palabras_emergencia = ['suicid', 'matarme', 'acabar con todo', 'no quiero vivir', 'morir']
    if any(palabra in texto_lower for palabra in palabras_emergencia):
        nivel_riesgo_max = 'emergencia'
    
    return {
        'nivel_riesgo': nivel_riesgo_max,
        'categorias_detectadas': categorias_detectadas,
        'num_categorias': len(categorias_detectadas)
    }

# ==================== CONSEJOS ESPECÍFICOS ====================
def _generar_consejos_categoria(categorias):
    """Genera consejos específicos por categoría detectada"""
    
    CONSEJOS_CATEGORIA = {
        'violencia_fisica': """
🔴 VIOLENCIA FÍSICA - RIESGO ALTO

ACCIONES INMEDIATAS:
• Busca un lugar seguro
• Documenta lesiones (fotos)
• Acude a un centro de salud
• Denuncia: 911 o 144

IMPORTANTE:
• La violencia física tiende a escalar
• No es tu culpa
• No estás exagerando
• Mereces estar segura

📞 AYUDA URGENTE:
• 911 - Emergencias
• 144 - Línea de violencia 24/7
• Refugios disponibles
""",
        
        'violencia_psicologica': """
😔 VIOLENCIA PSICOLÓGICA

SEÑALES QUE ESTÁS VIVIENDO:
• Insultos y humillaciones
• Te hacen dudar de ti misma
• Minimizan tus sentimientos
• Gaslighting (distorsión de realidad)

ESTRATEGIAS:
• Confía en tu percepción
• Habla con personas de confianza
• Busca apoyo profesional
• Establece límites claros

📞 APOYO:
• 144 - Orientación
• 141 - Recursos
""",
        
        'control_aislamiento': """
🚫 CONTROL Y AISLAMIENTO

PATRONES DETECTADOS:
• Celos excesivos
• Control de amistades
• Vigilancia constante
• Restricción de libertad

RECUPERA TU AUTONOMÍA:
• Reconecta con tu red de apoyo
• Mantén contacto con familia/amigos
• Tienes derecho a privacidad
• El amor no controla

📞 ORIENTACIÓN:
• 144 - Asesoramiento
• 141 - Recursos
""",
        
        'amenazas_intimidacion': """
⚠️ AMENAZAS E INTIMIDACIÓN

SITUACIÓN GRAVE:
• Las amenazas son un delito
• Pueden escalar a violencia física
• Tu seguridad está en riesgo

ACCIONES:
• Documenta todas las amenazas
• No minimices la situación
• Busca protección legal
• Medidas cautelares disponibles

📞 URGENTE:
• 911 - Emergencias
• 144 - Protección inmediata
• Denuncia necesaria
""",
        
        'violencia_sexual': """
🔞 VIOLENCIA SEXUAL - URGENTE

LO QUE DEBES SABER:
• NO es tu culpa
• Un "no" es suficiente
• El consentimiento es voluntario
• Es un delito

BUSCA AYUDA:
• No te bañes antes de denunciar
• Acude a hospital (kit de violación)
• Denuncia: 089 o 911
• Apoyo psicológico disponible

📞 LÍNEAS ESPECIALIZADAS:
• 089 - Denuncia anónima
• 911 - Emergencias
• 144 - Apoyo integral
""",
        
        'violencia_digital': """
📱 VIOLENCIA DIGITAL/CIBERNÉTICA

PROTEGE TU PRIVACIDAD:
• Cambia todas tus contraseñas
• Activa verificación en 2 pasos
• Revisa apps con acceso a ubicación
• Bloquea en todas las redes

SI HAY CONTENIDO ÍNTIMO:
• Denuncia (Ley Olimpia)
• Solicita eliminación a plataformas
• Guarda evidencia
• Es un delito

📞 AYUDA:
• 089 - Denuncia ciberacoso
• 144 - Orientación legal
""",
        
        'manipulacion_emocional': """
💔 MANIPULACIÓN EMOCIONAL

TÁCTICAS COMUNES:
• Culpabilización constante
• Chantaje emocional
• Gaslighting
• Ciclo de abuso

RECUERDA:
• No eres responsable de su felicidad
• Tus emociones son válidas
• El amor no manipula
• Mereces respeto genuino

RECUPERACIÓN:
• Terapia individual
• Red de apoyo
• Límites saludables

📞 APOYO:
• 144 - Orientación psicológica
• 141 - Recursos
""",
        
        'violencia_economica': """
💰 VIOLENCIA ECONÓMICA

SEÑALES:
• Control total del dinero
• Impedimento para trabajar
• Dependencia forzada
• Sabotaje laboral

TUS DERECHOS:
• Autonomía económica
• Derecho a trabajar
• Acceso a recursos
• Compensación por trabajo doméstico

RECURSOS:
• Programas de empleabilidad
• Apoyo económico temporal
• Asesoría legal gratuita

📞 INFORMACIÓN:
• 144 - Orientación legal
• 141 - Programas disponibles
"""
    }
    
    respuesta = ""
    for categoria in categorias.keys():
        if categoria in CONSEJOS_CATEGORIA:
            respuesta += CONSEJOS_CATEGORIA[categoria] + "\n"
    
    return respuesta

def _generar_consejos_emocionales(emociones, patrones):
    """Genera consejos específicos según emociones detectadas"""
    consejos_por_emocion = {
        'agobio': "🌪️ Para manejar el agobio:\n• Respira profundo 3 veces\n• Haz una lista de prioridades\n• Divide tareas en pasos pequeños\n• Tómate descansos",
        'tristeza': "💙 Para la tristeza:\n• Habla con alguien de confianza\n• Sal a caminar\n• Escribe sobre tus sentimientos\n• Permite llorar si lo necesitas",
        'enojo': "🔥 Para el enojo:\n• Respira antes de hablar\n• Aléjate momentáneamente\n• Haz ejercicio\n• Expresa lo que sientes con calma",
        'miedo': "🛡️ Para el miedo:\n• Identifica qué te asusta\n• Busca un lugar seguro\n• Rodéate de personas de confianza\n• Practica relajación",
        'felicidad': "🌈 ¡Disfruta este momento!\n• Vive el presente\n• Comparte tu alegría\n• Agradece por este sentimiento\n• Mereces ser feliz",
        'confusion': "💫 Para la confusión:\n• Escribe tus opciones\n• Date tiempo para decidir\n• Pide opiniones objetivas\n• Enfócate en una cosa a la vez",
        'impotencia': "💪 Para la impotencia:\n• Enfócate en lo que sí puedes controlar\n• Metas pequeñas alcanzables\n• Celebra cada logro\n• Pide ayuda"
    }
    
    consejo = ""
    for emocion in emociones:
        if emocion in consejos_por_emocion:
            consejo = consejos_por_emocion[emocion]
            break
    
    if not consejo:
        consejo = "🌻 Estrategias de autocuidado:\n• Respira conscientemente\n• Habla con alguien de confianza\n• Haz actividad física\n• Cuida tu bienestar"
    
    consejo += "\n\n📞 Líneas de ayuda:\n• 144 - Apoyo 24/7\n• 141 - Orientación"
    
    return consejo

def _generar_respuesta_emergencia():
    """Respuesta para emergencias"""
    return """
🚨🚨 EMERGENCIA - AYUDA INMEDIATA 🚨🚨

Si estás pensando en lastimarte o estás en peligro:

📞 LLAMA AHORA:
• 911 - Emergencias
• 144 - Crisis 24/7
• Línea de la Vida: 800 911 2000
• SAPTEL: 55 5259 8121

🏥 ACCIONES INMEDIATAS:
• Ve al hospital más cercano
• Llama a un ser querido
• NO te quedes solo/a
• Habla con alguien AHORA

💖 RECUERDA:
• Tu vida es valiosa
• Este momento pasará
• Hay gente que te quiere ayudar
• Mereces sentirte mejor

Por favor, busca ayuda profesional ahora mismo.
Estoy aquí para apoyarte 💙
"""

# ==================== HANDLERS ====================
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Mensaje de bienvenida"""
    welcome_text = f"""
🌻 ¡Hola! Soy tu asistente de apoyo emocional

Puedo ayudarte a identificar 7 tipos de violencia:
🔴 Física
😔 Psicológica
🚫 Control y aislamiento
⚠️ Amenazas e intimidación
🔞 Sexual
📱 Digital/Cibernética
💔 Manipulación emocional
💰 Económica

📞 Líneas de ayuda 24/7:
• 144 - Violencia de género
• 911 - Emergencias
• 141 - Orientación
• 089 - Denuncia anónima

💬 Cómo usar:
• Escribe "analiza:" seguido del mensaje
• O cuéntame cómo te sientes

Estoy aquí para escucharte y apoyarte 💙

Versión: {analyzer.version} - Detección Completa
"""
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    user_text = message.text.strip()
    
    print(f"👤 Usuario {user_id}: {user_text}")
    
    # DETECTAR DESPEDIDAS
    despedidas = ['no gracias', 'adiós', 'chao', 'bye', 'hasta luego', 'gracias', 'listo', 'ok', 'vale', 'bueno']
    if any(desp in user_text.lower() for desp in despedidas) and len(user_text.split()) <= 3:
        respuestas_despedida = [
            "🌻 Hasta luego, cuídate mucho 💫",
            "💫 Nos vemos, estoy aquí cuando me necesites 🌷",
            "👋 ¡Hasta pronto! No dudes en escribir 💖",
            "🌟 Fue un gusto ayudarte. Cuídate ✨",
            "💕 Hasta la próxima, tu bienestar es importante 🌈"
        ]
        bot.reply_to(message, random.choice(respuestas_despedida))
        if user_id in user_context:
            del user_context[user_id]
        return
    
    # DETECTAR EMERGENCIA
    palabras_emergencia = ['suicid', 'matarme', 'acabar con todo', 'no quiero vivir', 'quiero morir']
    if any(palabra in user_text.lower() for palabra in palabras_emergencia):
        bot.reply_to(message, _generar_respuesta_emergencia())
        user_context[user_id] = {'estado': 'emergencia', 'conversacion_activa': True}
        return
    
    # ANÁLISIS EXPLÍCITO
    if 'analiza' in user_text.lower() or 'analizar' in user_text.lower():
        # Extraer texto a analizar
        texto_analizar = user_text.lower()
        for palabra in ['analiza', 'analizar', 'analyze', ':', 'este', 'mensaje']:
            texto_analizar = texto_analizar.replace(palabra, '')
        texto_analizar = texto_analizar.strip()
        
        if not texto_analizar or len(texto_analizar) < 5:
            bot.reply_to(message, "🔍 ¿Qué mensaje o situación quieres que analice?\n\nEjemplo: analiza: mi pareja me grita y me dice que soy inútil")
            return
        
        processing_msg = bot.reply_to(message, "🔍 Analizando la situación con detección completa...")
        time.sleep(1)
        
        try:
            # ANÁLISIS COMPLETO
            analysis = _analizar_completo(texto_analizar)
            
            nivel = analysis['nivel_riesgo']
            categorias = analysis['categorias_detectadas']
            
            # CONSTRUIR RESPUESTA
            if nivel == 'emergencia':
                respuesta = _generar_respuesta_emergencia()
                user_context[user_id] = {'estado': 'emergencia', 'conversacion_activa': True}
                
            elif nivel == 'alto':
                respuesta = "🔴 ANÁLISIS: RIESGO ALTO\n\n"
                respuesta += f"Se detectaron {len(categorias)} categoría(s) de violencia:\n\n"
                
                for cat, info in categorias.items():
                    nombre = cat.replace('_', ' ').title()
                    respuesta += f"{info['icono']} {nombre}\n"
                
                respuesta += "\n⚠️ ESTA ES UNA SITUACIÓN GRAVE\n\n"
                respuesta += "📞 BUSCA AYUDA INMEDIATA:\n"
                respuesta += "• 911 - Emergencias\n"
                respuesta += "• 144 - Violencia 24/7\n"
                respuesta += "• 141 - Orientación\n\n"
                respuesta += _generar_consejos_categoria(categorias)
                respuesta += "\n¿Estás en un lugar seguro ahora?"
                
                user_context[user_id] = {
                    'estado': 'alto_riesgo',
                    'categorias': categorias,
                    'conversacion_activa': True
                }
                
            elif nivel == 'moderado':
                respuesta = "🟡 ANÁLISIS: RIESGO MODERADO\n\n"
                respuesta += f"Se detectaron {len(categorias)} categoría(s):\n\n"
                
                for cat, info in categorias.items():
                    nombre = cat.replace('_', ' ').title()
                    respuesta += f"{info['icono']} {nombre}\n"
                
                respuesta += "\n⚠️ Estos patrones pueden escalar con el tiempo.\n\n"
                respuesta += _generar_consejos_categoria(categorias)
                respuesta += "\n¿Cómo te hace sentir esta situación?"
                
                user_context[user_id] = {
                    'estado': 'moderado_riesgo',
                    'categorias': categorias,
                    'conversacion_activa': True
                }
                
            else:
                respuesta = "🟢 ANÁLISIS: SIN SEÑALES CLARAS\n\n"
                respuesta += "No detecté patrones específicos de violencia en el mensaje.\n\n"
                respuesta += "Esto no significa que tu preocupación no sea válida.\n\n"
                respuesta += "Si algo te incomoda o preocupa, confía en tu intuición.\n\n"
                respuesta += "¿Hay algo específico que te genere malestar?"
                
                user_context[user_id] = {
                    'estado': 'sin_riesgo',
                    'conversacion_activa': True
                }
            
            bot.edit_message_text(
                respuesta,
                chat_id=message.chat.id,
                message_id=processing_msg.message_id
            )
            
        except Exception as e:
            print(f"❌ Error en análisis: {e}")
            bot.edit_message_text(
                "❌ Hubo un error al analizar. Por favor, intenta de nuevo o escribe 'ayuda' para más opciones.",
                chat_id=message.chat.id,
                message_id=processing_msg.message_id
            )
        return
    
    # DETECCIÓN AUTOMÁTICA DE EMOCIONES
    elif len(user_text) > 10 and user_id not in user_context:
        try:
            # Intentar análisis emocional primero
            emociones_analysis = analyzer.analyze_emotions_spanish(user_text)
            
            if emociones_analysis['emociones']:
                emociones_text = ', '.join(emociones_analysis['emociones'])
                
                # Respuesta especial para felicidad
                if 'felicidad' in emociones_analysis['emociones'] and len(emociones_analysis['emociones']) == 1:
                    respuesta = "🌈 ¡Qué alegría que te sientas feliz!\n\n"
                    respuesta += "Me encanta saber que estás bien. Disfruta este momento y recuerda que mereces ser feliz siempre.\n\n"
                    respuesta += "¿Quieres contarme qué te tiene tan contenta?"
                else:
                    respuesta = f"💭 Noto que te sientes {emociones_text}...\n\n"
                    respuesta += _generar_consejos_emocionales(
                        emociones_analysis['emociones'],
                        {}
                    )
                    respuesta += "\n\n¿Quieres contarme más sobre lo que está pasando?"
                
                bot.reply_to(message, respuesta)
                user_context[user_id] = {
                    'estado': 'emocional',
                    'emociones': emociones_analysis['emociones'],
                    'conversacion_activa': True
                }
                return
                
        except Exception as e:
            print(f"❌ Error en análisis emocional: {e}")
    
    # CONVERSACIÓN CONTINUA
    if user_id in user_context:
        contexto = user_context[user_id]
        estado_actual = contexto.get('estado')
        
        print(f"🔍 Estado actual: {estado_actual}")
        
        # DETECTAR PETICIONES DE AYUDA
        if any(palabra in user_text.lower() for palabra in ['ayuda', 'help', 'socorro', 'auxilio']):
            if estado_actual in ['emergencia', 'alto_riesgo']:
                respuesta = "🚨 AYUDA INMEDIATA DISPONIBLE:\n\n"
                respuesta += "📞 LLAMA AHORA:\n"
                respuesta += "• 911 - Emergencias\n"
                respuesta += "• 144 - Crisis 24/7\n"
                respuesta += "• Línea de la Vida: 800 911 2000\n\n"
                respuesta += "🏥 Ve al hospital más cercano\n"
                respuesta += "👥 Contacta a un ser querido\n"
                respuesta += "🚫 NO te quedes solo/a\n\n"
                respuesta += "Tu seguridad es lo más importante 💖"
            else:
                respuesta = "🌻 Estoy aquí para ayudarte.\n\n"
                respuesta += "Puedo:\n"
                respuesta += "• Analizar mensajes o situaciones\n"
                respuesta += "• Darte consejos prácticos\n"
                respuesta += "• Informarte sobre recursos\n"
                respuesta += "• Escucharte y apoyarte\n\n"
                respuesta += "📞 Líneas de ayuda:\n"
                respuesta += "• 144 - Violencia 24/7\n"
                respuesta += "• 141 - Orientación\n"
                respuesta += "• 911 - Emergencias\n\n"
                respuesta += "¿En qué específicamente necesitas ayuda?"
            
            bot.reply_to(message, respuesta)
            return
        
        # ANÁLISIS DE EMOCIONES EN LA RESPUESTA
        try:
            emociones_analysis = analyzer.analyze_emotions_spanish(user_text)
            emociones_detectadas = emociones_analysis['emociones']
        except:
            emociones_detectadas = []
        
        # DAR CONSEJOS Y CERRAR SI HAY EMOCIONES
        if emociones_detectadas:
            if 'felicidad' in emociones_detectadas and len(emociones_detectadas) == 1:
                respuesta = "🌈 ¡Me alegra que sigas feliz!\n\n"
                respuesta += "Sigue disfrutando este momento. La felicidad es un derecho que todos merecemos.\n\n"
                respuesta += "💫 ¡Que tengas un día maravilloso!"
            else:
                consejos = _generar_consejos_emocionales(
                    emociones_detectadas,
                    contexto.get('categorias', {})
                )
                respuesta = consejos
                respuesta += "\n\n💫 Espero que estos consejos te sean útiles. Estoy aquí si necesitas más apoyo."
            
            bot.reply_to(message, respuesta)
            del user_context[user_id]
            return
        
        # MANEJO POR ESTADO
        if estado_actual == 'emergencia':
            respuesta = "💙 ¿Lograste contactar ayuda?\n\n"
            respuesta += "Por favor, es importante que hables con alguien:\n\n"
            respuesta += "📞 Líneas 24/7:\n"
            respuesta += "• 911 - Emergencias\n"
            respuesta += "• 144 - Crisis emocional\n"
            respuesta += "• Línea de la Vida: 800 911 2000\n\n"
            respuesta += "No estás solo/a. Hay gente que quiere ayudarte 💖"
            bot.reply_to(message, respuesta)
            
        elif estado_actual == 'alto_riesgo':
            if any(palabra in user_text.lower() for palabra in ['sí', 'si', 'estoy bien', 'estoy segur']):
                respuesta = "💙 Me alegra que estés en un lugar seguro.\n\n"
                respuesta += "Es importante que consideres buscar ayuda profesional:\n\n"
                respuesta += _generar_consejos_categoria(contexto.get('categorias', {}))
                respuesta += "\n¿Hay algo más en lo que pueda apoyarte?"
            else:
                respuesta = "🚨 Tu seguridad es prioritaria.\n\n"
                respuesta += "Si no estás segura, por favor:\n"
                respuesta += "• Busca un lugar seguro\n"
                respuesta += "• Contacta a alguien de confianza\n"
                respuesta += "• Llama a las líneas de ayuda\n\n"
                respuesta += "📞 144 - Ayuda inmediata 24/7\n"
                respuesta += "📞 911 - Emergencias\n\n"
                respuesta += "¿Necesitas información sobre refugios o recursos?"
            
            bot.reply_to(message, respuesta)
            
        elif estado_actual == 'moderado_riesgo':
            if any(palabra in user_text.lower() for palabra in ['sí', 'si', 'claro', 'me preocupa']):
                respuesta = "💬 Entiendo tu preocupación.\n\n"
                respuesta += _generar_consejos_categoria(contexto.get('categorias', {}))
                respuesta += "\n¿Quieres hablar sobre algo específico?"
            else:
                respuesta = "🌻 Recuerda que mereces relaciones respetuosas y saludables.\n\n"
                respuesta += "Si las cosas empeoran, no dudes en buscar ayuda.\n\n"
                respuesta += "📞 Líneas disponibles:\n"
                respuesta += "• 144 - Orientación 24/7\n"
                respuesta += "• 141 - Recursos\n\n"
                respuesta += "💫 Cuídate mucho"
                del user_context[user_id]
            
            bot.reply_to(message, respuesta)
            
        elif estado_actual == 'emocional':
            respuesta = "💬 Gracias por compartir.\n\n"
            respuesta += "Recuerda cuidar de tu bienestar emocional. "
            respuesta += "No dudes en pedir ayuda cuando lo necesites.\n\n"
            respuesta += "📞 Líneas de apoyo:\n"
            respuesta += "• 144 - Apoyo emocional\n"
            respuesta += "• 141 - Orientación\n\n"
            respuesta += "💫 Estoy aquí si me necesitas"
            
            bot.reply_to(message, respuesta)
            del user_context[user_id]
            
        else:
            respuesta = "🌻 ¿En qué puedo ayudarte?\n\n"
            respuesta += "Puedes:\n"
            respuesta += "• Pedirme que analice una situación\n"
            respuesta += "• Contarme cómo te sientes\n"
            respuesta += "• Preguntarme sobre recursos\n\n"
            respuesta += "Escribe 'analiza:' seguido del mensaje que quieres revisar."
            
            bot.reply_to(message, respuesta)
            
    # MENSAJE INICIAL
    else:
        mensajes_inicio = [
            "💬 Hola, ¿cómo estás? Estoy aquí para escucharte",
            "🌻 ¡Hola! ¿En qué puedo acompañarte hoy?",
            "👋 Hola, cuéntame ¿qué tal tu día?",
            "💫 ¡Hola! ¿Quieres conversar sobre algo?",
            "🌸 Hola, estoy aquí para apoyarte. ¿Cómo te sientes?"
        ]
        bot.reply_to(message, random.choice(mensajes_inicio))

# ==================== INICIAR BOT ====================
if __name__ == "__main__":
    print("✅ Bot listo - Detección completa de 7 categorías")
    print("📋 Categorías monitoreadas:")
    for categoria in PATRONES_VIOLENCIA.keys():
        print(f"   • {categoria.replace('_', ' ').title()}")
    bot.polling()
                