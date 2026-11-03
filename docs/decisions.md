# Board decisions

Numbered, with reason and date. The hardware graph `hardware/graph.toml` is the source; `hardware/graph.json` beside it
is generated (`edakit graph json --write`).

## D-1 Set up for edakit (2026-11-03)

One made board `main` ("Desk LED"), sized to its parts, drawn in EasyEDA Pro (project `desk-led`), schematic with
labels. One build, no variants. JLCPCB makes it and places the SMD parts on the top side (Economic); 5 sets with
edakit's defaults (1.6 mm, green, white, lead-free HASL, 1 oz, tented vias). No budget, costs in EUR with Austrian VAT,
shipped to Austria like the Christmas bell. Private, used on the owner's desk in Austria. Requirements written now with
the skill requirements. No firmware, no documents quoting values, no scripts of its own. Reason: the owner's answers in
the setup interview.

## D-2 Requirements accepted (2026-11-03)

N-1 and R-1 to R-5 in `hardware/requirements.toml`, the owner's answers in the first round: the LED lights only while
the button is held (R-1), a CR2032 (R-2), JLCPCB places the SMD parts on top (R-3, from D-1), a green LED (R-4,
should) and a 12 × 12 mm tactile switch (R-5, should). Which green is the circuit designer's: a yellow-green LED (about
2.1 V) stays bright from a 3 V cell, a true green (about 3 V) is dimmer and fades as the cell empties.

## D-3 Parts and values (2026-11-03)

- **LED D1: Lite-On LTST-C170KGKT (C98221)**, AlInGaP green, 571 nm, VF 1.9–2.4 V at 20 mA. The common InGaN green
  (2.6–3.1 V, edakit's block LED C2297) stays dark on a used CR2032 (2.5 V). The colour is a yellowish green, the
  green R-4 asks for that lights from the cell.
- **Holder BT1: HanElectricity CR2032-B1 (C48601332)**, SMD, placed in Economic assembly; its drawing marks plus.
  The handbook's C70377 is "Standard Only", C22363833's drawing does not say which pad is plus.
- **Button SW1: Kinghelm KH-12X12X6H-SMT-D (C18186482)**, 12 × 12 mm, 6 mm high (R-5), the SMD type with the most stock.
- **R1 330 Ω (C17630, Basic)**: at least 1 mA into D1 from a used cell at its highest VF (1.17 mA in the simulation),
  4.4 mA from a fresh cell. That is above the CR2032's 3 mA continuous current while the button is held – accepted
  (LIM.i/cell): a press is short, 4.4 mA is far below the 15 mA pulse current, and holding longer only costs
  capacity. 390 Ω would leave 1.0 mA from a used cell, no margin. (The currents here rest on an assumed 10 Ω
  series resistance of D1 – corrected in D-4.)
- **No reverse-polarity part**: a cell upside down reverses D1 at 3.2 V, within its 5 V; a Schottky would cost the
  0.3 V the used cell needs (PATH.reverse accepted, scenario reversed/pressed).
- All four parts are Extended at JLCPCB except R1 – three extended-part fees per order.

## D-4 Circuit reviews M-1 and M-6 worked in (2026-11-03)

Both reviews found nothing that blocks and nothing important, seven notes each. Worked in:

- **D1's series resistance** is about 2 Ω by the datasheet's Fig. 2, not the 10 Ω assumed. With it a fresh cell gives
  at most 4.0 mA; a D1 of the highest VF bin on a cell used down to 2.5 V gets 0.82 mA – still lit (1–4 mcd), so R1
  stays 330 Ω, and the simulation counts an LED as lit from 0.5 mA (`criteria.led_on_min_a` in sim.json, 0.5–2 mcd
  for this LED by its Fig. 4) instead of edakit's 1 mA. 270 Ω would give 0.97 mA there and 5 mA fresh.
- **SW1 wired on the diagonal** (pins 1 and 4): right whichever way the internal pairs run.
- **SW1's land pattern** compared with the drawing: the feet land fully – the open point is closed.
- **BT1 takes a cell upside down**: depending on where its plus hook lands, the LED stays dark, sees −3.2 V (harmless)
  or the cell is shorted for a while. A '+' and the cell's outline in the silkscreen beside BT1 (layout note).
- M-6 for the purpose private: no duties of placing on the market; spare boards stay with the owner – a board given
  away makes the purpose gift and needs M-6 again (RoHS and REACH statements of R1, SW1, BT1 then). Keep cells away
  from small children; spent cells to a collection point. Support, not legal advice – nothing in it is guaranteed.

Proposed to edakit (when the owner asks): a battery holder fact for an upside-down cell (no contact, reversed,
short), the hand-over listing parts' open points for the layout, whether LED reverse voltage is derated on purpose.

## D-5 R-1 tested in both halves (2026-11-03)

R-1's evidence gets the simulation rows "LED dark" beside "LED on": the released scenarios test "only while the
button is held". Text and binding unchanged – the owner's answer to the M-1 review's note 3.

## D-6 Layout of board main, round 1 (2026-11-03)

Board 40 × 40 mm (fit to the parts, D-1), all parts on top, two JLCPCB tooling holes at (2, 38) and (38, 2). BT1
centred at the top: the cell (Ø 20 mm) ends 2 mm inside the top edge, where it is levered out; 4 mm free between the
cell and SW1 below it. SW1 on the cell's axis, R1 right of its LED_SW pad, D1 above R1 beside SW1 (the LED shows the
press), its anode straight above R1's. Freerouting: 3 nets (GND is the top pour alone), 2 vias – both VBAT, one under
the cell, one under SW1's body –, no track between the pads of a part or past a foreign pad, DRC 0. Placement, keep-out, pours and silkscreen in `hardware/boards/main.toml`.

