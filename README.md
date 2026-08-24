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

Q&A lives in [`data.json`](./data.json) so every device loads the same list. Saving in admin **publishes** that file to GitHub (needs a token).

### One-time token (so phones see new entries)

1. GitHub → Settings → Developer settings → Personal access tokens → **Fine-grained token**
2. Resource owner: your account; Repository: **LiduLetters only**
3. Permissions: **Contents: Read and write**
4. Paste it in Admin → Save token on this device (stays in this browser only)
5. **Save & publish** on an entry, or **Publish now** to send unpublished local entries live

GitHub Pages can take a short minute to update.

## Project layout

| File | Role |
|------|------|
| `index.html` | App (HTML / CSS / JS) |
| `data.json` | Shared Q&A list (source of truth on the live site) |
| `qr-code.png` | Stage QR → live URL |
| `DESIGN-NOTES.md` | Why the UX is the way it is |
| `README.md` | This file |
