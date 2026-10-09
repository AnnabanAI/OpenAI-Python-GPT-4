import json
import pytest
from annabanai_gateway.core import AnnabanGateway, HashChainAudit

def test_adapter_routes_and_audits(tmp_path):
    audit = HashChainAudit(tmp_path / "audit.jsonl")
    gateway = AnnabanGateway({"fake": lambda p: f"reply:{p}"}, audit)
    result = gateway.evaluate("hello", "fake")
    assert result["status"] == "completed"
    assert result["response"] == "reply:hello"
    assert result["executed"] is False
    assert audit.verify() == audit.previous_hash

def test_protected_action_requires_approval(tmp_path):
    gateway = AnnabanGateway({"fake": lambda p: "no"},
                             HashChainAudit(tmp_path / "audit.jsonl"))
    result = gateway.evaluate("pay", "fake", action="authorize_payment")
    assert result["status"] == "approval_required"

def test_approval_does_not_execute_action(tmp_path):
    gateway = AnnabanGateway({"fake": lambda p: "advice"},
                             HashChainAudit(tmp_path / "audit.jsonl"))
    result = gateway.evaluate("review", "fake", action="authorize_payment",
                              human_approved=True, authenticated_human=True)
    assert result["status"] == "completed"
    assert result["executed"] is False

def test_unknown_action_denied(tmp_path):
    gateway = AnnabanGateway({"fake": lambda p: "reply"},
                             HashChainAudit(tmp_path / "audit.jsonl"))
    assert gateway.evaluate("x", "fake", action="unknown")["status"] == "unknown_action"

def test_empty_prompt_rejected(tmp_path):
    gateway = AnnabanGateway({}, HashChainAudit(tmp_path / "audit.jsonl"))
    with pytest.raises(ValueError):
        gateway.evaluate(" ", "missing")

def test_tampering_detected(tmp_path):
    path = tmp_path / "audit.jsonl"
    audit = HashChainAudit(path)
    audit.append({"value": 1})
    record = json.loads(path.read_text())
    record["event"]["value"] = 99
    path.write_text(json.dumps(record) + "\n")
    with pytest.raises(ValueError):
        HashChainAudit(path)
