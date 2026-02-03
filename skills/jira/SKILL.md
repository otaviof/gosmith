---
name: jira
description: Fetch a Jira ticket body as markdown for planning sessions.
argument-hint: TICKET-KEY
allowed-tools: Bash, Write
model: haiku
---

## Instructions

1. **Fetch**: `jira issue view <TICKET-KEY> --plain` (add `--comments N` if requested)
2. **Convert**:
   - YAML frontmatter: `Title`, `Status`, `Link`, `Comments` (if present)
   - Body: `# \`title\`` heading followed by description text only
   - **Exclude from body**: status tables, metadata fields (Type, Assignee, Reporter, Priority, Created, Labels)
   - Convert Jira markup: `{{text}}` → backticks, `[text|url]` → markdown links
   - Strip ANSI codes
3. **Save**: `<TICKET-KEY>.md` (cwd, overwrites)
5. **Report**: Created `<TICKET-KEY>.md`
