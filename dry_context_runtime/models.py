from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ContextBlock:
    id: str
    content: str
    tags: set[str] = field(default_factory=set)
    token_estimate: int = 0


@dataclass(frozen=True)
class AgentSpec:
    id: str
    extends: list[str] = field(default_factory=list)
    adds: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class PolicyRule:
    id: str
    when: dict[str, Any]
    include: list[str] = field(default_factory=list)
    exclude: list[str] = field(default_factory=list)


@dataclass
class RuntimeState:
    """In-memory cache snapshot for a conversation/session."""

    cached_blocks: set[str] = field(default_factory=set)
    summary_refs: dict[str, str] = field(default_factory=dict)


@dataclass
class PlanResult:
    required: set[str]
    inject: set[str]
    keep_cached: set[str]
    evict: set[str]
