"""
ANALIZADOR DE DETECCIÓN DE VIOLENCIA - VERSIÓN 1.5
Para EvaBot - Por Frida
Detección de violencia digital, psicológica y patrones modernos de abuso
"""

class SentimentAnalyzer:
    def __init__(self):
        """Inicializa con categorías actualizadas de violencia digital y psicológica"""
        self.patterns = {
            "control": [
                "no salgas con", "no hables con", "dónde estás", 
                "con quién estás", "revisa tu celular", "celos",
                "controla", "vigila", "no te vistas así", "exige saber",
                # NUEVO EN v1.5: Patrones digitales
                "me muestras tus chats", "por qué no me contestas",
                "bloquea a", "elimina a", "qué haces en redes",
                "por qué subiste esa foto", "quién te dio like",
                "me pasas tu contraseña", "dónde has estado"
            ],
            "humillacion": [
                "eres una", "no sirves", "estás loca", "nadie te quiere",
                "gorda", "fea", "inútil", "dramática", "exagerada", "estúpida",
                # NUEVO EN v1.5: Humillaciones modernas
                "todas tus amigas son", "no sabes hacer nada",
                "estás mal de la cabeza", "eres una exagerada",
                "te lo buscas", "así te tratan por",
                "con ese cuerpo", "y encima te quejas"
            ],
            "amenazas": [
                "te voy a", "si no haces", "vas a ver", 
                "te arrepentirás", "suicid", "matar", "dañar",
                "golpear", "lastimar", "acabar contigo",
                # NUEVO EN v1.5: Amenazas digitales
                "subo tus fotos", "te expongo en redes",
                "le digo a todos que", "voy a publicar eso",
                "te voy a hacer quedar mal", "nadie te va a creer",
                "pago para que", "contrato a alguien para"
            ],
            "aislamiento": [
                "no veas a tu familia", "tus amigas son", 
                "no confíes en", "solo te tengo a mí", "no salgas sin mí",
                # NUEVO EN v1.5: Aislamiento moderno
                "tus amigos son unos", "tu familia te manipula",
                "deja de hablar con", "no vayas a esa reunión",
                "no te juntes con", "esos no son tus amigos",
                "te están usando", "solo yo te entiendo"
            ],
            "violencia_economica": [
                "no te doy dinero", "me das tu sueldo", 
                "no trabajes", "dependes de mí", "controlo el dinero",
                # NUEVO EN v1.5: Control económico moderno
                "gastas mucho en", "no necesitas trabajar",
                "yo te mantengo", "para qué quieres dinero",
                "te pago solo si", "esa compra no la necesitas",
                "devuélvelo", "no sabes administrar"
            ],
            # NUEVA CATEGORÍA EN v1.5: VIOLENCIA DIGITAL
            "violencia_digital": [
                "pásame tus contraseñas", "quiero acceso a tu cuenta",
                "por qué me bloqueaste", "acepta mi solicitud en redes",
                "etiquétame en todo", "dónde estás en tiempo real",
                "enciende tu ubicación", "respóndeme ahora mismo",
                "por qué no estás en línea", "sube una foto conmigo",
                "quita esa publicación", "qué comentarios te ponen"
            ],
            # NUEVA CATEGORÍA EN v1.5: MANIPULACIÓN EMOCIONAL
            "manipulacion_emocional": [
                "si me quisieras", "una novia de verdad haría",
                "es por tu bien", "te lo digo porque te amo",
                "sin mí no eres nada", "nadie te va a aguantar como yo",
                "después de todo lo que hice por ti", "eres mi única razón para vivir",
                "si te vas me muero", "me haces esto después de todo",
                "estás loco si piensas eso", "exageras todo"
            ]
        }
        
        # Sistema MEJORADO en v1.5
        self.severity_keywords = {
            "leve": ["celos", "molesto", "enojado", "disgustado"],
            "moderado": ["amenaza", "humillación", "control", "obligar", "manipular"],
            "alto": ["matar", "suicidio", "golpear", "dañar", "lastimar", "exponer", "publicar"]
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
        """NUEVO EN v1.5: Calcula nivel de severidad con criterios más precisos"""
        if not patterns:
            return "ninguno"
        
        # ALTO RIESGO: Amenazas directas, violencia digital grave o múltiples categorías graves
        if ("amenazas" in patterns or 
            "violencia_digital" in patterns and len(patterns) >= 2 or
            any(word in text for word in self.severity_keywords["alto"])):
            return "alto"
        
        # MODERADO RIESGO: Comportamientos de control serios, manipulación o 2+ categorías
        control_serio = [
            "revisa tu celular", "controla", "vigila", "no te vistas así", 
            "exige saber", "pásame tus contraseñas", "me muestras tus chats",
            "bloquea a", "elimina a", "enciende tu ubicación"
        ]
        
        if (any(patron_serio in text for patron_serio in control_serio) or
            "manipulacion_emocional" in patterns or
            len(patterns) >= 2):
            return "moderado"
        
        # LEVE: Un solo patrón menos grave
        return "leve"
    
    def _generate_response(self, severity):
        """NUEVO EN v1.5: Genera respuestas más específicas y útiles"""
        responses = {
            "ninguno": "No detecté indicios claros de violencia. Recuerda que estoy aquí para escucharte cuando lo necesites 💜",
            
            "leve": "He detectado algunos comportamientos que podrían ser señal de alerta. ¿Quieres contarme más sobre esta situación? Podemos identificar juntas si hay patrones preocupantes.",
            
            "moderado": "⚠️ He detectado varios patrones de comportamiento que son señales de violencia psicológica. Esto incluye control, manipulación o aislamiento. ¿Estás en un lugar seguro? ¿Necesitas ayuda para planificar tu seguridad?",
            
            "alto": "🆘 ¡RIESGO ALTO DETECTADO! 🆘 \n\nPor favor, considera contactar:\n• Línea 144 - Violencia de género (24/7)\n• 911 - Emergencias\n• Línea de la Esperanza - Prevención suicidio\n\nTu seguridad es lo más importante. Si estás en peligro inmediato, busca un lugar seguro."
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


# Pruebas completas del sistema v1.5
if __name__ == "__main__":
    print("🔍 PROBANDO VERSIÓN 1.5 - VIOLENCIA DIGITAL Y PATRONES MODERNOS")
    print("=" * 60)
    
    test_messages = [
        "Mi novio revisa mi celular y no me deja ver a mis amigas",
        "Me exige que le pase mis contraseñas de redes sociales",
        "Dice que si lo dejo sube mis fotos íntimas a internet",
        "Siempre me dice que sin él no soy nada y que nadie me va a querer",
        "Me controla el dinero y no me deja trabajar",
        "Hoy tuve un día maravilloso con mis amigos!",
        "Si no le muestro mis chats se enoja y me hace sentir culpable",
        "Dice que estoy loca por sentirme incómoda con sus celos"
    ]
    
    for message in test_messages:
        print(f"\n📨 Mensaje: '{message}'")
        result = analyze_sentiment(message)
        print(f"   🎯 Riesgo: {result['nivel_riesgo']}")
        print(f"   📊 Patrones: {result['patrones_detectados']}")
        print(f"   💬 Respuesta: {result['respuesta_recomendada']}")
        print("   " + "-" * 40)
        