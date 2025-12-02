# CRM System - PythonAnywhere Setup Tutorial

Dieses Tutorial führt Sie Schritt für Schritt durch die Einrichtung des CRM-Systems auf PythonAnywhere.

## Voraussetzungen

- Ein PythonAnywhere-Account (kostenlos oder bezahlt)
- Grundkenntnisse in der Linux-Kommandozeile

## Teil 1: MySQL Datenbank einrichten

### 1.1 Datenbank erstellen

1. Loggen Sie sich in PythonAnywhere ein
2. Gehen Sie zum Tab **"Databases"**
3. Unter "MySQL" klicken Sie auf **"Initialize MySQL"** (falls noch nicht geschehen)
4. Setzen Sie ein MySQL-Passwort und merken Sie es sich
5. Erstellen Sie eine neue Datenbank mit dem Namen: `yourusername$crm_db`
   - Ersetzen Sie `yourusername` mit Ihrem PythonAnywhere-Benutzernamen
   - Beispiel: Wenn Ihr Username `maxmuster` ist, dann: `maxmuster$crm_db`

### 1.2 Datenbankverbindung notieren

Ihre MySQL-Verbindungsdaten:
```
Host: yourusername.mysql.pythonanywhere-services.com
Benutzername: yourusername
Passwort: [Ihr MySQL-Passwort]
Datenbankname: yourusername$crm_db
```

## Teil 2: Projekt hochladen

### 2.1 Dateien über Dashboard hochladen

1. Gehen Sie zum Tab **"Files"**
2. Navigieren Sie zu Ihrem Home-Verzeichnis (z.B. `/home/yourusername/`)
3. Erstellen Sie einen neuen Ordner namens `crm_app`
4. Laden Sie alle Projektdateien in diesen Ordner hoch

**ODER**

### 2.2 Via Bash Console (empfohlen)

1. Öffnen Sie eine **Bash Console** (Tab "Consoles" → "Bash")
2. Laden Sie das Projekt herunter (wenn Sie es auf GitHub haben):

```bash
cd ~
git clone https://github.com/IhrUsername/crm_app.git
cd crm_app
```

**ODER** erstellen Sie die Struktur manuell:

```bash
cd ~
mkdir -p crm_app/views
mkdir -p crm_app/templates
mkdir -p crm_app/static
mkdir -p crm_app/migrations
cd crm_app
```

Dann kopieren Sie alle Dateien über das Files-Dashboard in die entsprechenden Ordner.

## Teil 3: Virtual Environment und Dependencies

### 3.1 Virtual Environment erstellen

```bash
cd ~/crm_app
python3.10 -m venv venv
source venv/bin/activate
```

### 3.2 Dependencies installieren

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Erstellen Sie `requirements.txt` mit diesem Inhalt (falls noch nicht vorhanden):

```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
PyMySQL==1.1.0
cryptography==41.0.7
python-dotenv==1.0.0
```

## Teil 4: Umgebungsvariablen konfigurieren

### 4.1 .env Datei erstellen

Erstellen Sie eine Datei `.env` im Hauptverzeichnis (`~/crm_app/.env`):

```bash
nano ~/crm_app/.env
```

Fügen Sie folgendes ein (passen Sie die Werte an):

```bash
SECRET_KEY=ihr-sehr-sicherer-geheimer-schluessel-hier
DATABASE_URL=mysql+pymysql://yourusername:yourpassword@yourusername.mysql.pythonanywhere-services.com/yourusername$crm_db
```

**Wichtig:**
- Ersetzen Sie `yourusername` mit Ihrem PythonAnywhere-Benutzernamen
- Ersetzen Sie `yourpassword` mit Ihrem MySQL-Passwort
- Generieren Sie einen sicheren SECRET_KEY (z.B. mit `python -c "import secrets; print(secrets.token_hex(32))"`)

Speichern Sie mit `CTRL+X`, dann `Y`, dann `Enter`.

