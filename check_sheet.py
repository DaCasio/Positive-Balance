from datetime import date, timedelta
import json
import requests
import csv

# Google Sheet URL (CSV Export Link)
sheet_url = "https://docs.google.com/spreadsheets/d/1syH5ntimv_5juHGOZo0LUgLO1Jk2kEQjhno8Kl21jzw/export?format=csv&gid=0"

# Download the CSV-Daten
response = requests.get(sheet_url)
response.raise_for_status()

# CSV-Daten parsen
lines = response.text.splitlines()
reader = csv.reader(lines)
data = list(reader)

# Erste Zeile (Monate) und zweite Zeile (Kontostände) extrahieren
months = data[0]
balances = data[1]

# Finde die erste positive Balance (ohne führendes Minus)
positive_index = next((i for i, balance in enumerate(balances) if not balance.startswith('-')), None)

def parse_month(month_str):
    month, year = month_str[:3], month_str[3:]
    month_map = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    return date(int(year), month_map[month], 1)

if positive_index is not None:
    positive_date = parse_month(months[positive_index])
    current_date = date.today()
    delta = positive_date - current_date

    # Berechne Monate und Tage
    if delta.days < 0:
        months_count = 0
        days_count = 0
    else:
        months_count = (delta.days // 30) + 1  # +1, da der erste Monat mitzählt
        days_count = delta.days % 30

    result = {
        "frames": [
            {
                "text": f"M{months_count} T{days_count}",
                "icon": "i11386"
            },
            {
                "text": balances[positive_index],
                "icon": "i66330"
            }
        ]
    }

    # Schreibe das Ergebnis in die JSON-Datei
    with open("output_lametric.json", "w") as json_file:
        json.dump(result, json_file, indent=4)
else:
    print("No positive balance found.")
