---
name: make
description: Run or discover Makefile targets. Use for build automation.
argument-hint: [target|--list|--help <target>]
allowed-tools: Bash, Read
model: haiku
---

## Instructions

1. **Validate**: Search for `Makefile` in cwd, parent dirs up to 3 levels

2. **Parse arguments**:
   - `--list` → List targets with descriptions
   - `--help <target>` → Show target prerequisites and commands
   - `<target>` → Execute target
   - (none) → Run default target

3. **Execute**:
   - **List mode**: `grep '^[a-zA-Z0-9_-]*:' Makefile` to extract targets
   - **Help mode**: Read Makefile, show target line and prerequisites
   - **Run mode**: `make <target>`, capture stdout/stderr

4. **Report**:
   - List: Target names with inline comments as descriptions
   - Help: Prerequisites and command lines
   - Run: "Target `<target>` completed (exit: 0)" or error with stderr summary

5. **Edge cases**:
   - No Makefile: "No Makefile found in current or parent directories"
   - Target not found: List available targets
   - Make failure: Report exit code and last 10 lines of stderr