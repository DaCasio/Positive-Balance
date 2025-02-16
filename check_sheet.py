from datetime import date
import json
import requests
import csv
from calendar import monthrange

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
positive_index = next((i for i, bal in enumerate(balances) if bal and not bal.startswith('-')), None)

if positive_index is None:
    print("Kein positiver Balance-Wert gefunden.")
    exit(0)

def parse_month(month_str):
    """
    Wandelt einen Monatsstring, z.B. "Jan25", in ein date-Objekt um.
    Es wird davon ausgegangen, dass der Monatsname immer dreistellig und die Jahreszahl immer zweistellig ist.
    """
    month_part = month_str[:3]
    year_part = month_str[3:]
    if len(year_part) != 2:
        raise ValueError("Jahreszahl im Monatstring stimmt nicht: " + month_str)
    year_full = "20" + year_part
    month_map = {
        'Jan': 1,
        'Feb': 2,
        'Mär': 3,
        'Apr': 4,
        'Mai': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Okt': 10,
        'Nov': 11,
        'Dez': 12,
    }
    if month_part not in month_map:
        raise ValueError("Unbekannter Monatsname: " + month_part)
    return date(int(year_full), month_map[month_part], 1)

def calculate_months_and_days(start_date, end_date):
    """
    Berechnet die exakten Monate und Tage zwischen zwei Daten.
    """
    months_count = 0
    current_date = start_date

    while current_date < end_date:
        # Anzahl der Tage im aktuellen Monat ermitteln
        days_in_month = monthrange(current_date.year, current_date.month)[1]
        
        # Prüfen, ob das Enddatum im aktuellen Monat liegt
        if current_date.year == end_date.year and current_date.month == end_date.month:
            days_count = (end_date - current_date).days
            return months_count, days_count
        
        # Zum nächsten Monat wechseln
        current_date = date(
            current_date.year + (current_date.month // 12),
            (current_date.month % 12) + 1,
            1
        )
        
        months_count += 1

# Berechne das Datum des ersten positiven Monats
positive_date = parse_month(months[positive_index])
current_date = date.today()

if positive_date < current_date:
    months_count, days_count = 0, 0
else:
    months_count, days_count = calculate_months_and_days(current_date, positive_date)

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

# Schreibe das Ergebnis in die JSON-Datei output_lametric.json
with open("output_lametric.json", "w") as json_file:
    json.dump(result, json_file, indent=4)
