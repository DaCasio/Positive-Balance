# Positive Balance Checker

Dieses Projekt überwacht ein öffentlich zugängliches Google Sheet, das prognostizierte Kontostände für verschiedene Monate enthält.  
Das Skript `check_sheet.py` sucht von links nach rechts in der zweiten Zeile (Balances) nach dem ersten positiven Wert (einem Wert, der **nicht** mit "-" beginnt).  
Sobald dieser positive Wert gefunden ist, wird das dazugehörige Monatsdatum aus der ersten Zeile (Monate) ausgelesen, in ein Datum konvertiert  
und die exakte Zeitdifferenz (in vollen Monaten und verbleibenden Tagen) zwischen dem aktuellen Datum und dem positiven Monat berechnet.

Das Ergebnis wird in der JSON-Datei `output_lametric.json` gespeichert. Diese Datei kann beispielsweise von einer LaMetric App abgerufen werden,  
um die Informationen anzuzeigen.

## Voraussetzungen

- Python 3.x
- Abhängigkeiten: `requests`

Installiere die Abhängigkeiten mit:

pip install requests

## Verwendung

1. Öffne die Datei `check_sheet.py` und überprüfe, ob die Variable `sheet_url` auf den korrekten CSV-Export-Link deines Google Sheets zeigt.
2. Stelle sicher, dass das Google Sheet in der ersten Zeile Monatsangaben im Format dreistellig (z. B. `Jan25`, `Feb25`, `Mär25`, `Dez25` usw.)  
   und in der zweiten Zeile die entsprechenden Kontostände enthält.
3. Führe das Skript lokal aus:

python check_sheet.py

4. Die Ergebnisse werden in der Datei `output_lametric.json` abgelegt.

## Funktionsweise

- Das Skript lädt die CSV-Daten aus dem Google Sheet und parst die ersten beiden Zeilen.
- Es wird von links nach rechts nach dem ersten positiven Kontostand gesucht (Wert ohne führendes "-").
- Das zugehörige Monatsdatum wird aus dem entsprechenden Eintrag (z. B. `Dez25`) ermittelt und in ein Datum umgewandelt.
- Anschließend wird die exakte Differenz zwischen dem aktuellen Datum und diesem Datum in vollen Monaten und Tagen berechnet.
- Das Ergebnis wird in folgendem JSON-Format abgespeichert:

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


## Dynamische Anpassung

Da sich die Inhaltsspalten im Google Sheet ändern können (z. B. Startmonat und Anzahl der Monate variieren),  
sucht das Skript immer von links nach rechts nach dem ersten positiven Wert. Somit passt es sich dynamisch an Veränderungen im Sheet an.

---

Kopiere einfach beide Dateien (den Code und die README.md) in dein Repository. Du kannst den Code jederzeit wiederverwenden, indem du ihn exakt so einfügst.
