# BOM notes

Costs are indicative USD prices at quantity 1 for a concept estimate, not quotes. Every line is priced, with a supplier or supplier type. Totals are checked by `docs/04-calcs/sizing.py` (LDZ-CAL-001, section 10).

- Items 1 to 7 (per puck, quantity 2) and item 12 are the two-slot bay kit. Value-engineering target: USD 120 (`budget_usd`, a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 116.00 (USD 4.00 under the target). One puck costs USD 54.00.
- Under LDZ-DDR-001 D6 (decided by Amish, 2026-09-25: go with recommendation; LDZ-DDR-002) the target covers the two-puck kit only. `budget_usd` stays 120.
- Items 8 to 10 are the sign option: USD 101.00, costed separately from the kit.
- Item 11, the host FieldNode, is priced once in the FieldNode BOM ($126.00, FND-CAL-001) and shown here for reference; it is outside the two-puck kit cost. A bay with the sign costs USD 343.00.
- Item 5 changed at TRL 3 ($12.00 to $14.00): one Schottky diode per cell and an 85 °C hybrid pulse capacitor (LDZ-CAL-001, section 3). Decided by Amish, 2026-09-25: go with recommendation (LDZ-DDR-002, O6).
- Line numbers match the callouts in `media/exploded.png`.
- Item 7 is now two-part road-marker epoxy rather than a bitumen pad (LDZ-DDR-002, O3); the indicative price is unchanged at $4.00 per puck.
- A LoRaWAN gateway (TwinKit or an existing network) is not included; one is needed within 300 m of each bay (R4 as restated). The sign option needs a private network server for its downlinks (LDZ-DDR-002, O5).
- Design for construction (LDZ-DDR-003, 2026-10-01): item 6 is now a printed base tray with a locating ring, cradles, standoffs, an antenna rib and fill and vent holes (price unchanged); item 3 names the prototyping board and programming pads; item 9 names the enclosure, screws and gland; item 10 is now an aluminium channel bracket with a band clamp and bolts (USD 7.00, was USD 5.00); item 12 adds sealant, M2 screws and mould release (USD 8.00, was USD 6.00).
- Item 13 is one-off tooling for casting domes (printed mould master and core plug, silicone mould rubber), USD 35.00; it is not part of the per-kit cost.

Decided by Amish on 2026-10-02 (LDZ-DEC-001): the base tray is printed ASA sanded with 80 grit (item 4); the sign face (line 8) keeps a placeholder legend until the trial city is chosen and is then drawn to that city's sign rules (item 6); the potting (line 6) need not be a clear grade unless it costs no more (item 9); US915 is the default band, which sets the antenna band in line 4 (item 2). The line 4 band change is a follow-up and is not yet in `bom.csv`.
