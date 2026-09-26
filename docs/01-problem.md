---
doc_id: LDZ-PRB-001
title: LoadZone problem statement
project: LoadZone
doc_type: Problem statement
version: "0.3"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (users, context, constraints, prior work, out of scope)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Reflect LDZ-DDR-001 (budget scope, installation, network) and the gateway distance found in LDZ-CAL-001
---

# LoadZone problem statement

Delivery drivers cannot see whether a loading bay is free before they reach it, so when the bay is taken they double-park in a traffic lane, a bike lane or a crosswalk, and cities have no routine record of how their loading bays are used. LoadZone aims to report the state of each vehicle slot in a loading bay, in real time and without cameras, at a cost low enough for a city, a business district or a community group to try on one street.

## The problem in numbers

Loading bays in busy districts are full much of the day, and many of the vehicles in them are not delivering. In a 2017 observation study of five locations in downtown Seattle, passenger vehicles were 52 % of all vehicles parked in commercial vehicle load zones, and 41 % of commercial vehicles parked in unauthorized locations, rising to 55 to 65 % near retail centers ([Urban Freight Lab, 2019](https://urbanfreightlab.com/publications/the-final-50-feet-of-the-urban-goods-delivery-system-tracking-curb-use-in-seattle/)). The same research group reports that commercial vehicle load zones often reach 90 % occupancy or more during business hours ([Urban Freight Lab, Final 50 Feet](https://urbanfreightlab.com/final-50-feet/)).

Stops are short, so information has to be quick. In the Seattle study, 60 % of delivery vehicles parked for 15 minutes or less and 81 % for 30 minutes or less ([Urban Freight Lab, 2019](https://urbanfreightlab.com/publications/the-final-50-feet-of-the-urban-goods-delivery-system-tracking-curb-use-in-seattle/)). A bay can change state several times an hour, which static signs and occasional manual surveys cannot capture.

Demand keeps growing. Online sales rose from 16 % to 19 % of all retail sales in 2020 ([UNCTAD, 2021](https://unctad.org/news/global-e-commerce-jumps-267-trillion-covid-19-boosts-online-sales)), and in Great Britain van traffic rose 2.3 % to 59.0 billion vehicle miles in the year to September 2024 ([Department for Transport](https://www.gov.uk/government/statistics/provisional-road-traffic-estimates-great-britain-october-2023-to-september-2024)).

## Users and context

| User | Need |
| --- | --- |
| Delivery and service drivers | Know, before arriving, which bay or slot is free; avoid circling and double parking |
| City curb and transport teams | Occupancy, turnover and dwell time by bay and hour, to set bay size, hours and pricing |
| Parking enforcement | Know which bays have overstays without a patrol or a camera |
| Shops and business districts | Shared loading space that works for their suppliers; evidence to request more bays |
| Cyclists and pedestrians | Fewer vans stopped in bike lanes and at crossings |

The setting is an on-street loading bay along a curb, typically long enough for one to three vans, on a street with shops, offices or homes. The street may already have poles (lighting or signs) that a city allows sensors to be fixed to. A LoRaWAN gateway may already exist nearby (a city network, The Things Network or the lab's TwinKit gateway), or one must be added. From road level under a parked van a puck reaches only about 350 m in a street canyon (LDZ-CAL-001), so a gateway within about 300 m of the bay is likely to be needed.

## Prior work

- **Parking occupancy sensing is established.** San Francisco's SFpark pilot (2011 to 2013) collected and published real-time availability for 7,000 of the city's 28,800 metered spaces ([SFMTA](https://www.sfmta.com/projects/sfpark-pilot-program)). Commercial in-ground and surface parking sensors are sold today, usually as closed devices tied to a vendor's platform and subscription.
- **Curb data standards exist.** The Open Mobility Foundation's Curb Data Specification defines a Curbs API for bay locations and rules, an Events API that can take events from sensors, and a Metrics API for dwell time and occupancy ([Open Mobility Foundation](https://www.openmobilityfoundation.org/about-cds/)). An open sensor that can feed this format lets cities compare sensor data with carrier data.
- **Cities are testing digital curbs.** In 2024 a collaborative of cities funded through the US Department of Transportation SMART grants program began comparative research on curb infrastructure, policy and demand, with the Urban Freight Lab ([Urban Freight Lab](https://urbanfreightlab.com/research-projects/open-mobility-foundation-smart-grant-curb-collaborative/)).
- **Low-power magnetometers are cheap and common.** Parts such as the LIS2MDL are 3-axis, 16-bit sensors with a ±50 gauss range, a single-measurement mode and an operating range of -40 to +85 °C ([STMicroelectronics](https://www.st.com/en/mems-and-sensors/lis2mdl.html)).
- **The lab's FieldNode** provides the LoRaWAN radio core, firmware base and, for the sign option, the solar power and pole mount.

What is missing is an open, inspectable bay sensor that a small city or a community group can build, bond to the road and connect to any LoRaWAN server, with data in an open curb format and no camera.

## Constraints

- Garage-buildable prototype, $120 USD or less for a two-slot bay (two pucks). The optional sign and its host FieldNode are costed separately and are outside this budget (LDZ-DDR-001, D6, adopted for TRL 3 pending Amish's review).
- No cameras or microphones; the device may report only slot state (free or occupied), timestamps and device health.
- No cutting or coring of the road for the prototype; the puck is bonded to the surface and removable.
- Installation only with the road authority's permit, by a trained crew under traffic management.
- Battery powered for at least five years; no wiring in the road.
- Uses the FieldNode radio core so firmware and tools are shared across the lab.
- The sign option needs a private network server (such as TwinKit) or a city network that allows about 200 downlinks a day; The Things Network allows 10 per device ([TTN](https://www.thethingsnetwork.org/docs/lorawan/duty-cycle/)).
- Must survive being driven over by loaded delivery trucks, road salt, water, oil and summer road temperatures.

## Out of scope

- Payment, booking or reservation of bays (the data can feed such systems later).
- Enforcement actions or identifying vehicles; LoadZone never reads number plates.
- Passenger car parking guidance at scale (the same puck could do it, but it is not the target).
- In-ground (cored) installation, which needs road works; noted as a later variant.

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design

For LoadZone the intended users are delivery drivers, a city curb or transport team and the shops on one test street. Questions for them: would drivers look at a sign, a map layer or neither; which bay lengths and slot splits are typical; and which data the city needs to act on.
