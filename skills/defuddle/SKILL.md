---
name: defuddle
description: Extract readable web content, removing navigation/ads to save tokens.
argument-hint: URL [--property NAME]
model: haiku
---

# Defuddle

## Instructions

1. **Validate**: If URL ends in `.md`, use WebFetch directly and return content

2. **Parse arguments**:
   - `--property <name>` → Extract metadata (title, description, domain, author, date)
   - `--json` → Return full JSON output
   - (default) → Return markdown content

3. **Execute**: `npx -y defuddle parse <URL> --md` (or with flags as specified)

4. **Report**:
   - Default: Print markdown content to stdout
   - Property mode: Print metadata value
   - JSON mode: Print full JSON structure

5. **Edge cases**:
   - `.md` URL: Skip defuddle, use WebFetch
   - Network error: "Failed to fetch content from <URL>"
   - Parse failure: "Defuddle could not extract content"
   - Missing property: "Property '<name>' not found"

## Usage Examples

| Goal            | Command                                     |
| :-------------- | :------------------------------------------ |
| Parse to stdout | `npx -y defuddle parse <url> --md`          |
| Get Metadata    | `npx -y defuddle parse <url> -p <property>` |
| JSON Output     | `npx -y defuddle parse <url> --json`        |

## Options

- `-p <name>`: Metadata (title, description, domain, author, date)
- `-o <file>`: Save output to local file
- `--json`: Full JSON output
- `--md`: Markdown output (default for this skill)
