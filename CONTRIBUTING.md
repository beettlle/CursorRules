# Contributing to Cursor Rules

## Context Window Efficiency (CRITICAL)

**Every token counts.** These rules files are loaded into the LLM's context window. Verbose contributions waste tokens and reduce the number of rules that can be active simultaneously.

### Core Principles

1. **Density Over Verbosity**: Every sentence must carry maximum information density.
2. **Structure Over Prose**: Use structured formats (tables, lists, emojis) instead of paragraphs.
3. **Cross-Reference, Don't Duplicate**: Link to other sections instead of repeating content.
4. **Minimal But Complete Examples**: Code examples should be the smallest possible that still demonstrates the pattern.
5. **Detection Over Explanation**: Focus on how to detect the problem, not lengthy explanations of why it's a problem.

## Required Format Structure

Each anti-pattern or rule MUST follow this exact structure:

```markdown
### X.Y Rule Name (CRIT if critical)

**CRITICAL:** One-sentence summary of the rule.

❌ Bad: `minimal code example` (key detail in parentheses)
✅ Good: `minimal code example` OR brief description
⚠️ Why: One sentence explaining impact
🔧 Fix: One sentence with solution approach
📍 See: Cross-reference to other files/sections if applicable

**Detect:** Comma-separated list of detection criteria (no full sentences)
```

### Format Requirements

- **❌ Bad / ✅ Good**: Use inline code blocks for examples. Keep examples to 1-3 lines maximum.
- **⚠️ Why**: Single sentence. Focus on impact, not theory.
- **🔧 Fix**: Single sentence. Action-oriented.
- **📍 See**: Use cross-references like `critical-rules-quick-reference.mdc section 1.1` instead of repeating content.
- **Detect**: Comma-separated phrases, not full sentences. Maximum 5-7 items.

## What NOT to Do

### ❌ Verbose Explanations

```markdown
### Bad Example

This anti-pattern occurs when developers create unnecessary abstraction layers that don't add any value beyond simple delegation. This is problematic because it increases code complexity without providing any benefits. The service layer pattern is often misused in this way, where a service class simply wraps a repository and passes through all method calls without adding any business logic or coordination between multiple dependencies. This violates the Single Responsibility Principle and makes the code harder to test and refactor.

**Why this is wrong:**
- Adds complexity without value
- Violates SRP
- Harder to test
- Harder to refactor
- Creates unnecessary indirection
```

**Problem**: 150+ tokens of explanation that could be 20 tokens.

### ✅ Dense Format

```markdown
### 1.1 Ghost Layer Prevention (CRIT)

**CRITICAL:** Services, managers, handlers, and other abstraction layers must add value beyond simple delegation.

❌ Bad: `class Service { func get() { return repo.get() } }` (>80% single-line delegation)
✅ Good: Service coordinates multiple repos OR adds logic OR delete layer
⚠️ Why: Adds complexity without value, violates SRP, harder to test/refactor
🔧 Fix: Delete if >80% delegation; keep only if coordinates multiple deps or adds logic
📍 See: Examples in `critical-rules-quick-reference.mdc` section 1

**Detect:** >80% methods are `return other.method()`, wraps single dep, exists for pattern only
```

**Result**: Same information in ~60 tokens.

## Code Example Guidelines

### ❌ Too Verbose

```markdown
**Bad Pattern:**
```python
# This is a very bad example of how not to write code
# It demonstrates multiple anti-patterns including
# hardcoded values, poor naming, and lack of error handling
def process_user_data(user_data_dict):
    # First we check if the user data exists
    if user_data_dict is not None:
        # Then we extract the name
        user_name = user_data_dict.get('name', '')
        # And the email
        user_email = user_data_dict.get('email', '')
        # Finally we return a formatted string
        return f"{user_name} <{user_email}>"
    else:
        return None
```
```

### ✅ Minimal But Complete

```markdown
❌ Bad: `def process(data): return data['name'] + data['email']` (no validation, hardcoded keys)
✅ Good: `def process(data: UserData) -> str: validate(data); return f"{data.name} <{data.email}>"`
```

