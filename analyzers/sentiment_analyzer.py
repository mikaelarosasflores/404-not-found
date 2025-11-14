"""
ANALIZADOR DE DETECCIÓN DE VIOLENCIA CON TRANSFORMERS - VERSIÓN FINAL OPTIMIZADA
Integra análisis de sentimientos con IA y detección de 7 categorías de violencia
"""

import os
from dotenv import load_dotenv
from transformers import pipeline
import re
from typing import Dict, List, Any
import warnings

warnings.filterwarnings('ignore')
load_dotenv()

class SecurityAnalyzer:
    def __init__(self):
        self.version = "v5.0 - Análisis Completo con IA y 7 Categorías"
        print("🔄 Inicializando SecurityAnalyzer...")
        
        self._initialize_patterns()
        self._initialize_severity_system()
        self._initialize_emotional_patterns()
        self._initialize_ai_models()
        
        print("✅ SecurityAnalyzer listo para el bot")
    
    def _initialize_ai_models(self):
        """Inicializa modelos de Transformers optimizados para español"""
        try:
            print("🤖 Cargando modelos de IA...")
            
            # Modelo principal de sentimientos en español
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="pysentimiento/robertuito-sentiment-analysis",
                tokenizer="pysentimiento/robertuito-sentiment-analysis"
            )
            
            # Modelo alternativo de emociones (más detallado)
            try:
                self.emotion_analyzer = pipeline(
                    "text-classification",
                    model="finiteautomata/beto-emotion-analysis",
                    tokenizer="finiteautomata/beto-emotion-analysis",
                    top_k=None
                )
                print("✅ Modelo de emociones cargado")
            except:
                self.emotion_analyzer = None
                print("⚠️ Modelo de emociones no disponible, usando análisis basado en reglas")
            
            self.ai_models_loaded = True
            print("✅ Modelos de IA cargados exitosamente")
            
        except Exception as e:
            print(f"⚠️ No se pudieron cargar los modelos de IA: {e}")
            print("⚠️ Se usará análisis basado en reglas (funcional pero menos preciso)")
            self.sentiment_analyzer = None
            self.emotion_analyzer = None
            self.ai_models_loaded = False

    def _initialize_patterns(self):
        """7 CATEGORÍAS DE VIOLENCIA - PATRONES EXPANDIDOS Y OPTIMIZADOS"""
        self.patterns = {
            "violencia_fisica": [
                # Acciones directas
                "golpe", "pega", "pegó", "golpeó", "golpearme", "pegarme", "me pegó", 
                "me golpeó", "me pego", "me golpeo", "empujar", "empujó", "patear", "pateó",
                "abofetear", "cachetada", "puñetazo", "zarandear", "maltratar", "abusar",
                # Acciones físicas específicas
                "lastimar", "jalar", "jalón", "pellizcar", "ahogar", "quemar", "tirar del pelo",
                "agredir", "agredió", "lastimó", "maltrato físico", "me jala", "me empujó",
                "me pateó", "me arañó", "me mordió", "me zarandeó",
                # Evidencias físicas
                "moretones", "moretón", "marcas", "heridas", "sangre", "golpes", "lesiones",
                "me dejó marca", "me lastimó físicamente", "violencia física",
                # Contexto y amenazas físicas
                "me puso la mano encima", "levantó la mano", "cerró el puño",
                "tiró objetos", "rompió cosas", "aventó cosas"
            ],
            
            "violencia_psicologica": [
                # Insultos y descalificaciones
                "te odio", "odio", "eres un", "eres una", "no sirves", "estúpido", "estúpida",
                "inútil", "no vales", "das lástima", "loco", "loca", "idiota", "imbécil",
                "pendejo", "pendeja", "tonta", "tonto", "fracasado", "fracasada",
                # Humillación y menosprecio
                "humillación", "insulta", "ofende", "menospreciar", "ridiculizar", "burla",
                "ningunear", "despreciar", "criticar constantemente", "denigrar",
                "me hace sentir mal", "me humilla", "me grita", "me hace sentir poca cosa",
                # Manipulación psicológica
                "gaslighting", "hacerte dudar", "exagerada", "exagerado", "manipula",
                "loca", "histérica", "paranoica", "no pasó", "te lo inventas",
                "nunca dije eso", "estás imaginando cosas",
                # Crítica destructiva
                "nunca haces nada bien", "todo lo haces mal", "eres un fracaso",
                "no eres suficiente", "nadie te va a querer", "eres lo peor",
                "me arrepiento de", "fuiste un error", "no deberías haber nacido"
            ],
            
            "control_aislamiento": [
                # Prohibiciones y restricciones
                "no me deja", "no me permite", "prohibe", "prohíbe", "no salgas",
                "no veas a", "no hables con", "aléjate de", "no te juntes",
                # Control y vigilancia
                "controla", "vigila", "celos", "celoso", "celosa", "me controla",
                "me vigila", "me espía", "me persigue", "me sigue",
                # Interrogatorios
                "dónde vas", "con quién estás", "qué haces", "dónde estás",
                "con quién hablas", "quién te llamó", "quién te escribió",
                # Control digital
                "revisa mi", "revisa tus", "revisa el", "celular", "teléfono",
                "redes sociales", "contraseñas", "chats", "mensajes", "whatsapp",
                "me revisa el celular", "exige mis contraseñas", "quiere mis claves",
                # Aislamiento social
                "controla mis amistades", "no me deja ver a mi familia",
                "me aleja de", "me aisla", "no quiere que salga",
                "prohíbe trabajar", "no me deja estudiar", "me mantiene encerrada",
                # Control de actividades
                "exige", "obliga", "controla todas mis", "no me deja salir",
                "controla con quién hablo", "no me deja tener amigos",
                "tiene que saber todo", "reportarme constantemente"
            ],
            
            "amenazas_acoso": [
                # Amenazas directas de violencia
                "te voy a matar", "matar", "matarte", "acabar contigo", "lastimar",
                "dañar", "hacerte daño", "te voy a pegar", "te voy a golpear",
                # Amenazas de suicidio
                "suicid", "me voy a matar", "me mato", "me suicido", "me quito la vida",
                "si me dejas me mato", "por tu culpa me voy a matar",
                # Amenazas psicológicas
                "vas a pagar", "me las vas a pagar", "te juro que", "vas a ver",
                "te arrepentirás", "no sabes de lo que soy capaz",
                # Acoso y persecución
                "te busco", "ir a tu casa", "sé dónde vives", "sé dónde trabajas",
                "perseguir", "acosar", "hostigar", "estar pendiente", "vigilar",
                "esperar afuera", "seguirte", "te voy a encontrar", "no te vas a escapar",
                # Comunicación obsesiva
                "llamadas constantes", "mensajes obsesivos", "bombardeo de mensajes",
                "aparecer sin avisar", "controlar horarios", "aparece en todos lados",
                # Amenazas indirectas
                "amenaza", "amenazó", "muerte", "peligro", "consecuencias graves",
                "te vas a arrepentir", "esto no se queda así"
            ],
            
            "violencia_digital": [
                # Dispositivos y plataformas
                "celular", "teléfono", "móvil", "smartphone", "whatsapp", "telegram",
                "instagram", "facebook", "twitter", "tiktok", "redes sociales",
                # Control de cuentas
                "chats", "mensajes", "conversaciones", "contraseñas", "claves", "passwords",
                "acceso a tu", "acceso a mis", "hackear", "cuentas", "perfiles",
                "controla todas mis cuentas", "exige las contraseñas",
                # Vigilancia digital
                "vigilar redes", "controlar internet", "revisar mensajes", "espiar chats",
                "controlar redes", "stalkear", "revisa mis conversaciones",
                "revisa mi historial", "controla mis redes", "monitorea",
                # Manipulación de contenido
                "fotos", "videos", "publicar", "subir fotos", "compartir fotos",
                "etiquetar", "difundir", "distribuir", "fotos íntimas",
                "contenido sexual", "revenge porn", "pornografía venganza",
                # Ubicación y rastreo
                "ubicación", "localización", "gps", "rastreador", "localizador",
                "encuentra mi", "compartir ubicación", "online", "última conexión",
                # Software malicioso
                "spyware", "keylogger", "aplicaciones espía", "software de control",
                # Bloqueos y restricciones
                "bloquear", "eliminar", "borrar", "desactivar cuentas"
            ],
            
            "manipulacion_emocional": [
                # Dependencia emocional
                "sin mí no eres nada", "nadie te va a querer", "nadie más te aguanta",
                "no vas a encontrar a nadie más", "eres mía", "me perteneces",
                # Chantaje emocional
                "me debes", "chantaje", "si no haces", "te voy a dejar",
                "si me quisieras", "si me amaras", "demuéstrame que",
                # Victimización
                "me muero sin ti", "me haces esto", "por mi culpa es infeliz",
                "me haces sufrir", "victimizarse", "hacerte sentir mal",
                "soy tu única razón", "razón de vivir", "todo lo que hago es por ti",
                # Culpabilización
                "por tu culpa", "culpable", "es tu culpa", "tú me obligas",
                "me haces hacer esto", "me obligas a", "tú provocas",
                "me haces enojar", "me sacas de mis casillas",
                # Descalificación emocional
                "desagradecido", "desagradecida", "ingrato", "ingrata",
                "eres egoísta", "no piensas en mí", "solo piensas en ti",
                # Presión y coerción
                "obligar", "presionar", "manipula", "me manipula",
                "me hace sentir culpable", "me presiona", "me obliga",
                # Justificaciones tóxicas
                "es por tu bien", "lo hago porque te quiero", "es para cuidarte",
                "nadie te va a cuidar como yo", "solo yo te entiendo",
                # Ciclos de abuso
                "love bombing", "bombardeo de amor", "promete cambiar",
                "va a ser diferente", "no va a volver a pasar", "perdóname"
            ],
            
            "violencia_economica": [
                # Control financiero
                "dinero", "sueldo", "salario", "ingresos", "quincena", "pago",
                "controla el dinero", "controla mi sueldo", "me quita el dinero",
                "me quita mi sueldo", "administra todo el dinero",
                # Restricciones económicas
                "no te doy dinero", "no me da dinero", "no me da para gastos",
                "gastas mucho", "justifica gastos", "justificar cada centavo",
                "explica cada peso", "pide facturas", "revisa mis compras",
                # Control de cuentas
                "cuentas", "tarjetas", "débito", "crédito", "banco", "cajero",
                "controla mis cuentas", "quitar tarjetas", "bloquea tarjetas",
                "retira dinero sin permiso", "usa mi tarjeta sin permiso",
                # Impedimento laboral
                "no me deja trabajar", "prohibir trabajar", "sabotea mi trabajo",
                "prohíbe trabajar", "no me permite trabajar", "me hace renunciar",
                "boicotea mis entrevistas", "no me deja estudiar",
                # Dependencia económica
                "dependes de mí", "te mantengo", "yo pago todo", "sin mí no tienes",
                "dependo económicamente", "no tengo dinero propio",
                "no puedo trabajar", "me mantiene sin dinero",
                # Presupuesto y gastos
                "presupuesto", "ahorros", "gastos", "compras", "facturas",
                "controla mis gastos", "aprueba mis compras",
                # Extorsión y deudas
                "obligar a trabajar", "extorsión económica", "deudas forzadas",
                "deudas a mi nombre", "firma documentos", "firma préstamos",
                "vende mis cosas", "empeña", "saca créditos"
            ]
        }

    def _initialize_severity_system(self):
        """Sistema de severidad OPTIMIZADO con palabras clave específicas"""
        self.severity_keywords = {
            "emergencia": [
                # Riesgo inmediato de vida
                "suicid", "matarme", "quitarme la vida", "acabar con todo",
                "no quiero vivir", "quiero morir", "me voy a matar",
                # Violencia física grave actual
                "me está pegando", "me está golpeando", "estoy sangrando",
                "tengo miedo de morir", "va a matarme", "me va a matar ahora"
            ],
            
            "alto": [
                # Violencia física
                "golpe", "pega", "pegó", "golpeó", "golpearme", "pegarme", "me pegó",
                "me golpeó", "patear", "pateó", "abofetear", "puñetazo", "cachetada",
                "me lastimó", "me hirió", "sangre", "moretones", "heridas",
                # Amenazas graves
                "te voy a matar", "matar", "matarte", "lastimar", "dañar",
                "acabar contigo", "hacerte daño", "muerte", "peligro de muerte",
                # Violencia sexual
                "violó", "violación", "abuso sexual", "me forzó", "me obligó sexualmente",
                "agresión sexual", "violencia sexual",
                # Situaciones de peligro
                "tengo miedo", "me da miedo", "tengo mucho miedo", "terror",
                "estoy aterrada", "amenaza con arma", "tiene un arma"
            ],
            
            "moderado": [
                # Control y aislamiento
                "no me deja", "controla", "vigila", "celos excesivos", "prohíbe",
                "me aisla", "no puedo salir", "no puedo ver a nadie",
                # Violencia psicológica
                "te odio", "inútil", "no sirves", "no vales", "eres un fracaso",
                "humillación", "insulta", "menosprecia", "me grita todo el tiempo",
                # Amenazas
                "amenaza", "amenazó", "me amenaza con", "chantaje",
                # Persecución
                "perseguir", "acosar", "hostigar", "me sigue", "me espía",
                # Control digital
                "revisa mi celular", "espía mis mensajes", "controla mis redes",
                "hackea mis cuentas", "publicó fotos sin permiso",
                # Manipulación
                "manipula", "me hace sentir culpable", "chantaje emocional",
                "sin mí no eres nada", "nadie te va a querer",
                # Control económico
                "controla mi dinero", "no me da dinero", "me quita el sueldo",
                "no me deja trabajar", "dependo económicamente"
            ],
            
            "leve": [
                # Señales tempranas
                "celos", "revisa", "pregunta mucho", "quiere saber todo",
                "mensajes constantes", "llama mucho",
                # Control suave
                "celular", "redes sociales", "contraseñas", "ubicación",
                # Presión económica
                "dinero", "gastos", "justificar", "explica tus compras",
                # Comentarios negativos
                "crítica", "se burla a veces", "hace comentarios"
            ]
        }

    def _initialize_emotional_patterns(self):
        """Patrones emocionales COMPLETOS Y EXPANDIDOS"""
        self.emociones_espanol = {
            'tristeza': [
                'triste', 'tristeza', 'deprimida', 'deprimido', 'depresión',
                'apenada', 'apenado', 'desanimada', 'desanimado', 'desánimo',
                'desesperada', 'desesperado', 'desesperación', 'desolada', 'desolado',
                'melancólica', 'melancólico', 'melancolía', 'afligida', 'afligido',
                'desconsolada', 'desconsolado', 'infeliz', 'desdichada', 'desdichado',
                'desesperanzada', 'desesperanzado', 'abatida', 'abatido', 'decaída', 'decaído',
                'llorar', 'lloro', 'lágrimas', 'llorando', 'sollozar'
            ],
            
            'enojo': [
                'enojada', 'enojado', 'enojo', 'enfadada', 'enfadado', 'enfado',
                'molesta', 'molesto', 'furia', 'rabia', 'furioso', 'furiosa',
                'indignada', 'indignado', 'indignación', 'irritada', 'irritado',
                'colérica', 'colérico', 'cólera', 'airada', 'airado', 'ira',
                'frustrada', 'frustrado', 'frustración', 'harto', 'harta', 'hartazgo',
                'enfurecida', 'enfurecido', 'exasperada', 'exasperado', 'rabioso', 'rabiosa'
            ],
            
            'miedo': [
                'asustada', 'asustado', 'miedo', 'temerosa', 'temeroso', 'temor',
                'atemorizada', 'atemorizado', 'aterrada', 'aterrado', 'terror',
                'espantada', 'espantado', 'nerviosa', 'nervioso', 'nervios',
                'ansiosa', 'ansioso', 'ansiedad', 'angustia', 'angustiada', 'angustiado',
                'preocupada', 'preocupado', 'preocupación', 'intranquila', 'intranquilo',
                'amedrentada', 'amedrentado', 'pánico', 'pavor', 'espanto',
                'inquieta', 'inquieto', 'alarmada', 'alarmado'
            ],
            
            'felicidad': [
                'feliz', 'felicidad', 'contenta', 'contento', 'alegre', 'alegría',
                'emocionada', 'emocionado', 'entusiasmada', 'entusiasmado', 'entusiasmo',
                'optimista', 'esperanzada', 'esperanzado', 'esperanza',
                'eufórica', 'eufórico', 'euforia', 'radiante', 'jubilosa', 'jubiloso',
                'satisfecha', 'satisfecho', 'plena', 'pleno', 'plenitud',
                'dichosa', 'dichoso', 'animada', 'animado', 'gozosa', 'gozoso',
                'bien', 'genial', 'fantástico', 'maravilloso', 'excelente', 'increíble'
            ],
            
            'soledad': [
                'sola', 'solo', 'soledad', 'aislada', 'aislado', 'aislamiento',
                'abandonada', 'abandonado', 'abandono', 'desamparada', 'desamparado',
                'incomprendida', 'incomprendido', 'desprotegida', 'desprotegido',
                'excluida', 'excluido', 'marginada', 'marginado', 'rechazada', 'rechazado'
            ],
            
            'agobio': [
                'agobiada', 'agobiado', 'agobio', 'estresada', 'estresado', 'estrés',
                'sobrecargada', 'sobrecargado', 'abrumada', 'abrumado',
                'presionada', 'presionado', 'presión', 'angustiada', 'angustiado',
                'agotada', 'agotado', 'agotamiento', 'exhausta', 'exhausto',
                'saturada', 'saturado', 'colapsada', 'colapsado', 'desbordada', 'desbordado',
                'no puedo más', 'es demasiado', 'es mucho'
            ],
            
            'confusion': [
                'confundida', 'confundido', 'confusión', 'desorientada', 'desorientado',
                'perdida', 'perdido', 'desconcertada', 'desconcertado', 'desconcierto',
                'despistada', 'despistado', 'aturdida', 'aturdido', 'aturdimiento',
                'dudosa', 'dudoso', 'dudas', 'indecisa', 'indeciso', 'indecisión',
                'no sé qué hacer', 'no entiendo', 'no comprendo'
            ],
            
            'frustracion': [
                'frustrada', 'frustrado', 'frustración', 'desilusionada', 'desilusionado',
                'decepcionada', 'decepcionado', 'decepción', 'desalentada', 'desalentado',
                'desencantada', 'desencantado', 'desmoralizada', 'desmoralizado',
                'desanimada', 'desanimado'
            ],
            
            'impotencia': [
                'impotente', 'impotencia', 'indefensa', 'indefenso', 'desvalida', 'desvalido',
                'incapaz', 'inútil', 'incompetente', 'desesperanza', 'sin poder',
                'atrapada', 'atrapado', 'sin salida', 'sin opciones', 'vulnerable',
                'débil', 'sometida', 'sometido', 'dominada', 'dominado'
            ],
            
            'culpa': [
                'culpable', 'culpa', 'arrepentida', 'arrepentido', 'arrepentimiento',
                'remordimiento', 'penitente', 'autocrítica', 'autocrítico',
                'me siento mal', 'es mi culpa', 'yo tengo la culpa'
            ],
            
            'vergüenza': [
                'vergüenza', 'avergonzada', 'avergonzado', 'pena', 'bochorno',
                'humillada', 'humillado', 'mortificada', 'mortificado',
                'apenada', 'apenado', 'ruborizada', 'ruborizado'
            ],
            
            'ansiedad': [
                'ansiosa', 'ansioso', 'ansiedad', 'nervios', 'nerviosa', 'nervioso',
                'tensa', 'tenso', 'tensión', 'inquieta', 'inquieto', 'inquietud',
                'alterada', 'alterado', 'intranquila', 'intranquilo'
            ],
            
            'esperanza': [
                'esperanza', 'esperanzada', 'esperanzado', 'optimista', 'optimismo',
                'confiada', 'confiado', 'ilusionada', 'ilusionado', 'ilusión',
                'animada', 'animado', 'motivada', 'motivado'
            ]
        }

    def _analyze_with_ai(self, text):
        """Análisis emocional avanzado con Transformers"""
        if not self.ai_models_loaded or len(text) < 5:
            return None
        
        try:
            ai_analysis = {}
            
            # Análisis de sentimiento (positivo/negativo/neutral)
            if self.sentiment_analyzer:
                try:
                    sentiment_result = self.sentiment_analyzer(text[:512])[0]
                    ai_analysis['sentimiento'] = {
                        'etiqueta': sentiment_result['label'],
                        'confianza': round(sentiment_result['score'], 3)
                    }
                except Exception as e:
                    print(f"⚠️ Error en análisis de sentimiento: {e}")
            
            # Análisis de emociones específicas (si está disponible)
            if self.emotion_analyzer:
                try:
                    emotion_results = self.emotion_analyzer(text[:512])
                    if emotion_results and len(emotion_results) > 0:
                        # Tomar las top 3 emociones
                        top_emotions = sorted(
                            emotion_results[0],
                            key=lambda x: x['score'],
                            reverse=True
                        )[:3]
                        
                        ai_analysis['emociones_ia'] = [
                            {
                                'emocion': em['label'],
                                'confianza': round(em['score'], 3)
                            }
                            for em in top_emotions if em['score'] > 0.1
                        ]
                except Exception as e:
                    print(f"⚠️ Error en análisis de emociones: {e}")
            
            # Análisis basado en reglas (siempre ejecutar)
            emociones_detectadas = self._analizar_emociones_espanol(text)
            ai_analysis['emociones_reglas'] = emociones_detectadas
            
            # Combinar ambos análisis
            emociones_finales = list(set(emociones_detectadas))
            if 'emociones_ia' in ai_analysis:
                for em_ia in ai_analysis['emociones_ia']:
                    emocion_esp = self._mapear_emocion_ia(em_ia['emocion'])
                    if emocion_esp and emocion_esp not in emociones_finales:
                        if em_ia['confianza'] > 0.5:
                            emociones_finales.append(emocion_esp)
            
            ai_analysis['emociones_combinadas'] = emociones_finales
            
            return ai_analysis
            
        except Exception as e:
            print(f"❌ Error en análisis IA: {e}")
            return None

    def _mapear_emocion_ia(self, emocion_ia):
        """Mapea emociones del modelo IA a nuestras categorías"""
        mapeo = {
            'joy': 'felicidad',
            'sadness': 'tristeza',
            'anger': 'enojo',
            'fear': 'miedo',
            'surprise': 'confusion',
            'disgust': 'enojo',
            'trust': 'esperanza',
            'anticipation': 'esperanza',
            'positive': 'felicidad',
            'negative': 'tristeza',
            'neutral': None
        }
        return mapeo.get(emocion_ia.lower())

    def _analizar_emociones_espanol(self, text):
        """DETECCIÓN COMPLETA DE EMOCIONES EN ESPAÑOL con análisis de contexto"""
        text_lower = text.lower()
        emociones_detectadas = []
        scores = {}
        
        for emocion, palabras in self.emociones_espanol.items():
            matches = 0
            for palabra in palabras:
                if palabra in text_lower:
                    matches += 1
            
            if matches > 0:
                # Calcular score basado en frecuencia
                score = min(matches * 0.4, 1.0)
                scores[emocion] = score
                emociones_detectadas.append(emocion)
        
        # Ordenar por score y tomar las top 3
        if scores:
            emociones_ordenadas = sorted(
                scores.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
            emociones_detectadas = [em[0] for em in emociones_ordenadas]
        
        return emociones_detectadas

    def analyze_message(self, text):
        """
        Análisis principal MEJORADO con IA
        
        Returns:
            dict: Análisis completo con patrones, riesgo, IA y recomendaciones
        """
        if not text or not isinstance(text, str):
            return self._empty_analysis()
        
        text_lower = text.lower().strip()
        
        # Análisis con IA (si está disponible)
        ai_analysis = self._analyze_with_ai(text_lower)
        
        # Detección de patrones de violencia
        detected_patterns = self._detect_patterns_intelligent(text_lower)
        
        # Cálculo de severidad mejorado
        severity_level = self._calculate_severity_improved(text_lower, detected_patterns)
        
        # Generar respuesta contextual
        response = self._generate_contextual_response_improved(
            severity_level, 
            detected_patterns, 
            ai_analysis
        )
        
        # Análisis emocional
        emotional_analysis = self.analyze_emotions_spanish(text)
        
        return {
            "patrones_detectados": detected_patterns,
            "nivel_riesgo": severity_level,
            "respuesta_recomendada": response,
            "ai_analysis": ai_analysis,
            "analisis_emocional": emotional_analysis,
            "timestamp": self._get_timestamp()
        }

    def _detect_patterns_intelligent(self, text):
        """Detección inteligente de patrones con scoring"""
        detected = {}
        
        for category, keywords in self.patterns.items():
            matches_found = []
            score = 0
            
            for keyword in keywords:
                if keyword in text:
                    matches_found.append(keyword)
                    # Dar más peso a palabras más específicas
                    score += len(keyword.split())
            
            if matches_found:
                detected[category] = {
                    'palabras': matches_found,
                    'score': score,
                    'cantidad': len(matches_found)
                }
        
        return detected

    def _calculate_severity_improved(self, text, patterns):
        """Cálculo de severidad MEJORADO con múltiples niveles"""
        
        # NIVEL EMERGENCIA - Riesgo inmediato de vida
        for palabra in self.severity_keywords["emergencia"]:
            if palabra in text:
                return "emergencia"
        
        # Si no hay patrones, verificar emociones fuertes
        if not patterns:
            emociones_fuertes = ['miedo', 'enojo', 'tristeza', 'agobio', 'impotencia']
            emociones_detectadas = self._analizar_emociones_espanol(text)
            
            if any(emocion in emociones_fuertes for emocion in emociones_detectadas):
                return "leve"
            return "ninguno"
        
        # NIVEL ALTO - Violencia física, sexual o amenazas graves
        categorias_alto_riesgo = [
            "violencia_fisica", 
            "amenazas_acoso", 
            "violencia_sexual"
        ]
        
        if any(cat in patterns for cat in categorias_alto_riesgo):
            return "alto"
        
        # Verificar palabras clave de alto riesgo
        if any(word in text for word in self.severity_keywords["alto"]):
            return "alto"
        
        # NIVEL ALTO - Múltiples categorías (3 o más)
        if len(patterns) >= 3:
            return "alto"
        
        # NIVEL MODERADO - Combinaciones específicas peligrosas
        combinaciones_moderadas = [
            ("control_aislamiento", "manipulacion_emocional"),
            ("control_aislamiento", "violencia_economica"),
            ("violencia_psicologica", "manipulacion_emocional"),
            ("violencia_digital", "control_aislamiento")
        ]
        
        for comb in combinaciones_moderadas:
            if all(cat in patterns for cat in comb):
                return "moderado"
        
        # NIVEL MODERADO - 2 o más categorías
        if len(patterns) >= 2:
            return "moderado"
        
        # NIVEL MODERADO - Palabras clave específicas
        if any(word in text for word in self.severity_keywords["moderado"]):
            return "moderado"
        
        # NIVEL LEVE - Un solo patrón o señales tempranas
        if patterns:
            return "leve"
        
        return "ninguno"

    def _generate_contextual_response_improved(self, severity, patterns, ai_analysis=None):
        """Respuestas contextuales MEJORADAS con IA y líneas de ayuda"""
        
        # NIVEL EMERGENCIA
        if severity == "emergencia":
            respuesta = "🚨🚨 EMERGENCIA - NECESITAS AYUDA INMEDIATA 🚨🚨\n\n"
            respuesta += "Si estás pensando en lastimarte o estás en peligro inminente:\n\n"
            respuesta += "📞 LLAMA AHORA:\n"
            respuesta += "• 911 - Emergencias\n"
            respuesta += "• 144 - Crisis 24/7\n"
            respuesta += "• Línea de la Vida: 800 911 2000\n"
            respuesta += "• SAPTEL: 55 5259 8121\n\n"
            respuesta += "🏥 ACCIONES INMEDIATAS:\n"
            respuesta += "• Ve al hospital más cercano\n"
            respuesta += "• Llama a un familiar o amigo\n"
            respuesta += "• NO te quedes solo/a\n"
            respuesta += "• Habla con alguien AHORA\n\n"
            respuesta += "💖 Tu vida es valiosa. Este momento pasará.\n"
            respuesta += "Hay personas que quieren ayudarte."
            return respuesta
        
        # NIVEL ALTO
        elif severity == "alto":
            respuesta = "🔴 ANÁLISIS: RIESGO ALTO\n\n"
            
            if "violencia_fisica" in patterns:
                respuesta += "⚠️ VIOLENCIA FÍSICA DETECTADA\n\n"
                respuesta += "NECESITAS AYUDA INMEDIATA:\n"
                respuesta += "• 📞 144 - Violencia 24/7\n"
                respuesta += "• 📞 911 - Emergencias\n"
                respuesta += "• 🏥 Ve a urgencias si hay lesiones\n"
                respuesta += "• 📸 Documenta lesiones (fotos)\n"
                respuesta += "• 👮 Considera hacer denuncia\n\n"
                
            elif "amenazas_acoso" in patterns:
                respuesta += "⚠️ AMENAZAS Y ACOSO DETECTADOS\n\n"
                respuesta += "TU SEGURIDAD ES PRIORIDAD:\n"
                respuesta += "• 📞 911 - Emergencias\n"
                respuesta += "• 📞 144 - Protección 24/7\n"
                respuesta += "• 🏠 Busca un lugar seguro\n"
                respuesta += "• 👥 No te quedes solo/a\n"
                respuesta += "• 📱 Ten el 911 en marcación rápida\n\n"
                
            else:
                respuesta += f"Se detectaron {len(patterns)} categorías de violencia:\n\n"
                for cat, info in patterns.items():
                    nombre = cat.replace('_', ' ').title()
                    respuesta += f"• {nombre} ({info['cantidad']} indicadores)\n"
                respuesta += "\n"
            
            respuesta += "📞 LÍNEAS DE AYUDA:\n"
            respuesta += "• 144 - Violencia de género\n"
            respuesta += "• 141 - Orientación mujeres\n"
            respuesta += "• 137 - Víctimas violencia\n"
            respuesta += "• 089 - Denuncia anónima\n\n"
            respuesta += "🛡️ ACCIONES IMPORTANTES:\n"
            respuesta += "• Informa a personas de confianza\n"
            respuesta += "• Guarda evidencia (mensajes, fotos)\n"
            respuesta += "• Considera medidas de protección\n"
            respuesta += "• No estás sola/o en esto\n\n"
            respuesta += "💪 Recuerda: Mereces vivir sin violencia."
            
        # NIVEL MODERADO
        elif severity == "moderado":
            respuesta = "🟡 ANÁLISIS: RIESGO MODERADO\n\n"
            
            if patterns:
                respuesta += "Patrones detectados:\n"
                for cat, info in patterns.items():
                    nombre_bonito = {
                        'violencia_psicologica': '😔 Violencia psicológica',
                        'control_aislamiento': '🚫 Control y aislamiento',
                        'violencia_digital': '📱 Violencia digital',
                        'manipulacion_emocional': '💔 Manipulación emocional',
                        'violencia_economica': '💰 Violencia económica'
                    }.get(cat, cat.replace('_', ' ').title())
                    
                    respuesta += f"• {nombre_bonito} ({info['cantidad']} indicadores)\n"
            
            respuesta += "\n⚠️ Estos patrones pueden escalar con el tiempo.\n\n"
            respuesta += "📞 LÍNEAS DE APOYO:\n"
            respuesta += "• 144 - Violencia doméstica 24/7\n"
            respuesta += "• 141 - Orientación y recursos\n"
            respuesta += "• 137 - Víctimas de violencia\n\n"
            respuesta += "💡 RECOMENDACIONES:\n"
            respuesta += "• Habla con personas de confianza\n"
            respuesta += "• Documenta situaciones\n"
            respuesta += "• Busca apoyo psicológico\n"
            respuesta += "• Establece límites claros\n\n"
            respuesta += "¿Quieres contarme más sobre esta situación?"
            
        # NIVEL LEVE
        elif severity == "leve":
            respuesta = "🟡 ANÁLISIS: SEÑALES DE ALERTA\n\n"
            
            if patterns:
                respuesta += "Señales tempranas detectadas:\n"
                for cat, info in patterns.items():
                    nombre = cat.replace('_', ' ').title()
                    respuesta += f"• {nombre}\n"
                respuesta += "\n"
            
            respuesta += "Estas son señales que merecen atención.\n\n"
            respuesta += "📞 RECURSOS DE APOYO:\n"
            respuesta += "• 144 - Asesoramiento\n"
            respuesta += "• 141 - Información\n"
            respuesta += "• Centros de atención local\n\n"
            respuesta += "💭 REFLEXIONA SOBRE:\n"
            respuesta += "• ¿Te sientes libre en la relación?\n"
            respuesta += "• ¿Puedes expresarte sin miedo?\n"
            respuesta += "• ¿Respetan tus decisiones?\n"
            respuesta += "• ¿Te sientes valorada/o?\n\n"
            respuesta += "¿Cómo te hace sentir esta situación?"
            
        # SIN RIESGO
        else:
            respuesta = "🟢 ANÁLISIS: SIN SEÑALES CLARAS\n\n"
            respuesta += "No detecté patrones específicos de violencia.\n\n"
            
            # Si hay análisis emocional, incluirlo
            if ai_analysis and 'emociones_combinadas' in ai_analysis:
                emociones = ai_analysis['emociones_combinadas']
                if emociones:
                    respuesta += f"Noto que te sientes: {', '.join(emociones)}\n\n"
            
            respuesta += "Si necesitas apoyo emocional:\n"
            respuesta += "• 144 - Orientación psicológica\n"
            respuesta += "• 141 - Información recursos\n"
            respuesta += "• Centros de escucha\n\n"
            respuesta += "💭 Confía en tu intuición.\n"
            respuesta += "Si algo te incomoda, es válido hablarlo.\n\n"
            respuesta += "¿Hay algo específico que te preocupa?"
        
        return respuesta

    def analyze_emotions_spanish(self, text):
        """
        Análisis completo de emociones en español con IA
        
        Returns:
            dict: Emociones detectadas y consejos personalizados
        """
        # Análisis con IA
        ai_analysis = self._analyze_with_ai(text)
        
        # Obtener emociones combinadas (IA + reglas)
        if ai_analysis and 'emociones_combinadas' in ai_analysis:
            emociones = ai_analysis['emociones_combinadas']
        else:
            emociones = self._analizar_emociones_espanol(text)
        
        if not emociones:
            return {
                "emociones": [],
                "consejo": "💬 ¿Puedes contarme más sobre cómo te sientes?",
                "intensidad": 0,
                "ai_info": ai_analysis
            }
        
        # Calcular intensidad
        intensidad = self._calcular_intensidad_emocional(text, emociones)
        
        # Generar consejo personalizado
        consejo = self._generar_consejo_emocional(emociones, intensidad)
        
        return {
            "emociones": emociones,
            "consejo": consejo,
            "intensidad": intensidad,
            "ai_info": ai_analysis
        }

    def _calcular_intensidad_emocional(self, text, emociones):
        """Calcula la intensidad emocional del texto"""
        # Palabras intensificadoras
        intensificadores = ['muy', 'mucho', 'demasiado', 'super', 'extremadamente', 
                           'totalmente', 'completamente', 'bastante', 'increíblemente']
        
        # Signos de exclamación e interrogación
        exclamaciones = text.count('!') + text.count('¡')
        interrogaciones = text.count('?') + text.count('¿')
        
        # Palabras en mayúsculas
        palabras_mayusculas = sum(1 for palabra in text.split() if palabra.isupper() and len(palabra) > 2)
        
        # Score base
        intensidad = 0.3
        
        # Aumentar por número de emociones
        intensidad += len(emociones) * 0.1
        
        # Aumentar por intensificadores
        intensidad += sum(0.1 for intensif in intensificadores if intensif in text.lower()) * 0.1
        
        # Aumentar por signos
        intensidad += (exclamaciones + interrogaciones) * 0.05
        
        # Aumentar por mayúsculas
        intensidad += palabras_mayusculas * 0.05
        
        return min(intensidad, 1.0)

    def _generar_consejo_emocional(self, emociones, intensidad=0.5):
        """Genera consejos personalizados según emociones detectadas"""
        
        consejos_por_emocion = {
            'tristeza': "💙 Veo que estás triste...\n\n• Permítete sentir sin juzgarte\n• Escucha música que te reconforte\n• Sal a caminar en la naturaleza\n• Habla con alguien de confianza\n• Escribe sobre tus sentimientos\n\n📞 Si necesitas apoyo:\n• 144 - Apoyo emocional\n• 141 - Orientación",
            
            'enojo': "🔥 Noto que estás enojada/o...\n\n• Respira profundamente 3 veces\n• Aléjate momentáneamente\n• Haz ejercicio físico\n• Expresa lo que sientes con calma\n• Escribe antes de hablar\n\n📞 Si necesitas ayuda:\n• 144 - Contención emocional",
            
            'miedo': "🛡️ Detecto que tienes miedo...\n\n• Identifica qué te asusta específicamente\n• Busca un lugar seguro\n• Rodéate de personas de confianza\n• Practica técnicas de relajación\n• Recuerda: Eres más fuerte de lo que crees\n\n📞 Si necesitas protección:\n• 911 - Emergencias\n• 144 - Protección 24/7",
            
            'felicidad': "🌈 ¡Qué alegría que te sientas feliz!\n\n• Disfruta plenamente este momento\n• Comparte tu alegría con otros\n• Haz algo que te guste\n• Agradece por esta sensación\n• Recuerda que mereces ser feliz siempre\n\n💫 ¡Sigue así!",
            
            'soledad': "🌌 Siento que te sientes solo/a...\n\n• Llama a un ser querido ahora\n• Sal a un lugar público\n• Únete a grupos con intereses comunes\n• Voluntariado o actividades sociales\n• Recuerda: No estás solo/a\n\n📞 Líneas de acompañamiento:\n• 144 - Compañía emocional\n• 141 - Redes de apoyo",
            
            'agobio': "🌪️ Siento que estás agobiada/o...\n\n• Respira profundamente 5 veces\n• Haz una lista de prioridades\n• Enfócate en una cosa a la vez\n• Tómate descansos obligatorios\n• Pide ayuda - no tienes que hacerlo todo\n\n📞 Si necesitas orientación:\n• 144 - Contención\n• 141 - Recursos de apoyo",
            
            'frustracion': "💢 Detecto frustración...\n\n• Acepta que está bien no lograr todo\n• Celebra pequeños avances\n• Cambia de actividad temporalmente\n• Ajusta tus expectativas\n• Pide ayuda cuando la necesites\n\n📞 Apoyo disponible:\n• 144 - Orientación",
            
            'confusion': "💫 Entiendo que te sientes confundida/o...\n\n• Escribe todo sin filtrar\n• Haz una lista de pros y contras\n• Date tiempo para decidir\n• Consulta con alguien objetivo\n• Confía en tu intuición\n\n📞 Asesoramiento:\n• 144 - Orientación\n• 141 - Información",
            
            'impotencia': "💪 Noto que te sientes impotente...\n\n• Enfócate en lo que SÍ puedes controlar\n• Busca pequeñas victorias diarias\n• Pide ayuda profesional\n• Recuerda tu fuerza interior\n• Este sentimiento es temporal\n\n📞 Apoyo:\n• 144 - Empoderamiento\n• 141 - Recursos",
            
            'culpa': "💭 Siento que te sientes culpable...\n\n• Los sentimientos de culpa son normales\n• Habla sobre lo que sientes\n• Practica el auto-perdón\n• Aprende de la experiencia\n• Mereces compasión\n\n📞 Apoyo emocional:\n• 144 - Orientación psicológica",
            
            'vergüenza': "🌻 Noto que sientes vergüenza...\n\n• Todos cometemos errores\n• Comparte con alguien de confianza\n• Practica la autocompasión\n• Estos sentimientos pasarán\n• Eres más que tus errores\n\n📞 Apoyo:\n• 144 - Orientación",
            
            'ansiedad': "😰 Detecto ansiedad...\n\n• Respira: 4 segundos inhala, 7 retén, 8 exhala\n• Enfócate en el presente\n• Identifica pensamientos catastróficos\n• Haz ejercicio físico\n• Limita cafeína y azúcar\n\n📞 Ayuda profesional:\n• 144 - Crisis de ansiedad\n• Considera terapia especializada",
            
            'esperanza': "🌟 Veo esperanza en ti...\n\n• Cultiva ese sentimiento positivo\n• Establece metas alcanzables\n• Rodéate de personas positivas\n• Visualiza tu futuro deseado\n• La esperanza es el primer paso\n\n💫 ¡Sigue adelante!"
        }
        
        # Si hay una sola emoción
        if len(emociones) == 1:
            consejo_base = consejos_por_emocion.get(
                emociones[0],
                "🌻 Estoy aquí para escucharte. ¿Quieres contarme más?"
            )
            
            # Añadir nota sobre intensidad si es alta
            if intensidad > 0.7:
                consejo_base += "\n\n⚠️ Noto que la intensidad de tus emociones es alta. "
                consejo_base += "Considera buscar apoyo profesional si persiste."
            
            return consejo_base
        
        # Si hay múltiples emociones
        else:
            # Caso especial: felicidad mezclada
            if 'felicidad' in emociones:
                otras = [e for e in emociones if e != 'felicidad']
                if otras:
                    return f"🌈 Veo que te sientes feliz pero también {', '.join(otras)}...\n\nEs normal tener emociones mezcladas. Disfruta tu felicidad y recuerda que las otras emociones también son válidas.\n\n📞 Apoyo disponible:\n• 144 - Orientación emocional"
            
            # Múltiples emociones negativas
            consejo_base = f"💭 Noto que estás sintiendo {', '.join(emociones)}...\n\n"
            consejo_base += "ESTRATEGIAS PARA EMOCIONES MÚLTIPLES:\n"
            consejo_base += "• Escribe todo lo que sientes sin filtrar\n"
            consejo_base += "• Permítete sentir cada emoción\n"
            consejo_base += "• Habla con alguien de confianza\n"
            consejo_base += "• Practica mindfulness o meditación\n"
            consejo_base += "• Las emociones son temporales\n\n"
            consejo_base += "📞 Líneas de apoyo:\n"
            consejo_base += "• 144 - Orientación psicológica 24/7\n"
            consejo_base += "• 141 - Información y recursos\n\n"
            
            if intensidad > 0.7:
                consejo_base += "⚠️ La intensidad emocional es alta. "
                consejo_base += "Considera buscar apoyo profesional.\n\n"
            
            consejo_base += "💖 Estoy aquí si necesitas hablar más."
            
            return consejo_base

    def _empty_analysis(self):
        """Respuesta para análisis vacío"""
        return {
            "patrones_detectados": {},
            "nivel_riesgo": "ninguno",
            "respuesta_recomendada": "No pude analizar el mensaje. ¿Podrías reformularlo?",
            "ai_analysis": None,
            "analisis_emocional": {
                "emociones": [],
                "consejo": "¿Puedes contarme más?"
            }
        }

    def _get_timestamp(self):
        """Retorna timestamp actual"""
        from datetime import datetime
        return datetime.now().isoformat()

    def get_statistics(self):
        """Retorna estadísticas del analizador"""
        return {
            "version": self.version,
            "ai_models_loaded": self.ai_models_loaded,
            "categorias_violencia": len(self.patterns),
            "emociones_detectables": len(self.emociones_espanol),
            "total_patrones": sum(len(keywords) for keywords in self.patterns.values()),
            "models": {
                "sentiment": self.sentiment_analyzer is not None,
                "emotion": self.emotion_analyzer is not None
            }
        }


# ==================== TESTING Y UTILIDADES ====================
def print_analysis_report(analysis):
    """Imprime un reporte formateado del análisis"""
    print("\n" + "="*70)
    print("📊 REPORTE DE ANÁLISIS COMPLETO CON IA")
    print("="*70)
    
    # Nivel de riesgo
    print(f"\n🎯 NIVEL DE RIESGO: {analysis['nivel_riesgo'].upper()}")
    
    # Patrones detectados
    if analysis['patrones_detectados']:
        print(f"\n⚠️ PATRONES DE VIOLENCIA DETECTADOS: {len(analysis['patrones_detectados'])}")
        for cat, info in analysis['patrones_detectados'].items():
            print(f"\n   📌 {cat.replace('_', ' ').title()}:")
            print(f"      - Indicadores encontrados: {info['cantidad']}")
            print(f"      - Palabras clave: {', '.join(info['palabras'][:5])}")
    else:
        print("\n✅ No se detectaron patrones de violencia")
    
    # Análisis emocional
    if 'analisis_emocional' in analysis:
        emociones = analysis['analisis_emocional']
        if emociones['emociones']:
            print(f"\n💭 EMOCIONES DETECTADAS: {', '.join(emociones['emociones'])}")
            print(f"   Intensidad: {emociones.get('intensidad', 0):.2f}/1.00")
    
    # Análisis de IA
    if analysis.get('ai_analysis'):
        ai = analysis['ai_analysis']
        print("\n🤖 ANÁLISIS CON IA:")
        if 'sentimiento' in ai:
            print(f"   Sentimiento: {ai['sentimiento']['etiqueta']} "
                  f"(confianza: {ai['sentimiento']['confianza']:.2f})")
        if 'emociones_ia' in ai:
            print(f"   Emociones IA: {[e['emocion'] for e in ai['emociones_ia']]}")
    
    # Respuesta recomendada
    print("\n💬 RESPUESTA RECOMENDADA:")
    print("─" * 70)
    print(analysis['respuesta_recomendada'])
    print("─" * 70)
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    print("🔬 PROBANDO ANALIZADOR MEJORADO CON IA\n")
    
    analyzer = SecurityAnalyzer()
    
    # Mostrar estadísticas
    print("\n📈 ESTADÍSTICAS DEL ANALIZADOR:")
    stats = analyzer.get_statistics()
    for key, value in stats.items():
        print(f"   • {key}: {value}")
    
    # Casos de prueba
    test_cases = [
        "Mi pareja me grita y me dice que soy inútil todo el tiempo, me hace sentir muy mal",
        "Se enoja cuando hablo con mis amigas y revisa mi celular constantemente",
        "Me amenaza con matarme si lo dejo, tengo mucho miedo",
        "Estoy muy feliz hoy, todo va genial en mi vida",
        "Me siento confundida y no sé qué hacer con mi relación",
        "Me pega y luego me pide perdón pero siempre vuelve a hacerlo, tengo moretones",
        "No me deja trabajar y controla todo mi dinero, no puedo comprar nada"
    ]
    
    print("\n" + "="*70)
    print("CASOS DE PRUEBA")
    print("="*70)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"CASO {i}: {test}")
        print(f"{'='*70}")
        
        analysis = analyzer.analyze_message(test)
        print_analysis_report(analysis)
        
        input("\nPresiona Enter para continuar...")
    
    print("\n✅ Pruebas completadas")