- **Copper on both faces** (no large copper-free areas): GND poured on top (`pour_only`: both GND pads sit in it, no
  GND track or via), VBAT on the bottom – GND has no pad or via
  there, and a fanout via for it would sit beside BT1's tab, visible; VBAT's two vias hold the bottom pour. Measured in
  the Gerber: 87 % copper on top, 94 % on the bottom, no copper-free circle above Ø 1 mm outside BT1's hatched area.
  `[copper] min_cover` 40 % per face makes the gate warn when a face loses its pour.
- **BT1's hatched area kept free literally** (hand-over note): a routing keep-out keeps tracks and vias out, and a
  NO_POURS region keeps the top pour out. edakit 1.1.0 keeps only hole circles free of its pours, so the project script
  `pour_keepouts` (`hardware/scripts/pour_keepouts.py`, kind easyeda) sets the region; it stays through later fills.
  Measured: 0 mm² of top copper in the area. The area is a keep-out of the top face, where the holder's minus contact
  lies; the bottom pour runs under it, 1.6 mm of laminate away (layout review 3, note 2).
- **Silkscreen:** the cell's outline, a '+' 2 mm above BT1's plus tab and "+ UP" left of the cell – both stay visible
  with the cell in. `[looks]`: top is the face on the desk, at most 2 vias.
- **Pour fills fail with easyeda-mcp-pro 1.8.0:** `route all` fills a net's pours in one rebuild call (M-10); with two
  pours that came back "no-copper", and after one failure, or once pours had been created in the same EasyEDA session,
  even a single pour did. What worked: the pours created by edakit (`pcb.pour`), EasyEDA restarted, then each pour
  rebuilt alone through the bridge, then `pcb apply` for the tooling holes, `route drc`, `silk apply`. This round was
  routed that way (`route read`, `route`, `check`, `apply` one by one); the next `route all` stops at its pours step
  the same way until edakit or the bridge changes.
- Layout reviews 1 to 3 (agent pcb-reviewer) worked in: top pour, "+ UP" and '+' at the tab, SW1 centred with R1/D1
  beside it, `[looks]`, no track between pads, no via next to a pad, D1 turned so its anode sits above R1's, a VBAT
  pour on the bottom judged without risk. The last step (D1 turned, GND pour-only) was not reviewed again – the
  release's M-5 review reads it. Not a layout matter: stick-on feet.

edakit: open – proposed on 2026-11-03, each as its own issue:
[#335](https://github.com/tgd1975/edakit/issues/335) keep-outs with `what = "all"` keep pours out (the project script
then goes); [#336](https://github.com/tgd1975/edakit/issues/336) pours fill on easyeda-mcp-pro 1.8.0;
[#337](https://github.com/tgd1975/edakit/issues/337) `schematic copy` on a fresh project failed with
"DMT_Schematic.getSchematicInfo: TypeError … 'Symbol'" and should point to `schematic layout`, which built the board
schematic instead; [#338](https://github.com/tgd1975/edakit/issues/338) a `[[silk.art]]` entry with `file =` instead of
`svg` passed `pcb plan` and crashed `silk apply` (KeyError); [#339](https://github.com/tgd1975/edakit/issues/339)
`ensure_pcb_focus` in a project script before `open_pcb` crashed (KeyError 'uuid'); the rules
[#340](https://github.com/tgd1975/edakit/issues/340) GEO.pour also on a seen face without a pour,
[#341](https://github.com/tgd1975/edakit/issues/341) vias keep a distance from reflowed SMD pads and
[#342](https://github.com/tgd1975/edakit/issues/342) no track between the two pads of a small chip part.

## D-7 MIT licence, licence check, public example repository (2026-11-03)

The repository is public on GitHub as an example of a project built with edakit, under the MIT licence like edakit
itself (`LICENSE`). Nothing in it is someone else's work: the parts entries quote facts – pins, ratings, order codes –
from the datasheets and catalogue pages each entry names in `sources`, the datasheets themselves are not in the
repository; `hardware/boards/main.geometry.json` holds pad positions edakit measured from the library footprints in
EasyEDA. README.md's Licence section says so, and names any third-party file that comes later with its source and
licence, as edakit's README does for its test designs.

The project check `licence` (`hardware/scripts/licence_check.py`, stage LIC of the gate and the pre-commit hook) holds
that: LICENSE is MIT with its copyright line; the Licence section says MIT and that it is not legal advice; every
tracked file of a kind that usually comes from someone else (PDF, 3D model, library footprint or symbol, EDA archive,
photo) is named in a row of it, and every row's path exists; every parts entry names its sources. Reason: the owner's
wish – the licence on MIT and a licence check after edakit's. A reading of the licences, not legal advice.

Registered in edakit's gallery with the form "built with edakit": [#343](https://github.com/tgd1975/edakit/issues/343).
The repository is private until the owner makes it public.
