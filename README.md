# The Hebrew Lens

An interactive study app that explains two books in plain language:

1. **Lost in Translation**: 15 Hebrew words (Shalom, Nahash, Qorban, Dam, Brit, Ezer, Kadosh, Shachah, Sane, Naqam, Shevet, Ge-Hinnom, Yir'ah, Emunah, Aphar).
2. **The Gospel Before Christianity**: atonement, sacrifice, salvation, judgment and redemption read through Jewish eyes, in six parts.

Every topic has a plain-English explanation, an animated "skeleton" of the argument, flowcharts and other diagrams,
key passages, take-aways, reflection questions and a quiz. There are also flashcards, a big-picture map, a glossary,
search, read-aloud, progress tracking and seven colour schemes with light/dark mode.

The whole app is available in **English and Tamil (தமிழ்)**. Switch with the EN | தமிழ் control in the top-right corner;
the choice and your reading progress are remembered.

## Use it

- **Download:** [`index.html`](index.html) is the whole app in one file. Download it and open it in any browser,
  on a phone, tablet or computer. It works offline.
- **Install as an app:** enable GitHub Pages (Settings → Pages → Deploy from branch → `main` / root). Then open
  `https://<user>.github.io/<repo>/` and use "Add to Home Screen" (iPhone/iPad) or "Install app" (Android, Chrome, Edge).

## Edit

Content lives in `content/*.json` (English) and `content/ta/*.json` (Tamil, same structure); the app shell and
interface text for both languages are in `src/app.html`. Check a Tamil file with
`python3 tools/check_ta.py content/<file>.json content/ta/<file>.json`. Rebuild with:

```sh
python3 build.py
```
