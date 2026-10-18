"""Fail-closed integration contract. Never claim CP15 computations without the original engine."""
ENGINE_STATUS = "NOT_CONNECTED"
CONTRACT_VERSION = "0.1"

def validate_engine_contract():
    return {
        "contract_version": CONTRACT_VERSION,
        "authority": "CP15 / Master Decision & Facts Register v1.14",
        "engine_status": ENGINE_STATUS,
        "engine_executed": False,
        "financial_close_approved": False,
        "required_inputs": ["amazon_transaction_csv", "returns_master", "updated_cogs"],
        "planned_outputs": ["event_ledger", "reconciliation", "exceptions", "evidence_states"],
        "implementation_note": "Original CP15 engine is not present. No calculations or accounting rules are substituted.",
    }

def run_cp15_engine(*args, **kwargs):
    raise RuntimeError("CP15_ENGINE_NOT_CONNECTED: original validated engine required")
