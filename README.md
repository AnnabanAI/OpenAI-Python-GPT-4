# AnnabanAI Provider-Neutral Governance Gateway

A persistent reference implementation for routing model requests through a human-governed policy layer, recording tamper-evident audit events, and requiring approval before protected actions.

## Status
- Implemented: provider-neutral adapter interface, policy checks, approval gate, JSONL SHA-256 audit chain, unit tests, and a local benchmark.
- Not claimed: provider-native integration, independent factual verification, production certification, or partnership with any model provider.
- External actions are not implemented. A production executor must independently enforce authorization.

## Quick start
Requires Python 3.11 or newer.

    python -m venv .venv
    source .venv/bin/activate
    python -m pip install -e ".[dev]"
    pytest
    annabanai-gateway --provider demo --prompt "What does AnnabanAI do?"

On Windows PowerShell, activate with .venv\Scripts\Activate.ps1.

## Providers
Adapters accept a prompt string and return response text. Real adapters require official SDKs, valid credentials, timeouts, rate limits, and budget limits. Never commit API keys.

## Audit integrity
The JSONL audit chain detects record changes when checked against a trusted checkpoint. A hash chain alone does not prevent truncation or file replacement, and it does not prove logged claims are true. Production deployments should anchor checkpoints in independent, access-controlled storage.

## Human governance
Protected actions are denied unless both an authenticated-human assertion and explicit approval are present. This reference implementation does not authenticate users; production callers must obtain identity and approval from a trusted authorization service, never from untrusted request fields.

## Contents
- config/policy.yaml — default policy.
- src/annabanai_gateway/ — gateway, audit chain, demo adapter, CLI.
- tests/ — policy and audit tests.
- benchmarks/ — offline smoke benchmark.
- docs/provider-integration-proposal.md — proposed integration and evaluation plan.

Provider integrations are disabled until implemented, authorized, and configured.
