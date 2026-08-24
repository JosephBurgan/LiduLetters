# Lidu Letters

Mobile-first site for letterboard Q&A: speech-bubble home, browse by topic / event / date, and a short About page.

**Live (share this):** https://josephburgan.github.io/LiduLetters/

**Stage QR:** `qr-code.png`  
(Optionally regenerated with a `?v=...` query when you need phones to skip an old cached build.)

**Design intent / feedback log:** see [`DESIGN-NOTES.md`](./DESIGN-NOTES.md)

## Local preview

Open `index.html` in a browser, or:

```bash
npx --yes serve .
```

## Admin

Public UI has no admin button. Open:

`https://josephburgan.github.io/LiduLetters/#admin`

Q&A lives in [`data.json`](./data.json) so every device loads the same list.

### Multiple people adding entries (no shared token)

Do **not** put the GitHub token in the website. Invite people as **collaborators** instead:

1. [Invite collaborators](https://github.com/JosephBurgan/LiduLetters/settings/access)
2. They open `#admin`, fill **Add entry**, hit **Save**
3. GitHub opens an issue draft — they click **Submit**
4. A GitHub Action appends `data.json` and the live site updates

Only **OWNER / collaborator** issues are ingested (so random public issues cannot write the site).

### Instant publish from one computer (optional token)

For the machine that should write the repo directly (usually Joseph’s desktop):

1. Fine-grained token, repo **LiduLetters only**, **Contents: Read and write**
2. Admin → paste token → **Save token on this device**
3. **Save** on an entry publishes immediately

GitHub Pages can take a short minute to update.

## Project layout

| File | Role |
|------|------|
| `index.html` | App (HTML / CSS / JS) |
| `data.json` | Shared Q&A list (source of truth on the live site) |
| `qr-code.png` | Stage QR → live URL |
| `DESIGN-NOTES.md` | Why the UX is the way it is |
| `README.md` | This file |
