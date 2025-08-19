# Serviço de monitorização das datas e avisos

import datetime
import tkinter as tk
from tkinter import messagebox
from data_handler import load_data

def check_expiration_and_alert():
    """Verifica a validade dos softwares e exibe alertas."""
    data = load_data()
    today = datetime.date.today()
    expiring_soon = []

    for software in data["softwares"]:
        try:
            validade_date = datetime.datetime.strptime(software["validade"], "%Y-%m-%d").date()
            diff_days = (validade_date - today).days

            if software.get("renovacao", "").lower() != "nao":
                if 0 <= diff_days <= 90:  # expira em até 3 meses
                    expiring_soon.append(software)
                elif diff_days < 0:  # já venceu
                    expiring_soon.append(software)

        except ValueError:
            print(f"Data inválida para o software: {software['nome']}")

    if expiring_soon:
        message = "Os seguintes softwares estão com a validade próxima ou vencida:\n\n"
        for soft in expiring_soon:
            message += f"Software: {soft['nome']}\n"
            message += f"Validade: {soft['validade']}\n"
            message += "-------------------\n"

        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning("Aviso de Validade de Software", message)
        root.destroy()

if __name__ == "__main__":
    check_expiration_and_alert()