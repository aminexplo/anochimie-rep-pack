# Leave-one-form-out selection of the widget subset.
# The subset is chosen on one form (best F-beta, ties averaged) and evaluated on the other.
import csv
from pathlib import Path
from statistics import mean

from calib import FILES, harmonic, label, load

OUT = Path(__file__).resolve().parent / "out" / "A_lofo.csv"

rows = []
for det in FILES:
    data = load(det)
    conf, emp = data["conference"], data["employee"]
    published = max(conf, key=lambda s: harmonic(conf[s]["f"], emp[s]["f"]))
    for src, tgt in (("conference", "employee"), ("employee", "conference")):
        best = max(v["f"] for v in data[src].values())
        tied = [s for s, v in data[src].items() if v["f"] == best]
        t = [data[tgt][s] for s in tied]
        rows.append([det, src, tgt, len(tied), "; ".join(label(s) for s in sorted(tied, key=sorted)),
                     round(mean(x["f"] for x in t), 3), round(min(x["f"] for x in t), 3),
                     round(max(x["f"] for x in t), 3), round(mean(x["p"] for x in t), 3),
                     round(mean(x["r"] for x in t), 3), data[tgt][published]["f"],
                     data[tgt][frozenset()]["f"]])

OUT.parent.mkdir(exist_ok=True)
with open(OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["detector", "selected_on", "evaluated_on", "tied_subsets", "subsets",
                "f_heldout", "f_min", "f_max", "p_heldout", "r_heldout", "f_in_sample", "f_data_only"])
    w.writerows(rows)

for r in rows:
    print(r[0], r[1][:4], "->", r[2][:4], "ties", r[3], "F", r[5], "(in-sample", r[10], ", data only", r[11], ")")
