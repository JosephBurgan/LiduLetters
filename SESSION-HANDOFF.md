# Session handoff — Lidu Letters

**Date left:** 2026-08-24 (evening)  
**Live site:** https://josephburgan.github.io/LiduLetters/  
**Repo:** `JosephBurgan/LiduLetters` (GitHub Pages from `main`)  
**Local clone:** `C:\Users\Joseph\Documents\LiduLetters`  
**Latest commit:** `0d578ab` — Add sheet seed CSV and refuse sync that would drop letters

Read this first, then `DESIGN-NOTES.md` (UX decisions — do not re-litigate unless Joseph asks). **Do not redo the UI unless something is broken.**

---

## Why this is a new session

Joseph connected **Google Drive** in Grok Build (`/mcps`). The previous session started *before* that OAuth, so Drive tools never appeared there — only `google_calendar`. Calendar OAuth does **not** include Drive/Sheets.

This new session should see Drive tools (`google_drive_search` or similar). Confirm with `search_tool` for Drive **before** asking Joseph to reconnect.

There is still **no Google Forms MCP**. The Form is created in the browser (`GOOGLE-FORM.md`). Drive is for the spreadsheet half.

---

## Goal of this session

**Create the Lidu Letters Google Sheet, link a Google Form, put URLs in the repo, keep the live site in sync.**

Desired loop:

1. Helpers fill a **Google Form** (phone-friendly).
2. Responses land in a **Google Sheet** Joseph can edit like a normal spreadsheet.
3. GitHub Action copies the published CSV into `data.json` (~every 15 min, or manual **Actions → Sync Google Sheet**). Optionally Grok can also pull via Drive MCP and commit `data.json`.

### If Drive MCP tools exist (expected)

1. Search Drive for an existing spreadsheet named **Lidu Letters**. Reuse it if it already has the right headers; do not create a duplicate.
2. If none: create spreadsheet **Lidu Letters** with headers (exact titles):

   `Id | Question | Answer | Date | Event name | Location | Tags | Show on home page | More / references`

   (`Timestamp` may appear later if a Form is linked — extra columns are ignored by sync.)
3. Seed the 24 existing letters from `sheet-seed.csv` (or `data.json`). **Required before first sync** — otherwise one Form row would replace the live board. Sync now **refuses** to shrink `data.json` unless the workflow is run with **allow_shrink**.
4. Make the sheet readable for GitHub: anyone-with-link **Viewer**, plus **File → Share → Publish to the web → CSV**. Copy the `/pub?output=csv` URL.
5. Google Form: Joseph still creates it in the browser (no Forms MCP). Questions must match `GOOGLE-FORM.md` titles. Responses tab → link to **this** spreadsheet (not a second new one) if Google offers that.
6. Write `formUrl` + `csvUrl` into `google-sheet.json` and push `main`.
7. Run **Sync Google Sheet** (or pull via MCP and commit `data.json` if the published CSV is not ready yet). Confirm row count ≥ 24.
8. After Pages updates, **Add a letter** appears on Home and About (`loadSheetConfig` already wired; hidden until `formUrl` is set).

### If Drive MCP is still missing

Say so immediately. `/mcps` → Google Drive enabled + `i` if unauthenticated → `r` refresh. Do not walk through Calendar again. Fallback: Joseph creates Form+Sheet in the browser per `GOOGLE-FORM.md` and pastes the two URLs.

---

## What shipped last session (do not redo)

| Piece | Status |
|---|---|
| Site UI / letterboard / Browse / About / `#admin` | Done — do not restyle |
| `data.json` (24 letters) | Done — live source of truth until sheet takes over |
| Form/Sheet **plumbing** | Done — `google-sheet.json` still empty URLs |
| `sheet-seed.csv` | Done — 24 rows, Form column order, with **Id** |
| Sync shrink-guard | Done — `scripts/sync_sheet.py` exits 1 if sheet has fewer rows than `data.json` unless `ALLOW_SHRINK=1` |
| Workflow input `allow_shrink` | Done — `.github/workflows/sync-sheet.yml` |
| `GOOGLE-FORM.md` | Updated with seed + publish steps |

**Share URL:** https://josephburgan.github.io/LiduLetters/  
(No `?v=` for other people.)

---

## Google Form / Sheet contract

Exact Form question titles (`GOOGLE-FORM.md`):

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

Extra sheet column **Id** (not a Form question): keep existing ids 1–24. New Form rows can leave Id blank; sync assigns `1000 + row index`.

Config (`google-sheet.json` — still empty):

```json
{
  "formUrl": "https://docs.google.com/forms/d/e/..../viewform",
  "csvUrl": "https://docs.google.com/spreadsheets/d/e/..../pub?output=csv"
}
```

- **formUrl** — Forms Send tab (site **Add a letter** button)
- **csvUrl** — published CSV (must contain `/pub?output=csv`)
- Sheet: anyone-with-link **view** + published as CSV

Sync aliases live in `scripts/sync_sheet.py` (`question`→`q`, `event name`→`event`, `tags`→`topics`, `show on home page`→`home`, etc.).

---

## Why GitHub token is not for helpers

A token in the public page = anyone can rewrite the repo. Helpers use **Form/Sheet**. Joseph may still use a fine-grained PAT on **his** desktop `#admin` (`Contents: Read and write` on `LiduLetters` only).

---

## Known bugs / gotchas (fixed unless they regress)

- Home title going invisible after leaving mid-spell: do **not** measure title gradient while Home is `display:none`; re-spell on every visit to Home; do **not** re-spell on “Show different bubbles”.
- Letterboard first paint must never be full opacity (~6–8% white, square cells centered, grow from page center).
- Browse two columns at ≥1280px must be **two independent stacks**, not one CSS grid of shared rows.
- Expanded bubble: center of the bubble stage; dim overlay full viewport.
- Desktop bubbles: field ~460px wide (near footer buttons), not full 720+.
- First sheet sync **must not** drop the 24 letters (seed + shrink-guard).

---

## Key files

| File | Role |
|---|---|
| `index.html` | Entire app |
| `data.json` | Live Q&A list (24 entries) |
| `sheet-seed.csv` | Import/seed for the Google Sheet |
| `google-sheet.json` | Form + CSV URLs (empty until this session) |
| `GOOGLE-FORM.md` | Human Form/Sheet setup |
| `scripts/sync_sheet.py` | CSV → `data.json` |
| `.github/workflows/sync-sheet.yml` | Cron 15 min + manual, optional `allow_shrink` |
| `.github/workflows/ingest-qa.yml` | Legacy collaborator issue ingest |
| `DESIGN-NOTES.md` | Product/UX rationale |
| `qr-code.png` | Stage QR |

Admin: `https://josephburgan.github.io/LiduLetters/#admin`

---

## Suggested first prompt

> Continue Lidu Letters from `C:\Users\Joseph\Documents\LiduLetters\SESSION-HANDOFF.md`. Google Drive MCP should now be connected. Create/reuse spreadsheet **Lidu Letters**, seed it from `sheet-seed.csv`, help hook a Google Form, put `formUrl` + `csvUrl` in `google-sheet.json`, and keep the live site in sync. Don’t redo the UI unless something is broken.
