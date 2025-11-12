# core/classifier.py
import re

def classify_text(text: str):
    """
    Clasifica texto detectando violencia verbal, psicológica y manipulación emocional.
    Devuelve un diccionario con tipo, severidad, evidencias y recomendaciones.
    """
    if not text:
        return {"detected": False, "categories": [], "severity": "desconocida", "evidence": [], "recommendations": []}

    t = text.lower()

    # Palabras ofensivas comunes
    insultos = [
        "idiota", "imbecil", "estúpida", "tarada", "inútil", "mierda", "asquerosa", "gorda", "cerda",
        "loca", "zorra", "fea", "tonta", "burra", "fracasada", "mentirosa", "sirvienta", "negra de mierda",
        "no servís para nada", "das asco", "sos una carga", "nadie te quiere", "no valés nada"
    ]

    # Frases de manipulación emocional / psicológica
    manipulacion = [
         "estás exagerando", "eso nunca pasó", "te inventás todo",
         "sin mí no sos nada", "nadie te va a creer", "si me quisieras",
         "yo hago todo por vos", "todo es tu culpa", "me obligás a enojarme",
         "no hables con tus amigas", "no salgas con tu familia"
    ]

    # Amenazas leves o implícitas
    amenazas = [
         "vas a ver", "te voy a arruinar", "no sabés con quién te metés",
         "me vas a pagar", "voy a publicar eso", "te voy a denunciar sin motivo"
    ]

    evidencia = []

    for palabra in insultos + manipulacion + amenazas:
        if re.search(rf"\b{re.escape(palabra)}\b", t):
            evidencia.append(palabra)

    categorias = []
    severidad = "baja"

    if any(p in t for p in insultos):
        categorias.append("verbal")
        severidad = "media"
    if any(p in t for p in manipulacion):
        categorias.append("psicológica")
        severidad = "media"
    if any(p in t for p in amenazas):
        categorias.append("amenaza")
        severidad = "alta"

    recomendaciones = []
    if categorias:
        recomendaciones = [
            "No respondas a las agresiones; guardá evidencia (capturas).",
            "Bloqueá/silenciá a la persona agresora en la plataforma.",
            "Contale a alguien de confianza o buscá apoyo.",
        ]
        if "psicológica" in categorias:
            recomendaciones.append("No justifiques ni minimices los ataques; no es tu culpa.")
        if "amenaza" in categorias:
            recomendaciones.append("Buscá ayuda urgente si te sentís en riesgo. Llamá al 911 o Línea 144.")

    return {
        "detected": bool(categorias),
        "categories": categorias,
        "severity": severidad,
        "evidence": evidencia,
        "recommendations": recomendaciones,
    }
