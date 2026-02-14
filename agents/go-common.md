---
name: go-common
type: context
description: "Common policies for Go agents. Referenced by go-architect, go-developer, go-tester, go-reviewer."
---

# Go Agent Family — Common Policies

## Code Quality

**Directive:** Use `/go-code` skill for idioms, naming, style, error handling, and YAGNI/KISS principles.

## Design Philosophy

| Principle                | Guidelines                                                                                                                       |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| **Functional-First**     | Functions as parameters over interfaces for single-method behaviors; closures for cross-cutting concerns; avoid over-abstraction |
| **Dependency Injection** | Constructor injection for dependencies; no global state (except immutable `init()` config); accept interfaces, return structs    |
| **Immutability**         | Immutable structs where possible; deliberate pointer usage; value receivers for non-mutating methods                             |
| **Generics**             | Use `[T any]` only when significantly reducing duplication; prefer concrete types                                                |
| **Concurrency**          | All goroutines must specify: context cancellation, backpressure (buffer sizes), exit conditions                                  |
| **Errors**               | Sentinel errors for domain (`ErrNotFound`); wrapped errors (`%w`) for infra; lowercase messages with context                     |

## Go Version

**Minimum:** Go 1.21+ | **Default:** Go 1.23+ (per `go.mod`). Enables: `slices`/`maps`/`cmp`, range-over-func, fuzz.

## Tool Versioning via `go tool`

**Directive:** Use `go tool` (Go 1.24+) over `go install` for reproducible tooling.

| Aspect | `go install` | `go tool` |
|--------|--------------|-----------|
| Version tracking | Manual or none | Automatic in `go.mod` |
| Reproducibility | `@latest` is mutable | Exact version pinned |
| Binary location | `${GOPATH}/bin` (shared) | Module cache (isolated) |
| Team consistency | Requires discipline | Enforced by module |
| Checksums | Not verified | Verified via `go.sum` |

**Setup:** `go get -tool <package>@<version>` — adds tool dependency to `go.mod`

**Execute:** `go tool <name> [args]` — runs tool using pinned version

**Use for:** linters (`golangci-lint`), generators (`protoc-gen-go`), release tools (`goreleaser`)

## Automation via Makefile

**Directive:** Use `/make` skill for Makefile operations. Fall back to raw Go commands only when no Makefile exists.

| Principle | Application |
|-----------|-------------|
| Invocation | `/make --list` \| `/make <target>` \| `/make` (default) |
| Skill-first | Invoke `/make --list` before running commands |
| Target reuse | Depend on existing targets; don't duplicate |
| Graceful fallback | Skill handles missing Makefile automatically |
| Scripts isolation | Scripts NEVER call `make`; Makefile orchestrates |
| Structure | See `/make` skill for modular `include` patterns |

## PLAN.md

- **Default:** `./PLAN.md` — **Alternative:** `docs/design/PLAN.md` if exists
- One active PLAN.md per feature branch

## Step Tracking

PLAN.md **Implementation Steps** table is source of truth.

**Status:** `pending` → `in-progress` → `done` | `blocked: <reason>`

| Agent        | Responsibility                                                        |
| ------------ | --------------------------------------------------------------------- |
| go-developer | Mark `in-progress` before starting, `done` after tests pass           |
| go-tester    | Update testing steps, flag `blocked` if untestable                    |
| go-reviewer  | Mark `done` on approval, `blocked` if changes requested               |
| *All agents* | Ensure steps `done` before handoff                                    |

## Workflow

```
go-architect (PLAN.md) → go-developer (*.go) → go-tester (*_test.go) → go-reviewer (PR) → MERGE
```

## Escalation

| From         | To           | Trigger                  |
| ------------ | ------------ | ------------------------ |
| go-developer | go-architect | Design flaw or ambiguity |
| go-tester    | go-developer | Code not testable        |
| go-reviewer  | go-architect | Deviates from PLAN.md    |

**Format:** `ESCALATION [Type]: [Issue] — Location: [ref] — Suggestion: [fix]`

## Iteration Limits

| Metric                  | Limit | Action                     |
| ----------------------- | ----- | -------------------------- |
| Plan revisions          | 3     | Escalate to human          |
| Developer blockers/step | 2     | Re-evaluate with Architect |
| Reviewer rounds         | 3     | Sync meeting required      |
| Tester critical bugs    | 5     | Pause and re-architect     |

## MCRF

Per [mcrf.md](mcrf.md) — all Go agents MUST apply MCRF before producing output. Use 0.9 threshold for concurrency and security.

## File Naming

| Type     | Pattern     | Example                |
| -------- | ----------- | ---------------------- |
| Package  | lowercase   | `auth`, `handler`      |
| Source   | snake_case  | `user_service.go`      |
| Test     | `*_test.go` | `user_service_test.go` |
| Fixtures | `testdata/` | `testdata/valid.json`  |
| Mocks    | `mock_*.go` | `mock_repository.go`   |

## Output Contract

All responses: **Confidence** (0.0-1.0) + **Caveats** (limitations, risks).

**Blocker (< 0.7):** Stop, document, escalate, request clarification. Domain-specific outputs defined per agent.
