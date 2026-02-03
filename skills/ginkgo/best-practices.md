# Ginkgo Test Authoring Patterns

Kubernetes-aligned conventions for writing Ginkgo tests.

## Kubernetes Conventions

| Pattern | Usage |
|---------|-------|
| `DeferCleanup()` | Prefer over `defer`/`AfterEach` (LIFO, timeout-aware) |
| `Eventually(ctx, func)` | Polling with context; avoid `wait.Poll*` |
| `Consistently()` | Verify condition holds over duration |
| `By("step")` | Mark steps for timeout debugging |

**Avoid**: `DescribeTable`/`Entry`, boolean assertions, `ctx` shadowing.

## Composability & Functional Design

### Prepare-Act-Verify Sequence

```go
It("does something", func(ctx context.Context) {
    // PREPARE
    input := setupInput()
    // ACT
    result, err := sut.Execute(ctx, input)
    // VERIFY
    Expect(err).NotTo(HaveOccurred())
    Expect(result).To(Equal(expected))
})
```

### Subject Action Pattern

`JustBeforeEach` separates configuration from execution:

```go
JustBeforeEach(func() { result, err = sut.Execute(input) })  // ACT

Context("valid", func() {
    BeforeEach(func() { input = validInput() })  // PREPARE
    It("succeeds", func() { Expect(err).NotTo(HaveOccurred()) })  // VERIFY
})
```

### Dependency Injection

Inject in `BeforeSuite`, access via closure (no globals):

```go
var db *sql.DB
var _ = BeforeSuite(func() { db = setupTestDB() })
var _ = AfterSuite(func() { db.Close() })
```

### Helper Functions

Use `GinkgoHelper()` so failures point to spec code:

```go
func ExpectReady(ctx context.Context, name string) {
    GinkgoHelper()
    Expect(client.Get(ctx, name)).To(HaveStatus("Ready"))
}
```