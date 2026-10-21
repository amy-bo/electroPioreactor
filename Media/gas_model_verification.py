"""Detect workbook definition drift beyond the companions' selected output checks.

This records inputs, formulas and defined names, never expected computed answers.
A matching record is NOT proof of recalculation: use real Excel after every edit.
After an intentional rebase and Excel recalculation, run this module with --record,
then rerun both companions. Presentation changes alone do not invalidate it.
"""
import hashlib
import json
from pathlib import Path
import posixpath
import sys
import xml.etree.ElementTree as ET
import zipfile

NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
RID = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
RECORD = 'electroPioreactorGasModel-verification.json'


def workbook_definition(path):
    """Stable scalar inputs plus formula/name definitions, excluding formula caches."""
    inputs, formulas = [], []
    with zipfile.ZipFile(path) as z:
        wb = ET.fromstring(z.read('xl/workbook.xml'))
        rels = {r.get('Id'): r.get('Target') for r in
                ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        shared = ([''.join(si.itertext()) for si in ET.fromstring(z.read('xl/sharedStrings.xml'))]
                  if 'xl/sharedStrings.xml' in z.namelist() else [])
        for sheet in wb.find('m:sheets', NS):
            target = rels[sheet.get(RID)]
            part = target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/' + target)
            for cell in ET.fromstring(z.read(part)).findall('.//m:sheetData/m:row/m:c', NS):
                key = [sheet.get('name'), cell.get('r')]
                f, v = cell.find('m:f', NS), cell.find('m:v', NS)
                if f is not None:
                    # Shared-formula anchors and ranges are part of the definition.
                    formulas.append(key + [f.text or '', sorted(f.attrib.items())])
                    continue
                t = cell.get('t', 'n')
                if t == 'inlineStr':
                    value = ''.join(cell.find('m:is', NS).itertext())
                elif v is None:
                    continue
                elif t == 's':
                    value = shared[int(v.text)]
                elif t == 'n':
                    value = float(v.text)
                else:
                    value = v.text
                inputs.append(key + [value])
        names = sorted((n.get('localSheetId', ''), n.get('name'), n.text or '')
                       for n in wb.findall('m:definedNames/m:definedName', NS))
    def digest(value):
        return hashlib.sha256(json.dumps(value, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
    return dict(version=1, input_count=len(inputs), formula_count=len(formulas), name_count=len(names),
                inputs_sha256=digest(sorted(inputs)), formulas_sha256=digest(sorted(formulas)),
                names_sha256=digest(names))


def verify_definition(path):
    """Fail closed if any declared input/formula/name changed since the reviewed rebase."""
    record = Path(path).with_name(RECORD)
    try:
        expected = json.loads(record.read_text())
    except (OSError, ValueError) as exc:
        raise SystemExit(f'Missing or invalid workbook verification record: {record}: {exc}')
    actual = workbook_definition(path)
    if actual != expected:
        changed = ', '.join(k for k in actual if actual[k] != expected.get(k))
        raise SystemExit('WORKBOOK DEFINITION DRIFT (' + changed + '): rebase both companions, '
                         'recalculate in Excel, explicitly record the new definition, and rerun all checks.')


if __name__ == '__main__':
    path = Path(__file__).with_name('electroPioreactorGasModel.xlsx')
    if sys.argv[1:] == ['--record']:
        path.with_name(RECORD).write_text(json.dumps(workbook_definition(path), indent=2) + '\n')
        print('Recorded inputs/formulas/names only. Now run both companions; this does not attest recalculation.')
    elif not sys.argv[1:]:
        verify_definition(path)
        print('Workbook definition matches the reviewed rebase (formula caches checked by the companions).')
    else:
        raise SystemExit('Usage: python3 gas_model_verification.py [--record]')
