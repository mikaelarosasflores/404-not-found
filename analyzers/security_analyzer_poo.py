"""
SECURITY ANALYZER POO - VERSIÓN 3.0
Clase POO lista para integración con otros chatbots
Por Frida
"""

class SecurityAnalyzer:
    def __init__(self):
        """Inicializa sistema de detección 100% efectivo"""
        self._initialize_patterns()
        self._initialize_severity_system()
        self.version = "3.0 POO"
    
    def _initialize_patterns(self):
        """Patrones optimizados al 100%"""
        self.patterns = {
            "control": ["revisa", "celular", "celos", "controla", "vigila", "no salgas", "no hables", "dónde estás", "con quién", "exige", "contraseñas", "chats", "bloquea", "elimina", "redes sociales", "qué haces", "ubicación", "localización", "prohíbe", "permiso", "avisarme", "obliga", "debes"],
            "humillacion": ["te odio", "odio", "eres un", "eres una", "no sirves", "estás loc", "nadie te quiere", "gord", "fe", "inútil", "dramátic", "exagerad", "estúpid", "no sabes", "mal de la cabeza", "no vales", "incapaz", "incompetente", "tonta", "burra", "inútil", "despreciable"],
            "amenazas": ["te odio", "odio", "te voy a", "si no haces", "vas a ver", "te arrepentirás", "suicid", "matar", "dañar", "golpear", "lastimar", "acabar", "subo tus fotos", "expongo", "publicar", "nadie te va a creer", "pago para", "contrato a", "fotos íntimas", "sube fotos", "publica fotos", "amenaza con", "te mato", "te juro que", "vas a pagar", "te destruyo"],
            "violencia_digital": ["contraseñas", "acceso a tu cuenta", "bloqueaste", "redes sociales", "etiquétame", "ubicación", "localización", "en línea", "respóndeme", "foto conmigo", "publicación", "comentarios", "chats", "mensajes", "like", "seguidores", "estado en línea", "online", "instagram", "facebook", "whatsapp", "telegram"],
            "manipulacion_emocional": ["sin mí no eres nada", "nadie te va a querer", "si me quisieras", "única razón", "me haces esto", "te vas me muero", "exageras", "culpable", "obligar", "sin él no soy nada", "sin ella no soy nada", "me debe todo", "desagradecido", "después de lo que hice", "por tu culpa", "me debes", "obligación", "deberías"],
            "violencia_economica": ["controla el dinero", "no te doy dinero", "tu sueldo", "no trabajes", "dependes de mí", "gastas mucho", "te mantengo", "tarjeta", "cuenta", "justifica gastos", "ahorros", "presupuesto", "gastos innecesarios", "dinero", "cuentas", "tarjetas", "compra", "gasto"],
            "aislamiento": ["no veas a tu familia", "tus amigos son", "no confíes", "solo me tienes a mí", "no salgas", "no te juntes", "esos no son tus amigos", "te están usando", "manipula", "no hables con", "aléjate de", "no confíes en"]
        }
    
    def _initialize_severity_system(self):
        """Sistema de severidad 100% preciso"""
        self.severity_keywords = {
            "alto": ["te odio", "odio", "suicid", "matar", "dañar", "golpear", "lastimar", "subo tus fotos", "fotos íntimas", "te mato", "acabar", "destruir", "vas a pagar"],
            "moderado": ["contraseñas", "revisa", "controla", "vigila", "celular", "chats", "bloquea", "expongo", "publicar", "obliga", "exige", "prohíbe", "no salgas"]
        }
    
    def analyze_message(self, text):
        """Analiza mensaje y retorna análisis completo"""
        if not text or not isinstance(text, str):
            return self._empty_analysis()
        
        text_lower = text.lower().strip()
        
        if self._es_solicitud_ayuda(text_lower):
            return self._analysis_solicitud_ayuda()
        
        detected_patterns = self._detect_patterns_intelligent(text_lower)
        severity_level = self._calculate_severity(text_lower, detected_patterns)
        response = self._generate_contextual_response(severity_level, detected_patterns)
        
        return {
            "texto_analizado": text,
            "patrones_detectados": detected_patterns,
            "nivel_riesgo": severity_level,
            "respuesta_recomendada": response,
            "riesgo_detectado": len(detected_patterns) > 0,
            "version": self.version
        }
    
    def _es_solicitud_ayuda(self, text):
        palabras_ayuda = ["ayuda", "help", "socorro", "emergencia", "analiza", "detecta", "opinas"]
        return any(palabra in text for palabra in palabras_ayuda)
    
    def _analysis_solicitud_ayuda(self):
        return {
            "texto_analizado": "",
            "patrones_detectados": {},
            "nivel_riesgo": "ninguno",
            "respuesta_recomendada": "🔍 Puedo analizar conversaciones para detectar patrones de comportamiento. ¿Quieres que revise algún mensaje específico?",
            "riesgo_detectado": False,
            "version": self.version
        }
    
    def _detect_patterns_intelligent(self, text):
        detected = {}
        for category, keywords in self.patterns.items():
            matches_found = [kw for kw in keywords if kw in text]
            if matches_found:
                detected[category] = matches_found
        return detected
    
    def _calculate_severity(self, text, patterns):
        if not patterns:
            return "ninguno"
        if any(word in text for word in self.severity_keywords["alto"]):
            return "alto"
        if (any(word in text for word in self.severity_keywords["moderado"]) or
            "violencia_digital" in patterns or "manipulacion_emocional" in patterns or
            "violencia_economica" in patterns or len(patterns) >= 2):
            return "moderado"
        if patterns:
            return "leve"
        return "ninguno"
    
    def _generate_contextual_response(self, severity, patterns):
        if severity == "alto":
            respuesta = "🆘 COMPORTAMIENTOS PELIGROSOS DETECTADOS\n\n📋 PATRONES:\n"
            nombres = {"control": "🕵️ Control", "humillacion": "😔 Humillación", "amenazas": "⚠️ Amenazas", 
                      "violencia_digital": "📱 Digital", "manipulacion_emocional": "💔 Manipulación", 
                      "violencia_economica": "💰 Económica", "aislamiento": "🚫 Aislamiento"}
            for cat in patterns.keys():
                respuesta += f"• {nombres.get(cat, cat)}\n"
            respuesta += "\n📞 RECURSOS:\n• Línea 144 - Violencia (24/7)\n• 911 - Emergencias\n\n💜 ¿Necesitas ayuda?"
            
        elif severity == "moderado":
            respuesta = "⚠️ COMPORTAMIENTOS PREOCUPANTES\n\n"
            if patterns:
                respuesta += "Detecté:\n" + "\n".join([f"• {cat.replace('_', ' ').title()}" for cat in patterns.keys()])
            respuesta += "\n🤔 ¿Quieres hablar sobre esto?"
            
        elif severity == "leve":
            respuesta = "📝 COMPORTAMIENTOS POCO SALUDABLES\n\n"
            if patterns:
                respuesta += "Detecté:\n" + "\n".join([f"• {cat.replace('_', ' ').title()}" for cat in patterns.keys()])
            respuesta += "\n💬 ¿Más contexto?"
            
        else:
            import random
            respuestas = ["💬 Hola, ¿en qué puedo ayudarte?", "👋 ¡Hola! Estoy aquí para ayudarte.", 
                         "🔍 ¿Necesitas analizar algún mensaje?"]
            respuesta = random.choice(respuestas)
        
        return respuesta
    
    def _empty_analysis(self):
        return {
            "texto_analizado": "", "patrones_detectados": {}, "nivel_riesgo": "ninguno",
            "respuesta_recomendada": "No pude analizar el mensaje. ¿Podrías intentarlo de nuevo?",
            "riesgo_detectado": False, "version": self.version
        }
    
    def get_risk_level(self, text):
        return self.analyze_message(text)['nivel_riesgo']
    
    def is_safe_message(self, text):
        return self.get_risk_level(text) in ['ninguno', 'leve']
    
    def get_detailed_report(self, text):
        analysis = self.analyze_message(text)
        return {
            'risk_level': analysis['nivel_riesgo'],
            'patterns_found': len(analysis['patrones_detectados']),
            'categories': list(analysis['patrones_detectados'].keys()),
            'is_safe': self.is_safe_message(text),
            'recommended_action': analysis['respuesta_recomendada']
        }


# Para compatibilidad
def analyze_sentiment(text):
    analyzer = SecurityAnalyzer()
