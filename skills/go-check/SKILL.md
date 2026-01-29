---
name: go-check
description: Run Go verification pipeline (build + test + vet + lint).
argument-hint: [--quick|--full]
allowed-tools: Bash
model: haiku
---

## Instructions

1. **Validate**: Check `go.mod` exists in cwd or parent dirs

2. **Detect automation**: Check for `Makefile` with targets: `build`, `test`, `vet`, `lint`

3. **Dispatch**:
   - `--quick`: Build + vet only (skip tests)
   - `--full`: Build + test + vet + lint + staticcheck
   - (default): Build + test + vet

4. **Execute**:
   - **Makefile path**: `make build test vet` (or available targets)
   - **Raw path**: `go build ./... && go test ./... && go vet ./...`
   - Capture duration per step with `time` command

5. **Aggregate**: Collect exit codes, durations, error summaries

6. **Format**:
   ```markdown
   ## GO CHECK RESULTS

   | Step  | Status | Duration |
   |-------|--------|----------|
   | build | PASS   | 2.1s     |
   | test  | PASS   | 4.3s     |
   | vet   | PASS   | 0.8s     |

   **Overall:** PASS
   ```

7. **Report**:
   - Summary table with overall status
   - If FAIL: Include first error from failed step

8. **Edge cases**:
   - No go.mod: "Not a Go project"
   - Partial failure: Continue remaining steps, report all
   - Missing Makefile targets: Fall back to raw Go commands
   - `--full` without lint tools: Warn "staticcheck not found, skipping"