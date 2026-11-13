# Players under pressure

Streamlit dashboard for the SupeRR Selector Season 2, Round 1 report: the top 10 batters and bowlers under
pressure (IPL and T20I, 2022 to 2026), the pressure definitions, metrics and formulas, the evidence for every
player, the selection decisions, reliability checks, and a re-weighting lab.

Run locally:

    pip install -r requirements.txt
    streamlit run app.py

Deploy on Streamlit Community Cloud: push this folder to a public GitHub repo, then at share.streamlit.io choose
"Create app", pick the repo and branch, and set the main file to `app.py`.

Files:
- `app.py` pages and layout
- `content.py` report text and small tables
- `scoring.py` percentile scoring, near-equal ordering and the pressure rules
- `appdata.py` all the report data, embedded, so the app runs with only the `.py` files
- `data/` optional: the same data as CSV plus the report PDF (only used for the PDF download button)
