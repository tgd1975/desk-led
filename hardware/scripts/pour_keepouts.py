"""NO_POURS regions in EasyEDA for every [[routing.keepouts]] with what = "all" of a board file (D-6).

edakit 1.1.0 keeps those areas free of tracks and vias (Freerouting's DSN) but its pours only of the hole circles, so a
pour on that layer would fill them. This script sets a NO_POURS region per keep-out on its layers; the regions stay in
the PCB through `edakit route all` / `route pours` (edakit deletes only its own hole regions), so every later fill
leaves the areas free. Run it with `edakit run pour_keepouts` under the EasyEDA claim, then `edakit route pours`.
Idempotent: the regions of its last run are replaced (ids in <artifacts>/pcb/<board>_pour_keepouts.json).

Usage: python hardware/scripts/pour_keepouts.py [board]   (default: main)
"""
import json
import sys

from edakit import config, eda
from edakit.eda import api, ensure_pcb_focus, open_pcb
from edakit.pcb import LAYER_ID, NO_POURS, outline_arg

board_name = sys.argv[1] if len(sys.argv) > 1 else "main"
cfg = config.load()
board = cfg.board(board_name)
memo = cfg.artifact("pcb", f"{board.name}_pour_keepouts.json")
mine = set(json.loads(memo.read_text())) if memo.exists() else set()

areas = []
for k in board.routing.get("keepouts", []):
    if k.get("what", "wire") != "all":
        continue
    if "rect" in k:
        x0, y0, x1, y1 = k["rect"]
        pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    else:
        pts = [tuple(p) for p in k["polygon"]]
    layers = [k["layer"]] if isinstance(k.get("layer"), str) else list(k.get("layer", ["TOP", "BOTTOM"]))
    areas += [(layer, [board.eda_point(x, y) for x, y in pts]) for layer in layers]

mcp = eda.connect(cfg)
try:
    open_pcb(mcp, board.pcb)
    old = [st["PrimitiveId"] for st in map(eda.state, api(mcp, "PCB_PrimitiveRegion.getAll") or [])
           if st["PrimitiveId"] in mine]
    if old:
        api(mcp, "PCB_PrimitiveRegion.delete", old)
    made = []
    for n, (layer, pts) in enumerate(areas, 1):
        ensure_pcb_focus(mcp)
        r = api(mcp, "PCB_PrimitiveRegion.create", LAYER_ID[layer], outline_arg(pts), [NO_POURS], f"keepout_{n}")
        if not r:
            raise SystemExit(f"NO_POURS region {n} on {layer} not created")
        made.append(eda.state(r).get("PrimitiveId") or r.get("primitiveId"))
        print(f"  NO_POURS {layer}: " + ", ".join(f"({x:g}, {y:g})" for x, y in pts))
    memo.write_text(json.dumps([m for m in made if m]))
    print(f"{len(made)} region(s) set, {len(old)} old one(s) replaced")
finally:
    mcp.close()
