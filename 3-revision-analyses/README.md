### Revision analyses

Scripts for the analyses added in the revision. Each script reads files from this package and writes its results to `out/`. They need Python 3 with `numpy`, `scipy` and `openpyxl`. Run them from this folder, e.g. `python A_lofo.py`.

| Script | Output | Content |
|---|---|---|
| `A_lofo.py` | `out/A_lofo.csv` | Leave-one-form-out selection of the widget subset: the subset is chosen on one form and evaluated on the other (tied subsets averaged), with the in-sample and data-only values for comparison |
| `B_logs_only.py` | `out/B_logs_only.csv` | Ablation for Isolation Forest, DBSCAN and SOM with three arms (user data + logs, user data only, logs only); each arm removes one source from the published configuration. It needs the detection implementation and its aggregated inputs, which are not part of this package |
| `C_beta.py` | `out/C_beta.csv` | Selected widget subset for beta = 0.1, 0.3, 0.5 and 1.0 |
| `D_rq3_aggregation.py` | `out/D_rq3.csv` | Priority of the misalignment categories (RQ3) under the harmonic, arithmetic and geometric means and an effort-weighted harmonic mean |
| `E_rq2_counts.py` | `out/E_rq2.csv` | Number of listed, correct and covered items behind the RQ2 precision and recall of each LLM |
| `F_rq5_friedman.py` | `out/F_rq5.csv` | Friedman test and Kendall's W on the developer ratings of the eight LLMs (RQ5) |

`calib.py` reads the calibration sheets in `1-workaround-detection-package/calibrations/` and is used by `A_lofo.py` and `C_beta.py`.
