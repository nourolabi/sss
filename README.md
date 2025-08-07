# Glanzwerk Rheinland - Rechnungssystem

Ein intelligentes Rechnungssystem für die Autowäscherei Glanzwerk Rheinland in Neuwied, Deutschland.

## 🚗 Über das Projekt

Das Glanzwerk Rechnungssystem ist eine benutzerfreundliche Webanwendung, die speziell für die Autowäscherei Glanzwerk Rheinland entwickelt wurde. Das System automatisiert die Rechnungserstellung und generiert professionelle PDF-Rechnungen mit integriertem Stammkundenrabatt-System.

## ✨ Hauptfunktionen

- **Deutsche Benutzeroberfläche** - Vollständig lokalisiert
- **Automatische Steuerberechnung** - MwSt 19% wird automatisch berechnet
- **Stammkundenrabatt** - 10% automatischer Rabatt nach 5 Besuchen
- **PDF-Rechnungsgenerierung** - Sofortiger Download professioneller Rechnungen
- **Glanzwerk-Branding** - Rechnungsdesign entspricht der Unternehmensidentität
- **Kundendatenbank** - Automatische Verfolgung der Kundenbesuche

## 🛠️ Technologie-Stack

- **Frontend:** Streamlit
- **Backend:** Python 3.11
- **Datenbank:** SQLite
- **PDF-Generierung:** fpdf2
- **Hosting:** Streamlit Cloud

## 🏢 Serviceangebot

1. **Grundreinigung** - 50,00€ (netto)
2. **Intensivreinigung** - 80,00€ (netto)
3. **Premium-Wäsche** - 120,00€ (netto)

## 📋 Installation und Verwendung

### Lokale Installation

1. Repository klonen:
```bash
git clone https://github.com/[username]/glanzwerk-rechnungssystem.git
cd glanzwerk-rechnungssystem
```

2. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

3. Anwendung starten:
```bash
streamlit run app.py
```

### Online-Version

Die Anwendung ist live verfügbar unter: [Streamlit Cloud Link wird hier eingefügt]

## 🏪 Unternehmensinformationen

**Glanzwerk Rheinland**  
Krasnaer Str. 1  
56566 Neuwied  
Deutschland  

**Kontakt:**  
📞 Telefon: +49 171 1858241  
📧 E-Mail: Glanzwerk.Rheinland@gmail.com  
🌐 Website: glanzwerk-rheinland.de  

**Slogan:** "Grün gedacht, sauber gemacht"

## 📖 Benutzerhandbuch

### Rechnung erstellen

1. **Kundendaten eingeben**
   - Kundenname in das entsprechende Feld eingeben
   - Fahrzeugnummer/Kennzeichen eingeben

2. **Dienstleistung auswählen**
   - Aus dem Dropdown-Menü die gewünschte Dienstleistung wählen

3. **Rechnung generieren**
   - Auf "Rechnung generieren" klicken
   - System berechnet automatisch alle Beträge
   - Rechnungsvorschau wird angezeigt

4. **PDF herunterladen**
   - Auf "PDF-Rechnung herunterladen" klicken
   - PDF wird automatisch generiert und heruntergeladen

### Stammkundenrabatt

- Das System verfolgt automatisch Kundenbesuche
- Nach dem 5. Besuch wird automatisch 10% Rabatt gewährt
- Rabatt wird deutlich in der Rechnung hervorgehoben

## 🔧 Technische Details

### Datenbankschema

```sql
-- Kundentabelle
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Besuchstabelle
CREATE TABLE visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    visit_date TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

### Preisberechnung

- **Nettobetrag:** Basispreis der gewählten Dienstleistung
- **MwSt (19%):** Automatisch berechnet
- **Bruttobetrag:** Netto + MwSt
- **Stammkundenrabatt:** 10% Rabatt nach 5 Besuchen
- **Endbetrag:** Brutto - Rabatt (falls anwendbar)

## 🚀 Deployment

### Streamlit Cloud

1. Repository auf GitHub hochladen
2. Mit Streamlit Cloud verbinden
3. App bereitstellen

### Lokales Deployment

```bash
streamlit run app.py --server.port 8501
```

## 📝 Lizenz

Dieses Projekt wurde speziell für Glanzwerk Rheinland entwickelt.

## 👨‍💻 Entwickler

**Mazen Design**  
Spezialisiert auf Webanwendungen für kleine und mittelständische Unternehmen.

## 🔮 Zukünftige Erweiterungen

- E-Mail-Integration für automatischen Rechnungsversand
- WhatsApp-API für Rechnungsversand
- Erweiterte Kundenverwaltung
- Rechnungshistorie und Archiv
- Umsatz- und Kundenstatistiken
- Multi-Standort-Unterstützung

---

*Entwickelt mit ❤️ für Glanzwerk Rheinland*

