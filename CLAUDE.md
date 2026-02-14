# `CLAUDE.md`

Claude Code plugin packaging agents and skills for team sharing.

## Directives

- Inspect `agents/` and `skills/` to understand available capabilities
- Use [agent-expert](agents/agent-expert.md) when creating or modifying agents (includes token optimization)
- Use [skill-expert](agents/skill-expert.md) when creating or modifying skills (includes token optimization)
- Validate all `[text](path)` markdown links after changes
- Update `README.md` when agents/skills are added/removed or descriptions change
- Bump version in [plugin.json](.claude-plugin/plugin.json) and [marketplace.json](.claude-plugin/marketplace.json) when modifying agents or skills

## Component Requirements

| Component | MCRF | Persona | Shared Policy |
|-----------|------|---------|---------------|
| **Agents** | Required (reference [mcrf.md](agents/mcrf.md), [execution-discipline.md](agents/execution-discipline.md)) | Required (`/agent-persona`) | Reference if applicable |
| **Skills** | Optional (for complex logic) | Not needed | N/A |

**Shared policies** (`*-common.md`): Referenced by agents for cross-cutting standards. Not invoked directly.

**Agent vs Skill**: Use agents for stateful, multi-step reasoning. Use skills for discrete, repeatable tasks with minimal tokens.

## Meta-Cognitive Reasoning Framework (MCRF)

All agents reference [mcrf.md](agents/mcrf.md) for structured reasoning. When working in this repository, apply MCRF per that directive. Skip for trivial changes (typos, single-line fixes).

## Structure

| Path | Contents |
|------|----------|
| `agents/mcrf.md` | Meta-Cognitive Reasoning Framework (shared) |
| `agents/execution-discipline.md` | Behavioral guardrails (shared) |
| `agents/*.md` | Agents (YAML frontmatter + Persona) |
| `skills/*/SKILL.md` | Skills |
| `.claude-plugin/plugin.json` | Plugin manifest (for local development) |
| `.claude-plugin/marketplace.json` | Marketplace catalog (for distribution) |
| `README.md` | User documentation |
| `CLAUDE.md` | Agent/development guidance |
