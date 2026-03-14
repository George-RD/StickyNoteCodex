from __future__ import annotations

from .models import PlanResult, RuntimeState
from .policy import PolicyEngine
from .store import RuntimeConfig


class ContextRuntime:
    """Compile minimal context projections for each call."""

    def __init__(self, config: RuntimeConfig) -> None:
        self.config = config

    def plan_call(
        self,
        *,
        agent_id: str,
        task: str,
        workflow: str,
        state: RuntimeState,
    ) -> PlanResult:
        agent = self.config.agents[agent_id]
        required = set()

        for profile in agent.extends:
            required.update(self.config.resolve_profile(profile))
        required.update(agent.adds)

        required = PolicyEngine.apply(
            rules=self.config.policies,
            signal={"agent": agent_id, "task": task, "workflow": workflow},
            current=required,
        )

        inject = required - state.cached_blocks
        keep_cached = required & state.cached_blocks
        evict = state.cached_blocks - required

        return PlanResult(required=required, inject=inject, keep_cached=keep_cached, evict=evict)

    def materialize(self, block_ids: set[str]) -> list[str]:
        return [self.config.blocks[b].content for b in sorted(block_ids) if b in self.config.blocks]
