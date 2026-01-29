---
name: jira
description: Retrieve a Jira story and convert to markdown for planning sessions. Takes a ticket number like RHTAP-6131.
argument-hint: <TICKET-KEY>
allowed-tools: Bash, Write
model: haiku
---

## Instructions

1. **Validate**: `which jira` must exist, ticket key matches `[A-Z]+-[0-9]+`

2. **Fetch**: `jira issue view <TICKET-KEY> --plain` (add `--comments N` if requested)

3. **Convert**:
   - Title format: `# ` followed by the ticket key, colon, and title wrapped in backticks. Example: # RHTAP-123: \`Fix login bug\`
   - `{{text}}` → `` `text` ``, `[text|url]` → `[text](url)`
   - Strip ANSI codes and Unicode decorations
   - Include Status section: type, status, assignee, reporter, priority, dates
   - Preserve description with markup converted

4. **Save**: `<TICKET-KEY>.md` at user-specified path or cwd (overwrites)

5. **Report**: "Created `<TICKET-KEY>.md` with Jira story content"
