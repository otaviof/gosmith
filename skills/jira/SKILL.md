---
name: jira
description: Fetch Jira tickets as clean markdown using native ADF format.
argument-hint: TICKET-KEY [--comments N]
model: haiku
---

## Instructions

1. **Locate**: Find `jira.py` alongside this skill file
2. **Execute**: `python3 <path>/jira.py <TICKET-KEY>` (append `--comments N` to include comments)
3. **Report**: Print script output to stdout

## Features

- Converts Jira's native Atlassian Document Format (ADF) to markdown
- Preserves formatting: **bold**, *italic*, `code`, links, tables, code blocks
- Supports headings, lists (ordered/unordered), blockquotes, and tables
- Optional comment extraction with `--comments N` flag
- YAML frontmatter with title, status, and link metadata