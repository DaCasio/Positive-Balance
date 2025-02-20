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
        raise ValueError("Ungültiger Jahres-Teil im Monat: " + month_str)
    year_full = int("20" + year_part)
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
    return date(year_full, month_map[month_part], 1)

def add_months(orig_date, months):
    """
    Addiert eine bestimmte Anzahl von Monaten zu orig_date.
    Falls der Tag im Zielmonat nicht existiert, wird der letzte gültige Tag gewählt.
    """
    new_month = orig_date.month - 1 + months
    new_year = orig_date.year + new_month // 12
    new_month = new_month % 12 + 1
    new_day = orig_date.day
    max_day = monthrange(new_year, new_month)[1]
    if new_day > max_day:
        new_day = max_day
    return date(new_year, new_month, new_day)

def calculate_months_and_days_exact(start_date, end_date):
    """
    Berechnet die exakten vollen Monate und verbleibenden Tage zwischen zwei Daten.
    Beispiel: Vom 16.02.2025 bis 01.12.2025 sollten 9 Monate und 15 Tage resultieren.
    """
    # Gesamtdifferenz in Monaten (ohne Berücksichtigung der Tage)
    total_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    # Falls der Tag von start_date größer ist als der Tag von end_date, ist noch kein voller Monat vergangen.
    if start_date.day > end_date.day:
        total_months -= 1
    anchor_date = add_months(start_date, total_months)
    days_remainder = (end_date - anchor_date).days
    return total_months, days_remainder

# Berechne das Datum des ersten positiven Monats (z. B. "Dez25") 
positive_date = parse_month(months[positive_index])
current_date = date.today()

if positive_date <= current_date:
    months_count, days_count = 0, 0
else:
    months_count, days_count = calculate_months_and_days_exact(current_date, positive_date)

result = {
    "frames": [
        {
            "text": f"M{months_count} T{days_count}",
            "icon": "11386"
        },
        {
            "text": balances[positive_index],
            "icon": "66330"
        }
    ]
}

# Schreibe das Ergebnis in die JSON-Datei output_lametric.json
with open("output_lametric.json", "w") as json_file:
    json.dump(result, json_file, indent=4)