**Rule**: Code examples should be 1-3 lines. If you need more, the pattern is too complex to be a single rule.

## Detection Criteria Format

### ❌ Verbose Detection

```markdown
**How to detect this pattern:**
- Look for classes that have methods that only call other methods without adding any logic
- Check if the service layer is just passing through calls to the repository
- See if there are multiple layers of indirection that don't add value
- Verify if the abstraction layer actually coordinates multiple dependencies or adds business logic
```

### ✅ Compact Detection

```markdown
**Detect:** >80% methods are `return other.method()`, wraps single dep, exists for pattern only
```

**Rule**: Detection criteria should be comma-separated phrases, not sentences. Maximum 5-7 items.

## Cross-Referencing Strategy

### ❌ Duplication

```markdown
### Performance Anti-Pattern

**CRITICAL:** Never execute I/O operations inside loops.

This is critical because:
- Database queries in loops cause O(N²) complexity
- Network calls in loops can cause timeouts
- File I/O in loops exhausts system resources
- UI freezes when processing large collections

See also: Ghost Layer Prevention, Business Logic Location
```

### ✅ Cross-Reference

```markdown
### 2.1 Performance-First Collection Handling (CRIT)

**CRITICAL:** Never execute an I/O operation (Database, Network, File) inside a loop.

❌ Bad: `for item in items { await processItem(item) }` (I/O in loop = O(N²))
✅ Good: Batch operations - fetch once, modify in-memory, save once
⚠️ Why: UI freezes at scale, database exhaustion, poor UX
🔧 Fix: Always use batch operations for I/O; fetch once, modify in-memory, save once; use bulk APIs
📍 See: Examples in `critical-rules-quick-reference.mdc` section 2.1

**Detect:** `for item in collection { await processItem(item) }` patterns, database query in loop, API call per item, each iteration refetches/resaves shared state
```

**Rule**: If content exists elsewhere, reference it. Don't repeat.

## Tables for Meta-Rules

Use tables for compact representation of multiple related rules:

```markdown
|Smell|Detect|Action|
|-----|------|------|
|"Shut Up, Compiler"|Code silences warnings vs fixes root cause|Refactor to address root cause; never dismiss warnings|
|"False Positive Fallacy"|Claims warnings are false positives without fixing|Investigate and fix; never dismiss warnings without solution|
```

**Rule**: Tables are more token-efficient than bullet lists for structured data.

## Language-Specific Rules

When adding language-specific rules:

1. **Reference universal rules**: Start with "For universal anti-patterns: See `general-llm-anti-patterns.mdc`"
2. **Focus on language idioms**: Only include patterns specific to that language
3. **Use language examples**: Code examples must be in the target language
4. **Link to standards**: Reference official style guides (PEP 8, Swift API Guidelines, etc.)

## Review Checklist

Before submitting a PR, verify:

- [ ] Each rule follows the exact format structure (❌ Bad, ✅ Good, ⚠️ Why, 🔧 Fix, 📍 See, Detect)
- [ ] Code examples are 1-3 lines maximum
- [ ] Detection criteria are comma-separated phrases (not sentences)
- [ ] Cross-references used instead of duplication
- [ ] No verbose explanations or paragraphs
- [ ] Every sentence carries maximum information density
- [ ] Tables used for structured meta-rules
- [ ] Language-specific rules reference universal rules
- [ ] Frontmatter includes proper `description`, `globs`, and `alwaysApply`

## Token Budget Guidelines

- **Quick Reference File**: Target <100 lines total
- **Category Section**: Target <50 lines per anti-pattern
- **Code Example**: Maximum 3 lines
- **Detection Criteria**: Maximum 7 items, comma-separated
- **Why/Fix**: One sentence each

**Remember**: If your contribution is longer than existing similar rules, it's probably too verbose. Cut it in half, then cut it again.

## Examples of Excellent Contributions

Study these files for density and structure:
- `critical-rules-quick-reference.mdc` - Maximum density
- `general-llm-anti-patterns.mdc` sections 1.1-1.7 - Perfect format
- `documentation-policy.mdc` - Concise and complete

These files represent the target density and structure for all contributions.

