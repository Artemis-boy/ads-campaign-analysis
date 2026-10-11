# Ads Campaign Analysis (Meta Ads Style)

Portfolio project — Junior Data Analyst. End-to-end analysis of 6 months of
Meta Ads-style campaign data (Facebook & Instagram): dirty data generation,
cleaning, metric computation (CTR, CPC, conversion rate, CPA, ROAS),
visualization, and a business report in PDF.

## Results at a glance

- **2,634 clean rows** (from 3,090 raw; 456 removed: 80 duplicates, 240 rows
  with empty cells, 136 cost outliers)
- **Best campaign:** Retargeting Pengunjung (FB) — ROAS **4.20x**, CPA Rp35.690
- **Best volume:** Flash Sale Weekend (IG) — 4,273 conversions, ROAS 4.13x
- **Platform winner:** Instagram (ROAS 4.04x, CPA Rp37.170) vs Facebook
  (ROAS 3.95x, CPA Rp37.987)
- **Key insight:** CTR is flat (~2%) across all campaigns — profitability is
  decided downstream, by conversion rate and CPA.

## Metrics

| Metric | Formula |
|---|---|
| CTR | clicks / impressions × 100 |
| CPC | cost / clicks |
| Conversion rate | conversions / clicks × 100 |
| CPA | cost / conversions |
| ROAS | conversions × Rp150,000 / cost |

## Project structure

```text
ads-campaign-analysis/
├── generate_data.py   # dirty dummy data generator (Meta Ads style)
├── clean.py           # cleaning: dedup, date parsing, NA removal, IQR outliers
├── analyze.py         # CTR/CPC/CR/CPA/ROAS per campaign & platform
├── visualize.py       # 4 PNG charts
├── report.py          # 1-2 page PDF report (Bahasa Indonesia)
├── data/raw/          # raw CSV (generated, git-ignored)
├── data/clean/        # clean CSV (generated, git-ignored)
└── output/            # summary CSVs, PNGs, PDF report
```

## How to run

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python generate_data.py
python clean.py
python analyze.py
python visualize.py
python report.py
```

## Tech

Python · pandas · matplotlib · numpy · fpdf2
