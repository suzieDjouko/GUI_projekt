__# BlauWelle - GUI zur Auswahl von Schiffsreisen
## 1. Einfuehrung
### 1.1 Projektbeschreibung

- Funktion 1: Auswahl der Meerart
- Funktion 2: Filterung nach N�chten
- Funktion 3: Reisezeitplanung

---

## 2. Hauptfunktionen

### 2.1. Filterung und Auswahl
- **Meerart**: Auswahl zwischen Ostsee, Nordsee, Mittelmeer etc.
- **Anzahl der uebernachtungen**: Filterung ueber einen Bereich von +/-2 Naechten.
- **Staedte**: Moeglichkeit, mehrere Staedte mit Bildern auszuwaehlen.
- **Schiffstypen**: Anzeige verfuegbarer Schiffstypen mit Bildern.
- **Kabinentypen**: Darstellung von Kabinen mit Preisen und Bildern.

### 2.2. Ergebnisanzeige
- Liste mit Reisen, die den gewaehlten Kriterien entsprechen.
- Wichtige Informationen wie Reisenummer, Meerart, uebernachtungen, besuchte Staedte, Schiffstyp und Kabinentyp werden angezeigt.
- Markierung von Reisen, die ueber dem Nutzerkapital liegen (ausgegraut).

### 2.3. Nutzerkapital
- Zufaellige Kapitalerhoehung (1.000 -3.000) bei jeder Anmeldung.
- Kapitalmaximum: 20.000 .
- Das Kapital wird bei jeder Buchung aktualisiert und gespeichert.
- Anzeige des aktuellen Kontostands in der GUI.

### 2.4. Nutzerkapital
- Auswahl des Start- und Enddatums innerhalb des Zeitraums Mai bis Oktober 2025.
- Einschraenkungen fuer Abfahrtstage basierend auf Schiffstypen.

### 2.5. Buchungsabschluss
- Erstellung einer Textdatei mit allen Buchungsdetails.
- Erstellung einer Textdatei mit allen Buchungsdetails.
- Aktualisierung des Nutzerkapitals nach der Buchung.


---

# 3. Projektarchitektur

## 3.1. Technologien
- **Python**: Hauptprogrammiersprache.
- **PyQt5**: Erstellung der grafischen Benutzeroberflaeche.
- **Pandas**: Verarbeitung und Filterung der Excel-Daten.
- **SQLite**: Verwaltung der Nutzerdaten (Username, Passwort, Kontostand).

## 3.2. Dateistruktur
- `main.py`: Hauptdatei, Einstiegspunkt der Anwendung.
- `styles.py`: Definition von CSS-Stilen fuer die GUI.
- `database_action.py`: Datenbankoperationen (z. B. Nutzerkapital aktualisieren).
- `functionen.py`: Hilfsfunktionen fuer die Filterlogik.
- `checking_funktion.py`: Validierung der Benutzereingaben.

### Verzeichnisse fuer Bilder:
- `images/Hafenstaedte`: Bilder der Staedte.
- `images/Schiffstypen`: Bilder der Schiffstypen.
- `images/Kabinentypen`: Bilder der Kabinenarten.

---