## Teil 5: Datenbank initialisieren

### 5.1 Tabellen erstellen und Beispieldaten einfügen

```bash
cd ~/crm_app
source venv/bin/activate
python migrations/init_db.py
```

Sie sollten eine Ausgabe wie diese sehen:
```
=== CRM Datenbank-Initialisierung ===

Erstelle Datenbanktabellen...
✓ Tabellen erfolgreich erstellt!
Füge Beispieldaten ein...
✓ 4 Benutzer erstellt
✓ 10 Produkte erstellt
✓ 15 Kunden erstellt
✓ 60 Bestellungen erstellt
...
```

## Teil 6: Web App konfigurieren

### 6.1 Web App erstellen

1. Gehen Sie zum Tab **"Web"**
2. Klicken Sie auf **"Add a new web app"**
3. Wählen Sie Ihre Domain (z.B. `yourusername.pythonanywhere.com`)
4. Wählen Sie **"Manual configuration"**
5. Wählen Sie **Python 3.10**

### 6.2 WSGI-Konfigurationsdatei bearbeiten

1. Auf der Web-App-Seite finden Sie den Link zur WSGI-Konfigurationsdatei
2. Klicken Sie darauf und **löschen Sie den gesamten Inhalt**
3. Fügen Sie folgenden Code ein:

```python
import sys
import os
from dotenv import load_dotenv

# Pfad zum Projekt
path = '/home/yourusername/crm_app'
if path not in sys.path:
    sys.path.insert(0, path)

# .env Datei laden
load_dotenv(os.path.join(path, '.env'))

# Flask App importieren
from app import app as application
```

**Wichtig:** Ersetzen Sie `yourusername` mit Ihrem tatsächlichen Benutzernamen!

4. Klicken Sie auf **"Save"**

### 6.3 Virtual Environment verknüpfen

1. Auf der Web-App-Seite scrollen Sie zu **"Virtualenv"**
2. Geben Sie den Pfad ein: `/home/yourusername/crm_app/venv`
3. Klicken Sie auf das Häkchen zum Speichern

### 6.4 Static Files konfigurieren

1. Scrollen Sie zu **"Static files"**
2. Fügen Sie einen neuen Eintrag hinzu:
   - **URL:** `/static/`
   - **Directory:** `/home/yourusername/crm_app/static/`

### 6.5 Reload der Web App

Klicken Sie oben rechts auf den grünen Button **"Reload yourusername.pythonanywhere.com"**

## Teil 7: Testen

### 7.1 Website aufrufen

Öffnen Sie in Ihrem Browser: `https://yourusername.pythonanywhere.com`

Sie sollten die CRM-Startseite mit drei Übersichten sehen:
- Übersicht Kunden
- Übersicht Bestellungen
- Übersicht Kontakte

### 7.2 Funktionalität testen

Testen Sie folgende Features:
- ✅ Startseite mit 3 Übersichten
- ✅ Suche nach Kunden
- ✅ Kundendetails mit KPIs anzeigen
- ✅ Datumsbereich-Filter für Umsatz
- ✅ Tabs (Bestellungen, Kontakte, Stammdaten)
- ✅ Globale Bestellübersicht mit Suche
- ✅ Globale Kontaktübersicht mit Kanalfilter

## Teil 8: Fehlerbehebung

### Problem: "502 Bad Gateway"

**Lösung:**
1. Prüfen Sie die Error-Logs: Web-Tab → Log files → Error log
2. Stellen Sie sicher, dass der WSGI-Pfad korrekt ist
3. Prüfen Sie, ob die Virtual Environment richtig verknüpft ist

### Problem: "Database connection error"

**Lösung:**
1. Prüfen Sie die `.env` Datei auf Tippfehler
2. Verifizieren Sie Ihre MySQL-Zugangsdaten im Databases-Tab
3. Stellen Sie sicher, dass der Datenbankname das Format `username$dbname` hat

### Problem: "Module not found"

