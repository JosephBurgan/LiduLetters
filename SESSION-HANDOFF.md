# Session handoff — Lidu Letters

**Date left:** 2026-08-24  
**Live site:** https://josephburgan.github.io/LiduLetters/  
**Repo:** `JosephBurgan/LiduLetters` (GitHub Pages from `main`)  
**Local clone:** `C:\Users\Joseph\Documents\LiduLetters`

Read this first, then `DESIGN-NOTES.md` (UX decisions — do not re-litigate unless Joseph asks).

---

## Goal of the next session

**Connect Google Sheets (and Form) so multiple people can add Q&A without GitHub tokens**, and Joseph can edit a spreadsheet easily.

Desired loop:

1. Helpers fill a **Google Form** (phone-friendly).
2. Responses land in a **Google Sheet** Joseph can edit like a normal spreadsheet.
3. The live site stays in sync (sheet → `data.json` on GitHub, or Grok writes `data.json` from the sheet in-session).

Joseph will try to add **Google Sheets MCP** in a **new Grok session** (`/mcps`). Calendar is already connected in Grok Build; **that does not include Sheets**. Sheets needs its own OAuth.

If Sheets MCP is available in the new session:

- Create a spreadsheet named **Lidu Letters** with the column headers below (or confirm one Joseph already made).
- Optionally create/link a Google Form that writes to that sheet (Forms MCP may still be missing — Form can be created in the browser using `GOOGLE-FORM.md`).
- Put `formUrl` + `csvUrl` into `google-sheet.json` and push.
- Confirm GitHub Action **Sync Google Sheet** can pull CSV → `data.json`, or pull live via MCP and commit `data.json`.
- Show **Add a letter** on the home page (already wired; appears when `formUrl` is set).

If Sheets MCP is **not** connected: walk Joseph through `/mcps` / Google consent, or fall back to him creating the Form in the browser and pasting the two URLs.

---

## What is already shipped (do not rebuild)

Mobile-first letterboard site: Home bubbles → About → Browse. Sonic blue / purple / dark theme.

| Piece | Status |
|---|---|
| Home: speech bubbles, letterboard backdrop, `LIDU LETTERS` spell-in | Done |
| Browse: topic/event/date filters, search, optional meta checkbox | Done |
| About Lidu (Acid For Squares + Telepathy Tapes, trimmed copy) | Done |
| Admin `#admin` (not public `+`) | Done |
| `data.json` as public source of truth | Done |
| Optional GitHub token publish (Joseph’s desktop only) | Done — token stays in **that browser**, never in the repo |
| Collaborator → GitHub issue → Action ingest | Done — heavier than Joseph wants for helpers |
| Google Form/Sheet **plumbing** | Done — waiting on real Form/Sheet URLs |
| UX notes | `DESIGN-NOTES.md` |

**Share URL for feedback:** https://josephburgan.github.io/LiduLetters/  
(No `?v=` for other people. Use a cache-bust query only when Joseph’s phone is stuck on an old Pages build.)

---

## Google Form / Sheet contract

Exact Form question titles (see `GOOGLE-FORM.md`):

| Title | Type |
|---|---|
| Question | Paragraph, required |
| Answer | Paragraph, required |
| Date | Date |
| Event name | Short answer |
| Location | Short answer |
| Tags | Short answer (commas) |
| Show on home page | Yes / No |
| More / references | Paragraph |

Config file: `google-sheet.json`

```json
{
  "formUrl": "https://docs.google.com/forms/d/e/..../viewform",
  "csvUrl": "https://docs.google.com/spreadsheets/d/e/..../pub?output=csv"
}
```

Sync: `scripts/sync_sheet.py` + `.github/workflows/sync-sheet.yml` (cron every 15 min + manual **Actions → Sync Google Sheet → Run workflow**).

Sheet must be **anyone with the link can view** and **published to the web as CSV**.

---

## Why GitHub token is not “for everyone on #admin”

A token in the public page = anyone can rewrite the repo.  
Multiple helpers should use **Form/Sheet**, not a shared PAT.

Joseph may still paste a fine-grained PAT on **his** desktop for instant `#admin` publish (`Contents: Read and write` on `LiduLetters` only). Optional once the sheet is live.

---

## Known bugs / gotchas (fixed unless they regress)

- Home title going invisible after leaving mid-spell: do **not** measure title gradient while Home is `display:none`; re-spell on every visit to Home; do **not** re-spell on “Show different bubbles”.
- Letterboard first paint must never be full opacity (~6–8% white, square cells centered, grow from page center).
- Browse two columns at ≥1280px must be **two independent stacks**, not one CSS grid of shared rows.
- Expanded bubble: center of the bubble stage; dim overlay full viewport.
- Desktop bubbles: field ~460px wide (near footer buttons), not full 720+.

---

## Key files

| File | Role |
|---|---|
| `index.html` | Entire app |
| `data.json` | Live Q&A list |
| `google-sheet.json` | Form + CSV URLs (empty until Joseph creates them) |
| `GOOGLE-FORM.md` | Human setup for Form/Sheet |
| `scripts/sync_sheet.py` | CSV → `data.json` |
| `.github/workflows/sync-sheet.yml` | Scheduled/manual sync |
| `.github/workflows/ingest-qa.yml` | Collaborator issue ingest (legacy helper path) |
| `DESIGN-NOTES.md` | Product/UX rationale |
| `qr-code.png` | Stage QR |

Admin: `https://josephburgan.github.io/LiduLetters/#admin`

---

## Suggested first prompt in the new session

> Continue Lidu Letters from `C:\Users\Joseph\Documents\LiduLetters\SESSION-HANDOFF.md`. Goal: hook Google Sheets (MCP if available) and a Google Form so multiple people can add Q&A into a Sheet I can edit, and the live site stays in sync. Don’t redo the UI unless something is broken.

If Sheets tools exist, use them. If not, say so and help connect `/mcps`.
