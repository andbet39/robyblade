import csv
from collections import Counter

with open("beyblade_parts.csv") as f:
    rows = list(csv.DictReader(f))

total = len(rows)
cats = Counter(r["category"] for r in rows)
print(f"Total rows: {total}")
print("By category:")
for cat, n in sorted(cats.items()):
    print(f"  {cat:15s} {n}")

blade = next(r for r in rows if r["part_id"] == "Blade-DS-001")
print("\nSpot-check Blade-DS-001:")
print(f"  name={blade['name']}  type={blade['type']}  weight_g={blade['weight_g']}  stock_combo={blade['stock_combo']}  ratchet={blade['stock_combo_ratchet']}  bit={blade['stock_combo_bit']}")

rat = next(r for r in rows if r["part_id"] == "Rat-360-001")
print("Spot-check Rat-360-001:")
print(f"  name={rat['name']}  contact_points={rat['contact_points']}  height_mm={rat['height_mm']}  weight_g={rat['weight_g']}")

bit = next(r for r in rows if r["part_id"] == "Bit-F-001")
print("Spot-check Bit-F-001:")
print(f"  name={bit['name']}  gears={bit['gears']}  burst={bit['burst_resistance']}  weight_g={bit['weight_g']}")
