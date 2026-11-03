"""Licence check of the repository (D-7), after edakit's own (its README's Licence section and
tests/test_open_designs.py): the repository is MIT, and anything that is not the project's own work is named in
README.md's Licence section with its source and licence.

Checks:
  1. LICENSE is the MIT licence with a copyright line.
  2. README.md has a section "## Licence" that says MIT and that it is not legal advice.
  3. Every tracked file of a kind that usually comes from someone else – datasheets, 3D models, library footprints and
     symbols, EDA project archives, photos – is named in a row of that section with its licence, and every path a row
     names exists.
  4. Every parts entry names where its facts come from (`sources`), so that its data stays facts quoted from a named
     datasheet or catalogue, not a copy of it.

Run by hand (`python3 hardware/scripts/licence_check.py`), by the pre-commit hook and as stage LIC of the release gate.
The last stdout line is a JSON list of [id, check, actual, expected, ok] rows (edakit handbook 8.1); exit 1 on a
failure. Standard library only.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# kinds of file that usually come from someone else: datasheets, 3D models, footprints/symbols, EDA archives, photos
FOREIGN = {".pdf", ".step", ".stp", ".wrl", ".kicad_mod", ".kicad_sym", ".lib", ".epro", ".elibz", ".zip", ".jpg",
           ".jpeg", ".dxf"}
ID = "LIC"


def tracked():
    """The files git tracks or would add (staged or untracked, not ignored)."""
    out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    return sorted({line for line in out.splitlines() if line and (ROOT / line).exists()})


def section(readme):
    """README.md's Licence section, without its heading, or None."""
    m = re.search(r"^## Licen[cs]e\s*$(.*?)(?=^## |\Z)", readme, re.M | re.S)
    return m.group(1) if m else None


def rows_of(text):
    """The table rows of the section: (path cell, whole row)."""
    rows = []
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.lstrip().startswith("|") and len(cells) >= 3 and not set(cells[0]) <= set("-: ") \
                and cells[0].lower() != "path":
            rows.append((cells[0], line))
    return rows


def main():
    results = []

    def row(check, actual, expected, ok):
        results.append([ID, check, actual, expected, bool(ok)])

    lic = (ROOT / "LICENSE").read_text(encoding="utf-8") if (ROOT / "LICENSE").exists() else ""
    mit = lic.startswith("MIT License") and "Permission is hereby granted, free of charge" in lic
    row("LICENSE is MIT", "MIT" if mit else ("missing" if not lic else "other text"), "MIT", mit)
    row("LICENSE names the copyright holder", "yes" if re.search(r"Copyright \(c\) \d{4} \S", lic) else "no", "yes",
        re.search(r"Copyright \(c\) \d{4} \S", lic))

    readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").exists() else ""
    sec = section(readme)
    row("README.md has a Licence section", "yes" if sec is not None else "no", "yes", sec is not None)
    sec = sec or ""
    flat = " ".join(sec.split())
    row("the section says MIT", "yes" if "MIT" in flat else "no", "yes", "MIT" in flat)
    row("the section says it is not legal advice", "yes" if "not legal advice" in flat else "no", "yes",
        "not legal advice" in flat)

    files = tracked()
    named = rows_of(sec)
    paths = [re.sub(r"[`*]", "", cell) for cell, _ in named]
    foreign = [f for f in files if Path(f).suffix.lower() in FOREIGN]
    unnamed = [f for f in foreign if not any(f == p or (p.endswith("/") and f.startswith(p)) for p in paths)]
    row("third-party files named in the Licence section", ", ".join(unnamed) or "all", "all", not unnamed)
    gone = [p for p in paths if not (ROOT / p).exists()]
    row("every path the section names exists", ", ".join(gone) or "all", "all", not gone)

    bare = []
    for f in files:
        if f.startswith("hardware/parts/") and f.endswith(".json"):
            entry = json.loads((ROOT / f).read_text(encoding="utf-8"))
            if not entry.get("sources"):
                bare.append(Path(f).name)
    row("every parts entry names its sources", ", ".join(bare) or "all", "all", not bare)

    for r in results:
        print(f"{'ok  ' if r[4] else 'FAIL'} {r[1]}: {r[2]}")
    print(json.dumps(results, ensure_ascii=False))
    return 0 if all(r[4] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
