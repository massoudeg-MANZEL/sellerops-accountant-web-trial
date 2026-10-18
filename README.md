# SellerOps Accountant Web Trial v0.3

Extends v0.2 with an explicit fail-closed CP15 engine integration contract. **Not a CP15 engine implementation**. No financial close functionality.

## Deployment
Upload `app.py`, `engine_contract.py`, `requirements.txt` to the existing GitHub repository (README optional). Streamlit will redeploy. Do not upload transaction data or internal engine files to a public repository.

## Tests
`python -m unittest test_engine_contract.py`

## Scope
- v0.2 CSV descriptive inspection preserved.
- Contract states required inputs and planned outputs, with NOT_CONNECTED status.
- Missing original engine is an explicit blocking dependency. No CP15 rules invented.
- Public deployment is not suitable for sensitive MANZEL data.
