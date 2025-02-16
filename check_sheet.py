import requests
import csv
import json

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

if positive_index is not None:
    result = {
        "frames": [
            {
                "text": months[positive_index],
                "icon": "i100"
            },
            {
                "text": balances[positive_index],
                "icon": "i101"
            }
        ]
    }

    # Write the result to a JSON file
    with open("output_lametric.json", "w") as json_file:
        json.dump(result, json_file, indent=4)
else:
    print("No posi
