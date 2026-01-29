---
name: go-cover
description: Generate Go test coverage report with package breakdown.
argument-hint: [package-pattern]
allowed-tools: Bash
model: haiku
---

## Instructions

1. **Validate**: Check `go.mod` exists in cwd or parent dirs

2. **Execute**:
   - Pattern: `<ARG>` or default `./...`
   - `--html`: Generate `coverage.html` and report path
   - Run: `go test -coverprofile=coverage.out -covermode=atomic <pattern>`

3. **Parse**: Extract per-package coverage from `coverage.out`
   - Skip mode/total lines
   - Group by package path
   - Calculate percentage: (covered statements / total statements) × 100

4. **Format**:
   ```markdown
   ## COVERAGE REPORT

   | Package        | Coverage | Target | Status |
   |----------------|----------|--------|--------|
   | pkg/domain     | 87.2%    | 80%    | PASS   |
   | pkg/service    | 72.1%    | 80%    | FAIL   |

   **Overall:** 83.4% | **Target:** 80% | **Status:** PASS
   ```

5. **Report**:
   - Standard: Markdown table with overall status
   - HTML mode: "Coverage report: `coverage.html`"

6. **Edge cases**:
   - No tests: "No test files found in `<pattern>`"
   - Build failure: Report compilation errors (first 5 lines)
   - Target: Env `GO_COVER_TARGET` or default 80%