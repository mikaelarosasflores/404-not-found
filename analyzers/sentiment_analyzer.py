"""
ANALIZADOR DE SENTIMIENTO - DETECCIÓN DE PATRONES
Para EvaBot - Por Frida
"""

class SentimentAnalyzer:
    def __init__(self):
        """Inicializa con más patrones de violencia"""
        self.patterns = {
            "control": [
                "no salgas con", "no hables con", "dónde estás",
                "revisa tu celular", "celos", "controla", "vigila"
            ],
            "humillacion": [
                "eres una", "no sirves", "estás loca", "nadie te quiere",
                "gorda", "fea", "inútil", "dramática"
            ],
            "amenazas": [
                "te voy a", "si no haces", "suicid", "matar", 
                "dañar", "vas a ver", "te arrepentirás"
            ]
        }
    
    def analyze_text(self, text):
        """Analiza texto y detecta patrones de violencia"""
        if not text:
            return {"error": "Texto vacío"}
        
        text_lower = text.lower()
        detected = {}
        
        # Detección de patrones
        for category, patterns in self.patterns.items():
            matches = []
            for pattern in patterns:
                if pattern in text_lower:
                    matches.append(pattern)
            if matches:
                detected[category] = matches
        
        # Sistema básico de riesgo
        if "amenazas" in detected:
            riesgo = "alto"
        elif len(detected) > 0:
            riesgo = "leve"
        else:
            riesgo = "ninguno"
        
        return {
            "texto_analizado": text,
            "patrones_detectados": detected,
            "nivel_riesgo": riesgo  # CORREGIDO: Ahora siempre es 'nivel_riesgo'
        }


def analyze_sentiment(text):
    """Función para uso externo"""
    analyzer = SentimentAnalyzer()
    return analyzer.analyze_text(text)


# Pruebas básicas
if __name__ == "__main__":
    print("🔍 PROBANDO DETECCIÓN DE PATRONES")
    print("=" * 40)
    
    # Varios mensajes de prueba
    test_messages = [
        "Mi novio tiene celos y revisa mi celular",
        "Hoy estoy muy feliz",
        "Me dijo que si lo dejaba se suicidaría"
    ]
    
    for test in test_messages:
        print(f"\n📨 Mensaje: '{test}'")
        resultado = analyze_sentiment(test)
        print(f"   🎯 Riesgo: {resultado['nivel_riesgo']}")
        print(f"   📊 Patrones: {resultado['patrones_detectados']}")