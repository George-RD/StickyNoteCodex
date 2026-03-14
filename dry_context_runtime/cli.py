from __future__ import annotations

import argparse
import json

from .engine import ContextRuntime
from .models import RuntimeState
from .store import ConfigLoader


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="DRY context runtime")
    sub = parser.add_subparsers(dest="command", required=True)

    plan = sub.add_parser("plan", help="Compute minimal injection plan")
    plan.add_argument("--config", required=True)
    plan.add_argument("--agent", required=True)
    plan.add_argument("--task", required=True)
    plan.add_argument("--workflow", default="default")
    plan.add_argument("--cached", nargs="*", default=[])

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "plan":
        config = ConfigLoader.load(args.config)
        runtime = ContextRuntime(config)
        state = RuntimeState(cached_blocks=set(args.cached))
        plan = runtime.plan_call(
            agent_id=args.agent,
            task=args.task,
            workflow=args.workflow,
            state=state,
        )

        payload = {
            "required": sorted(plan.required),
            "inject": sorted(plan.inject),
            "keep_cached": sorted(plan.keep_cached),
            "evict": sorted(plan.evict),
            "prompt_segments": runtime.materialize(plan.inject),
        }
        print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
