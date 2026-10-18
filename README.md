# SellerOps Accountant Web Trial v0.2

Independent Streamlit data-quality prototype, **not** the CP15 accounting engine.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Scope

- Amazon Transaction CSV upload (one or multiple files)
- Type counts and Refund row counts
- Required column / blank-value checks
- Exact-content duplicate review signals (never auto-delete)
- JSON quality report and CSV preview export

No financial reconciliation, COGS, returns eligibility, M08/M09 decisioning, or monthly-close certification.
Do not upload sensitive production reports to a public demo without privacy and access review.
