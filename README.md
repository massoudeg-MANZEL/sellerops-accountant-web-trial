# SellerOps Accountant Web Trial v0.1

A runnable Streamlit **data inspection prototype**, not the CP15 Accountant engine.

## Local run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Online hosting
Deploy this folder on a private Streamlit-compatible hosting environment, with access controls and a data-handling policy. Do not upload MANZEL confidential reports to a public deployment.

## Scope
- Amazon Transaction CSV upload with preamble auto-detection.
- File row counts, Refund type counts, transaction type distribution, and a preview export.
- No accounting calculations, financial close, M08/M09 rule implementation, or CP15 equivalence claims.
- CP15 is the explicitly adopted authority; older pointer CP13 is stale.
