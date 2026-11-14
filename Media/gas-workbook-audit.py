#!/usr/bin/env python3
"""Read-only OOXML integrity and cell-Key audit; no spreadsheet dependencies.

Checks stored styles, including blank entry cells and row/column defaults.
Excel remains necessary to recalculate and inspect rendered layout.
"""
from collections import Counter
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
RID = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
EXPECTED_NA = {
    'Chemistry': {'D161', 'D208', 'D209', 'D258'},
    'Biology': {'D45', 'D46', 'D47', 'D48'},
    'Mass Transfer': {'D22', 'D23', 'D24', 'D25', 'D542', 'D543'},
}


def audit(path):
    issues, counts = [], Counter()
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
        if bad:
            issues.append(f'ZIP checksum failure: {bad}')
        root = ET.fromstring(z.read('xl/styles.xml'))
        fonts = list(root.find('m:fonts', NS))
        fills = list(root.find('m:fills', NS))
        borders = list(root.find('m:borders', NS))
        styles = list(root.find('m:cellXfs', NS))
        dxfs = list(root.find('m:dxfs', NS))
        wb = ET.fromstring(z.read('xl/workbook.xml'))
        rels = {r.get('Id'): r.get('Target') for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        shared = [''.join(s.itertext()) for s in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        sheets = list(wb.find('m:sheets', NS))
        names = set()
        for name in wb.findall('m:definedNames/m:definedName', NS):
            key = (name.get('localSheetId'), name.get('name').lower())
            if key in names or '#REF!' in (name.text or ''):
                issues.append(f'Invalid/duplicate name: {key}')
            names.add(key)
        # Only fills represented by the Summary Key; unfilled cells are also valid.
        allowed_rgb = {'FFFFF2CC', 'FFFFC000', 'FF4472C4', 'FFC6EFCE', 'FFFFEB9C', 'FFFFC7CE'}
        allowed_theme = {('3', 0.6), ('8', 0.6), ('9', -0.25), ('5', 0.0), ('4', 0.4)}
        used_styles = set()
        for sh in sheets:
            name = sh.get('name')
            target = rels[sh.get(RID)]
            part = target.lstrip('/') if target.startswith('/') else 'xl/' + target
            sheet = ET.fromstring(z.read(part))
            seen = set()
            for c in sheet.findall('m:sheetData/m:row/m:c', NS):
                ref = c.get('r'); loc = f'{name}!{ref}'
                if ref in seen:
                    issues.append(f'{loc}: duplicate cell')
                seen.add(ref)
                counts['cells'] += 1
                sid = int(c.get('s', 0)); used_styles.add(sid)
                style = styles[sid]; font = fonts[int(style.get('fontId', 0))]
                col = font.find('m:color', NS)
                colour = col.attrib if col is not None else {}
                f = c.find('m:f', NS); v = c.findtext('m:v', '', NS)
                numeric = c.get('t', 'n') == 'n' and bool(v)
                if f is not None:
                    counts['formulas'] += 1
                    if (f.text or '').startswith('HYPERLINK'):
                        if font.find('m:sz', NS).get('val') != '9' or font.find('m:u', NS) is None:
                            issues.append(f'{loc}: link must be 9-point and underlined')
                    if '#REF!' in (f.text or ''):
                        issues.append(f'{loc}: broken formula reference')
                    if any(len(s) > 255 for s in re.findall(r'"((?:[^"]|"")*)"', f.text or '')):
                        issues.append(f'{loc}: formula string exceeds Excel limit')
                    if c.find('m:v', NS) is None:
                        issues.append(f'{loc}: formula cache missing')
                    if numeric and colour.get('rgb') != 'FF000000':
                        issues.append(f'{loc}: numeric formula is not black')
                elif colour.get('rgb') == 'FF0000FF' and font.find('m:u', NS) is None:
                    if font.find('m:b', NS) is None:
                        issues.append(f'{loc}: input is not bold')
                    if int(style.get('numFmtId', 0)) not in (0, 177):
                        issues.append(f'{loc}: editable input must use General (or yyyy-mm-dd)')
                if c.get('t') == 'e':
                    counts['intentional_NA'] += 1
                    if v != '#N/A' or ref not in EXPECTED_NA.get(name, set()):
                        issues.append(f'{loc}: unexpected cached error {v}')
            for row in sheet.findall('m:sheetData/m:row', NS):
                if row.get('s'):
                    used_styles.add(int(row.get('s')))
            for col in sheet.findall('m:cols/m:col', NS):
                if col.get('style'):
                    used_styles.add(int(col.get('style')))
            for cf in sheet.findall('.//m:cfRule', NS):
                if cf.get('type') in ('colorScale', 'dataBar'):
                    issues.append(f'{name}: forbidden conditional format {cf.get("type")}')
                if cf.get('dxfId') is not None:
                    d = dxfs[int(cf.get('dxfId'))]
                    fc = d.find('m:font/m:color', NS)
                    bg = d.find('m:fill/m:patternFill/m:bgColor', NS)
                    fg = d.find('m:fill/m:patternFill/m:fgColor', NS)
                    fill = bg if bg is not None and bg.get('rgb') else fg
                    pairs = {'FF006100': 'FFC6EFCE', 'FF9C5700': 'FFFFEB9C', 'FF9C0006': 'FFFFC7CE'}
                    if fc is None or not ((fc.get('rgb') in pairs and fill is not None and fill.get('rgb') == pairs[fc.get('rgb')]) or fc.get('theme') == '0'):
                        issues.append(f'{name}: conditional format is outside Key')
            validations = sheet.find('m:dataValidations', NS)
            if validations is not None and len(validations) != int(validations.get('count')):
                issues.append(f'{name}: invalid validation count')
        for sid in sorted(used_styles):
            s = styles[sid]; font = fonts[int(s.get('fontId', 0))]
            if font.find('m:name', NS).get('val') not in ('Calibri', 'Consolas'):
                issues.append(f'Style {sid}: font outside Key')
            fill = fills[int(s.get('fillId', 0))].find('m:patternFill', NS)
            if fill.get('patternType') not in ('none', 'gray125'):
                fg = fill.find('m:fgColor', NS)
                theme = (fg.get('theme'), round(float(fg.get('tint', 0)), 2))
                if fg.get('rgb') not in allowed_rgb and theme not in allowed_theme:
                    issues.append(f'Style {sid}: fill outside Key')
            if any(edge.get('style') is not None for edge in borders[int(s.get('borderId', 0))]):
                issues.append(f'Style {sid}: decorative border outside Key')
        counts.update(sheets=len(sheets), names=len(names), styles=len(used_styles))
    return dict(counts), issues


def audit_tables(path):
    """Each Excel Table: header cells hold exactly its column names, ids and names unique, no future functions."""
    issues = []
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        wb = ET.fromstring(z.read('xl/workbook.xml'))
        rels = {r.get('Id'): r.get('Target') for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        shared = [''.join(s.itertext()) for s in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        ids, tnames = set(), set()
        for sheet in wb.find('m:sheets', NS):
            part = 'xl/' + rels[sheet.get(RID)].lstrip('/').replace('xl/', '')
            rel = part.replace('worksheets/', 'worksheets/_rels/') + '.rels'
            if rel not in names:
                continue
            root = ET.fromstring(z.read(part))
            cells = {}
            for c in root.iter('{%s}c' % NS['m']):
                v = c.find('m:v', NS)
                if c.get('t') == 'inlineStr':
                    cells[c.get('r')] = ''.join(c.find('m:is', NS).itertext())
                elif c.get('t') == 's' and v is not None:
                    cells[c.get('r')] = shared[int(v.text)]
            for r in ET.fromstring(z.read(rel)):
                if not r.get('Type', '').endswith('/table'):
                    continue
                t = ET.fromstring(z.read('xl/' + r.get('Target').replace('../', '')))
                tn = t.get('name')
                if t.get('id') in ids or tn in tnames:
                    issues.append(f'Table {tn}: duplicate id or name')
                ids.add(t.get('id')); tnames.add(tn)
                m = re.fullmatch(r'([A-Z]+)(\d+):([A-Z]+)(\d+)', t.get('ref'))
                c0 = sum((ord(ch) - 64) * 26 ** k for k, ch in enumerate(reversed(m.group(1))))
                cols = [tc.get('name') for tc in t.find('m:tableColumns', NS)]
                if int(t.find('m:tableColumns', NS).get('count')) != len(cols):
                    issues.append(f'Table {tn}: tableColumns count mismatch')
                for k, name in enumerate(cols):
                    n, col = c0 + k, ''
                    while n:
                        n, rem = divmod(n - 1, 26)
                        col = chr(65 + rem) + col
                    if cells.get(f'{col}{m.group(2)}') != name:
                        issues.append(f'Table {tn}: header {col}{m.group(2)} is not "{name}"')
        for n in names:
            if n.startswith('xl/') and n.endswith('.xml') and b'_xlfn.' in z.read(n):
                issues.append(f'{n}: post-2019 function (_xlfn); the verification Excel crashes on these')
    return issues


if __name__ == '__main__':
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name('electroPioreactorGasModel.xlsx')
    counts, issues = audit(path)
    issues += audit_tables(path)
    print(counts)
    print('\n'.join(issues) if issues else 'PASS: workbook structure and cell-format Key checks')
    raise SystemExit(bool(issues))
