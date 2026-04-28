---
name: pr-comments
description: Fetch PR review comments, triage against codebase, apply fixes, generate reply report.
arguments:
  - name: pr_number
    description: Pull request number
    required: true
allowed-tools: Bash, Read, Edit, TodoWrite
model: opus
---

# PR Comments Review

Address PR review comments using MCRF with progressive confidence tracking.

## MCRF Workflow

**DECOMPOSE** → Fetch comments, detect sources (Phase 1)  
**SOLVE** → Categorize by action required (Phase 2)  
**VERIFY** → Read code, validate claims (Phase 3)  
**SYNTHESIZE** → Generate reply report (Phase 4)  
**REFLECT** → Final confidence + caveats

## Phase 1: Fetch & Parse (DECOMPOSE)

Detect repo owner/name and fetch all comment sources:

```bash
# Repo metadata
gh repo view --json nameWithOwner --jq '.nameWithOwner'

# PR overview
gh pr view $pr_number --json title,body,state,comments,reviews,reviewDecision

# Inline review comments
gh api repos/{owner}/{repo}/pulls/$pr_number/comments \
  --jq '.[] | {id, path, line, body, user: .user.login}'

# Review-level comments
gh api repos/{owner}/{repo}/pulls/$pr_number/reviews \
  --jq '.[] | {id, user: .user.login, state, body}'
```

**Report**: Count by source, parse confidence per comment.

### CodeRabbit Bot Parsing

CodeRabbit embeds structured feedback inside review bodies using nested `<details>` HTML blocks:

- **Actionable comments**: marked with `_Potential issue_` and severity badges
- **Nitpick comments**: inside `<summary>Nitpick comments</summary>` blocks, contain file path and line ranges
- **Outside diff comments**: inside `<summary>Outside diff range comments</summary>` blocks
- **Prompt for AI Agents**: inside `<summary>Prompt for AI Agents</summary>` — use these as implementation hints but always verify against code first

**Human patterns**: Short, conversational. "food for thought", "not a change on this PR", questions → typically observations not action requests.

## Phase 2: Triage & Plan (SOLVE)

Categorize each comment:

| Category | Criteria | Action |
|----------|----------|--------|
| **Actionable** | Bugs, factual errors, misleading docs, test gaps | Fix |
| **Food for thought** | Observations, future ideas, questions | Acknowledge |
| **Out of scope** | Requires changes beyond PR purpose | Acknowledge + explain |

Present triage table for user approval before proceeding:

| # | Source | File | What | Why | Category | Confidence |
|---|--------|------|------|-----|----------|------------|

**Wait for user confirmation.**

## Phase 3: Verify & Fix (VERIFY)

Track with TodoWrite. For each actionable item:

1. **Read** referenced file
2. **Assess** claim confidence after reading code
3. **Fix** only if confidence > 0.9 (else flag for manual review)
4. **Apply** using Edit tool
5. **Mark** TodoWrite item complete

**Constraints**: No commits, no GitHub API posts, only working tree edits.

## Phase 4: Generate Reply Report (SYNTHESIZE)

One section per comment with GitHub links:

- **Inline**: `https://github.com/{owner}/{repo}/pull/{pr}#discussion_r{id}`
- **Review**: `https://github.com/{owner}/{repo}/pull/{pr}#pullrequestreview-{id}`

**Format**:

```
### [Comment 1](link) — User: description ([file:L42](path#L42))
Confidence: 0.95

` ` `markdown
Fixed — what was done.
` ` `

---

### [Comment 2](link) — User: review nitpicks
Confidence: 0.90

` ` `markdown
All N items addressed:
- Item 1 description
- Item 2 description
` ` `
```

**Grouping**: Combine review-body nitpicks (CodeRabbit or human) under single section using review ID.

## Final Summary (REFLECT)

1. **Overall confidence** (0.0-1.0)
2. **Caveats**: Low-confidence fixes, ambiguous comments
3. **Manual review needed**: Items ≤ 0.9 confidence