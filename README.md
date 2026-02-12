# She's Viral - Content Creator Tool

<<<<<<< HEAD
Ein Frontend-Tool zur Erstellung von TikTok Content. Alle Daten werden lokal geladen - kein Backend-Server mehr erforderlich!

## 🚀 Schnellstart

Gehe ins Frontend-Verzeichnis und starte die App:

```bash
cd frontend
yarn install
yarn start
```

Die App läuft auf [http://localhost:3000](http://localhost:3000)
=======
Ein reines Frontend-Tool zur Erstellung von TikTok Content. Alle Daten werden lokal im Browser geladen - kein Backend-Server erforderlich!

## 🚀 Schnellstart

### Voraussetzungen
- Node.js (v18 oder höher)
- Yarn Package Manager

### Installation & Start

1. **Abhängigkeiten installieren:**
   ```bash
   yarn install
   ```

2. **Development Server starten:**
   ```bash
   yarn start
   ```

3. **Im Browser öffnen:**
   Die App läuft automatisch auf [http://localhost:3000](http://localhost:3000)
>>>>>>> ff5226ce448e6cbd1648b5898524a64b38efadc3

## 📁 Projektstruktur

```
<<<<<<< HEAD
├── frontend/           # React Frontend (reine Frontend-Anwendung)
│   ├── src/data/      # Alle Content-Daten als JSON
│   └── ...
├── backend/           # [VERALTET] Wird nicht mehr benötigt
=======
frontend/
├── src/
│   ├── data/
│   │   └── contentData.json    # Alle Content-Daten (Hooks, Scripts, Styles)
│   ├── components/ui/          # UI Komponenten
│   ├── App.js                  # Hauptkomponente
│   └── ...
├── package.json
>>>>>>> ff5226ce448e6cbd1648b5898524a64b38efadc3
└── README.md
```

## 📝 Daten bearbeiten

Alle Inhalte (Visual Styles, Hooks, Scripts) befinden sich in:
```
<<<<<<< HEAD
frontend/src/data/contentData.json
```

## 📖 Detaillierte Anleitung

Siehe [frontend/README.md](frontend/README.md) für mehr Details.

## Änderungen (Feb 2025)

- ✅ Kein Backend-Server mehr nötig
- ✅ Alle Daten in `contentData.json` 
- ✅ Einfacheres Deployment
- ✅ Schnellerer Start
=======
src/data/contentData.json
```

Bearbeite einfach diese Datei, um neue Inhalte hinzuzufügen oder bestehende zu ändern.

### Datenstruktur

**Visual Styles:**
```json
{
  "id": "vs1",
  "title": "Style Name",
  "images": ["url1", "url2"],
  "info": "Beschreibung"
}
```

**Hooks:**
```json
{
  "id": "h1",
  "category": "Ex TikTok",
  "idea": "Hook text...",
  "reference_links": "-",
  "notes": null
}
```

**Scripts:**
```json
{
  "id": "s1",
  "type": "other",  // "other", "engagement", oder "viral_plug"
  "paragraph1": "Erster Absatz...",
  "paragraph2": "Zweiter Absatz...",
  "notes": null
}
```

## 🛠 Verfügbare Scripts

- `yarn start` - Development Server starten
- `yarn build` - Production Build erstellen
- `yarn test` - Tests ausführen

## 🎨 Features

- **4-Schritt Content Creator:**
  1. Visual Style auswählen
  2. Hook auswählen
  3. 5 Scripts auswählen
  4. Zusammenfassung & Kopieren

- **Kein Backend nötig** - Alle Daten lokal
- **Responsive Design** - Funktioniert auf Desktop & Mobile
- **Copy-to-Clipboard** - Einfaches Kopieren der ausgewählten Inhalte

## 📄 Lizenz

Private Nutzung
>>>>>>> ff5226ce448e6cbd1648b5898524a64b38efadc3
