"""
ANALIZADOR DE SENTIMIENTO - VERSIÓN FINAL COMPLETA
Para EvaBot - Por Frida
"""

class SentimentAnalyzer:
    def __init__(self):
        """Inicializa con todas las categorías de violencia de género"""
        self.patterns = {
            "control": [
                "no salgas con", "no hables con", "dónde estás", 
                "con quién estás", "revisa tu celular", "celos",
                "controla", "vigila", "no te vistas así", "exige saber"
            ],
            "humillacion": [
                "eres una", "no sirves", "estás loca", "nadie te quiere",
                "gorda", "fea", "inútil", "dramática", "exagerada", "estúpida"
            ],
            "amenazas": [
                "te voy a", "si no haces", "vas a ver", 
                "te arrepentirás", "suicid", "matar", "dañar",
                "golpear", "lastimar", "acabar contigo"
            ],
            "aislamiento": [
                "no veas a tu familia", "tus amigas son", 
                "no confíes en", "solo te tengo a mí", "no salgas sin mí"
            ],
            "violencia_economica": [
                "no te doy dinero", "me das tu sueldo", 
                "no trabajes", "dependes de mí", "controlo el dinero"
            ]
        }
        
        # Sistema de palabras clave para determinar gravedad
        self.severity_keywords = {
            "leve": ["celos", "molesto", "enojado"],
            "moderado": ["amenaza", "humillación", "control", "obligar"],
            "alto": ["matar", "suicidio", "golpear", "dañar", "lastimar"]
        }
    
    def analyze_text(self, text):
        """Analiza texto y detecta violencia con sistema completo"""
        if not text:
            return self._empty_analysis()
        
        text_lower = text.lower().strip()
        
        # Detectar patrones de violencia
        detected_patterns = self._detect_patterns(text_lower)
        
        # Calcular nivel de severidad
        severity_level = self._calculate_severity(text_lower, detected_patterns)
        
        # Generar respuesta automática
        response = self._generate_response(severity_level)
        
        return {
            "texto_analizado": text,
            "patrones_detectados": detected_patterns,
            "nivel_riesgo": severity_level,
            "respuesta_recomendada": response,
            "riesgo_detectado": len(detected_patterns) > 0
        }
    
    def _detect_patterns(self, text):
        """Busca patrones de violencia en el texto"""
        detected = {}
        
        for category, patterns in self.patterns.items():
            matches_found = []
            for pattern in patterns:
                if pattern in text:
                    matches_found.append(pattern)
            
            if matches_found:
                detected[category] = matches_found
        
        return detected
    
    def _calculate_severity(self, text, patterns):
        """Calcula nivel de severidad basado en patrones detectados"""
        if not patterns:
            return "ninguno"
        
        # Si detectamos amenazas, es ALTO RIESGO
        if "amenazas" in patterns:
            return "alto"
        
        # Si detectamos palabras de alto riesgo
        for severe_word in self.severity_keywords["alto"]:
            if severe_word in text:
                return "alto"
        
        # Si hay múltiples tipos de violencia, es MODERADO
        if len(patterns) >= 2:
            return "moderado"
        
        # Un solo tipo de violencia es LEVE
        return "leve"
    
    def _generate_response(self, severity):
        """Genera respuesta automática según el nivel de riesgo"""
        responses = {
            "ninguno": "No detecté indicios claros de violencia. Estoy aquí para escucharte 💜",
            "leve": "He detectado algunos patrones de control. ¿Quieres contarme más sobre esta situación?",
            "moderado": "⚠️ He detectado comportamientos preocupantes. Esto podría ser violencia psicológica. ¿Estás a salvo?",
            "alto": "🆘 ¡ALTO RIESGO DETECTADO! 🆘 Por favor, contacta a: Línea 144 (violencia de género) o 911 (emergencias). Tu seguridad es lo más importante."
        }
        
        return responses.get(severity, responses["ninguno"])
    
    def _empty_analysis(self):
        """Manejo de texto vacío o inválido"""
        return {
            "texto_analizado": "",
            "patrones_detectados": {},
            "nivel_riesgo": "ninguno",
            "respuesta_recomendada": "No pude analizar el mensaje. ¿Podrías intentarlo de nuevo?",
            "riesgo_detectado": False
        }


def analyze_sentiment(text):
    """Función simple para análisis rápido desde otras partes del código"""
    analyzer = SentimentAnalyzer()
    return analyzer.analyze_text(text)


# Pruebas completas del sistema
if __name__ == "__main__":
    print("🔍 PROBANDO VERSIÓN FINAL DEL ANALIZADOR")
    print("=" * 50)
    
    test_messages = [
        "Mi novio revisa mi celular y no me deja ver a mis amigas",
        "Hoy tuve un día maravilloso!",
        "Me dijo que si lo dejaba se iba a suicidar",
        "Siempre me dice que no sirvo para nada y que soy una inútil",
        "Controla todo mi dinero y no me deja trabajar"
    ]
    
    for message in test_messages:
        print(f"\n📨 Mensaje: '{message}'")
        result = analyze_sentiment(message)
        print(f"   🎯 Riesgo: {result['nivel_riesgo']}")
        print(f"   📊 Patrones: {result['patrones_detectados']}")
        print(f"   💬 Respuesta: {result['respuesta_recomendada']}")
        print("   " + "-" * 40)