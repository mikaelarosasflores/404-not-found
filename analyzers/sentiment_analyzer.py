import warnings, re
from datetime import datetime
from typing import Dict, Any, List
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util

warnings.filterwarnings("ignore")

class SentimentAnalyzer:
    def __init__(self):
        self.senti = pipeline(
            "sentiment-analysis",
            model="pysentimiento/robertuito-sentiment-analysis",
            tokenizer="pysentimiento/robertuito-sentiment-analysis",
        )
        self.emb = SentenceTransformer("distiluse-base-multilingual-cased-v2")

        self.seeds: Dict[str, str] = {
            "violencia_fisica":       "me empujó, me golpeó, me lastimó, violencia física, moretones",
            "violencia_psicologica":  "me insulta, me humilla, me grita, me hace sentir mal, te odio",
            "control_aislamiento":    "no me deja salir, controla con quién hablo, me aíslam me prohíbe que hable con amigas",
            "amenazas_acoso":         (
                "te voy a hacer daño, te voy a matar, me va a matar, va a matarme, va a "
                "me dijo que me va a matar, amenaza, me amenaza, hostigar, acosar, perseguir, sicario, sicarios"
            ),
            "violencia_digital":      "revisa mi celular, contraseñas, espía mis mensajes, controla redes",
            "manipulacion_emocional": "me hace sentir culpable, chantaje emocional, sin mí no eres nada",
            "violencia_economica":    "controla mi dinero, no me deja trabajar, me quita el sueldo",
        }
        self.seed_vecs = {cat: self.emb.encode(txt) for cat, txt in self.seeds.items()}

        self.sev = {
            "emergencia": [
                "suicid", "matarme ahora", "me está pegando", "estoy sangrando",
                "me va a matar ahora", "va a matarme ahora"
            ],
            "alto": [
                "te voy a matar", "me va a matar", "va a matarme",
                "me dijo que me va a matar", "amenaza con matarme", "me amenaza con matarme",
                "arma", "sangre", "moretones", "sicario", "sicarios"
            ],
            "moderado": ["no me deja", "me sigue", "me espía", "me grita", "me hace sentir culpable"],
            "leve": ["celos", "mensajes constantes", "contraseñas"],
        }

        self.re_kill_threat = re.compile(
            r"\b(?:me|te|nos)\s+va(?:n)?\s+a\s+matar\b"
            r"|(?:\bva(?:n)?\s+a\s+matar(?:me|te|nos)?\b)"
            r"|(?:\b(?:matarme|matarte|matarnos)\b)"
            r"|(?:\bte\s+voy\s+a\s+matar\b)",
            re.IGNORECASE
        )

    def _sims(self, tl: str) -> Dict[str, float]:
        v_user = self.emb.encode(tl)
        return {cat: float(util.cos_sim(v_user, v_seed).item()) for cat, v_seed in self.seed_vecs.items()}

    def _risk(self, tl: str, sims: Dict[str, float], senti_label: str) -> str:
        if any(w in tl for w in self.sev["emergencia"]):
            return "emergencia"
        if self.re_kill_threat.search(tl):
            return "alto"
        if any(w in tl for w in self.sev["alto"]) or any(sims.get(c, 0.0) > 0.50 for c in ("violencia_fisica", "amenazas_acoso")):
            return "alto"
        if senti_label == "NEG" and any(sims.get(c, 0.0) > 0.40 for c in ("violencia_psicologica","control_aislamiento","manipulacion_emocional")):
            return "moderado"
        if any(v > 0.33 for v in sims.values()) or any(w in tl for w in (self.sev["moderado"] + self.sev["leve"])):
            return "leve"
        return "ninguno"

    def _tags(self, tl: str, sims: Dict[str, float]) -> List[str]:
        out: List[str] = []
        if "te odio" in tl or "odio" in tl:
            out += ["negativo", "posible_psicologica"]
        if self.re_kill_threat.search(tl) or any(k in tl for k in ["sicario","sicarios","te voy a","matarte","hacerte daño"]):
            out += ["posible_amenaza"]
        if any(k in tl for k in ["no me deja", "revisa mi celular", "contraseñas"]):
            out += ["posible_control"]
        if sims:
            out.append(f"top_emb:{max(sims, key=sims.get)}")
        return out

    def analyze(self, text: str) -> Dict[str, Any]:
        if not isinstance(text, str) or not text.strip():
            return {
                "sentimiento": None,
                "similitudes": {},
                "categoria_top": None,
                "score_top": None,
                "nivel_riesgo": "ninguno",
                "tags": [],
                "timestamp": datetime.now().isoformat(),
            }

        tl = text.lower().strip()
        s = self.senti(tl[:512])[0]
        sims = self._sims(tl)
        categoria_top = max(sims, key=sims.get) if sims else None
        score_top = sims.get(categoria_top) if categoria_top else None
        nivel_riesgo = self._risk(tl, sims, s["label"])
        tags = self._tags(tl, sims)

        return {
            "sentimiento": {"label": s["label"], "confianza": float(s["score"])},
            "similitudes": sims,
            "categoria_top": categoria_top,
            "score_top": score_top,
            "nivel_riesgo": nivel_riesgo,
            "tags": tags,
            "timestamp": datetime.now().isoformat(),
        }