# Rules for AI agents editing electroPioreactorGasModel.xlsx

These are agent-facing modelling rules. They used to sit in the spreadsheet's header but were removed because they are instructions for AI, not content for human review. Any AI (Claude or otherwise) editing `electroPioreactorGasModel.xlsx` must follow them. They are not part of what a human reviews in the model.

## Cell discipline
- Every cell is a number, text, or a formula. Nothing else.
- Formulae carry no embedded data values. Each datum lives in its own named, sourced cell. Only self-evident unit or stoichiometric integers may appear inline in a formula (e.g. the 2 in `2*wall`, the 4 electrons per O₂).
- Every parameter cell has a defined name (column B holds the name); reference cells by name in formulas, never by raw coordinate. Because references are by name, new parameters can be appended at the bottom without disturbing anything — cell position is irrelevant.
- Every value/source cell carries a one-line provenance in column E (Source / assumption).

## Selectors
- Selector inputs (dropdowns) accept exactly their listed valid values; anything else returns an error by design (the `IF(sel=valid1,…,IF(sel=valid2,…,NA()))` pattern). Do not soften these to default-on-invalid.

## Formats — every one is in the Summary Key (rows 163–178); use no other
- **Column E (Source / assumption) FILL = confidence**, with the Key's font colour on each fill:
  - verified / handbook / defined / standard: theme 3 tint 0.6, black text;
  - literature-supported (~90 %): theme 8 tint 0.6, black text;
  - design assumption (~70 %): `FFFFF2CC`, theme-3 text;
  - weak / coarse estimate (~50 %): `FFFFC000`, white text;
  - guess: theme 9 tint −0.25, white text;
  - DATA GAP (measure, do not invent): theme 5, white text.

  A lookup-table value with no source column of its own carries the fill itself; a `?` in a lookup table is DATA GAP.
- **Value font:** blue bold `FF0000FF` = an input you set or measure (Summary inputs, blue cells on the calculation sheets, every entry cell of the Calibrations and CO2 flows tables, empty or not); black `FF000000` = a formula. Labels, units and notes are plain black Calibri (notes 9 pt).
- **Names** in column B: Consolas 9, `FF7030A0`. **Links** (HYPERLINK): Calibri 9, blue, underlined (white on a dark fill or a band).
- **Heading** = white bold on `FF4472C4`: column-header rows and sheet titles. **SUBHEADING** = white bold on theme 4 tint 0.4: section rows.
- **Traffic lights** are conditional formats using only the Key's three dxfs:
  - **OK:** `FF006100` on `FFC6EFCE`.
  - **Caution:** `FF9C5700` on `FFFFEB9C`.
  - **Problem:** `FF9C0006` on `FFFFC7CE`.

  They colour checks; experiment status (Done / Not needed, Approximate, Not done); input validation (Problem = empty-but-required or impossible, Caution = valid but not the best choice, thresholds in the Summary threshold rows); a model value overridden in Summary column G (Caution); and excluded data points (CO2 flows, Problem). The DATA GAP fill is also used as a conditional format on Summary column E, while the start-up power is extrapolated.
- **Never used:** colour scales, data bars, coloured cell outlines, grey "computed" fills. Rule anchors: Excel anchors a multi-range rule at the top-left cell of the whole range, so write the formula against that cell.
- **Numbers:** formula results get about four significant figures (`#,##0` / `0.0` / `0.00` / `0.000` / `0.0000` / `0.00000` / `0.000E+00` by magnitude); plugin values on Summary rows 21–23 `0.00`; dates `yyyy-mm-dd`; inputs keep General so they show what was typed.
- **Summary rows are found by name, never by number**: the twin, the sensitivity model and the tests read `Summary <name>` (or `F@name` for another column of a named row).

## Lists that grow (media, calibrations, libraries)
- A list people add to is an Excel Table (ListObject) or a column of one, never a fixed block with spare rows. Formulas, dropdowns and names read the Table (`OFFSET` from its header / `Table[#Data]`, `ROWS`/`COLUMNS` of it), so a new row or column is picked up with no other edit, and nothing past a cut-off is silently ignored.
- A growing Table has nothing below it (rows) or to its right (columns) except blocks that move with it; give it its own sheet when that cannot be guaranteed.
- Media: one column per medium on the **Media** sheet; never a new sheet per medium. Its calculations are spilled formulas below the table, so a new medium column is calculated automatically. Chemistry picks the chosen medium by `MATCH` on `MediaList`.
- **No post-2019 functions** (anything stored with an `_xlfn.` prefix: XLOOKUP, FILTER, SEQUENCE, LET, DROP, the `#` spill operator / ANCHORARRAY…): Excel on the verification Mac crashes on them. Dynamic-array spills of classic functions (MMULT, TRANSPOSE, INDEX, OFFSET, IF) are fine; refer to a spill with `OFFSET(anchor,0,0,rows,cols)`.
- In defined names, refer to another sheet-local name with its sheet prefix (`Media!med_n`), or Excel returns #NAME?. Refer to a whole Table as `Table[#Data]`, not the bare table name.

## Data gaps
- Pink (DATA GAP) cells are to be measured, never invented. Do not replace a flagged gap with a guessed number to make the sheet look complete.

## Units, language, provenance
- SI units, UK English throughout.
- File origin and version history live in git, not in the sheet. Do not add provenance/origin text to the spreadsheet.

## Editing mechanics (vibe container specifics)
- Excel does not live-reload. Only one editor (human or agent) holds the file at a time; an agent edits only when the human confirms Excel is closed.
- No Excel calc engine is available in the container, so set `fullCalcOnLoad` after any edit and verify changed numbers independently (e.g. recompute in Python).
- openpyxl is not pip-installable here (PyPI is firewalled); vendor it from a GitHub mirror onto `sys.path`.
