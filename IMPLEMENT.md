# Implementation Plan: 25 Changes for Go Development Standards

**Phased implementation plan optimized for LLM context windows. Each phase is small, dense, and complete.**

---

## Phase 1: Foundation & Philosophy (2 changes)
**Context:** Lines 10-16  
**Estimated time:** 10 minutes  
**Rationale:** Sets foundation; minimal context needed

### Change 1.1: Add Universal Anti-Patterns Cross-Reference
**Location:** After line 14  
**Action:** Insert 2 lines  
**Context window:** ~20 lines

```markdown
**For universal anti-patterns:** See `general-llm-anti-patterns.mdc`.

---
```

### Change 1.2: Expand Philosophy Section
**Location:** Replace lines 10-14  
**Action:** Replace with expanded version  
**Context window:** ~10 lines

```markdown
## Philosophy

Go's design philosophy centers on simplicity, reliability, and concurrency:

- **Simplicity:** Clear is better than clever. Go intentionally omits complex features to reduce cognitive load.
- **Minimalism:** "Less is more" - Go focuses on essential features, avoiding unnecessary complexity.
- **Readability:** Write code for the reader, not the writer. Code should be self-documenting.
- **Explicit over Implicit:** Errors are explicit, behavior is predictable. No hidden magic.
- **Principle of Least Surprise:** Code should behave in the most obvious way possible.
- **Standard Library:** Prefer standard lib over external deps whenever possible.
- **Idiomatic:** Follow community conventions (fmt, naming, structure). Use `gofmt` for formatting.
- **Compiled Performance:** Go compiles to machine code for fast execution and static type checking.
- **Concurrency-First:** Built-in goroutines and channels enable efficient concurrent programming.
```

---

## Phase 2: Core Language Features - Part 1 (5 changes)
**Context:** After line 89 (Section 1.8)  
**Estimated time:** 50 minutes  
**Rationale:** Adds critical language features; sequential numbering

### Change 2.1: Add Defer Usage (Section 1.9)
**Location:** After line 89  
**Action:** Insert new section  
**Context window:** ~15 lines

```markdown
### 1.9 Defer Usage (CRIT)
**CRITICAL:** Always use `defer` for cleanup operations (files, mutexes, connections).

❌ Bad: `f := os.Open(...); ...; f.Close()` (manual cleanup)
✅ Good: `defer f.Close()` OR `defer mu.Unlock()`
⚠️ Why: Ensures cleanup even on early returns/panics; prevents resource leaks
🔧 Fix: Use `defer` immediately after acquiring resource
📍 See: `general-llm-anti-patterns.mdc` Rule 5.4
**Detect:** Manual cleanup without defer, mutex unlock without defer, file close without defer

```

### Change 2.2: Add Range Loop Variable Capture (Section 1.10)
**Location:** After new Section 1.9  
**Action:** Insert new section  
**Context window:** ~10 lines

```markdown
### 1.10 Range Loop Variable Capture (CRIT)
**CRITICAL:** Capture loop variables explicitly in goroutines/closures.

❌ Bad: `for _, v := range items { go func() { use(v) }() }` (all use last value)
✅ Good: `for _, v := range items { v := v; go func() { use(v) }() }`
⚠️ Why: Loop variables reused; closures capture by reference; causes race conditions
🔧 Fix: Explicitly capture loop variable: `v := v` before closure
**Detect:** Goroutines/closures in range loops without explicit capture, all iterations use same value

```

### Change 2.3: Add Generics Usage (Section 1.11)
**Location:** After new Section 1.10  
**Action:** Insert new section  
**Context window:** ~10 lines

```markdown
### 1.11 Generics Usage (CRIT)
**CRITICAL:** Use generics for type-safe reusable code; prefer generics over `interface{}`.

❌ Bad: `func Max(a, b interface{}) interface{}` (type assertions needed)
✅ Good: `func Max[T comparable](a, b T) T` (type-safe)
⚠️ Why: Generics provide type safety; reduce runtime assertions; clearer APIs
🔧 Fix: Use generics for reusable logic; use constraints (`comparable`, `any`, custom); avoid `interface{}`
📍 See: Section 3.3 for `interface{}` abuse
**Detect:** `interface{}` when generics would work, excessive type assertions, no generic constraints

```

