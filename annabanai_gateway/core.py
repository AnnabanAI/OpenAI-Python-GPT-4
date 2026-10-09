from __future__ import annotations
import hashlib, json, os, time, uuid
from pathlib import Path
from typing import Any, Callable

POLICY_VERSION = "1.0.0"
PROTECTED_ACTIONS = frozenset({
    "execute_external_transaction", "modify_production_system",
    "authorize_payment", "publish_binding_commitment",
})
ALLOWED_ACTIONS = frozenset({"analyze", "summarize", "recommend", "compare"})


class HashChainAudit:
    """Append-only JSONL SHA-256 chain; assumes a single writer.

    Detects changed records against a trusted checkpoint. It does not prevent
    truncation or prove truth; production needs locking and external checkpoints.
    """
    def __init__(self, path: str | Path = "annaban_audit.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)
        self.previous_hash = self.verify()

    @staticmethod
    def canonical(value: dict[str, Any]) -> bytes:
        return json.dumps(value, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False).encode("utf-8")

    def verify(self) -> str:
        previous = "GENESIS"
        with self.path.open("r", encoding="utf-8") as stream:
            for n, line in enumerate(stream, 1):
                if not line.strip():
                    continue
                record = json.loads(line)
                if record.get("previous_hash") != previous:
                    raise ValueError(f"Broken audit chain at line {n}")
                body = {k: v for k, v in record.items() if k != "record_hash"}
                expected = hashlib.sha256(self.canonical(body)).hexdigest()
                if record.get("record_hash") != expected:
                    raise ValueError(f"Invalid record hash at line {n}")
                previous = expected
        return previous

    def append(self, event: dict[str, Any]) -> dict[str, Any]:
        body = {
            "event_id": str(uuid.uuid4()),
            "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "policy_version": POLICY_VERSION,
            "previous_hash": self.previous_hash,
            "event": event,
        }
        digest = hashlib.sha256(self.canonical(body)).hexdigest()
        record = {**body, "record_hash": digest}
        fd = os.open(self.path, os.O_WRONLY | os.O_APPEND)
        with os.fdopen(fd, "a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        self.previous_hash = digest
        return record


class AnnabanGateway:
    """Provider-neutral router. This code does not execute external actions."""
    def __init__(self, adapters: dict[str, Callable[[str], str]],
                 audit: HashChainAudit) -> None:
        self.adapters, self.audit = dict(adapters), audit

    def evaluate(self, prompt: str, provider: str, action: str = "analyze",
                 human_approved: bool = False,
                 authenticated_human: bool = False) -> dict[str, Any]:
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")
        if action not in PROTECTED_ACTIONS and action not in ALLOWED_ACTIONS:
            self.audit.append({"decision":"denied","reason":"unknown_action",
                               "provider":provider,"action":action})
            return {"status":"unknown_action","executed":False}
        if action in PROTECTED_ACTIONS and not (
            authenticated_human and human_approved
        ):
            self.audit.append({"decision":"denied",
                               "reason":"human_approval_missing",
                               "provider":provider,"action":action})
            return {"status":"approval_required","executed":False,
                    "action":action}
        adapter = self.adapters.get(provider)
        if adapter is None:
            self.audit.append({"decision":"unavailable",
                               "reason":"adapter_not_registered",
                               "provider":provider,"action":action})
            return {"status":"provider_unavailable","executed":False,
                    "provider":provider}
        start = time.perf_counter()
        try:
            response = adapter(prompt)
        except Exception as exc:
            self.audit.append({"decision":"provider_error","provider":provider,
                               "error_type":type(exc).__name__})
            raise
        latency = (time.perf_counter()-start)*1000
        request_id = str(uuid.uuid4())
        response_hash = hashlib.sha256(response.encode("utf-8")).hexdigest()
        self.audit.append({"decision":"response_received","provider":provider,
                           "request_id":request_id,"action":action,
                           "latency_ms":round(latency,2),
                           "response_sha256":response_hash,
                           "verification_status":"not_independently_verified"})
        return {"status":"completed","executed":False,"provider":provider,
                "request_id":request_id,"latency_ms":round(latency,2),
                "response":response,"response_sha256":response_hash,
                "verification_status":"not_independently_verified"}


def demo_adapter(prompt: str) -> str:
    return ("DEMO ONLY: no external model or factual verification was used. "
            f"Prompt characters: {len(prompt)}.")
