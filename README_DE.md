🇬🇧 [English](README.md) | 🇩🇪 [Deutsch](README_DE.md)

# Tag 2 — Nachmittags-Lab
## Assets, Abhaengigkeiten und I/O

### Lernziele

Am Ende dieses Labs wirst du in der Lage sein:

- Ein neues Dagster-Projekt von Grund auf zu **erstellen** (Wiederholung von Tag 1)
- Assets mit expliziten Return-Type-Annotationen zu **definieren**
- Assets ueber Abhaengigkeitsdeklarationen zu **verketten**
- Reale, unsaubere Daten innerhalb eines Assets zu **bereinigen und validieren**
- Daten ueber Assets hinweg zu **aggregieren** und Ergebnisse in Dagit zu ueberpruefen
- Mehrere Datenquellen in einem Multi-Input-Asset zu **verknuepfen**

---

## Setup

Bevor du mit den Aufgaben beginnst, erstelle ein neues Projekt und bereite die Daten vor.

### Schritt 1 — Projekt erstellen

Erstelle ein neues Dagster-Projekt mit dem Namen **`shopflow`** in diesem Verzeichnis. Schau in deine Tag-1-Notizen oder in die [Dagster-Dokumentation](https://docs.dagster.io), falls du den Befehl nicht mehr weisst.

> **Hinweis:** Am Tag 1 hast du einen `uvx create-dagster@latest ...`-Befehl verwendet.

Wechsle nach dem Erstellen mit `cd` in das `shopflow/`-Verzeichnis fuer alle weiteren Schritte.

### Schritt 2 — Abhaengigkeiten installieren

```bash
uv sync
source .venv/bin/activate
```

### Schritt 3 — Datendatei erstellen

Erstelle ein `data/`-Verzeichnis im Projektstamm (neben `src/`) und lege eine Datei namens `orders.csv` mit folgendem Inhalt an:

```csv
order_id,customer_id,product_id,quantity,price,order_date,timestamp,status
1,1,3,1,129.99,2026-01-01,2026-01-01T08:15:00Z,delivered
2,5,11,2,79.98,2026-01-01,2026-01-01T09:30:00Z,delivered
3,2,7,1,49.99,2026-01-02,2026-01-02T10:00:00Z,shipped
4,8,1,3,59.97,2026-01-02,2026-01-02T14:20:00Z,pending
5,3,15,1,199.99,2026-01-03,2026-01-03T11:45:00Z,cancelled
6,1,9,2,39.98,2026-01-03,2026-01-03T16:00:00Z,delivered
7,6,4,1,89.99,2026-01-04,2026-01-04T08:30:00Z,shipped
8,4,12,1,149.99,2026-01-04,2026-01-04T12:10:00Z,delivered
9,7,2,4,119.96,2026-01-05,2026-01-05T09:00:00Z,pending
10,9,8,1,29.99,2026-01-05,2026-01-05T15:30:00Z,delivered
11,2,5,2,69.98,2026-01-06,2026-01-06T10:15:00Z,shipped
12,10,14,1,249.99,2026-01-06,2026-01-06T13:45:00Z,delivered
13,,6,1,59.99,2026-01-07,2026-01-07T08:00:00Z,delivered
14,5,10,2,99.98,2026-01-07,2026-01-07T11:30:00Z,
15,3,13,1,179.99,2026-01-08,2026-01-08T09:20:00Z,DELIVERED
16,8,1,0,0.00,2026-01-08,2026-01-08T14:00:00Z,pending
17,1,7,,44.99,2026-01-09,2026-01-09T10:00:00Z,shipped
18,6,3,2,259.98,2026-01-09,2026-01-09T16:30:00Z,delivered
19,4,11,1,79.99,2026-01-10,2026-01-10T08:45:00Z,returned
20,2,9,3,59.97,2026-01-10,2026-01-10T12:00:00Z,  Shipped
```

### Schritt 4 — Setup ueberpruefen

Starte den Entwicklungsserver und pruefe, ob alles funktioniert:

```bash
dg dev
```

Oeffne Dagit unter **http://localhost:3000**. Du solltest die Standard-Dagster-Startseite ohne Fehler sehen. Sobald das bestaetigt ist, stoppe den Server (`Ctrl+C`) — du startest ihn spaeter bei den Aufgaben erneut.

### Schritt 5 — Arbeitsdatei erstellen

Das erstellte Projekt hat einen `defs/`-Ordner, aber noch keine Asset-Dateien. Erstelle die Datei, in der dein gesamter Asset-Code geschrieben wird:

```
src/shopflow/defs/assets.py
```

Dagster erkennt Assets aus dem `defs/`-Ordner automatisch, sodass diese Datei automatisch geladen wird.

---

## Aufgaben

Schliesse **mindestens die Grundstufe** ab, bevor du weitermachst. Die Fortgeschrittenen- und Expertenstufe sind Zusatzaufgaben — bearbeite sie, wenn du frueh fertig wirst.

> **Erinnerung:** Du brauchst `from dagster import asset` und `import csv` am Anfang von `assets.py`. Wenn Dagster deine Assets ausfuehrt, ist das Arbeitsverzeichnis das **Projektstammverzeichnis** (`shopflow/`), sodass `data/orders.csv` als relativer Pfad korrekt aufgeloest wird.

### 🟢 Grundstufe

1. **Implementiere `raw_orders`**
   - Lies `data/orders.csv` mit Pythons eingebautem `csv.DictReader`.
   - Gib die Daten als `list[dict]` zurueck.
   - Fuege die Return-Type-Annotation `-> list[dict]` hinzu.
   - Materialisiere das Asset in Dagit und pruefe, ob es erfolgreich ist.

2. **Implementiere `cleaned_orders`**
   - Deklariere die Abhaengigkeit von `raw_orders` ueber einen Funktionsparameter mit Type-Annotation.
   - Ueberspringe jede Zeile, in der ein Pflichtfeld (`order_id`, `customer_id`, `product_id`, `quantity`, `price`, `order_date`, `status`) leer ist.
   - Normalisiere das `status`-Feld auf Kleinbuchstaben und entferne Leerzeichen am Rand.
   - Ueberspringe Zeilen, deren Status nicht einer der folgenden ist: `pending`, `shipped`, `delivered`, `cancelled`.
   - Konvertiere `quantity` zu `int` und `price` zu `float`.
   - Gib eine neue Liste bereinigter Dictionaries zurueck — veraendere die Originalzeilen nicht.

3. **Ueberpruefen des Graphen**
   - Oeffne den Asset-Graphen in Dagit. Stelle sicher, dass der Pfeil von `raw_orders` zu `cleaned_orders` zeigt.
   - Materialisiere beide Assets zusammen. Wie viele Zeilen liefert `cleaned_orders`? Schreibe die Antwort als Kommentar in deinen Code.

4. **Fehlerhafte Zeilen untersuchen**
   - Schau dir `orders.csv` an und identifiziere, welche Zeilen von deiner Bereinigungslogik entfernt werden und warum. Schreibe einen Kommentar mit den Zeilennummern und dem jeweiligen Grund (z.B. "Zeile 13 — leere customer_id").

---

### 🔵 Fortgeschritten

1. **Erstelle `order_summary`**
   - Erstelle ein neues Asset, das von `cleaned_orders` abhaengt.
   - Gib ein Dictionary mit folgenden Eintraegen zurueck:
     - `total_orders`: die Anzahl der bereinigten Zeilen
     - `total_revenue`: die Summe von `quantity * price` fuer alle Zeilen
     - `orders_by_status`: ein Dictionary, das jeden Status seiner Anzahl zuordnet (z.B. `{"delivered": 8, "shipped": 3, ...}`)
   - Fuege die Return-Type-Annotation `-> dict` hinzu.
   - Materialisiere und pruefe, ob die Ausgabe angesichts der CSV-Daten sinnvoll ist.

2. **Abhaengigkeitskette testen**
   - Materialisiere nur `order_summary`, ohne vorher die vorgelagerten Assets zu materialisieren. Was macht Dagster?
   - Materialisiere jetzt nur `raw_orders` erneut. Pruefe in Dagit — werden `cleaned_orders` und `order_summary` als veraltet markiert? Warum oder warum nicht?

3. **I/O-Manager-Verhalten erklaeren**
   - Schreibe in einem Kommentar am Anfang von `assets.py` in 2–3 Saetzen: Wie wird der Wert von `raw_orders` an `cleaned_orders` uebergeben? Welcher I/O-Manager wird verwendet und wo werden die Daten gespeichert?

4. **Szenarien klassifizieren**
   - Gib fuer jedes der folgenden Szenarien an, ob du ein `@asset`, ein `@op` oder ein `define_asset_job()` verwenden wuerdest, und erklaere in einem Satz warum:
     - (a) Eine Tabelle, die taegliche Website-Besuche aggregiert
     - (b) Versand einer Warn-E-Mail, wenn ein Pipeline-Schritt fehlschlaegt
     - (c) Ausfuehrung von `raw_orders`, `cleaned_orders` und `order_summary` nach einem Zeitplan jeden Morgen

---

### 🟣 Experte

1. **Zweite Datenquelle hinzufuegen: `raw_products`**
   - Erstelle eine Datei `data/products.csv` mit den Spalten: `product_id`, `name`, `category`, `unit_price`. Fuege mindestens 10 Zeilen ein.
   - Erstelle ein `raw_products`-Asset, das diese Datei liest und `list[dict]` zurueckgibt.

2. **`enriched_orders` erstellen**
   - Erstelle ein Asset, das von **sowohl** `cleaned_orders` als auch `raw_products` abhaengt.
   - Suche fuer jede bereinigte Bestellung das passende Produkt anhand der `product_id` und fuege `name` und `category` des Produkts zum Bestell-Dictionary hinzu.
   - Falls ein Produkt nicht gefunden wird, setze `name` auf `"Unknown"` und `category` auf `"Unknown"`.
   - Gib die angereicherte Liste zurueck.

3. **Asset-Graphen analysieren**
   - Oeffne den Asset-Graphen in Dagit. Skizziere oder beschreibe die vollstaendige Graphstruktur — wie viele Knoten, wie viele Kanten, und welche Assets koennen parallel ausgefuehrt werden?
   - Materialisiere alles. Aendere dann eine Zeile in `products.csv` und materialisiere nur `raw_products` erneut. Welche nachgelagerten Assets markiert Dagit als veraltet?

4. **Entscheidung zum Abhaengigkeitsstil**
   - Stelle dir vor, dass du an Tag 3 `loaded_orders` schreiben wirst, das `cleaned_orders`-Daten mit benutzerdefiniertem SQL in eine PostgreSQL-Tabelle einfuegt.
   - Wuerdest du die Abhaengigkeit ueber einen Funktionsparameter oder `deps` deklarieren? Schreibe 3–4 Saetze zur Begruendung deiner Wahl, wobei du darauf eingehst, wie die Daten fliessen und was der I/O-Manager tun (oder nicht tun) wuerde.
