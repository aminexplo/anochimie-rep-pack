### Replication package

This folder contains the replication package for the paper _Automated Detection of Workarounds for Software Improvement._ It includes the experimental applications and datasets from the reference user study, the LLM prompts, outputs, and calibration files used for workaround detection, as well as the assessment materials and developer user study artifacts for insight generation.

### Prerequisites
- Python 3.11.7
- Windows 11 (tested platform; apps use Tk/CustomTkinter)
- Install dependencies:
```bash
pip install customtkinter==5.2.2 tkcalendar pillow
```
- For regenerating the paper figures (`figure-generation/`):
```bash
pip install pandas numpy matplotlib openpyxl
```

### Layout
- `0-workarounds-reference-user-study-dataset/`
  - `code/`: TA apps (Open/Predetermined/Controlled), HR app, REG app, common widgets, and themes/icons
  - `data/`: HR/REG/TA datasets (chunked CSVs)
  - `instructions/`: task PDFs for each app
  - `exit_survey.xlsx`, `stat_tests.xlsx`, `user_workaround_data.csv`
- `1-workaround-detection-package/`
  - `prompts/`: prompt-emp.txt, prompt-conf.txt
  - `LLM-results/`: model-specific outputs for employee and conference tasks 
  - `calibrations/`: calibration spreadsheets
  - `workarounds_assessment-v3.xlsx`
  - `Precision and recall of each algorithm on the forms.pdf`: per-algorithm detection visualizations
- `2-insight-generation-package/`
  - `instructions/`: assessment PDFs
  - `llm-mapping.txt`, `user-study-dev-results.xlsx` (developer ratings and statistical tests)
  - Completeness/Clarity/Difficulty rating PDFs: per-criterion visualizations of the developer ratings
- `figure-generation/`
  - `make_paper_figures.py`: regenerates the paper figures (RQ1 detection bars, RQ4 Likert box plots) from the raw data in this package
  - `fig-rq1-detection-bars.pdf`, `fig-rq4-likert-boxplots.pdf`: the generated figures

### Run the reference user study apps
1) Open a terminal and change directory so assets resolve correctly:
```bash
cd material/rep/0-workarounds-reference-user-study-dataset/code
```
2) Launch an app:
```bash
python ta1.py    # TA - Open
python ta2.py    # TA - Predetermined
python ta3.py    # TA - Controlled
python hr.py     # HR
python reg.py    # REG
```
3) Follow the corresponding PDF in `material/rep/0-workarounds-reference-user-study-dataset/instructions`.
4) Logs and saved data will appear under `m_*/logs/<user_name>/` created at runtime.

Note: The datasets intentionally contain fields that do not map 1:1 to the forms (e.g., TA "Bonus", multi-valued topics in REG, multiple phone numbers in HR) to elicit user workarounds.

### LLM prompts and outputs (workaround detection)
- Prompts are in `material/rep/1-workaround-detection-package/prompts/`.
- Model outputs are provided under `material/rep/1-workaround-detection-package/LLM-results/<Model>/` (separate files for employee and conference tasks).
- Calibration sheets are in `material/rep/1-workaround-detection-package/calibrations/`.
- Re-running can yield different outputs; the provided files enable verification.