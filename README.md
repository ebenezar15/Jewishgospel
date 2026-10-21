# The Hebrew Lens

An interactive study app that explains two books in plain language:

1. **Lost in Translation**: 15 Hebrew words (Shalom, Nahash, Qorban, Dam, Brit, Ezer, Kadosh, Shachah, Sane, Naqam, Shevet, Ge-Hinnom, Yir'ah, Emunah, Aphar).
2. **The Gospel Before Christianity**: atonement, sacrifice, salvation, judgment and redemption read through Jewish eyes, in six parts.

Every topic has a plain-English explanation, an animated "skeleton" of the argument, flowcharts and other diagrams,
key passages, take-aways, reflection questions and a quiz. There are also flashcards, a big-picture map, a glossary,
search, read-aloud, progress tracking and seven colour schemes with light/dark mode.

## Use it

- **Download:** [`index.html`](index.html) is the whole app in one file. Download it and open it in any browser,
  on a phone, tablet or computer. It works offline.
- **Install as an app:** enable GitHub Pages (Settings → Pages → Deploy from branch → `main` / root). Then open
  `https://<user>.github.io/<repo>/` and use "Add to Home Screen" (iPhone/iPad) or "Install app" (Android, Chrome, Edge).

## Edit

Content lives in `content/*.json`; the app shell is `src/app.html`. Rebuild with:

```sh
python3 build.py
```
