# LoadZone

**Area:** Smart Cities · **Status:** Concept · **Prototype budget:** about $120 USD · **Difficulty:** 2 of 5

A curbside loading bay occupancy sensor that shows delivery drivers which bays are free and gives cities data on curb use.

## Concept rationale

Knowing bay availability reduces circling and double parking.

## Burning platform

Urban deliveries are growing, and curb space is among the most contested public space.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab.

## Problem

Delivery vehicles double-park when loading bays are occupied or unknown, blocking lanes and bike paths.

## Concept

A curbside loading bay occupancy sensor that shows delivery drivers which bays are free and gives cities data on curb use.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- In-ground or surface magnetometer sensor
- FieldNode radio core
- Solar signage option
- Dashboard

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Street furniture and pole mounts must be installed only with the asset owner's permission, by trained crews, with fall protection and traffic management as local rules require.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Smart cities set.
