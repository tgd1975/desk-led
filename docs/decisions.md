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
