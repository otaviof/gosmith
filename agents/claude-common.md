---
name: claude-common
type: context
description: "Shared policies for Claude Code extensibility. Referenced by agent-expert, skill-expert."
---

# Skills vs. Agents

Both extend Claude Code capabilities but serve different purposes.

| Aspect | Skill | Agent |
|--------|-------|-------|
| **Purpose** | Execute a discrete, repeatable task | Embody domain expertise and reasoning |
| **Invocation** | User-invoked via `/skill-name` | Context-invoked based on task type |
| **Scope** | Single action with clear input/output | Multi-step problem-solving |
| **State** | Stateless (run and done) | Stateful reasoning across a session |
| **Model** | Prefer `haiku` (simple transforms) | Match complexity (`sonnet`/`opus`) |
| **Token budget** | Minimal (<500 tokens ideal) | As needed for expertise depth |

## When to Create

| Indicator | → Skill | → Agent |
|-----------|---------|---------|
| Action type | Single, discrete | Multi-step reasoning |
| I/O contract | Well-defined, deterministic | Context-dependent |
| Invocation | Repeated with different args | Task-type triggered |
| Judgment | Minimal | Domain expertise required |

**Examples:** Skills: `/jira`, `/commit`, `/format` · Agents: `go-architect`, `go-reviewer`, `openshift-expert`

**Authority:** `skill-expert` for skills, `agent-expert` for agents.

---

# Token Optimization

## Techniques

| Do | Don't |
|----|-------|
| Tables over bullet lists | Repeated bold headers with colons |
| Cross-reference shared content | Copy-paste context |
| Use/Skip columns for selection | Verbose "Do NOT use" lists |
| Imperative: "**Validate**: `pattern`" | Tutorial: "You should validate by..." |
| Terse output: "Created `file.md`" | Verbose: "Operation completed successfully..." |
| Start minimal | Kitchen sink features |

**Rules:** Execution-critical only. Reference, don't repeat. Trust model reasoning.

## Preserve As-Is

Code examples, role identity prose — these require prose flow or exact syntax. MCRF lives in [mcrf.md](mcrf.md); agents reference it, don't inline it.

## Checklist

| Section | Action |
|---------|--------|
| "When to Use" | → Use/Skip table |
| Numbered principles | → Principle/Application table |
| Repeated content | → Reference common file |

---

# Link Validation

**Directive:** Verify all document links when creating or modifying agents/skills.

| Check | Requirement |
|-------|-------------|
| File links | Target file exists at path |
| Anchor links | Target section header exists (e.g., `#workflow` not `#agent-workflow`) |
| Skill references | Skill exists in `skills/` directory |
| Cross-references | Linked content matches current structure |

**Common issues:** Renamed sections break anchors. Moved files break paths. Verify after refactoring.