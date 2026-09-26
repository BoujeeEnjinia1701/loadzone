# BOM notes

Costs are indicative USD prices at quantity 1 for a concept estimate, not quotes. Every line is priced, with a supplier or supplier type. Totals are checked by `docs/04-calcs/sizing.py` (LDZ-CAL-001, section 10).

- Items 1 to 7 (per puck, quantity 2) and item 12 are the two-slot bay kit: $114.00 against the $120 `budget_usd`, a margin of $6.00. One puck costs $54.00.
- Under LDZ-DDR-001 D6 (decided by Amish, 2026-09-25: go with recommendation; LDZ-DDR-002) the budget covers the two-puck kit only. `budget_usd` stays $120.
- Items 8 to 10 are the sign option: $97.00, outside the budget.
- Item 11, the host FieldNode, is priced once in the FieldNode BOM ($126.00, FND-CAL-001) and shown here for reference; it is outside the LoadZone budget. A bay with the sign costs $337.00.
- Item 5 changed at TRL 3 ($12.00 to $14.00): one Schottky diode per cell and an 85 °C hybrid pulse capacitor (LDZ-CAL-001, section 3). Decided by Amish, 2026-09-25: go with recommendation (LDZ-DDR-002, O6).
- Line numbers match the callouts in `media/exploded.png`.
- Item 7 is now two-part road-marker epoxy rather than a bitumen pad (LDZ-DDR-002, O3); the indicative price is unchanged at $4.00 per puck.
- A LoRaWAN gateway (TwinKit or an existing network) is not included; one is needed within 300 m of each bay (R4 as restated). The sign option needs a private network server for its downlinks (LDZ-DDR-002, O5).
