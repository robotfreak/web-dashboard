# Web Dashboard

Ein flexibles, dark-themed Dashboard für Self-Hosted Services mit Health Checks.

![Dashboard Screenshot](screenshot.png)

---

## ✨ FEATURES

- **🎨 Dark Theme** — Angenehm für die Augen
- **⚡ Health Checks** — Automatische Status-Prüfung aller Services
- **📊 Kategorien** — Services gruppiert nach Typ (Projects, Infrastructure, Tools, Monitoring)
- **🏷️ Tags** — Schnelle Identifikation der Technologie
- **🔄 Auto-Refresh** — Status aktualisiert sich automatisch
- **📱 Responsive** — Funktioniert auf Desktop, Tablet und Mobile
- **🔧 Flexibel** — Einfach per YAML konfigurierbar

---

## 🚀 SCHNELLSTART

### **1. Repository klonen:**

```bash
git clone https://github.com/robotfreak/web-dashboard.git
cd web-dashboard
```

### **2. Python Virtual Environment einrichten:**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **3. Konfiguration anpassen:**

```bash
cp config.yaml.example config.yaml
# config.yaml nach Bedarf bearbeiten
```

### **4. Dashboard starten:**

```bash
# Manuell (Development):
python app.py

# Oder mit Systemd (Production):
sudo systemctl enable ki-os-dashboard.service
sudo systemctl start ki-os-dashboard
```

### **5. Öffnen im Browser:**

```
http://localhost:8050
```

---

## 📋 KONFIGURATION

### **config.yaml Aufbau:**

```yaml
services:
  - name: "Service Name"
    url: "http://ip:port"
    icon: "icon-name"
    category: "Projects"
    description: "Kurze Beschreibung"
    health_endpoint: "/api/health"  # Optional
    tags: ["tag1", "tag2"]

categories:
  - "Projects"
  - "Infrastructure"
  - "Tools"
  - "Monitoring"

dashboard:
  title: "Mein Dashboard"
  subtitle: "Meine Services"
  refresh_interval: 60
  theme: "dark"
  show_status: true
  show_tags: true
```

### **Verfügbare Icons:**

- `inventory` — Lagerverwaltung
- `makerspace` — Makerspace Logger
- `spool` — Spool/Filament
- `openscad` — 3D CAD
- `wordpress` — WordPress
- `tailscale` — Tailscale VPN
- `github` — GitHub
- `obsidian` — Obsidian Vault
- `terminal` — Terminal/CLI
- `cockpit` — Cockpit Web Console
- `raspberry` — Raspberry Pi
- `server` — Allgemeiner Server
- `database` — Datenbank
- `cloud` — Cloud Service

---

## 🔧 SYSTEMD SERVICE

### **Installation:**

```bash
# Service-Datei anpassen (Pfade!)
sudo nano /etc/systemd/system/ki-os-dashboard.service

# Inhalt anpassen:
# - WorkingDirectory auf deinen Pfad setzen
# - User anpassen (pi oder dein User)

# Service installieren:
sudo systemctl daemon-reload
sudo systemctl enable ki-os-dashboard
sudo systemctl start ki-os-dashboard

# Status prüfen:
systemctl status ki-os-dashboard
```

### **Service-Template (`ki-os-dashboard.service`):**

```ini
[Unit]
Description=KI-OS Dashboard
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/ki-os-dashboard
ExecStart=/home/pi/ki-os-dashboard/venv/bin/python app.py
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```

---

## 📦 SUBMODULE NUTZUNG

### **In einem anderen Projekt einbinden:**

```bash
# In dein Projekt-Repo wechseln
cd /path/to/dein/projekt

# Dashboard als Submodule hinzufügen
git submodule add https://github.com/robotfreak/web-dashboard.git dashboard

# Ins Dashboard wechseln
cd dashboard

# Konfiguration für dieses Projekt erstellen
cp config.yaml.example config.yaml
# config.yaml bearbeiten (Services für dieses Projekt)

# Commiten
git add .
git commit -m "Dashboard als Submodule hinzugefügt"
```

