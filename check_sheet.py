from datetime import date, timedelta
from decimal import Decimal, ROUND_DOWN, getcontext
import json
import requests
import csv

# Google Sheet URL (CSV Export Link)
sheet_url = "https://docs.google.com/spreadsheets/d/1syH5ntimv_5juHGOZo0LUgLO1Jk2kEQjhno8Kl21jzw/export?format=csv&gid=0"

# Download the CSV data
response = requests.get(sheet_url)
response.raise_for_status()

# Parse the CSV data
lines = response.text.splitlines()
reader = csv.reader(lines)
data = list(reader)

# Extract the first row (months) and second row (balances)
months = data[0]
balances = data[1]

# Find the first positive balance
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

    # Berechne die Anzahl der Monate und Tage
    months_count = delta.days // 30
    days_count = delta.days % 30

    # Anpassung: Berechne die Anzahl der Monate und Tage korrekt
    if delta.days < 0:
        months_count = 0
        days_count = 0
    else:
        months_count = delta.days // 30
        days_count = delta.days % 30

    result = {
        "frames": [
            {
                "text": f"M{months_count} T{days_count}",
                "icon": "i11386"  # Icon ID für den Monat
            },
            {
                "text": balances[positive_index],
                "icon": "i66330"  # Icon ID für den Wert
            }
        ]
    }

    # Write the result to a JSON file
    with open("output_lametric.json", "w") as json_file:
        json.dump(result, json_file, indent=4)
else:
    print("No positive balance found.")
