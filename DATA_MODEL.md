# Beyblade X — Data Model Specification

> Version: 1.0  
> Derived from scraped data: `beyblade_parts.csv`, `beyblade_meta_analytics.csv`, `beyblade_combined.csv`  
> Scope: Beyblade X (BX/UX/CX product lines) — tournament meta analytics + parts catalogue

---

## Overview

The dataset models two distinct domains:

| Domain | Purpose | Primary CSV |
|---|---|---|
| **Parts Catalogue** | Physical parts with specs | `beyblade_parts.csv` |
| **Meta Analytics** | Tournament combo performance | `beyblade_meta_analytics.csv` / `beyblade_combined.csv` |

A **Combo** is an assembly of exactly one Blade + one Ratchet + one Bit, plus optional Assist Blade and Lock Chip. Performance is tracked per Season.

---

## Entity Definitions

### 1. `Part` — Base catalogue entry

All scraped parts share a common base schema. Category-specific fields extend it.

| Field | Type | Required | Description |
|---|---|---|---|
| `part_id` | `string` | ✅ | Unique identifier. Format: `{Category}-{Initials}-{Seq}` e.g. `Blade-DS-001`, `Bit-F-001`, `Rat-060-001` |
| `name` | `string` | ✅ | Human-readable name. e.g. `Dran Sword`, `1-60`, `F (Flat)` |
| `category` | `enum` | ✅ | See **Part Categories** table below |
| `is_beyblade_part` | `boolean` | ✅ | `true` if it is an actual bey component; `false` for accessories, launchers, arenas |
| `product_code_full` | `string` | ✅ | Official product code. e.g. `BX-01`, `UX-03`, `CX-13` |
| `product_line` | `enum` | ✅ | `BX` \| `UX` \| `CX` |
| `product_number` | `string` | ⚠️ | Numeric suffix of the product code. May be absent for sets/promos |
| `source_url` | `string (URL)` | ✅ | Canonical URL on bey-library or equivalent catalogue source |
| `variant_count` | `integer ≥ 0` | ✅ | Number of known colour/material variants. `0` if unknown or single |

#### Part Categories

| Value | Description |
|---|---|
| `blade` | Main blade (standard BX/UX) |
| `over-blade` | Over-Blade attachment (CX line) |
| `assist-blade` | Assist Blade attachment (CX line) |
| `ratchet` | Ratchet (middle layer) |
| `bit` | Bit (bottom driver) |
| `x-over` | Legacy cross-over / OB-series blades |
| `other` | Non-part products (launchers, arenas, accessories) |

---

### 2. `Blade` — extends `Part` where `category = "blade"`

| Field | Type | Required | Notes |
|---|---|---|---|
| `type` | `enum` | ✅ | `Attack` \| `Defense` \| `Stamina` \| `Balance` |
| `spin` | `enum` | ✅ | `Right` \| `Left` |
| `weight_g` | `float` | ✅ | Weight in grams |
| `stock_combo` | `string` | ⚠️ | Default Ratchet+Bit combo string. Format: `{ratchet_name} {bit_name}` e.g. `3-60 Flat` |
| `stock_combo_ratchet` | `string` | ⚠️ | Ratchet name component of stock combo. e.g. `3-60` |
| `stock_combo_bit` | `string` | ⚠️ | Bit name component of stock combo. e.g. `Flat` |

---

### 3. `XOverBlade` — extends `Part` where `category = "x-over"`

Same fields as `Blade`. These are older OB/DZ-series blades that are legal in some formats.

| Field | Type | Required | Notes |
|---|---|---|---|
| `type` | `enum` | ✅ | `Attack` \| `Defense` \| `Stamina` \| `Balance` |
| `spin` | `enum` | ✅ | `Right` \| `Left` |
| `weight_g` | `float` | ✅ | Weight in grams |
| `stock_combo` | `string` | ⚠️ | Same format as Blade's `stock_combo` |
| `stock_combo_ratchet` | `string` | ⚠️ | |
| `stock_combo_bit` | `string` | ⚠️ | |

---

### 4. `AssistBlade` — extends `Part` where `category = "assist-blade"`

Assist Blades are secondary blades attached to a Blade in the CX (Cross) system.

| Field | Type | Required | Notes |
|---|---|---|---|
| `type` | `enum` | ✅ | `Attack` \| `Defense` \| `Stamina` \| `Balance` |
| `spin` | `enum` | ✅ | `Right` \| `Left` |
| `weight_g` | `float` | ✅ | Weight in grams |
| `high_level_mm` | `float` | ⚠️ | Height of the elevated position in mm. Only present for height-changing parts |

---

### 5. `OverBlade` — extends `Part` where `category = "over-blade"`

Over-Blades are wraparound attachments in the CX system.

| Field | Type | Required | Notes |
|---|---|---|---|
| `type` | `enum` | ✅ | `Attack` \| `Defense` \| `Stamina` \| `Balance` |
| `spin` | `enum` | ✅ | `Right` \| `Left` |
| `weight_g` | `float` | ⚠️ | Weight in grams (may be absent for some promos) |

---

