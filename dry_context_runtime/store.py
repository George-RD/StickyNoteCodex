from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from .models import AgentSpec, ContextBlock, PolicyRule


@dataclass
class RuntimeConfig:
    blocks: dict[str, ContextBlock]
    profiles: dict[str, list[str]]
    agents: dict[str, AgentSpec]
    policies: list[PolicyRule]

    def resolve_profile(self, profile_name: str) -> set[str]:
        seen: set[str] = set()

        def _visit(name: str) -> None:
            if name in seen:
                return
            seen.add(name)
            for item in self.profiles.get(name, []):
                if item.startswith("profile:"):
                    _visit(item.split(":", 1)[1])

        _visit(profile_name)
        resolved: set[str] = set()
        for name in seen:
            for item in self.profiles.get(name, []):
                if not item.startswith("profile:"):
                    resolved.add(item)
        return resolved


class ConfigLoader:
    @staticmethod
    def load(path: str | Path) -> RuntimeConfig:
        raw = yaml.safe_load(Path(path).read_text())

        blocks = {
            key: ContextBlock(
                id=key,
                content=value.get("content", ""),
                tags=set(value.get("tags", [])),
                token_estimate=value.get("token_estimate", 0),
            )
            for key, value in raw.get("blocks", {}).items()
        }

        profiles = raw.get("profiles", {})
        agents = {
            key: AgentSpec(
                id=key,
                extends=value.get("extends", []),
                adds=value.get("adds", []),
            )
            for key, value in raw.get("agents", {}).items()
        }

        policies = [
            PolicyRule(
                id=p.get("id", f"policy-{idx}"),
                when=p.get("when", {}),
                include=p.get("include", []),
                exclude=p.get("exclude", []),
            )
            for idx, p in enumerate(raw.get("policies", []), start=1)
        ]

        return RuntimeConfig(blocks=blocks, profiles=profiles, agents=agents, policies=policies)
