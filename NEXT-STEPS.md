# 🚀 NÄCHSTE SCHRITTE — web-dashboard Repo erstellen

## 1. GitHub Repository erstellen

Gehe auf: https://github.com/new

**Einstellungen:**
- **Repository name:** `web-dashboard`
- **Beschreibung:** "Flexibles Dark-Theme Dashboard für Self-Hosted Services mit Health Checks"
- **Sichtbarkeit:** Öffentlich (oder Privat wenn gewünscht)
- **❌ NICHT** initialisieren (kein README, kein .gitignore, keine Lizenz — das haben wir schon!)

**Erstellen klicken!**

---

## 2. Lokales Repo pushen

```bash
cd ~/ki-os/web-dashboard
git remote add origin git@github.com:robotfreak/web-dashboard.git
git push -u origin main
```

---

## 3. Als Submodule in KI-OS einbinden

Das Dashboard ist bereits im KI-OS Repo unter `web-dashboard/`.

**Option A: Als regulärer Ordner belassen**
- ✅ Einfach, funktioniert sofort
- ❌ Nicht als Submodule getrennt

**Option B: Als Submodule umwandeln (empfohlen):**

```bash
cd ~/ki-os
# Aktuelles web-dashboard entfernen (nur Git-Referenz, nicht die Dateien)
git rm --cached web-dashboard
git commit -m "refactor: web-dashboard für Submodule vorbereiten"

# Als Submodule hinzufügen
git submodule add git@github.com:robotfreak/web-dashboard.git web-dashboard
cd web-dashboard

# Config für KI-OS erstellen
cp config.yaml.example config.yaml
# config.yaml anpassen (Services für KI-OS)

# Commiten
cd ..
git add .
git commit -m "feat: web-dashboard als Submodule eingebunden"
git push
```

---

## 4. Dashboard Service ist bereits aktualisiert

```bash
# Service läuft bereits als web-dashboard.service
systemctl status web-dashboard

# Läuft auf Port 8050
curl http://localhost:8050/
```

---

## 5. In anderen Projekten einbinden (Beispiel: Makerspace)

```bash
cd ~/makerspace-logger  # Oder dein Makerspace Repo
git submodule add git@github.com:robotfreak/web-dashboard.git dashboard
cd dashboard

# Config für Makerspace erstellen
cp config.yaml.example config.yaml
# config.yaml bearbeiten für Makerspace Services

# Commiten
cd ..
git add .
git commit -m "web-dashboard als Submodule für Makerspace"
git push
```

---

## ✅ CHECKLISTE

- [ ] GitHub Repo `web-dashboard` erstellt
- [ ] Lokales Repo gepusht (`git push -u origin main`)
- [ ] In KI-OS als Submodule eingebunden (optional)
- [ ] Service läuft als `web-dashboard.service` auf Port 8050
- [ ] In anderen Projekten eingebunden (z.B. Makerspace)
- [ ] README im web-dashboard Repo aktualisiert (Screenshot?)

---

## 📝 NAMENSKONSISTENZ

| Alt (ki-os-dashboard) | Neu (web-dashboard) |
|----------------------|---------------------|
| `ki-os-dashboard/` | `web-dashboard/` |
| `ki-os-dashboard.service` | `web-dashboard.service` |
| `github.com/robotfreak/ki-os-dashboard` | `github.com/robotfreak/web-dashboard` |
| Syslog: `ki-os-dashboard` | Syslog: `web-dashboard` |

---

**Viel Erfolg!** (◕‿◕) ✨
