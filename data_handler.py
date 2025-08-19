import json
import os

FILE_PATH = "software_agenda.json"
DEFAULT_PATH = "softwares_default.json"

def load_data():
    """Carrega os dados da agenda de um arquivo JSON."""
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    # se não existir, carrega o default
    if os.path.exists(DEFAULT_PATH):
        with open(DEFAULT_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    return {"softwares": []}

def save_data(data):
    """Salva os dados da agenda em um arquivo JSON."""
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)