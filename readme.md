Hier ist der generierte Text für die `README.md`-Datei:

---

# Positive Balance Checker

Dieses Projekt überwacht ein öffentlich zugängliches Google Sheet, das prognostizierte Kontostände für verschiedene Monate enthält.  
Das Skript `check_sheet.py` durchsucht die zweite Zeile des Sheets (Balances) von links nach rechts nach dem ersten positiven Wert (einem Wert, der **nicht** mit "-" beginnt).  
Sobald der erste positive Wert gefunden wurde, wird das zugehörige Monatsdatum aus der ersten Zeile (Monate) ausgelesen, in ein Datum umgewandelt,  
und die exakte Zeitdifferenz (in vollen Monaten und verbleibenden Tagen) zwischen dem aktuellen Datum und diesem Monat berechnet.

Das Ergebnis wird in der JSON-Datei `output_lametric.json` gespeichert, die beispielsweise von einer LaMetric-App abgerufen werden kann, um die Informationen anzuzeigen.

---

## Voraussetzungen

- **Python 3.x**
- **Abhängigkeiten**: `requests`

Installiere die Abhängigkeit mit:

```bash
pip install requests
```

---

## Verwendung

1. Öffne die Datei `check_sheet.py` und überprüfe, ob die Variable `sheet_url` den korrekten CSV-Export-Link deines Google Sheets enthält.
2. Stelle sicher, dass das Google Sheet wie folgt aufgebaut ist:
   - **Erste Zeile**: Monatsangaben im dreistelligen Format, z. B. `Jan25`, `Feb25`, `Mär25`, `Dez25` usw.
   - **Zweite Zeile**: Die entsprechenden Kontostände (positiv oder negativ).
3. Führe das Skript mit folgendem Befehl aus:

```bash
python check_sheet.py
```

4. Die Ergebnisse werden in der Datei `output_lametric.json` abgelegt.

---

## Funktionsweise

1. Das Skript lädt die CSV-Daten automatisch aus dem angegebenen Google Sheet.
2. Es parst die ersten beiden Zeilen:
   - **Monate** aus der ersten Zeile.
   - **Kontostände** aus der zweiten Zeile.
3. Von links nach rechts sucht das Skript nach dem ersten positiven Kontostand (ein Wert ohne führendes "-").
4. Sobald der Wert gefunden ist:
   - Der zugehörige Monat (z. B. `Dez25`) wird in ein Datum umgewandelt.
   - Die Zeitdifferenz zwischen dem aktuellen Datum und dem positiven Monat wird in vollen Monaten und verbleibenden Tagen berechnet.
5. Das Ergebnis wird als JSON-Datei `output_lametric.json` im folgenden Format gespeichert:

```json
{
    "frames": [
        {
            "text": "M9 T15",
            "icon": "i11386"
        },
        {
            "text": "252,11",
            "icon": "i66330"
        }
    ]
}
```

---

## Ergebnis-Anpassung

- **Dynamik**: Sollte sich der Inhalt des Google Sheets ändern (z. B. andere Startspalte oder zusätzliche Monate), passt sich das Skript automatisch an, indem es immer von links nach rechts sucht.
- **Genauigkeit**: Es wird die Zeitdifferenz (Monate und verbleibende Tage) exakt berechnet.

---

## Beispielausgabe

Angenommen, heute ist der **20. Februar 2025**, und der erste positive Kontostand liegt im Monat **Dezember 2025** (mit einem Wert von **252,11**).  
Das Ergebnis in der Datei `output_lametric.json` wäre:

```json
{
    "frames": [
        {
            "text": "M9 T10",
            "icon": "i11386"
        },
        {
            "text": "252,11",
            "icon": "i66330"
        }
    ]
}
```

---

### Hinweise

Dieses Skript kann flexibel angepasst und in anderen Projekten verwendet werden. Kopiere die Dateien einfach in dein Repository und passe bei Bedarf die URL des Google Sheets an.