### **Dashboard updaten:**

```bash
# In allen Projekten die das Submodule nutzen:
cd dashboard
git pull origin main

# Oder im Hauptrepo:
git submodule update --remote
```

### **Beispiel-Projekte:**

- **KI-OS** → `ki-os/dashboard/` (KI-OS Services)
- **Makerspace** → `makerspace/dashboard/` (Makerspace Services)
- **Repair-Café** → `repair-cafe/dashboard/` (Repair-Café Services)

Jedes Projekt hat seine **eigene `config.yaml`** mit projekt-spezifischen Services!

---

## 🎨 ANPASSUNGEN

### **Farben ändern (in `templates/index.html`):**

```css
:root {
    --bg-primary: #0f0f1a;      /* Hintergrund */
    --bg-secondary: #1a1a2e;    /* Karten */
    --text-primary: #ffffff;    /* Text */
    --accent: #4a9eff;          /* Akzentfarbe */
}
```

### **Eigene Icons hinzufügen:**

1. SVG-Icon in `static/icons/` speichern
2. In `templates/index.html` Icon-Namen registrieren
3. In `config.yaml` verwenden

---

## 📊 HEALTH CHECKS

Das Dashboard prüft automatisch alle `http://` und `https://` Services:

- **online** ✅ — Service antwortet mit Status < 500
- **offline** ❌ — Service antwortet nicht oder mit Fehler 500+
- **local** 📁 — `file://` oder `terminal://` URLs (nicht prüfbar)

**Health Endpoint:** Standardmäßig `/api/health`, kann pro Service angepasst werden.

---

## 🔒 SICHERHEIT

### **Empfohlene Einstellungen:**

1. **Nur im lokalen Netz** — Dashboard nicht öffentlich exponieren
2. **Tailscale VPN** — Zugriff nur über VPN (z.B. `100.x.x.x:8050`)
3. **Firewall** — Port 8050 nur für vertrauenswürdige IPs freigeben
4. **Keine sensiblen Daten** — Keine API-Keys oder Passwörter in config.yaml

### **Beispiel: UFW Firewall (nur Tailscale):**

```bash
sudo ufw allow from 100.0.0.0/8 to any port 8050
sudo ufw deny 8050
```

---

## 🛠️ ENTWICKLUNG

### **Dependencies:**

```txt
Flask==3.0.0
PyYAML==6.0.1
requests==2.31.0
```

### **Projektstruktur:**

```
ki-os-dashboard/
├── app.py                  # Flask App (Kern-Logik)
├── config.yaml.example     # Konfigurations-Vorlage
├── config.yaml             # Projekt-spezifische Config (nicht committen!)
├── requirements.txt        # Python Dependencies
├── web-dashboard.service   # Systemd Service-Datei
├── README.md              # Diese Datei
├── templates/
│   └── index.html         # HTML Template (Dark Theme)
├── static/
│   └── icons/             # SVG Icons (optional)
└── venv/                  # Python Virtual Environment
```

---

## 📝 CHANGELOG

### **v1.0.0 (2026-09-05)**
- ✅ Erstes Release
- ✅ Dark Theme UI
- ✅ Health Checks für alle Services
- ✅ Kategorien und Tags
- ✅ Auto-Refresh
- ✅ Systemd Service
- ✅ Submodule-fähig
- ✅ Umbenennung zu `web-dashboard`

---

## 🤝 BEITRAGEN

Fehler gefunden oder Feature-Wunsch?

1. Issue auf GitHub erstellen
2. Oder Pull Request schicken

---

## 📞 SUPPORT

**GitHub Issues:** https://github.com/robotfreak/web-dashboard/issues

**Dokumentation:** Siehe README.md

---

## 📄 LIZENZ

MIT License — Frei nutzbar, änderbar und weiterverteilbar.

---

**Viel Spaß mit deinem Dashboard!** (◕‿◕) ✨
