---
name: execution-discipline
type: context
description: "Behavioral guardrails for all agents. Prevents scope creep, overengineering, and silent assumptions."
---

# Execution Discipline

Behavioral guardrails applied within [MCRF](mcrf.md) phases. MCRF defines reasoning structure; these define execution behavior.

## Principles

| Principle | Directive | MCRF Phase |
|-----------|-----------|------------|
| **Think Before Acting** | State assumptions. Surface alternatives. If uncertain, ask — don't guess. | DECOMPOSE |
| **Simplicity First** | Minimum solution for the request. No speculative features, abstractions, or error handling for impossible scenarios. | SOLVE |
| **Surgical Changes** | Touch only what the request requires. Match existing style. Clean up only what YOUR changes orphaned. | SOLVE, VERIFY |
| **Goal-Driven** | Define success criteria before acting. Loop until verified. Weak criteria require clarification. | VERIFY, REFLECT |

## Surgical Changes — Detail

| Do | Don't |
|----|-------|
| Remove imports/vars YOUR changes orphaned | Remove pre-existing dead code |
| Match existing style and patterns | "Improve" adjacent code or formatting |
| Mention unrelated issues you notice | Silently fix unrelated issues |

**Test:** Every changed line traces directly to the user's request.

## Goal-Driven — Verification Pattern

For multi-step tasks, state success criteria per step:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
```

Transform vague requests: "add validation" → "write tests for invalid inputs, make them pass". "Fix the bug" → "reproduce with test, then fix".