### Change 2.4: Add Channel Patterns (Section 1.12)
**Location:** After new Section 1.11  
**Action:** Insert new section  
**Context window:** ~10 lines

```markdown
### 1.12 Channel Patterns (CRIT)
**CRITICAL:** Use channels for communication, not just synchronization; always close channels properly.

❌ Bad: `for { select { case <-done: return } }` (busy wait, channel never closed)
✅ Good: `for v := range ch { process(v) }` OR `select { case <-ctx.Done(): return }`
⚠️ Why: Prevents goroutine leaks, enables proper shutdown, avoids resource exhaustion
🔧 Fix: Close channels when done; use `range` over channels; prefer context-based cancellation
**Detect:** Channels never closed, select without default causing blocking, busy-wait patterns

```

### Change 2.5: Add Zero Values (Section 1.13)
**Location:** After new Section 1.12  
**Action:** Insert new section  
**Context window:** ~10 lines

```markdown
### 1.13 Zero Values (CRIT)
**CRITICAL:** Leverage Go's zero values; design types to be useful at zero value.

❌ Bad: `var s Service; s.Init()` required, zero value unusable
✅ Good: `var s Service; s.Do()` works, zero value is valid state
⚠️ Why: Zero values reduce boilerplate; idiomatic Go; better ergonomics
🔧 Fix: Design types usable at zero value; avoid mandatory Init() methods; use zero values meaningfully
**Detect:** Mandatory Init() methods, zero value causes panics, types unusable without setup

```

---

## Phase 3: Core Language Features - Part 2 (5 changes)
**Context:** After Phase 2 sections  
**Estimated time:** 50 minutes  
**Rationale:** Completes core language features

### Change 3.1: Add Named Return Values (Section 1.14)
**Location:** After Section 1.13  
**Action:** Insert new section  
**Context window:** ~10 lines

```markdown
### 1.14 Named Return Values (CRIT)
**CRITICAL:** Use named return values only when they improve readability or enable deferred modifications.

❌ Bad: `func divide(a, b int) (int, error)` with unclear return meaning
✅ Good: `func divide(a, b int) (result int, err error)` OR `func divide(a, b int) (int, error)` (if clear)
⚠️ Why: Named returns can improve clarity but add verbosity; use when deferred functions modify them
🔧 Fix: Use named returns for clarity or when deferred functions need to modify them
📍 See: [Effective Go - Named Results](https://go.dev/doc/effective_go#named-results)
**Detect:** Named returns that don't improve clarity, unnamed returns that are unclear

```

### Change 3.2: Add Multiple Return Values (Section 1.15)
**Location:** After Section 1.14  
**Action:** Insert new section  
**Context window:** ~10 lines

```markdown
### 1.15 Multiple Return Values (CRIT)
**CRITICAL:** Use multiple return values for operations that can fail; error is always last.

❌ Bad: `func parse() string`, `func parse() (string, bool)` (bool for error)
✅ Good: `func parse() (string, error)`, `func read() ([]byte, error)`
⚠️ Why: Multiple returns enable explicit error handling; error last is Go convention
🔧 Fix: Return `(result, error)` for operations that can fail; error is always last
📍 See: [Effective Go - Multiple Returns](https://go.dev/doc/effective_go#multiple-returns)
**Detect:** Single return for operations that can fail, error not last, bool instead of error

```

### Change 3.3: Add Embedding (Section 1.16)
**Location:** After Section 1.15  
**Action:** Insert new section  
**Context window:** ~10 lines

```markdown
### 1.16 Embedding (CRIT)
**CRITICAL:** Use embedding to compose types; prefer composition over inheritance.

❌ Bad: Wrapper methods that only delegate, unnecessary indirection
✅ Good: `type Reader struct { io.Reader }`, `type Server struct { *http.Server }`
⚠️ Why: Embedding promotes methods; enables composition; cleaner than delegation
🔧 Fix: Embed interfaces/types directly; use embedding instead of wrapper methods
📍 See: [Effective Go - Embedding](https://go.dev/doc/effective_go#embedding)
**Detect:** Wrapper methods that only call embedded type, types that should embed instead

```

