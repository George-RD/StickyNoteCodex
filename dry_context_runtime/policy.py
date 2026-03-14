from __future__ import annotations

from .models import PolicyRule


class PolicyEngine:
    @staticmethod
    def apply(
        *,
        rules: list[PolicyRule],
        signal: dict[str, str],
        current: set[str],
    ) -> set[str]:
        result = set(current)
        for rule in rules:
            if PolicyEngine._matches(rule, signal):
                result.update(rule.include)
                result.difference_update(rule.exclude)
        return result

    @staticmethod
    def _matches(rule: PolicyRule, signal: dict[str, str]) -> bool:
        for key, expected in rule.when.items():
            if signal.get(key) != expected:
                return False
        return True
