"""
Core chatbot logic: leitura de dados, classes de domínio e API simples
"""
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

SALON_NAME = "Renovo Cabelereiros"
DEFAULT_PHONE = "+5588993294936"
LOCATION = "Rua Prefeito Manoel Matoso, 216, Planalto da Catumbela, Russas - CEP 62901-282. Maps: https://maps.google.com/?q=seu+endereco"

@dataclass
class Trend:
    nome: str
    descricao: str
    inspiracao_link: Optional[str] = None

    def formatted(self) -> str:
        txt = f"✨ {self.nome}:
   {self.descricao}"
        if self.inspiracao_link:
            txt += f"\n   Veja inspiração: {self.inspiracao_link}"
        return txt

class DataLoader:
    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = Path(data_dir)

    def load_trends(self) -> Dict[str, List[Trend]]:
        path = self.data_dir / "trends.json"
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        result = {}
        for k, v in raw.items():
            result[k] = [Trend(**item) for item in v]
        return result

    def load_price_list(self) -> Dict[str, str]:
        path = self.data_dir / "price_list.json"
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

def validate_phone(number: str) -> bool:
    if not number:
        return False
    number = number.strip()
    return bool(re.fullmatch(r"\+?\d{10,15}", number))

class ChatbotCore:
    def __init__(self, loader: DataLoader = None):
        self.loader = loader or DataLoader()
        self.trends = self.loader.load_trends()
        self.prices = self.loader.load_price_list()
        self.salon_name = SALON_NAME
        self.phone = DEFAULT_PHONE
        self.location = LOCATION

    def main_menu_text(self) -> str:
        return (
            f"Olá! Bem-vindo(a) ao {self.salon_name}! ✨ Como posso te ajudar hoje?\n"
            "1. 🌟 Conhecer as últimas tendências\n"
            "2. 🗓️ Agendar um horário / Consultar serviço\n"
            "3. 💲 Ver nossa tabela de preços\n"
            "4. 📍 Nossa localização\n"
            "5. 🗣️ Falar com um de nossos especialistas\n"
            "6. 👋 Sair"
        )

    def trends_menu_text(self) -> str:
        return (
            "Que ótimo que você quer ficar por dentro das novidades! O que te interessa mais no momento?\n"
            "1. ✂️ Cortes em alta\n"
            "2. 🎨 Cores e mechas do momento\n"
            "3. 💁‍♀️ Penteados para arrasar\n"
            "4. 💡 Dicas de cuidados e produtos tendência\n"
            "5. ↩️ Voltar ao menu principal"
        )

    def trends_text(self, key: str) -> str:
        items = self.trends.get(key, [])
        if not items:
            return "Ainda não cadastramos tendências para essa categoria. Volte em breve!"
        lines = [f"Super! As tendências de {key} que estão bombando são:"]
        for t in items:
            lines.append(t.formatted())
        lines.append("\nQual dessas te inspira mais? Gostaria de agendar uma avaliação para vermos qual combina com você?")
        return "\n\n".join(lines)

    def price_list_text(self) -> str:
        lines = ["Confira nossa tabela de preços (valores podem variar dependendo da complexidade e do profissional):"]
        for svc, price in self.prices.items():
            lines.append(f"- {svc}: {price}")
        return "\n".join(lines)

    def location_text(self) -> str:
        return f"Nossa localização: {self.location}"

    def specialist_contact_text(self) -> str:
        return f"Para falar com um especialista, ligue para {self.phone} ou deixe sua dúvida que retornaremos assim que possível."
