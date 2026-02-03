---
name: ginkgo
description: Run Ginkgo BDD tests with Kubernetes-aligned conventions.
argument-hint: --focus=PATTERN|--label=LABEL|--parallel
allowed-tools: Bash
model: haiku
---

## Instructions

1. **Validate**:
   - Check `go.mod` exists
   - Verify Ginkgo v2: `go list -m github.com/onsi/ginkgo/v2` (latest: v2.28.1)
   - Check `ginkgo` CLI: `which ginkgo` or suggest `go install github.com/onsi/ginkgo/v2/ginkgo@latest`

2. **Parse args**:
   - `--focus=PATTERN`: Run specs matching pattern (`-focus=PATTERN`)
   - `--label=LABEL`: Filter by label (`-label-filter=LABEL`)
   - `--parallel` or `-p`: Enable parallel execution
   - `--race`: Enable race detector
   - `--cover`: Generate coverage profile
   - (default): Run all specs in `./...`

3. **Execute**:
   - **Makefile path**: Check for `test`, `test-e2e`, `ginkgo` targets first
   - **Direct**: `ginkgo run [flags] ./...`
   - Add `-v` for verbose, `--poll-progress-after=30s` for stuck test visibility

4. **Report**:
   - Summary table: suite, passed, failed, skipped, duration
   - On FAIL: first failure with `ginkgo.By()` context
   - On timeout: last `By()` step before hang

5. **Edge cases**:
   - No Ginkgo suites: "No `*_suite_test.go` files found"
   - Missing CLI: "Install with `go install github.com/onsi/ginkgo/v2/ginkgo@latest`"
   - Parallel flakes: Suggest `--flake-attempts=2` for retries

6. **Patterns**: For test authoring best practices, see [best-practices.md](./best-practices.md)