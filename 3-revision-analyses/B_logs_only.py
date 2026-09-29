# Ablation for Isolation Forest, DBSCAN and SOM: user data + logs, user data only, logs only.
# Each arm removes one source from the published configuration; parameters and seeds are unchanged.
# Needs the detection implementation (main5.py, detection2/) and its aggregated inputs:
#   python B_logs_only.py <path to the detection implementation>
import csv
import os
import sys
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent / "out" / "B_logs_only.csv"
os.chdir(sys.argv[1])
sys.path.insert(0, os.getcwd())

import main5  # noqa: E402

WIDGETS = {
    "Isolation Forest": ("isolation_forest", {"InitialSaveTime", "EditCount", "LogLinesCount", "UsedWidgetsCount"}),
    "DBSCAN": ("dbscan", {"InitialSaveTime", "EditCount", "LogLinesCount", "UsedWidgetsCount",
                          "WidgetsRevisitCount", "AverageWidgetSwitchingDelay"}),
    "SOM": ("som", {"EditCount", "WidgetsRevisitCount", "AverageWidgetSwitchingDelay"}),
}


def run(ds, columns, key, similarity):
    data = pd.read_csv(f"resources/z_final_aggregated/{ds.file}")
    truth = pd.read_csv(main5.GROUND_TRUTH_PATH)
    truth = truth[truth["FormType"] == ds.form_type]
    det = main5.DETECTORS[key](data, list(columns))
    det.other_text_col_for_similarity = similarity
    det.detect_anomalies()
    true_ids = set(truth["RecordID"])
    found = set(det.anomalies[ds.id_column]) if len(det.anomalies) else set()
    p, r, f = main5.compute_prf(true_ids, found)
    return round(f, 3), round(p, 3), round(r, 3), len(true_ids & found), len(found)


rows = []
for name, (key, wset) in WIDGETS.items():
    widgets = [c for c in main5.WIDGET_COLUMNS if c in wset]
    for ds in main5.DATASETS[:2]:
        arms = {
            "user data + logs": (list(ds.original_columns) + widgets, "OverallFeedback"),
            "user data only": (list(ds.original_columns), "OverallFeedback"),
            "logs only": (widgets, ""),
        }
        for arm, (cols, sim) in arms.items():
            rows.append([name, ds.form_type, arm, *run(ds, cols, key, sim)])
            print(*rows[-1], sep="\t")

OUT.parent.mkdir(exist_ok=True)
with open(OUT, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["detector", "form", "arm", "f_beta", "precision", "recall", "true_positives", "flagged"])
    w.writerows(rows)
