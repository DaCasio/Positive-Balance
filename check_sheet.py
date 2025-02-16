import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

# Google Sheets API Zugangsdaten
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/your/credentials.json', scope)
client = gspread.authorize(creds)

# URL und GID aus Umgebungsvariablen holen
sheet_url = os.environ.get('GOOGLE_SHEET_URL')
sheet_gid = os.environ.get('GOOGLE_SHEET_GID')

# Google Sheet öffnen
sheet = client.open_by_url(sheet_url).get_worksheet_by_gid(int(sheet_gid))

# Daten aus Zeile 2 holen
data = sheet.row_values(2)

# Erste positive Zahl finden
positive_balance_index = next((i for i, x in enumerate(data) if not x.startswith('-')), None)

if positive_balance_index is not None:
    month = sheet.cell(1, positive_balance_index + 1).value
    balance = data[positive_balance_index]
    
    # JSON Datei erstellen
    with open('output.json', 'w') as json_file:
        json.dump({"month": month, "balance": balance}, json_file)
else:
    print("Kein positives Guthaben gefunden.")