### Change 3.4: Add Control Structures (Section 1.17)
**Location:** After Section 1.16  
**Action:** Insert new section  
**Context window:** ~10 lines

```markdown
### 1.17 Control Structures (CRIT)
**CRITICAL:** Use Go's control structures idiomatically; no parentheses needed.

❌ Bad: `if (condition) { }`, `for (i := 0; i < 10; i++) { }` (parentheses)
✅ Good: `if condition { }`, `for i := 0; i < 10; i++ { }`
⚠️ Why: Go doesn't require parentheses; cleaner syntax; idiomatic Go
🔧 Fix: Remove parentheses from if/for/switch; use Go's syntax
📍 See: [Effective Go - Control Structures](https://go.dev/doc/effective_go#control-structures)
**Detect:** Parentheses in if/for/switch, C/Java-style control structures

```

### Change 3.5: Add Initialization (Section 1.18)
**Location:** After Section 1.17  
**Action:** Insert new section  
**Context window:** ~10 lines

```markdown
### 1.18 Initialization (CRIT)
**CRITICAL:** Use initialization patterns idiomatically; prefer constants for immutable values.

❌ Bad: `var timeout = 10 * time.Second` (should be const), redundant initialization
✅ Good: `const timeout = 10 * time.Second`, `var cache = make(map[string]int)`
⚠️ Why: Constants enable compile-time evaluation; proper initialization reduces errors
🔧 Fix: Use `const` for immutable values; initialize variables properly
📍 See: [Effective Go - Constants](https://go.dev/doc/effective_go#constants), [Effective Go - Variables](https://go.dev/doc/effective_go#variables)
**Detect:** Variables that should be constants, redundant initialization, uninitialized variables

```

---

## Phase 4: Style & Formatting (4 changes)
**Context:** Section 2 (before/after existing sections)  
**Estimated time:** 30 minutes  
**Rationale:** Style sections grouped together

### Change 4.1: Add Formatting Section (Section 2.0)
**Location:** Before line 91 (before "Uber Style & Idioms")  
**Action:** Insert new section, update heading  
**Context window:** ~20 lines

```markdown
## Style & Formatting

### 2.0 Formatting (CRIT)
**CRITICAL:** Always use `gofmt` for formatting; it enforces Go's standard style.

❌ Bad: Manual formatting, inconsistent indentation, spaces instead of tabs
✅ Good: Run `gofmt -w .` or `go fmt ./...` before committing
⚠️ Why: Consistent formatting improves readability; gofmt is the standard; all Go code uses it
🔧 Fix: Use `gofmt` or configure editor to format on save; never manually format
📍 See: [Effective Go - Formatting](https://go.dev/doc/effective_go#formatting)
**Detect:** Inconsistent indentation, spaces for indentation, manual alignment

**Formatting Rules:**
- **Indentation:** Use tabs (gofmt emits tabs by default)
- **Line Length:** No limit; wrap if too long and indent with extra tab
- **Parentheses:** Go needs fewer parentheses; control structures don't use them

## Uber Style & Idioms
```

### Change 4.2: Fix Import Example (Section 2.3)
**Location:** Lines 111-118  
**Action:** Replace existing section  
**Context window:** ~10 lines

```markdown
### 2.3 Import Grouping (Style)
**CRITICAL:** Group imports: stdlib first, then 3rd party, then local, separated by blank lines.

❌ Bad: Mixed imports or no separation
✅ Good:
```go
import (
    "fmt"
    "os"
    
    "github.com/pkg/errors"
    
    "myproj/api"
)
```
⚠️ Why: Clear dependency structure; standard convention enforced by linters
🔧 Fix: Regroup imports manually or use `goimports -local`
**Detect:** Imports not separated by blank lines, stdlib mixed with 3rd party
```

### Change 4.3: Add Naming Conventions (Section 2.4)
**Location:** After line 118 (after Section 2.3)  
**Action:** Insert new section  
**Context window:** ~20 lines

