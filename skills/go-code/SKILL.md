---
name: go-code
description: Go code quality standards, idioms, and YAGNI/KISS development principles.
argument-hint: ""
allowed-tools: ""
model: haiku
---

## Core Principles

1. **YAGNI**: Implement only current requirements, no premature abstraction
2. **KISS**: Simple solutions, profile before optimizing
3. **Readability**: Clear code > clever code
4. **Format**: Run `go fmt` after changes, use `goimports`

## Naming

- MixedCaps (not snake_case): `UserService`, `GetUser`, `ErrNotFound`
- Acronyms all caps: `HTTP`, `ID`, `URL`
- Exported names start capital
- Short, descriptive names

## Patterns

### Interfaces
- Small, focused (<3 methods)
- Accept interfaces, return structs
- Define at point of use
- Names often end in -er

### Error Handling

**Requirements:**
- Wrap errors with `%w` for context: `fmt.Errorf("operation failed: %w", err)`
- Sentinel errors for domain logic: `var ErrNotFound = errors.New("not found")`
- Check with `errors.Is()` / `errors.As()`
- Messages: lowercase, no punctuation, add context

```go
func (s *Service) GetUser(ctx context.Context, id int) (*User, error) {
    user, err := s.repo.FindByID(ctx, id)
    if err != nil {
        return nil, fmt.Errorf("failed to get user: %w", err)
    }
    return user, nil
}
```

### Context
- First parameter: `ctx context.Context`
- Pass to all I/O operations
- Check cancellation in long-running operations

### Package Organization
- Group by functionality, not type
- `package user` with `Service`, `Repository`, `Handler`
- Not `package services` with all services

### Tests
```go
tests := []struct {
    name string
    a, b int
    want int
}{
    {"positive", 1, 2, 3},
    {"negative", -1, -2, -3},
}

for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        got := Add(tt.a, tt.b)
        if got != tt.want {
            t.Errorf("Add(%d, %d) = %d; want %d", tt.a, tt.b, got, tt.want)
        }
    })
}
```

## Anti-Patterns

| Pattern | Example | Fix |
|---------|---------|-----|
| Global State | `var defaultX = ...` | Immutable `init()` only |
| Naked Goroutines | `go func(){}()` | Context cancellation |
| Ignored Errors | `result, _ := op()` | Handle or document |
| Defer in Loops | `defer` in `for` | Manual cleanup |
| String Concat | `s += s2` in loops | `strings.Builder` |
| Large Interfaces | >3 methods | Split or rethink |
| Over-engineering | Factory for simple constructor | Direct `New()` |

## Performance

**sync.Pool:** Use for hot paths; always `Reset()` before `Put()`.

**Zero-alloc:** Pre-allocate slices (`make([]T, 0, cap)`), use `strings.Builder`, prefer `[]byte`.

**Profile:** `go test -cpuprofile=cpu.prof -bench=.` → `go tool pprof` → optimize → repeat.

## Functional Options Pattern

```go
type Server struct {
    host    string
    port    int
    timeout time.Duration
}

type Option func(*Server)

func WithPort(port int) Option {
    return func(s *Server) { s.port = port }
}

func NewServer(opts ...Option) *Server {
    s := &Server{
        host:    "localhost",
        port:    8080,
        timeout: 30 * time.Second,
    }
    for _, opt := range opts {
        opt(s)
    }
    return s
}

// Usage
srv := NewServer(WithPort(3000))
```