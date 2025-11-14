from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class HelpResource:
    title: str
    contact: str
    note: str = ""

@dataclass
class HelpDirectory:
    data: Dict[str, Dict[str, List[HelpResource]]] = field(default_factory=lambda: {
        "AR": {
            "general": [
                HelpResource("Línea 144", "144", "Atención 24/7 por violencias de género."),
                HelpResource("Emergencias", "911", "Riesgo inminente."),
            ],
            "digital": [
                HelpResource("Con Vos (AR)", "https://www.argentina.gob.ar/convos", "Orientación ante violencia digital."),
            ],
        },
        "US": {
            "general": [
                HelpResource("National Domestic Violence Hotline", "1-800-799-7233 / thehotline.org", "24/7 chat y teléfono."),
                HelpResource("Emergencias", "911", "Riesgo inminente."),
            ],
            "digital": [
                HelpResource("Cyber Civil Rights Initiative", "https://cybercivilrights.org", "Acoso/imagen íntima no consentida."),
            ],
        },
        "GLOBAL": {
            "general": [
                HelpResource("ONU Mujeres", "https://www.unwomen.org/es", "Recursos y orientación internacional."),
            ]
        }
    })

    def get(self, country: str, category: str) -> List[HelpResource]:
        country = (country or "GLOBAL").upper()
        category = (category or "general").lower()
        results: List[HelpResource] = []

        if country in self.data and category in self.data[country]:
            results.extend(self.data[country][category])
        if country in self.data and "general" in self.data[country]:
            results.extend(self.data[country]["general"])
        if "GLOBAL" in self.data and "general" in self.data["GLOBAL"]:
            results.extend(self.data["GLOBAL"]["general"])

        # dedup
        seen = set()
        uniq = []
        for r in results:
            key = (r.title, r.contact)
            if key not in seen:
                seen.add(key)
                uniq.append(r)
        return uniq