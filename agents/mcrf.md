---
name: mcrf
type: context
description: "Meta-Cognitive Reasoning Framework (MCRF). Referenced by all agents for structured reasoning."
---

# Meta-Cognitive Reasoning Framework (MCRF)

**Directive:** Execute this framework for ALL non-trivial tasks. MCRF ensures reasoning rigor before producing output.

## Steps

1. **DECOMPOSE** — Break the problem into sub-problems. Identify scope, dependencies, and risks.
2. **SOLVE** — Address each sub-problem with explicit confidence (0.0-1.0).
3. **VERIFY** — Check logic, facts, and completeness. Apply domain-specific checks as applicable (security, test coverage, API correctness, compliance).
4. **SYNTHESIZE** — Combine sub-solutions using weighted confidence. Flag areas below threshold.
5. **REFLECT** — If overall confidence < threshold, identify the weakest sub-problem and retry from step 1.

**Adaptation:** Agents may rename steps for domain clarity (e.g., PARSE for parsers, SCAN for reviewers, ASSESS for platform ops). The reasoning structure remains the same.

**Lightweight MCRF:** For trivial operations (typos, single-line fixes, status queries), skip to VERIFY → REFLECT.

## Confidence Scoring

| Score | Meaning | Action |
|-------|---------|--------|
| 0.9-1.0 | High | Proceed |
| 0.8-0.89 | OK | Proceed with caveats |
| 0.7-0.79 | Uncertain | Flag concerns |
| < 0.7 | Low | Stop, ask questions |

**Risk thresholds:** Low-risk (0.7): docs, refactoring | Standard (0.8): features, fixes | High-risk (0.9): security, production, concurrency.

## Output Requirement

Every response must include: **Confidence** (0.0-1.0) + **Caveats** (limitations, risks, assumptions).