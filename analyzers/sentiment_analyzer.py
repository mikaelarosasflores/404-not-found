"""
ANALIZADOR DE SENTIMIENTO - ESTRUCTURA BÁSICA
Para EvaBot - Por Frida
"""

class SentimentAnalyzer:
    def __init__(self):
        """Inicializa el analizador con categorías básicas"""
        self.patterns = {
            "control": [
                "no salgas con", "no hables con", "celos"
            ],
            "humillacion": [
                "eres una", "no sirves", "estás loca"
            ]
        }
    
    def analyze_text(self, text):
        """Función principal de análisis"""
        if not text:
            return {"error": "Texto vacío"}
        
        return {
            "texto": text,
            "patrones": {},
            "riesgo": "ninguno"
        }


def analyze_sentiment(text):
    """Función para uso externo"""
    analyzer = SentimentAnalyzer()
    return analyzer.analyze_text(text)
    