### 6. `Ratchet` — extends `Part` where `category = "ratchet"`

Ratchets determine gear count and height. The `name` encodes both: `{contact_points}-{height_tenths}` where `height_tenths / 10 = height_mm`. Example: `1-60` → 1 contact point, 6.0 mm.

| Field | Type | Required | Notes |
|---|---|---|---|
| `weight_g` | `float` | ✅ | Weight in grams |
| `contact_points` | `integer ≥ 0` | ✅ | Number of contact points (burst resistance protrusions). Derived from first part of name |
| `height_mm` | `float` | ✅ | Height in millimetres. Derived from second part of name (e.g. `60` → `6.0 mm`, `80` → `8.0 mm`) |
| `gears` | `integer` | ⚠️ | Number of internal gear teeth. Present only for Gear Ratchets |

> **Naming convention**: The scraper must parse `contact_points` and `height_mm` directly from the name string, not infer them. Both must be stored as separate numeric fields.

---

### 7. `Bit` — extends `Part` where `category = "bit"`

Bits are the bottom drivers and are categorised by movement profile.

| Field | Type | Required | Notes |
|---|---|---|---|
| `type` | `enum` | ✅ | `Attack` \| `Defense` \| `Stamina` \| `Balance` |
| `weight_g` | `float` | ✅ | Weight in grams |
| `gears` | `integer` | ⚠️ | Gear count. Only present for Gear Bits |
| `burst_resistance` | `enum` | ⚠️ | `High` \| `Low`. See note on gimmick bits below |

> **Gimmick Bits** (e.g. mode-change or height-change bits): `burst_resistance` should still be one of `High`/`Low` reflecting the default/primary mode. A free-text `notes` field is recommended for describing the gimmick behaviour. Do **not** embed gimmick descriptions in the `burst_resistance` field.

---

### 8. `Combo` — assembled bey used in tournaments

A Combo is identified by its component combination. The same combo may appear across multiple seasons.

| Field | Type | Required | Notes |
|---|---|---|---|
| `combo_key` | `string` | ✅ | Pipe-separated composite key. Format: `{blade}\|{assist_blade}\|{ratchet}\|{bit}\|{lock_chip}`. Use literal `None` for absent optional parts |
| `combo_url` | `string (URL)` | ✅ | Source URL for this combo on beybladexmeta.com or equivalent |
| `blade` | `string` | ✅ | Blade name (FK → `Blade.name` or `XOverBlade.name`) |
| `assist_blade` | `string \| null` | ✅ | Assist Blade name, or `null` / `"None"` if not used |
| `ratchet` | `string` | ✅ | Ratchet name (FK → `Ratchet.name`) |
| `bit` | `string` | ✅ | Bit name (FK → `Bit.name`) |
| `lock_chip` | `string \| null` | ✅ | Lock Chip identifier, or `null`/`"None"`. Currently observed: `"emperor"` |

---

### 9. `ComboPerformance` — tournament performance per combo per season

One record per (`combo_key`, `season`) pair.

| Field | Type | Required | Notes |
|---|---|---|---|
| `rank` | `integer ≥ 1` | ✅ | Rank within the season leaderboard |
| `season` | `string` | ✅ | Season label. Format: `Season YYYY` \| `Off Season YYYY` \| `All Time` |
| `combo_key` | `string` | ✅ | FK → `Combo.combo_key` |
| `combo_url` | `string (URL)` | ✅ | Direct URL to the combo+season page |
| `score` | `integer` | ✅ | Aggregate score (tournament point system) |
| `placements_1st` | `integer ≥ 0` | ✅ | Count of 1st place finishes |
| `placements_2nd` | `integer ≥ 0` | ✅ | Count of 2nd place finishes |
| `placements_3rd` | `integer ≥ 0` | ✅ | Count of 3rd place finishes |
| `placements_4th` | `integer ≥ 0` | ✅ | Count of 4th place finishes |
| `total_placements` | `integer ≥ 0` | ✅ | Sum of all placements (must equal sum of 1st–4th) |
| `win_rate` | `float [0, 1]` | ✅ | Fraction of results that are 1st place |
| `podium_rate` | `float [0, 1]` | ✅ | Fraction of results in top 3 |

---

### 10. `CombinedRecord` — denormalised flat view (beyblade_combined.csv)

`beyblade_combined.csv` merges `ComboPerformance` with selected part specs for easier analysis. It is a **derived** / **output** artefact, not a source of truth. Scrapers producing the combined file must additionally include:

| Field | Type | Source |
|---|---|---|
| `blade_weight_g` | `float` | `Blade.weight_g` |
| `blade_type` | `enum` | `Blade.type` |
| `blade_spin` | `enum` | `Blade.spin` |
| `blade_contact_points` | `integer` | Reserved — not populated in v1 |
| `ratchet_weight_g` | `float` | `Ratchet.weight_g` |
| `ratchet_gears` | `integer` | `Ratchet.gears` |
| `ratchet_burst_resistance` | `enum` | Derived from `Ratchet.contact_points` (see note) |
| `bit_weight_g` | `float` | `Bit.weight_g` |
| `bit_type` | `enum` | `Bit.type` |
| `bit_height_mm` | `float` | `Bit` height (sourced from ratchet height in v1; clarify in v2) |
| `assist_weight_g` | `float \| null` | `AssistBlade.weight_g` |
| `assist_type` | `enum \| null` | `AssistBlade.type` |
| `assist_high_level_mm` | `float \| null` | `AssistBlade.high_level_mm` |

