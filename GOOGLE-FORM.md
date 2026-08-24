# Google Form → Sheet → Lidu Letters

Helpers fill a **Google Form**. Answers land in a **Google Sheet** you can edit. GitHub copies the sheet into `data.json` about every 15 minutes (or when you run the sync by hand).

Grok **cannot create the Form or Sheet** until Google Drive / Sheets is connected in this session (`/mcps` — Calendar OAuth does not include Sheets). Forms is not in Grok’s connector catalog, so the Form is always created in the browser.

**Do this in the browser, then paste the two URLs into chat** (or into `google-sheet.json`). After they are on `main`, **Add a letter** appears on the live home page.

## 1. Create the form

1. Open [Google Forms](https://forms.google.com) → blank form
2. Title: **Lidu Letters**
3. Add these questions, in this order, with these exact titles:

| Title | Type | Required |
|---|---|---|
| Question | Paragraph | Yes |
| Answer | Paragraph | Yes |
| Date | Date | No |
| Event name | Short answer | No |
| Location | Short answer | No |
| Tags | Short answer | No — hint: *Separate by commas* |
| Show on home page | Multiple choice: **Yes** / **No** | Yes — default Yes |
| More / references | Paragraph | No |

4. Responses (the Responses tab) → green Sheets icon → **Create a new spreadsheet** named **Lidu Letters**

## 1b. Put the existing letters in the sheet (required before first sync)

The GitHub Action **replaces** `data.json` with whatever is in the sheet. If the sheet only has new Form rows, the live site would drop the current 24 letters. Sync **refuses** that unless you explicitly allow shrink.

In the new spreadsheet:

1. Insert a column on the left. Header: **Id** (Form will keep filling the other columns; Id stays blank on new responses and the sync assigns one)
2. Open [`sheet-seed.csv`](./sheet-seed.csv) in this repo
3. Copy the 24 data rows (not the header, unless your sheet header does not yet match)
4. Paste starting at row 2, lining **Id / Question / Answer / Date / Event name / Location / Tags / Show on home page / More / references** up with the Form headers
5. Confirm you now have **24 complete Q&A rows** before anyone else submits

You can keep editing those rows in the sheet like a normal spreadsheet.

## 2. Make the sheet readable for sync

In the spreadsheet:

1. File → **Share** → General access: **Anyone with the link** → **Viewer**
2. File → **Share** → **Publish to the web**
3. Choose the responses sheet, format **Comma-separated values (.csv)**
4. Publish
5. Copy the published CSV link (it contains `/pub?output=csv` or similar)

## 3. Point the site at your form and sheet

Edit `google-sheet.json` in this repo (or tell Grok the two URLs):

```json
{
  "formUrl": "https://docs.google.com/forms/d/e/..../viewform",
  "csvUrl": "https://docs.google.com/spreadsheets/d/e/..../pub?output=csv"
}
```

- **formUrl** — Send tab in Forms → link (so the site can show **Add a letter**)
- **csvUrl** — the published CSV from step 2

After that file is on `main`, GitHub Actions will refresh `data.json` from the sheet.

To sync immediately: GitHub → Actions → **Sync Google Sheet** → **Run workflow**.

If the action fails because the sheet has fewer rows than `data.json`, finish the seed paste (step 1b) and run it again. Only check **allow_shrink** if you really mean to delete letters.

## 4. Edit later

Open the spreadsheet, change a row, wait for the next sync (or run the workflow). The live site reads `data.json`.

Do not rename the column headers if you can avoid it. Extra columns (like Timestamp) are ignored.