```markdown
### 2.4 Naming Conventions (CRIT)
**CRITICAL:** Follow Go naming conventions: exported (capitalized) vs unexported, package names, acronyms.

❌ Bad: `func getData()`, `type jsonParser struct`, `package myPackage`
✅ Good: `func GetData()`, `type JSONParser struct`, `package mypackage`
⚠️ Why: Exported vs unexported controls API surface; package names should be lowercase
🔧 Fix: Capitalize exported identifiers; lowercase package names; acronyms all caps (JSON, XML)
**Detect:** Mixed case package names, lowercase exported funcs, inconsistent acronym casing

**Package Naming:**
- Lowercase, single-word names (no underscores, no mixedCaps)
- Package name is base name of source directory (`src/encoding/base64` → `base64`)
- Short, concise, evocative
- Exported names can avoid repetition (e.g., `bufio.Reader`, not `bufio.BufReader`)

**Getters:**
❌ Bad: `func GetName() string`, `func GetBalance() int`
✅ Good: `func Name() string`, `func Balance() int`
⚠️ Why: Go convention; package name provides context (`obj.Name()`, not `obj.GetName()`)
🔧 Fix: Remove "Get" prefix from getter methods
**Detect:** Methods named `Get*` that only return values

**Interface Naming:**
- Single-method interfaces: use "-er" suffix (`Reader`, `Writer`, `Closer`)
- Multiple methods: descriptive names (`ReadWriter`, `ReadWriteCloser`)

```

### Change 4.4: Add Package Design (Section 2.5)
**Location:** After new Section 2.4  
**Action:** Insert new section  
**Context window:** ~10 lines

```markdown
### 2.5 Package Design (CRIT)
**CRITICAL:** Packages should have single responsibility; use `internal/` for private APIs.

❌ Bad: Package with 20+ files doing everything, exported types that should be internal
✅ Good: Focused packages, `internal/` for project-private code, clear package boundaries
⚠️ Why: Large packages violate SRP; exported types create API surface; internal prevents external use
🔧 Fix: Split large packages; move private code to `internal/`; minimize exported surface
**Detect:** Packages with >10 files, exported types only used internally, no `internal/` usage

```

---

## Phase 5: Documentation & Tooling (3 changes)
**Context:** Section 2 (after Package Design)  
**Estimated time:** 25 minutes  
**Rationale:** Documentation-related sections grouped

### Change 5.1: Add Documentation Section (Section 2.6)
**Location:** After Section 2.5  
**Action:** Insert new section  
**Context window:** ~10 lines

```markdown
### 2.6 Documentation (CRIT)
**CRITICAL:** Public APIs must have `godoc` comments; use examples for complex APIs.

❌ Bad: `func Process()`, no examples, missing package doc
✅ Good: `// Process handles data transformation.`, `// Example:`, package-level doc
⚠️ Why: Undocumented APIs are hard to use; examples show usage; package docs explain purpose
🔧 Fix: Add `godoc` comments to all exported symbols; include examples; document packages
**Detect:** Exported funcs/types without comments, no examples, missing package doc

```

### Change 5.2: Add Doc Comments Section (Section 2.7)
**Location:** After Section 2.6  
**Action:** Insert new section  
**Context window:** ~10 lines

```markdown
### 2.7 Doc Comments (CRIT)
**CRITICAL:** Comments before top-level declarations are doc comments; they document the package or exported symbol.

