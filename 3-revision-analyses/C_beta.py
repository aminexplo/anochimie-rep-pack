# Sensitivity of the selected widget subset to beta.
# F-beta is recomputed from the true positives and flagged records of each subset.
import csv
from pathlib import Path

from calib import FILES, harmonic, label, load

OUT = Path(__file__).resolve().parent / "out" / "C_beta.csv"
BETAS = [0.1, 0.3, 0.5, 1.0]


def fbeta(v, b):
    if v["tp"] == 0:
        return 0.0
    p, r = v["tp"] / v["k"], v["tp"] / v["n"]
    return (1 + b * b) * p * r / (b * b * p + r)


rows = []
for det in FILES:
    data = load(det)
    conf, emp = data["conference"], data["employee"]
    published = max(conf, key=lambda s: harmonic(conf[s]["f"], emp[s]["f"]))
    for b in BETAS:
        h = {s: harmonic(fbeta(conf[s], b), fbeta(emp[s], b)) for s in conf}
        top = max(h.values())
        selected = sorted((s for s in h if abs(h[s] - top) < 1e-12), key=sorted)
        rows.append([det, b, "; ".join(label(s) for s in selected), published in selected,
                     round(fbeta(conf[published], b), 3), round(fbeta(emp[published], b), 3),
                     round(h[published], 3)])

OUT.parent.mkdir(exist_ok=True)
with open(OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["detector", "beta", "selected_subset", "same_as_at_0.3",
                "f_conf_of_0.3_subset", "f_emp_of_0.3_subset", "h_of_0.3_subset"])
    w.writerows(rows)

for r in rows:
    print(r[0], r[1], r[2], r[3])
