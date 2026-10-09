import json, statistics, tempfile, time
from pathlib import Path
from annabanai_gateway.core import AnnabanGateway, HashChainAudit, demo_adapter

def main():
    with tempfile.TemporaryDirectory() as temp:
        audit = HashChainAudit(Path(temp) / "benchmark.jsonl")
        gateway = AnnabanGateway({"demo": demo_adapter}, audit)
        times, count = [], 100
        for i in range(count):
            start = time.perf_counter()
            assert gateway.evaluate(f"benchmark {i}", "demo")["status"] == "completed"
            times.append((time.perf_counter()-start)*1000)
        ordered = sorted(times)
        print(json.dumps({
            "mode":"offline_demo_only","requests":count,"successes":count,
            "failures":0,"p50_latency_ms":round(statistics.median(ordered),3),
            "p95_latency_ms":round(ordered[int(.95*(count-1))],3),
            "audit_chain_verified":audit.verify()==audit.previous_hash,
            "provider_api_cost_usd":None,
            "note":"Does not measure real provider latency, model quality, or API cost."
        }, indent=2))

if __name__ == "__main__":
    main()
