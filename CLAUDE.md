# `CLAUDE.md`

Claude Code plugin packaging agents and skills for team sharing.

## Directives

- Inspect `agents/` and `skills/` to understand available capabilities
- Use [agent-expert](agents/agent-expert.md) when creating or modifying agents (includes token optimization)
- Use [skill-expert](agents/skill-expert.md) when creating or modifying skills (includes token optimization)
- Validate all `[text](path)` markdown links after changes
- Update `README.md` when agents/skills are added/removed or descriptions change

## Component Requirements

| Component | MCRF | Persona | Shared Policy |
|-----------|------|---------|---------------|
| **Agents** | Required (domain-adapted) | Required (`/agent-persona`) | Reference if applicable |
| **Skills** | Optional (for complex logic) | Not needed | N/A |

**Shared policies** (`*-common.md`): Referenced by agents for cross-cutting standards. Not invoked directly.

**Agent vs Skill**: Use agents for stateful, multi-step reasoning. Use skills for discrete, repeatable tasks with minimal tokens.

## Meta-Cognitive Reasoning Framework (MCRF)

When working in this repository, apply this framework:

| Step | Action | This Repository |
|------|--------|-----------------|
| **DECOMPOSE** | Break into sub-problems | Identify affected agents, skills, docs |
| **SOLVE** | Address with confidence 0.0-1.0 | Create/modify with token efficiency |
| **VERIFY** | Check correctness | Validate links, YAML frontmatter, structure |
| **SYNTHESIZE** | Integrate results | Update README, cross-references |
| **REFLECT** | If confidence <0.8, iterate | Re-check against agent-expert/skill-expert patterns |

Skip for trivial changes (typos, single-line fixes).

## Structure

| Path | Contents |
|------|----------|
| `agents/*.md` | Agents (YAML frontmatter + MCRF + Persona) |
| `skills/*/SKILL.md` | Skills |
| `.claude-plugin/plugin.json` | Plugin manifest (for local development) |
| `.claude-plugin/marketplace.json` | Marketplace catalog (for distribution) |
| `README.md` | User documentation |
| `CLAUDE.md` | Agent/development guidance |
