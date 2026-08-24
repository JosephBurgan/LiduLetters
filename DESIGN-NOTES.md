# Lidu Letters — design notes

Notes from product feedback so future sessions keep the same intent.
Shareable live URL: https://josephburgan.github.io/LiduLetters/

## Product goals

- **Mobile-first.** Primary use is scanning a stage QR on a phone.
- **Least info first.** Show the question; reveal the answer on tap; keep optional extras behind “More details” only when content exists.
- **Friendly loop.** Home bubbles → browse/filter → back to Home / change filters without dead ends.
- **Sonic blue theme** with complementary purple/green accents on a dark background.

## Navigation language

- Use **Home** everywhere for return-to-landing (not “Bubbles”, “Main Page”, or mixed labels).
- Top back controls use an iOS-style chevron + label.
- **Filters** is a control chip (slider icon + gradient), not a back-chevron — it must not look like navigation.

## Home (speech bubbles)

### Layout

- Landing is **one viewport, no page scroll**: title pinned top, footer buttons pinned bottom, bubbles only in the middle band.
- Footer order: **Show different bubbles** → **About Lidu** → **Browse all questions** (primary / highlighted).
- Bubbles are **fit-to-content**, capped ~half phone width, left/right columns with safe insets (right-side clipping was a real bug).
- Layout is **size-aware** with light jitter/stagger so it feels organic, not a rigid grid.
- Keep familiar **top breathing room** under the title; keep **bottom bubbles lifted** off the buttons (bottoms too low felt cramped).
- Do not let bubbles push footer controls off-screen.

### Interaction

- Idle bubbles gently float; float motion stays small so letters/bubbles don’t clip.
- Tap opens a **top-aligned scrollable panel** (glide to center/top). Tap (without scrolling) dismisses; scrolling keeps it open.
- Dim overlay must be **full-viewport** (`position: fixed`) — a stage-only dim left ugly side gaps.
- Expanded bubble shows **location · event · date under the answer**.
- **More details** only if `more` has real content (no empty toggle).

### Curation (`home` flag)

- Admin checkbox: **Show on the home page**.
- Home should favor questions that make sense to a first-time visitor.
- Contextual / in-crowd items stay in Browse only (examples turned off by default): closing/opening messages, “Did Lidu sense us on the Hill?”, comfort questions, etc.
- Vague titles like “Final message (Day N)” were renamed with place/day context for clarity.

### Title

- Spells **LIDU LETTERS** over ~2s with **no caret**.
- Full string is laid out/centered first; characters only fade in (avoids left/right recentering while typing).
- Gradient is **one shared sweep** across the word (per-letter mini-gradients looked wrong).

### Letterboard backdrop

- Faint white capital letters (~6–8% opacity), capsule shape.
- Prefer **slow fades** with **more frequent swaps** (busy enough to notice, not noisy).
- Respect `prefers-reduced-motion`.

## Browse (Questions)

- Sort hierarchy: **Topic / Event / Date** are primary; chips below are secondary filters.
- **Filters** panel collapses so scrolling the list stays clean; “Change topic / filter” **expands filters only** (no scroll-to-top jump).
- Event/date under each **question** is optional (checkbox, **off by default**) — avoids duplicate meta under question + answer.
- When that checkbox is off, meta appears once under the expanded answer.
- Search exists in Filters; keep it simple (substring). Smart/fuzzy search was deferred.

## About

- Explains what the site is and who Lidu is (nonspeaking autistic / letterboard; Telepathy Tapes context; Acid For Squares interview link).
- Keep About copy lean: no extra Spotify bullet; no long disclaimer footer; no third “Who is Lidu” paragraph about teachers/Mindsight unless product asks to restore it.
- Align Home back control with the title’s left margin.

## Admin (`#admin`)

- Not shown on the public UI (no floating `+`). Open via hash `#admin`.
- Flows: Add entry / Edit entries (list is not on the add form).
- Field groups: Question & answer → When & where (date, event, location) → Extra details (tags, more).
- Question/Answer/More textareas **grow downward** while typing.
- Tags hint: “Separate by commas”.

## Theming

- Unify interactive highlights on the **blue → purple** gradient (Filters chip, Sort buttons, active filter chips).
- Avoid a separate green “selected” chip language — it competed with Sort.

## Ops / caching

- Phones often cache GitHub Pages HTML. When testing your own changes, use a versioned URL or regenerate `qr-code.png` with `?v=...`.
- Shared feedback link stays the clean URL without query params.
