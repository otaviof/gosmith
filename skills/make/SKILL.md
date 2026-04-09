---
name: make
description: Run, discover, or review Makefile targets. Use for build automation.
argument-hint: target|--list|--help TARGET|--review [PATH]
allowed-tools: Bash, Read
model: haiku
---

## Instructions

1. **Validate**: Search for `Makefile` in cwd, parent dirs up to 3 levels (skip for `--review` with explicit path)

2. **Parse arguments**:
   - `--list` → List targets with descriptions
   - `--help <target>` → Show target prerequisites and commands
   - `--review [path]` → Check Makefile against best practices (default: found Makefile)
   - `<target>` → Execute target
   - (none) → Run default target

3. **Execute**:
   - **List mode**: `grep '^[a-zA-Z0-9_-]*:' Makefile` to extract targets
   - **Help mode**: Read Makefile, show target line and prerequisites
   - **Review mode**: Read Makefile (and `hack/` scripts if present), check for:
     * Recursive make: `$(MAKE)`, `${MAKE}`, `cd ... && make` in targets
     * Complex targets: >3 shell commands without delegation to `hack/` script
     * Scripts calling make: `hack/*.sh` that invoke `make` back (scripts are leaves)
     * Report: "PASS" or violations with line numbers and recommended fix
   - **Run mode**: `make <target>`, capture stdout/stderr

4. **Report**:
   - List: Target names with inline comments as descriptions
   - Help: Prerequisites and command lines
   - Review: "PASS" or "Issues found:" with violations and recommended fixes
   - Run: "Target `<target>` completed (exit: 0)" or error with stderr summary

5. **Edge cases**:
   - No Makefile: "No Makefile found in current or parent directories"
   - Target not found: List available targets
   - Make failure: Report exit code and last 10 lines of stderr

## Makefile Principles

| Principle | Guidance |
|-----------|----------|
| **Single source of authority** | Makefile is canonical entry point for all project automation |
| **No recursive make** | Never use `$(MAKE)` or `${MAKE}` inside targets; use `include` for unified dependency graph |
| **CI calls make, never reimplements** | CI/CD pipelines only trigger `make <target>`; all logic lives in Makefile and `hack/` scripts |
| **No duplication** | Logic exists in one place: Makefile target or `hack/` script — never repeated in CI config |
| **Modular via include** | Split into `build/*.mk` files; all form unified dependency graph |
| **Hack scripts for complexity** | Targets needing >3 commands → extract to `hack/<name>.sh`; Makefile passes values via env vars |
| **Scripts are leaves** | `hack/` scripts never call `make`; Makefile orchestrates, scripts execute |

## Hack Scripts Pattern

```makefile
# Target delegates to hack/ script via env vars
.PHONY: release
release: ## Build and publish release artifacts
	IMAGE_TAG=$(IMAGE_TAG) REGISTRY=$(REGISTRY) hack/release.sh
```

- Extract when a target exceeds 3 shell commands
- Script receives configuration through environment variables, not arguments
- Script is a leaf: it never calls `make` back

## Anti-Pattern: Recursive Make

```makefile
# WRONG — parallel automation hierarchies
$(MAKE) -C subdir clean

# RIGHT — unified via include
include subdir/subdir.mk
clean: subdir-clean
```

`include` maintains single dependency graph; recursive `$(MAKE)` breaks it.