# Rule Composition Guide

This document explains how Cursor Rules are composed and how to resolve conflicts.

## Rule Loading Order

1. **Always-on rules** (`alwaysApply: true`)
   - `critical-rules-quick-reference.mdc`
   - `general-llm-anti-patterns.mdc`
   - `documentation-policy.mdc`
   - `stet-integration.mdc`

2. **Language-specific rules** (`alwaysApply: false`, glob-based)
   - Load only for matching file types
   - Examples: `python-3-development-standards.mdc` for `**/*.py`

3. **Domain-specific rules** (`alwaysApply: false`, glob-based)
   - Load only when relevant
   - Examples: `ai-ml-development-standards.mdc` for ML code; `obsidian-vault-standards.mdc` for `**/*.base`, `**/*.canvas`, and vault `.md` (see rule scope: vault vs repo docs)

4. **Integration rules** (`alwaysApply: false`)
   - Load when needed
   - Examples: `cursor-integration.mdc` for Cursor-specific optimizations; `git-workflow-and-pr.mdc` for Git commits, branches, rebase/merge, and PR titles/descriptions (load when doing Git/PR tasks); `obsidian-integration.mdc` for Obsidian CLI and vault operations

## Standard Section Order (per file)

1. Persona — Role, Philosophy, Traits
2. Task/Scope — What this rule governs
3. Output Format — (if applicable) response structure
4. Forbidden/Constraints — Prohibited phrases or actions
5. Rules — Anti-patterns and behavioral rules (Bad/Good, Why, Fix, See, Detect)

## Rule Conflict Resolution

1. **Specificity wins**: Language-specific overrides universal when in conflict
2. **Domain-specific wins**: Domain-specific overrides language-specific when in conflict
3. **Explicit wins**: Explicit rules override implicit patterns

## Best Practices

- Use glob patterns to load only relevant rules
- Avoid redundant rule loading
- Use `alwaysApply: false` with appropriate globs for conditional rules
- Document rule conflicts when they occur

## Conflict Resolution Examples

### Example 1: Universal vs Language-Specific

**Conflict:** Universal rule says "use explicit types" but Python rule says "use type hints (PEP 484)"

**Resolution:** Python-specific rule wins (specificity wins)

### Example 2: Language-Specific vs Domain-Specific

**Conflict:** Python rule says "use list comprehensions" but AI/ML rule says "use explicit loops for GPU code"

**Resolution:** Domain-specific rule wins (more specific context)

### Example 3: Documentation Policy vs Obsidian Vault

**Conflict:** `documentation-policy.mdc` says do not create unsolicited `.md`; user asks to create a daily note in an Obsidian vault.

**Resolution:** Domain-specific `obsidian-vault-standards.mdc` and explicit user vault intent win; documentation-policy applies to repo/software docs, not PKM notes.

### Example 4: Swift 5.9 vs Swift 6 Language Mode

**Conflict:** Both `swift-5-9-development-standards.mdc` and `swift-6-development-standards.mdc` use `globs: ["**/*.swift"]`; 5.9 forbids `sending`/`consume` while 6 requires strict concurrency and allows those features.

**Resolution:** Project declares one language mode in `AGENTS.md`, Xcode **Swift Language Version**, or SwiftPM `swiftLanguageMode`. When Swift 6 is declared, `swift-6-*.mdc` supersedes 5.9 compatibility constraints. Optionally omit or remove the unused version’s rules from the project’s `.cursor/rules/` copy.

## Rules vs Agent Skills

| Layer | Location | Role |
|-------|----------|------|
| CursorRules `.mdc` | `.cursor/rules/` | Universal and domain anti-patterns; verification; globs |
| Agent Skills | `.cursor/skills/` or user install | Syntax, workflows, reference depth per [Agent Skills spec](https://agentskills.io/specification) |

**Obsidian:** Install upstream skills (link only, do not vendor in CursorRules):

```bash
npx skills add https://github.com/kepano/obsidian-skills
```

Pair with `obsidian-vault-standards.mdc` and `obsidian-integration.mdc`. See `cursor-integration.mdc` Category 4.

## See Also

- `cursor-integration.mdc` - Cursor-specific rule composition strategies
- `git-workflow-and-pr.mdc` - Git/PR workflow; overlaps with audit-workflow only in "verify before claiming done" (this rule governs Git/PR text; audit governs phase verification)
- `general-llm-anti-patterns.mdc` section 7.2b - Context window exhaustion prevention
- CONTRIBUTING.md - Rule authoring guidelines
