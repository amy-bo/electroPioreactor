# Rules for AI agents editing electroPioreactorGasModel.xlsx

These are agent-facing modelling rules. They used to sit in the spreadsheet's header but were removed because they are instructions for AI, not content for human review. Any AI (Claude or otherwise) editing `electroPioreactorGasModel.xlsx` must follow them. They are not part of what a human reviews in the model.

## Cell discipline
- Every cell is a number, text, or a formula. Nothing else.
- Formulae carry no embedded data values. Each datum lives in its own named, sourced cell. Only self-evident unit or stoichiometric integers may appear inline in a formula (e.g. the 2 in `2*wall`, the 4 electrons per O₂).
- Every parameter cell has a defined name (column B holds the name); reference cells by name in formulas, never by raw coordinate. Because references are by name, new parameters can be appended at the bottom without disturbing anything — cell position is irrelevant.
- Every value/source cell carries a one-line provenance in column E (Source / assumption).

## Selectors
- Selector inputs (dropdowns) accept exactly their listed valid values; anything else returns an error by design (the `IF(sel=valid1,…,IF(sel=valid2,…,NA()))` pattern). Do not soften these to default-on-invalid.

## Colour conventions — two orthogonal encodings
- **Column E (Source/assumption) FILL = confidence.** Six levels, legend in A5:A10: green `FFC6EFCE` = verified/handbook/defined/standard; light-blue `FFBDD7EE` = literature-supported ~90%; cream `FFFFF2CC` = design assumption ~70%; gold `FFFFE699` = weak/coarse estimate ~50%; peach `FFFCE4D6` = guess; pink `FFFFC7CE` = DATA GAP (measure, do not invent).
- **Column D (Value) FONT = provenance of the value:** blue `FF0000FF` (bold) = an input you set or measure; black `FF000000` = a formula/derived value. Apply rigorously to every cell, and keep this convention shown in the key.

## Data gaps
- Pink (DATA GAP) cells are to be measured, never invented. Do not replace a flagged gap with a guessed number to make the sheet look complete.

## Units, language, provenance
- SI units, UK English throughout.
- File origin and version history live in git, not in the sheet. Do not add provenance/origin text to the spreadsheet.

## Editing mechanics (vibe container specifics)
- Excel does not live-reload. Only one editor (human or agent) holds the file at a time; an agent edits only when the human confirms Excel is closed.
- No Excel calc engine is available in the container, so set `fullCalcOnLoad` after any edit and verify changed numbers independently (e.g. recompute in Python).
- openpyxl is not pip-installable here (PyPI is firewalled); vendor it from a GitHub mirror onto `sys.path`.
