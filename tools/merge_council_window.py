"""Reproduce the GUI merge from separately installed, hash-pinned dependencies.

No game files, dependency files or existing output are changed. See the project's
README for required versions and retain LICENSE-Council-Autopilot.txt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

ANCHOR = b'\t\t\t\t# two tabs hbox: your council and liege council'
MARKER = b'\t\t\t\t# Council Assignment Automation: only this control is added to the vanilla window.'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def merge(caa, autopilot, vanilla, license_bytes, lock):
    blobs = dict(caa=caa, autopilot=autopilot, vanilla=vanilla, autopilot_license=license_bytes)
    for key, data in blobs.items():
        if sha(data) != lock['inputs'][key]['sha256']:
            raise ValueError('Upstream changed: ' + key)
    if caa.count(MARKER) != 1 or caa.count(ANCHOR) != 1:
        raise ValueError('CAA insertion point is ambiguous')
    insertion = caa[caa.index(MARKER):caa.index(ANCHOR)]
    normalize = lambda data: data.decode('utf-8-sig').replace('\r\n', '\n')
    if normalize(caa.replace(insertion, b'', 1)) != normalize(vanilla):
        raise ValueError('CAA changes exceed the reviewed single control')
    if autopilot.count(ANCHOR) != 1 or MARKER in autopilot:
        raise ValueError('Autopilot insertion point is ambiguous')
    merged = autopilot.replace(ANCHOR, insertion + ANCHOR, 1)
    if merged.replace(insertion, b'', 1) != autopilot or merged.count(b'name = "caa_open_settings_button"') != 1:
        raise ValueError('Merged controls differ')
    callbacks = re.findall(rb"GetScriptedGui\(\s*'([^']+)'", autopilot)
    if not callbacks or any(merged.count(value) != autopilot.count(value) for value in set(callbacks)):
        raise ValueError('Autopilot callbacks differ')
    return merged


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--caa', required=True, type=Path, help='Installed Council Assignment Automation root')
    parser.add_argument('--autopilot', required=True, type=Path, help='Installed Council Autopilot root')
    parser.add_argument('--game', required=True, type=Path, help='CK3 game directory containing gui/')
    parser.add_argument('--lock', type=Path, default=Path(__file__).with_name('upstream-lock.json'))
    parser.add_argument('--output', required=True, type=Path, help='New output directory, never an existing mod directory')
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError('Preserve existing output; choose a new directory')
    lock = json.loads(args.lock.read_text(encoding='utf-8'))
    license_bytes = (args.autopilot / 'LICENSE').read_bytes()
    gui = Path('gui/window_council.gui')
    merged = merge((args.caa / gui).read_bytes(), (args.autopilot / gui).read_bytes(),
                   (args.game / gui).read_bytes(), license_bytes, lock)
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / 'gui').mkdir()
    (args.output / gui).write_bytes(merged)
    (args.output / 'LICENSE-Council-Autopilot.txt').write_bytes(license_bytes)
    print(json.dumps({'status': 'STATIC_MERGE_PASS', 'gui_sha256': sha(merged),
                      'license_sha256': sha(license_bytes), 'native_test_performed': False}))


if __name__ == '__main__':
    main()