❌ Bad: `func Process()`, no doc comment, missing package doc
✅ Good: `// Process handles data transformation.`, `// Package api provides HTTP handlers.`
⚠️ Why: Doc comments are the primary documentation; godoc generates docs from them
🔧 Fix: Add doc comments to all exported symbols; document packages with package comment
📍 See: [Effective Go - Commentary](https://go.dev/doc/effective_go#commentary), [Go Doc Comments](https://go.dev/doc/comment)
**Detect:** Exported funcs/types without doc comments, missing package doc, doc comments not before declaration

```

### Change 5.3: Add Tooling Section (Section 2.8)
**Location:** After Section 2.7  
**Action:** Insert new section  
**Context window:** ~15 lines

```markdown
### 2.8 Tooling (CRIT)
**CRITICAL:** Use Go's built-in tooling for formatting, imports, and dependency management.

**gofmt:**
❌ Bad: Manual formatting, inconsistent indentation
✅ Good: Run `gofmt -w .` or `go fmt ./...` before committing
⚠️ Why: Enforces standard formatting; all Go code uses gofmt
🔧 Fix: Use `gofmt` or configure editor to format on save

**go mod:**
❌ Bad: Manual dependency management, vendor directory without go.mod
✅ Good: `go mod init`, `go mod tidy`, `go mod download`
⚠️ Why: Ensures reproducible builds, clear dependency tracking, version management
🔧 Fix: Use `go mod` commands; commit go.mod and go.sum
**Detect:** Missing go.mod, manual dependency management, uncommitted go.sum

```

---

## Phase 6: Enhance Existing Sections (3 changes)
**Context:** Multiple locations  
**Estimated time:** 20 minutes  
**Rationale:** Fixes and enhancements to existing content

### Change 6.1: Enhance Section 1.5 (Pointer vs Value Receivers)
**Location:** Lines 55-62  
**Action:** Replace existing section  
**Context window:** ~10 lines

```markdown
### 1.5 Pointer vs Value Receivers (CRIT)
**CRITICAL:** Be consistent. Use pointers for mutability or large structs (>64 bytes). Use value receivers for small, immutable structs.

❌ Bad: Mixed receiver types, copying large structs, locking by value (`sync.Mutex` in struct)
✅ Good: `func (s *Service) Mutate()`, `func (s Service) Read()` (if small/immutable, <64 bytes)
⚠️ Why: Value receivers copy data (slow for large structs); value mutexes break locking; value receivers enable immutability
🔧 Fix: Use pointer `*T` if mutating or large; use value `T` if small and immutable; never copy `sync.Mutex`
**Detect:** `func (s Service)` where Service contains `sync.Mutex`, mixed `(s Service)` and `(s *Service)`, large structs with value receivers
```

### Change 6.2: Enhance Section 1.6 (Slice Preallocation)
**Location:** Lines 64-71  
**Action:** Replace existing section  
**Context window:** ~10 lines

```markdown
### 1.6 Slice & Map Preallocation (CRIT)
**CRITICAL:** Preallocate memory when size is known to avoid re-allocations.

❌ Bad: `var dest []int; for _, v := range src { dest = append(dest, v) }`
✅ Good: `dest := make([]int, 0, len(src)); ...` OR `dest := make([]int, len(src)); copy(dest, src)`
⚠️ Why: Repeated `append` triggers O(n) allocations/copies; prealloc is O(1)
🔧 Fix: Use `make([]T, 0, cap)` or `make(map[K]V, cap)`; use `copy()` for slice copying
**Detect:** `append` inside loop on empty slice, `make` without capacity arg
```

### Change 6.3: Enhance Section 1.8 (Table-Driven Tests)
**Location:** Lines 82-89  
**Action:** Replace existing section  
**Context window:** ~20 lines

```markdown
### 1.8 Table-Driven Tests (CRIT)
**CRITICAL:** Use table-driven tests for all logic.

❌ Bad: Repeated test logic, copy-pasted test functions
✅ Good:
```go
tests := []struct {
    name string
    in   int
    want int
}{
    {"positive", 5, 25},
    {"zero", 0, 0},
    {"negative", -3, 9},
}
for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        got := square(tt.in)
        if got != tt.want {
            t.Errorf("square(%d) = %d, want %d", tt.in, got, tt.want)
        }
    })
}
```
⚠️ Why: Easy to add cases; cleaner diffs; strict separation of logic/data
🔧 Fix: Refactor into `struct` slice; run loop with `t.Run(tt.name, ...)`
**Detect:** Multiple `t.Run` with duplicated setup logic, loose assertions
```

---

## Phase 7: Anti-Patterns & Testing (4 changes)
**Context:** Sections 3 and 4  
**Estimated time:** 30 minutes  
**Rationale:** Anti-patterns and testing grouped

### Change 7.1: Add Nil Interface Checks (Section 3.4)
**Location:** After line 147 (after Section 3.3)  
**Action:** Insert new section  
**Context window:** ~10 lines

```markdown
### 3.4 Nil Interface Checks (CRIT)
**CRITICAL:** Check for nil interfaces properly; `== nil` may not work as expected.

❌ Bad: `if err == nil { return }` (may fail with typed nil)
✅ Good: `if err != nil { return err }` OR check concrete type
⚠️ Why: Typed nil interfaces are not equal to nil; causes subtle bugs
🔧 Fix: Always check `err != nil`; use type assertions for typed nil checks
**Detect:** Direct nil comparison on interfaces, typed nil not caught

```

### Change 7.2: Add Variable Shadowing (Section 3.5)
**Location:** After new Section 3.4  
**Action:** Insert new section  
**Context window:** ~10 lines

```markdown
### 3.5 Variable Shadowing (CRIT)
**CRITICAL:** Avoid variable shadowing; use `:=` carefully.

❌ Bad: `err := do(); if err := do2(); err != nil { }` (shadows outer err)
✅ Good: `err := do(); if err2 := do2(); err2 != nil { }`
⚠️ Why: Shadowing hides bugs, makes debugging harder, loses error context
🔧 Fix: Use different variable names in inner scopes; be explicit with `:=` vs `=`
**Detect:** Variable redeclared in inner scope with same name, shadowed errors

```

### Change 7.3: Add Recover Usage (Section 3.6)
**Location:** After new Section 3.5  
**Action:** Insert new section  
**Context window:** ~10 lines

```markdown
### 3.6 Recover Usage (CRIT)
**CRITICAL:** Use `recover` only in deferred functions to handle panics gracefully; keep panic/recover within package.

❌ Bad: `recover()` outside deferred function, exposing panics to callers
✅ Good: `defer func() { if err := recover(); err != nil { log.Println(err) } }()`
⚠️ Why: Recover only works in deferred functions; panics should be converted to errors at package boundary
🔧 Fix: Use recover in deferred functions; convert panics to errors before returning to caller
📍 See: [Effective Go - Recover](https://go.dev/doc/effective_go#recover)
**Detect:** Recover outside deferred function, panics exposed to callers, recover not converting to error

```

### Change 7.4: Expand Testing Section (Sections 4.3-4.4)
**Location:** After line 167 (after Section 4.2)  
**Action:** Insert two new sections  
**Context window:** ~20 lines

```markdown
### 4.3 Test Helpers (CRIT)
**CRITICAL:** Use `t.Helper()` in test helper functions.

❌ Bad: Helper function without `t.Helper()`
✅ Good: `func helper(t *testing.T) { t.Helper(); ... }`
⚠️ Why: Marks function as helper; improves error reporting (shows actual test line)
🔧 Fix: Add `t.Helper()` to top of all helper functions
**Detect:** Helper functions without `t.Helper()`, unclear error locations in test output

### 4.4 Subtests (CRIT)
**CRITICAL:** Use `t.Run()` for subtests; enables better test organization.

❌ Bad: Multiple test functions for related cases
✅ Good: `t.Run("case1", func(t *testing.T) { ... })`
⚠️ Why: Better organization, parallel execution, clearer output
🔧 Fix: Group related tests using `t.Run()` subtests
**Detect:** Related tests not using subtests, multiple test functions for same feature

```

---

## Phase 8: Summary & Final Polish (2 changes)
**Context:** End of file  
**Estimated time:** 15 minutes  
**Rationale:** Final additions and fixes

### Change 8.1: Fix Section 2.1 (Add Uber-specific note)
**Location:** Lines 93-100  
**Action:** Replace existing section  
**Context window:** ~10 lines

```markdown
### 2.1 Prefix Unexported Globals (Style)
**CRITICAL:** Top-level unexported variables must have a `_` prefix to avoid scope confusion. *Note: This is Uber-specific style; Effective Go doesn't require this.*

❌ Bad: `var defaultTimeout = 10 * time.Second`
✅ Good: `var _defaultTimeout = 10 * time.Second`
⚠️ Why: Clearly distinguishes global scope from local scope; avoids collisions
🔧 Fix: Rename unexported globals with leading underscore
**Detect:** Top-level unexported vars without `_` prefix
```

### Change 8.2: Add Summary Section
**Location:** Before line 169 (before References)  
**Action:** Insert new section  
**Context window:** ~30 lines

```markdown
## Summary: Critical Go Rules

These patterns represent the most critical Go best practices:

1. **Error Handling** - Handle errors explicitly, wrap with context
2. **Concurrency Safety** - Manage goroutines, use WaitGroup/errgroup
3. **Context Propagation** - Context as first parameter
4. **Interface Design** - Define interfaces at use site
5. **Receiver Types** - Pointers for mutability/large structs
6. **Memory Preallocation** - Preallocate slices/maps when size known
7. **Functional Options** - Use for complex constructors
8. **Table-Driven Tests** - Use for all logic tests
9. **Defer Usage** - Always use defer for cleanup
10. **Range Loop Capture** - Capture loop variables explicitly
11. **Generics** - Use for type-safe reusable code
12. **Channel Patterns** - Close channels, use range/context
13. **Zero Values** - Design types usable at zero value
14. **Named Returns** - Use when improving clarity or enabling deferred modifications
15. **Multiple Returns** - Error is always last
16. **Embedding** - Prefer composition over inheritance
17. **Control Structures** - No parentheses needed
18. **Initialization** - Use constants for immutable values
19. **Formatting** - Always use gofmt
20. **Naming Conventions** - Exported vs unexported, package names, getters
21. **Package Design** - Single responsibility, use internal/
22. **Documentation** - godoc comments for public APIs
23. **Doc Comments** - Comments before declarations document symbols
24. **Tooling** - Use gofmt, go mod, goimports
25. **Test Helpers** - Use t.Helper() in helpers
26. **Subtests** - Use t.Run() for organization

---

```

---

## Implementation Summary

### Phase Breakdown:
- **Phase 1:** Foundation (2 changes) - 10 min
- **Phase 2:** Core Features Part 1 (5 changes) - 50 min
- **Phase 3:** Core Features Part 2 (5 changes) - 50 min
- **Phase 4:** Style & Formatting (4 changes) - 30 min
- **Phase 5:** Documentation & Tooling (3 changes) - 25 min
- **Phase 6:** Enhance Existing (3 changes) - 20 min
- **Phase 7:** Anti-Patterns & Testing (4 changes) - 30 min
- **Phase 8:** Summary & Polish (2 changes) - 15 min

**Total:** 25 changes across 8 phases  
**Total estimated time:** ~3.5 hours

### Context Window Optimization:
- Each phase focuses on 2-5 related changes
- Context window per change: 10-30 lines
- Sequential implementation minimizes context shifts
- Related sections grouped together

### Quality Assurance:
- Each change is complete and self-contained
- Formatting follows existing patterns
- Cross-references verified
- Section numbering maintained

### Implementation Notes:
- **Line numbers will shift** as sections are added; work top-to-bottom or adjust numbers as you go
- Keep existing format consistent throughout
- All new sections use "(CRIT)" marker except style sections marked "(Style)"
- Code examples use Go syntax highlighting where appropriate
- Verify all cross-references work after implementation

---

## Verification Checklist

After implementation, verify:

- [ ] All sections numbered correctly (1.1-1.18, 2.0-2.8, 3.1-3.6, 4.1-4.4)
- [ ] All sections follow format (CRITICAL, ❌ Bad, ✅ Good, ⚠️ Why, 🔧 Fix, 📍 See, Detect)
- [ ] Cross-references work (general-llm-anti-patterns.mdc, internal section references)
- [ ] Code examples are properly formatted
- [ ] Summary section lists all 26 critical rules
- [ ] File length increased from ~173 to ~400-500 lines
- [ ] No duplicate section numbers
- [ ] All emoji markers present (❌ ✅ ⚠️ 🔧 📍)
- [ ] All external links are valid
- [ ] Formatting is consistent throughout

---

**Ready to implement.** Each phase can be completed independently with minimal context window usage.

