# She's Viral - Content Creator Tool

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

## 📁 Projektstruktur

```
frontend/
├── src/
│   ├── data/
│   │   └── contentData.json    # Alle Content-Daten (Hooks, Scripts, Styles)
│   ├── components/ui/          # UI Komponenten
│   ├── App.js                  # Hauptkomponente
│   └── ...
├── package.json
└── README.md
```

## 📝 Daten bearbeiten

Alle Inhalte (Visual Styles, Hooks, Scripts) befinden sich in:
```
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
