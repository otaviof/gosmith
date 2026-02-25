---
name: jira
description: Fetch a Jira ticket body as markdown for planning sessions.
argument-hint: TICKET-KEY
allowed-tools: Bash
model: haiku
---

## Instructions

1. **Locate**: Find `jira.py` alongside this skill file
2. **Execute**: `python3 <path>/jira.py <TICKET-KEY>` (append `--comments N` if requested)
3. **Report**: Print script output