**Lösung:**
```bash
cd ~/crm_app
source venv/bin/activate
pip install -r requirements.txt
```

Dann Reload der Web App.

### Problem: "Static files (CSS) werden nicht geladen"

**Lösung:**
1. Überprüfen Sie die Static Files Konfiguration im Web-Tab
2. Stellen Sie sicher, dass der Pfad `/home/yourusername/crm_app/static/` korrekt ist
3. Reload der Web App

### Logs überprüfen

Bei Problemen können Sie die Logs einsehen:
1. Web-Tab → Log files
2. **Error log:** Zeigt Python-Fehler
3. **Server log:** Zeigt Web-Server-Aktivität
4. **Access log:** Zeigt alle Anfragen

## Teil 9: Wartung und Updates

### Code aktualisieren

```bash
cd ~/crm_app
source venv/bin/activate
# Änderungen vornehmen oder git pull
# Dann:
```

Reload der Web App im Web-Tab.

### Datenbank zurücksetzen

**WARNUNG: Dies löscht alle Daten!**

```bash
cd ~/crm_app
source venv/bin/activate
python migrations/reset_db.py  # Falls Sie dieses Script erstellt haben
# ODER manuell:
python
>>> from app import app, db
>>> with app.app_context():
>>>     db.drop_all()
>>>     db.create_all()
>>> exit()

python migrations/init_db.py
```

### Neue Beispieldaten hinzufügen

```bash
cd ~/crm_app
source venv/bin/activate
python migrations/init_db.py  # Fügt nur Daten hinzu, wenn DB leer ist
```

## Teil 10: Produktiv-Deployment (Optional)

Für ein produktives System:

### 10.1 Sicherheit verbessern

1. **Starken SECRET_KEY generieren:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

2. **HTTPS erzwingen** (standardmäßig aktiv auf PythonAnywhere)

3. **Datenbank-Backups** regelmäßig erstellen (MySQL-Tab → Download)

### 10.2 Performance optimieren

1. Upgrade auf einen kostenpflichtigen PythonAnywhere-Account für mehr CPU
2. Database-Indizes sind bereits optimiert (in models.py definiert)
3. Implementieren Sie Caching bei Bedarf

### 10.3 Monitoring

Überwachen Sie regelmäßig:
- CPU-Auslastung (Dashboard)
- Disk Space (Files-Tab)
- Error logs (Web-Tab)

## Zusammenfassung der Pfade

Hier alle wichtigen Pfade auf einen Blick (ersetzen Sie `yourusername`):

```
Projektordner:       /home/yourusername/crm_app/
Virtual Environment: /home/yourusername/crm_app/venv/
Static Files:        /home/yourusername/crm_app/static/
.env Datei:          /home/yourusername/crm_app/.env
WSGI Config:         (über Web-Tab zugänglich)
Database Host:       yourusername.mysql.pythonanywhere-services.com
Database Name:       yourusername$crm_db
```

## Support

Bei Problemen:
1. Prüfen Sie die Error Logs
2. Konsultieren Sie die [PythonAnywhere Help Pages](https://help.pythonanywhere.com/)
3. Überprüfen Sie die Flask-Dokumentation: [flask.palletsprojects.com](https://flask.palletsprojects.com/)

## Checkliste für erfolgreiches Deployment

- [ ] MySQL-Datenbank erstellt
- [ ] Projekt-Dateien hochgeladen
- [ ] Virtual Environment erstellt und Dependencies installiert
- [ ] .env Datei mit korrekten Zugangsdaten erstellt
- [ ] Datenbank initialisiert (init_db.py ausgeführt)
- [ ] Web App erstellt und WSGI konfiguriert
- [ ] Virtual Environment in Web App verknüpft
- [ ] Static Files konfiguriert
- [ ] Web App reloaded
- [ ] Website im Browser getestet
- [ ] Alle Features funktionieren

---

**Viel Erfolg mit Ihrem CRM-System! 🚀**