---

## Relationships

```
Blade ─────────────────────────────┐
AssistBlade (optional) ────────────┤
Ratchet ────────────────────────── ├──► Combo ──► ComboPerformance (per Season)
Bit ────────────────────────────── ┤
LockChip (optional string) ────────┘
```

- One **Combo** references exactly one Blade, one Ratchet, one Bit, and optionally an AssistBlade and a LockChip.
- One **Combo** may have multiple **ComboPerformance** records (one per season it appears in).
- Parts are independent of each other; many combos can share the same parts.

---

## Controlled Vocabularies

### `type` (Blade / AssistBlade / OverBlade / Bit)

| Value | Description |
|---|---|
| `Attack` | Optimised for knockouts / ring-outs |
| `Defense` | Optimised for absorbing hits and surviving |
| `Stamina` | Optimised for outlasting opponents |
| `Balance` | Hybrid — no single dominant trait |

> **Data quality note**: Current data contains `"Balacne"` (typo) and verbose descriptions like `"Plastic (~1.7 g) Assist Blade S (Slash)"`. Scrapers must normalise these to the four canonical values above. Hybrid parts should be categorised as `Balance`.

### `spin`

| Value |
|---|
| `Right` |
| `Left` |

> **Data quality note**: Current data contains `"ring"` — likely a scrape error. Scrapers must produce only `Right` or `Left`.

### `burst_resistance` (Bit)

| Value | Description |
|---|---|
| `High` | Hard to burst |
| `Low` | Easier to burst (typically Attack-type drivers) |

### `product_line`

| Value | Description |
|---|---|
| `BX` | Beyblade X standard line |
| `UX` | Ultimate X line |
| `CX` | Cross / CX system line |

### `season`

Format string. Current observed values:

| Value |
|---|
| `Season 2026` |
| `Off Season 2025` |
| `All Time` |

Future seasons should follow the pattern `Season YYYY` or `Off Season YYYY`.

---

## CSV Format Rules for Scrapers

1. **Encoding**: UTF-8, no BOM.
2. **Delimiter**: comma (`,`).
3. **Header row**: always present, lowercase with underscores.
4. **Null / absent values**: use empty string `""` for truly absent optional fields. Use literal string `"None"` only where the dataset convention already uses it (e.g., `combo_key` segments, `lock_chip`).
5. **Boolean**: use `True` / `False` (Python-style capitalisation, consistent with existing data).
6. **Floats**: use `.` decimal separator. No trailing zeros required. e.g. `6.0`.
7. **Integers**: no decimal point. e.g. `12`, not `12.0`.
8. **URLs**: full absolute URLs, no trailing slash.
9. **`combo_key`**: pipe-separated, no spaces: `{blade}|{assist_blade}|{ratchet}|{bit}|{lock_chip}` — replace absent parts with `None`.
10. **No duplicate rows** within the same (`combo_key`, `season`) pair in analytics CSVs.

---

## Known Data Quality Issues (v1)

| Issue | Location | Impact | Fix Required |
|---|---|---|---|
| `type = "Balacne"` typo | `beyblade_parts.csv` | Query/filter failures | Normalise to `Balance` |
| Verbose `type` strings for Assist Blades | `beyblade_parts.csv` | Not a clean enum | Normalise to canonical 4 values |
| `spin = "ring"` | `beyblade_parts.csv` | Invalid value | Map to correct spin or mark for review |
| Gimmick descriptions in `burst_resistance` | `beyblade_parts.csv` | Not a clean enum | Extract canonical `High`/`Low`, move description to a `notes` field |
| `bit_height_mm` in combined CSV appears to reflect ratchet height | `beyblade_combined.csv` | Misleading field name | Clarify whether this is bit-tip height or ratchet height; rename accordingly |
| `blade_contact_points` always empty | `beyblade_combined.csv` | Missing data | Populate from `Ratchet.contact_points` or clarify intended meaning |
| `ratchet_burst_resistance` in combined CSV always empty | `beyblade_combined.csv` | Missing data | Derive from `Ratchet.contact_points` (0 = no burst) or source from Bit |

---

## Recommended Extensions (Future Scrapers)

| Field | Entity | Description |
|---|---|---|
| `notes` | all parts | Free-text field for gimmick descriptions, errata, special rules |
| `release_date` | `Part` | Official release date for chronological analysis |
| `is_tournament_legal` | `Part` | Boolean flag for ban/restricted lists |
| `tournament_id` | `ComboPerformance` | Link performance to specific tournament events |
| `player_count` | `ComboPerformance` | Number of unique players using this combo per season |
| `image_url` | `Part` | Product/part image for UI use |
| `lock_chip` | `Part` (category) | Promote LockChip from a string field to a proper part entity |
