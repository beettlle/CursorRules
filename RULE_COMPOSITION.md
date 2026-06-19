# Rule Composition Guide

This document explains how Cursor Rules are composed and how to resolve conflicts.

## Rule Loading Order

1. **Always-on rules** (`alwaysApply: true`)
   - `critical-rules-quick-reference.mdc`
   - `general-llm-anti-patterns.mdc`
   - `documentation-policy.mdc`

2. **Language-specific rules** (`alwaysApply: false`, glob-based)
   - Load only for matching file types
   - Examples: `python-3-development-standards.mdc` for `**/*.py`

3. **Domain-specific rules** (`alwaysApply: false`, glob-based)
   - Load only when relevant
   - Examples: `ai-ml-development-standards.mdc` for ML code; `obsidian-vault-standards.mdc` for `**/*.base` and `**/*.canvas` (vault `.md` via intelligent apply, user mention, or `@` — see rule scope: vault vs repo docs); `taskplane-task-authoring.mdc` for `PROMPT.md`, `STATUS.md`, and tasks-root paths; `spine-task-authoring.mdc` for `.spine/`, `spine-tasks/`, and `dependencies.json` (see [Cursor Rules](https://cursor.com/docs/rules) — Apply to Specific Files)

4. **Integration rules** (`alwaysApply: false`)
   - Load when needed
   - Examples: `cursor-integration.mdc` for Cursor-specific optimizations; `git-workflow-and-pr.mdc` for Git commits, branches, rebase/merge, and PR titles/descriptions (load when doing Git/PR tasks); `stet-integration.mdc` when the user asks to run stet, dismiss findings, or triage reviews (Apply Intelligently via `description`, or `@stet-integration`); `obsidian-integration.mdc` for Obsidian CLI and vault operations; `taskplane-worker-cursor.mdc` when executing generic task packets; `spine-operator-cursor.mdc` when operating pi-spine batches; `spine-worker-cursor.mdc` when manually implementing spine packets (Apply Intelligently via `description`, or `@`-mention)

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
- Grice maxims are a **communication meta-layer**; they do not override language-specific, domain-specific, or audit rules

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

### Example 5: Documentation Policy vs Taskplane Task Packets

**Conflict:** `documentation-policy.mdc` says do not create unsolicited `.md`; user asks to create `PROMPT.md` and `STATUS.md` for a staged task.

**Resolution:** `taskplane-task-authoring.mdc` and explicit user task intent win; documentation-policy applies to repo/software docs, not orchestration artifacts under a tasks root.

### Example 6: Task Author vs Task Worker

**Conflict:** User says "create tasks for feature X" but the agent starts implementing code; or user says "implement TP-014" but the agent rewrites PROMPT scope.

**Resolution:** Authoring requests → `taskplane-task-authoring.mdc` (packets only). Execution requests → `taskplane-worker-cursor.mdc` (PROMPT is contract). If both are needed, author first unless the user explicitly asks to implement in the same turn.

### Example 7: Cooperative Brevity vs Brutal Audit Evidence

**Conflict:** Cooperative brevity (§9.8 in `general-llm-anti-patterns.mdc`) vs brutal-audit evidence requirements (longer structured output).

**Resolution:** When `*-brutal-audit.mdc` or `audit-workflow` applies, audit rules win (specificity + explicit audit intent). Grice Quantity/Manner still apply to *structure* (ordered sections, no filler), not to suppress required evidence.

### Example 8: Java 17 vs Java 21

**Conflict:** Both `java-17-development-standards.mdc` and `java-21-development-standards.mdc` use `globs: ["**/*.java"]`; 17 emphasizes `ExecutorService` patterns while 21 adds virtual-thread guidance.

**Resolution:** Project declares one LTS in `AGENTS.md`, build config, or toolchain. When Java 21 is declared, `java-21-development-standards.mdc` supersedes 17-specific concurrency guidance. Optionally omit or remove the unused version's rules from the project's `.cursor/rules/` copy.

### Example 9: Spine vs Taskplane

**Conflict:** Both `taskplane-task-authoring.mdc` and `spine-task-authoring.mdc` could apply; user says "create tasks for spine batch."

**Resolution:** When `.spine/spine-config.json` exists and the user mentions spine / `spine batch` / `SP-*`, `spine-task-authoring.mdc` wins for authoring. Taskplane rules remain valid for repos without pi-spine. Declare choice in project `AGENTS.md`.

### Example 10: Spine author vs operator vs worker

**Conflict:** User says "start spine batch on SP-010" but the agent starts editing PROMPT; or user says "implement SP-010" during an active batch.

**Resolution:** Batch/gate/integrate → `spine-operator-cursor.mdc`. Author packets → `spine-task-authoring.mdc`. Manual implementation → `spine-worker-cursor.mdc` only when batch inactive on that scope. If ambiguous, ask once.

### Example 11: Documentation Policy vs pi-spine Authoring Artifacts

**Conflict:** `documentation-policy.mdc` blocks unsolicited `.md`; user asks to create spine tasks including `{tasksRoot}/_explore/report.md`.

**Resolution:** `spine-task-authoring.mdc` and explicit spine task intent win for orchestration artifacts under the tasks root. Repo docs (`docs/`, README) still require explicit user request. Do not hand-edit `.spine/runtime/**`.

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

**pi-spine:** Install upstream package and skill (link only, do not vendor in CursorRules):

```bash
pi install npm:pi-spine
```

Pair with `spine-task-authoring.mdc`, `spine-operator-cursor.mdc`, and `spine-worker-cursor.mdc`. Deep decomposition uses pi-spine `create-spine-tasks` skill.

## See Also

- `cursor-integration.mdc` - Cursor-specific rule composition strategies
- `git-workflow-and-pr.mdc` - Git/PR workflow; overlaps with audit-workflow only in "verify before claiming done" (this rule governs Git/PR text; audit governs phase verification)
- `general-llm-anti-patterns.mdc` section 7.2b - Context window exhaustion prevention
- CONTRIBUTING.md - Rule authoring guidelines
