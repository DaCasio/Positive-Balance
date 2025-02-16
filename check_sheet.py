if positive_index is not None:
    positive_date = parse_month(months[positive_index])
    current_date = date.today()
    delta = positive_date - current_date

    # Berechne die Anzahl der Monate und Tage
    if delta.days < 0:
        months_count = 0
        days_count = 0
    else:
        # Berechne die Anzahl der Monate
        months_count = (delta.days // 30) + 1  # +1, da der erste Monat auch zählt
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
