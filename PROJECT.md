# Dry Context Runtime (Fresh Start)

A new Python project for building **DRY for AI** runtime orchestration.

## Core idea

Define context once, then compile minimal per-call projections:

- **Definition DRY**: reusable context blocks and inheritance
- **Transmission DRY**: only inject relevant blocks for each call
- **Storage DRY**: summarize older outputs and keep references
- **Reasoning DRY**: cache decisions and re-use them when valid

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
dry-context plan --config examples/runtime.yaml --agent architect --task design
```

## Configuration model

- `blocks`: canonical context atoms (single source of truth)
- `profiles`: named compositions of blocks (e.g. base/system/workflow)
- `agents`: per-agent inheritance and add-ons
- `policies`: selection rules for when a block applies

See `examples/runtime.yaml`.
