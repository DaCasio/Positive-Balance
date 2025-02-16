from datetime import date
import json
import requests
import csv

# Google Sheet URL (CSV Export Link)
sheet_url = "https://docs.google.com/spreadsheets/d/1syH5ntimv_5juHGOZo0LUgLO1Jk2kEQjhno8Kl21jzw/export?format=csv&gid=0"

# Download der CSV-Daten
response = requests.get(sheet_url)
response.raise_for_status()

# CSV-Daten parsen
lines = response.text.splitlines()
reader = csv.reader(lines)
data = list(reader)

if len(data) < 2:
    print("Fehler: Es wurden nicht genügend Zeilen aus dem CSV geladen.")
    exit(1)

# Extrahiere die erste Zeile (Monate) und die zweite Zeile (Balances)
months = data[0]
balances = data[1]

# Finde den Index der ersten positiven Balance (Zelle, die NICHT mit '-' beginnt)
positive_index = next((i for i, bal in enumerate(balances) if not bal.startswith('-')), None)

def parse_month(month_str):
    """
    Wandelt einen Monatsstring, z.B. "Aug25", in ein date-Objekt um.
    Ist das Jahr nur zweistellig, wird "20" vorangestellt.
    """
    month_part = month_str[:3]
    year_part = month_str[3:]
    if len(year_part) == 2:
        year_part = "20" + year_part
    month_map = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
        'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
        'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12,
    }
    return date(int(year_part), month_map[month_part], 1)

if positive_index is not None:
    positive_date = parse_month(months[positive_index])
    current_date = date.today()
    delta = positive_date - current_date

    # Hier erfolgt die Berechnung ohne +1: z. B. 166 Tage ergeben 5 Monate (166 // 30) und 16 Tage (166 % 30)
    months_count = delta.days // 30   
    days_count = delta.days % 30        

    result = {
        "frames": [
            {
                "text": f"M{months_count} T{days_count}",
                "icon": "i11386"  # Icon-ID für den Zeitraum
            },
            {
                "text": balances[positive_index],
                "icon": "i66330"  # Icon-ID für den Kontostand
            }
        ]
    }

    # Schreibe das Ergebnis in die JSON-Datei
    with open("output_lametric.json", "w") as json_file:
        json.dump(result, json_file, indent=4)
else:
    print("No positive balance found.")
