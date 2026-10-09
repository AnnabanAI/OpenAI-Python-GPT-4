import argparse, json
from .core import AnnabanGateway, HashChainAudit, demo_adapter

def main() -> None:
    parser = argparse.ArgumentParser(description="AnnabanAI governance gateway demo")
    parser.add_argument("--provider", default="demo")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--audit-path", default="annaban_audit.jsonl")
    args = parser.parse_args()
    audit = HashChainAudit(args.audit_path)
    gateway = AnnabanGateway({"demo": demo_adapter}, audit)
    print(json.dumps(gateway.evaluate(args.prompt, args.provider), indent=2))
    print(json.dumps({"audit_chain_verified": True, "last_hash": audit.verify(),
                      "note": "Hash integrity does not prove factual truth."}, indent=2))

if __name__ == "__main__":
    main()
