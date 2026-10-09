# AnnabanAI Provider-Neutral Governance Gateway

Persistent reference implementation for routing model requests through a human-governed policy layer, recording a tamper-evident audit chain, and gating protected actions.

## Status
- Implemented here: adapter interface, policy checks, approval gate, JSONL SHA-256 audit chain, tests, and offline benchmark.
- Not claimed: provider-native integration, independent factual verification, production certification, or provider partnership.
- External actions are not implemented. A production executor must independently enforce authorization.

## Quick start
Requires Python 3.11 or newer.

    python -m venv .venv
    source .venv/bin/activate
    python -m pip install -e ".[dev]"
    pytest
    annabanai-gateway --provider demo --prompt "What does AnnabanAI do?"

On Windows PowerShell, use .venv\Scripts\Activate.ps1.

## Contents
- config/annaban-policy.yaml — default policy
- annabanai_gateway/ — gateway, audit chain, demo adapter, CLI
- tests/ — automated tests
- benchmarks/run_benchmark.py — offline smoke benchmark
- docs/provider-integration-proposal.md — integration proposal and acceptance criteria
- main.py — existing OpenAI API example retained in the repository

Real provider adapters require authorized credentials, provider terms, timeouts, rate limits, and budget limits. No API keys should be committed.

The audit chain detects changed records against a trusted checkpoint. It does not prevent truncation or prove the truth of logged claims. Production should anchor checkpoints in independently controlled storage.

Protected-action approval fields in this reference implementation are demonstration inputs, not authentication. Production callers must derive identity and approval from a trusted authorization service. This code does not execute external actions.

Provider integrations remain disabled until implemented, authorized, and configured.
