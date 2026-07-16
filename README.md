# Cursor Rules for LLM-Assisted Development

This repository provides a centralized collection of **Cursor Rules** (`.mdc` files) designed to enforce best practices and mitigate common "bad habits" often introduced by LLM-assisted coding.

## Table of Contents

- [Purpose](#purpose)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [AGENTS.md for Non-Cursor Agents](#agentsmd-for-non-cursor-agents)
- [Local Model Integrations](#local-model-integrations)
- [Project-Specific Rules](#project-specific-rules)
- [Obsidian Vault Projects](#obsidian-vault-projects)
- [Taskplane Task Packets](#taskplane-task-packets)
- [pi-spine Task Packets](#pi-spine-task-packets)
- [Core Principles](#core-principles-universal)
- [Language Standards](#python-standards) (Python, iOS/Swift, Go, Java, JavaScript, Rust)
- [Extending](#extending)
- [Phase-Based Audit Workflows](#phase-based-audit-workflows)
- [Contributing](#contributing)

## Purpose

Large Language Models (LLMs) are powerful tools, but they often exhibit recurring behavioral anti-patterns, such as:

- **Ghost Layers**: Creating unnecessary wrapper classes that do nothing but delegate.
- **Hallucinations**: Inventing APIs or libraries that don't exist.
- **Complexity**: Over-engineering simple solutions (e.g., Factories for simple data objects).
- **Security Risks**: Hardcoding secrets or skipping input validation.
- **Performance Blindness**: Placing I/O operations inside loops.

This project codifies architectural, performance, and security standards into system prompts that Cursor automatically applies to your development workflow.

## Repository Structure

The core rules live in `.cursor/rules/`.

```text
.cursor/rules/
├── critical-rules-quick-reference.mdc  # Top 15 universal rules for fast context loading
├── general-llm-anti-patterns.mdc       # Comprehensive guide to LLM behavioral smells
├── python-3-development-standards.mdc  # Python-specific standards (PEP 8, Zen of Python)
├── go-1-21-development-standards.mdc   # Go-specific standards (Effective Go, Uber Style Guide)
├── java-17-development-standards.mdc   # Java 17 LTS (Effective Java, ExecutorService, Records)
├── java-21-development-standards.mdc   # Java 21 LTS (Effective Java, Virtual Threads, Records)
├── swift-5-9-development-standards.mdc # Swift 5.9; Apple platform minimum from project target
├── swift-6-development-standards.mdc   # Swift 6 strict concurrency; platform from project target
├── ios-ui-development-focus.mdc        # UI/UX best practices
├── ios-build-automation.mdc            # CI/CD and build automation rules
├── documentation-policy.mdc            # Rules for creating/editing documentation
├── owasp-secure-coding-practices.mdc   # OWASP-aligned secure coding checklist (input, output, auth, session, access, crypto, etc.)
├── tufte-visualization.mdc             # Tufte-aligned analytical charts, tables, dashboards (glob-scoped)
├── audit-workflow.mdc                  # Phase completion verification workflow
├── swift-5-9-brutal-audit.mdc          # Swift 5.9/iOS comprehensive phase audit
├── swift-6-brutal-audit.mdc            # Swift 6/iOS comprehensive phase audit
├── python-3-brutal-audit.mdc           # Python comprehensive phase audit
├── java-brutal-audit.mdc               # Java 17/21 comprehensive phase audit
├── go-1-21-brutal-audit.mdc            # Go 1.21+ comprehensive phase audit
├── javascript-3-development-standards.mdc  # JavaScript/TypeScript standards
├── javascript-3-brutal-audit.mdc       # JavaScript/TypeScript comprehensive phase audit
├── rust-development-standards.mdc      # Rust idioms, style, anti-patterns
├── rust-brutal-audit.mdc              # Rust comprehensive phase audit
├── obsidian-vault-standards.mdc       # Obsidian OFM, Bases, Canvas anti-patterns (glob-scoped)
├── obsidian-integration.mdc           # Obsidian CLI and plugin dev loop (on demand)
├── taskplane-task-authoring.mdc        # Task packet authoring (PROMPT.md, STATUS.md; glob + description)
├── taskplane-worker-cursor.mdc        # Execute task packets in Cursor (Apply Intelligently)
├── spine-task-authoring.mdc           # pi-spine packet authoring (SP-*, Contract, deps.json)
├── spine-operator-cursor.mdc          # pi-spine batch operator CLI (Apply Intelligently)
├── spine-worker-cursor.mdc            # Manual spine packet execution in Cursor (Apply Intelligently)
├── git-workflow-and-pr.mdc            # Git commits, branches, rebase/merge, PR titles (on demand)
├── stet-integration.mdc               # Stet CLI commands and dismiss reasons (on demand)
├── taskplane/                          # PROMPT and STATUS templates (@-referenced by authoring rule)
└── ...                                 # Other rules: ai-ml-development-standards.mdc, aws-*.mdc (5), cursor-integration.mdc, engineering-philosophy.mdc. See .cursor/rules/ for the full list.
```

## Installation

To use these rules in your project:

1. **Copy the `.cursor` folder** from this repository into the root of your project.

    ```bash
    cp -r /path/to/CursorRules/.cursor /path/to/your/project/
    ```

### Prune rules for your project

After copying, remove rules your project does not need. Keeping conflicting or unused rules wastes context and can produce contradictory guidance.

| Family | Keep one | Remove the other |
|--------|----------|------------------|
| **Swift** | `swift-5-9-*` **or** `swift-6-*` | Declare the choice in `AGENTS.md` |
| **Java** | `java-17-*` **or** `java-21-*` | Match your JDK/LTS |
| **Obsidian** | Vault projects only | If not a vault: delete `obsidian-vault-standards.mdc` and `obsidian-integration.mdc` |
| **Stet** | Optional | Loads on demand if kept; safe to delete if you do not use stet |

Example (Swift 6 + Java 21, no Obsidian):

```bash
cd /path/to/your/project/.cursor/rules
rm swift-5-9-development-standards.mdc swift-5-9-brutal-audit.mdc
rm java-17-development-standards.mdc
# Optional: rm obsidian-vault-standards.mdc obsidian-integration.mdc stet-integration.mdc
```

2. **Create a project-specific rules file** (see Project-Specific Rules below).
3. **Restart Cursor** or reload the window to ensure the rules are indexed.

## AGENTS.md for Non-Cursor Agents

Cursor reads `.cursor/rules/`; Aider, Gemini CLI, Zed, and similar tools read `AGENTS.md`. After copying `.cursor` into your project, create `AGENTS.md` so non-Cursor agents follow the same standards.

### Generating AGENTS.md for Your Project

Use this prompt with your AI agent to generate a project-specific AGENTS.md:

```
Read .cursor/rules/critical-rules-quick-reference.mdc and .cursor/rules/general-llm-anti-patterns.mdc.

Then scan this project to detect primary languages (e.g., *.py, *.go, *.java, *.swift, *.ts, *.tsx, package.json, go.mod, etc.) and Obsidian vault signals (*.base, *.canvas, .obsidian/).

Produce an AGENTS.md with:

1. **Intro**: Brief statement that this project uses CursorRules; full rules are in .cursor/rules/

2. **Universal Anti-Patterns**: Include the Top 15 universal anti-patterns from critical-rules-quick-reference.mdc (Bad/Good/Why format)

3. **Language-Specific References**: Based on detected languages, add a section referencing the appropriate .cursor/rules/ files:
   - Python: python-3-development-standards.mdc, python-3-brutal-audit.mdc
   - Go: go-1-21-development-standards.mdc, go-1-21-brutal-audit.mdc
   - Java: java-17-development-standards.mdc or java-21-development-standards.mdc, java-brutal-audit.mdc
   - Swift/iOS: swift-5-9-development-standards.mdc + swift-5-9-brutal-audit.mdc **or** swift-6-development-standards.mdc + swift-6-brutal-audit.mdc (one language mode per project; declare in AGENTS.md)
   - JavaScript/TypeScript: javascript-3-development-standards.mdc, javascript-3-brutal-audit.mdc
   - Rust: rust-development-standards.mdc, rust-brutal-audit.mdc
   - Obsidian vault: obsidian-vault-standards.mdc, obsidian-integration.mdc; install obsidian-skills via `npx skills add https://github.com/kepano/obsidian-skills`

4. **Project-Specific Sections**: Add placeholders or fill in from project files:
   - Dev environment tips (setup commands, build, run)
   - Testing instructions (how to run tests)
   - PR/commit instructions (title format, pre-merge checks)

5. **Phase Verification**: When to run brutal audits (reference the appropriate audit file per language)
```

### Tool-Specific Setup

| Tool | Configuration |
|------|---------------|
| **Aider** | Add to `.aider.conf.yml` in project root: `read: AGENTS.md` (or `read: [AGENTS.md]`) |
| **Gemini CLI** | Add to `.gemini/settings.json`: `{ "context": { "fileName": "AGENTS.md" } }` |
| **Zed** | Zed reads AGENTS.md automatically when present at project root (per [agents.md](https://agents.md) ecosystem) |
| **Ollama** | Use Modelfiles in `ollama/` for local review/refine; see [Local Model Integrations](#local-model-integrations) |

Ollama uses Modelfiles (system prompts) rather than AGENTS.md; see [Local Model Integrations](#local-model-integrations).

### Optional: Nested AGENTS.md

For monorepos or large codebases, place `AGENTS.md` in subdirectories. Agents (e.g., Codex, Gemini CLI) read the nearest file in the directory tree; the closest one takes precedence.

## Local Model Integrations

**Ollama**: Modelfiles in `ollama/` provide system prompts for local LLMs (different from AGENTS.md). Use for git-diff review and refinement workflows. See [ollama/README.md](ollama/README.md) for setup, requirements, and language addenda. Base model and parameters are configurable; `qwen3-coder:30b` is tested.

## Project-Specific Rules

In addition to the universal and language-specific rules, each project should maintain a **project-specific rules file** (e.g., `project-specific-standards.mdc` or `myproject-conventions.mdc`) in `.cursor/rules/` to capture:

- **Project-specific development standards** that may deviate slightly from general rules
- **Team conventions and cultural preferences** (naming patterns, architectural decisions)
- **Tool-specific configurations** (linters, formatters, build tools used in the project)
- **Domain-specific patterns** (business logic conventions, data handling approaches)
- **Legacy code considerations** (patterns to maintain for compatibility)

This file allows teams to customize the rules for their specific context while still benefiting from the universal anti-patterns and language standards. The project-specific file should reference and build upon the general rules, not duplicate them.

Example structure:

```markdown
---
description: "Project-specific development standards and conventions"
globs: ["**/*"]
alwaysApply: true
---

# Project-Specific Standards

**For universal anti-patterns:** See `general-llm-anti-patterns.mdc`
**For Python standards:** See `python-3-development-standards.mdc`

## Project Conventions

[Your project-specific rules here]
```

## Obsidian Vault Projects

Use CursorRules in an Obsidian vault the same way as in a code repo: copy `.cursor/` into the vault root (or workspace root that contains the vault).

1. **Rules (this repo):** `obsidian-vault-standards.mdc` loads for `**/*.md`, `**/*.base`, `**/*.canvas` when those files are in context. It covers anti-patterns only (wikilinks, YAML bases, canvas JSON, false CLI claims)—not full syntax reference.

2. **Skills (upstream, link only):** Install [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) for authoritative OFM, Bases, JSON Canvas, CLI, and Defuddle workflows:

   ```bash
   npx skills add https://github.com/kepano/obsidian-skills
   ```

   Or add skills to project `.cursor/skills/` per Cursor documentation. Do not copy skill trees into CursorRules.

3. **CLI:** When using the Obsidian CLI, load `obsidian-integration.mdc` (Obsidian must be running). See [Obsidian CLI help](https://help.obsidian.md/cli).

4. **Documentation policy:** `documentation-policy.mdc` still blocks unsolicited repo docs; it does not block user-requested vault notes. See the vault scope exception in that file.

5. **Optional:** Add a project-specific `.mdc` for vault naming (daily note format, folder layout, tag conventions).

## Taskplane Task Packets

Use CursorRules to **author** structured task packets in Cursor and **execute** them in Cursor or hand them to any runner that understands file-based task contracts. Rules follow [Cursor Project Rules](https://cursor.com/docs/rules) types—not a separate domain-pack format.

| Rule | [Cursor rule type](https://cursor.com/docs/rules) | Role |
|------|---------------------------------------------------|------|
| `taskplane-task-authoring.mdc` | Apply to Specific Files (`globs`) + `description` for intelligent apply | Create `PROMPT.md`, `STATUS.md`, update area `CONTEXT.md` |
| `taskplane-worker-cursor.mdc` | Apply Intelligently (`description`) or `@taskplane-worker-cursor` | Implement work defined in an active packet |

**Templates** (referenced with `@` from the authoring rule):

```text
.cursor/rules/taskplane/
├── prompt-template.md
└── status-template.md
```

**Typical workflow**

1. In Cursor: ask Agent to create task packets for a feature (authoring rule). Packets land under your tasks root (e.g. `taskplane-tasks/` or `docs/task-management/`).
2. Commit packets to git.
3. Execute in Cursor (`@PROMPT.md`, worker rule) or with any compatible orchestrator. Packets are runner-agnostic; format aligns with [Taskplane task format](https://github.com/HenryLach/taskplane/blob/main/docs/reference/task-format.md) for teams using that project.

**Custom tasks root:** Extend globs in a project-specific `.mdc`, for example:

```markdown
---
description: "Project Taskplane conventions"
globs: "docs/task-management/**, **/PROMPT.md"
alwaysApply: false
---

Tasks root: `docs/task-management/`. Prefix: `APP`. Test command: `npm test`.
```

**Documentation policy:** `documentation-policy.mdc` does not block user-requested `PROMPT.md` / `STATUS.md` under a tasks root. See `RULE_COMPOSITION.md` example 5.

## pi-spine Task Packets

Use CursorRules to **author** spine-compatible packets, **operate** pi-spine batches from Cursor, or **manually implement** packets when no batch is running. Requires [pi-spine](https://github.com/beettlle/pi-spine) (`pi install npm:pi-spine`; `spine init` in the consumer repo).

| Rule | [Cursor rule type](https://cursor.com/docs/rules) | Role |
|------|---------------------------------------------------|------|
| `spine-task-authoring.mdc` | Apply to Specific Files (`globs`) + `description` | Create `SP-*` packets, `dependencies.json`, Contract table |
| `spine-operator-cursor.mdc` | Apply Intelligently (`description`) or `@spine-operator-cursor` | `spine` CLI: plan, batch, diagnose, gate, integrate |
| `spine-worker-cursor.mdc` | Apply Intelligently (`description`) or `@spine-worker-cursor` | Manual in-Cursor implementation when batch inactive |

**Templates:** Reuse `@.cursor/rules/taskplane/prompt-template.md` and `status-template.md`. Spine **Contract** table format is documented in `spine-task-authoring.mdc`.

**Typical workflow**

1. `spine init` in consumer repo; configure `.spine/spine-config.json`.
2. In Cursor: author spine tasks (`spine-task-authoring.mdc`) under `spine-tasks/` (or configured `paths.tasksRoot`).
3. Validate and plan: `spine tasks validate`, `spine plan pending`, `spine preflight`.
4. Run batch: `spine batch start pending` (pi workers in lane worktrees—not Cursor Agent).
5. Land: `spine gate approve` → `spine integrate`.

**Spine vs Taskplane:** If `.spine/spine-config.json` exists and the user mentions spine / `SP-*`, prefer spine rules. Taskplane rules remain for runner-agnostic repos. See `RULE_COMPOSITION.md` examples 9–11.

**Prune:** Delete `spine-*.mdc` from your project's `.cursor/rules/` copy if you do not use pi-spine.

**Deep decomposition:** pi-spine ships `create-spine-tasks` skill—install via `pi install npm:pi-spine`; do not vendor into CursorRules.

## Core Principles (Universal)

The `general-llm-anti-patterns.mdc` file is language-agnostic and enforces:

- **Zero-Hallucination Policy**: Verify every API call; no "imaginary" libraries.
- **No Ghost Layers**: Services must add value, not just pass calls through.
- **Performance-First**: No database or network calls inside loops; bounded loops and queues with fail-fast.
- **Security**: No hardcoded secrets; strict input validation.
- **Code Quality**: No commented-out dead code; no "Shut Up, Compiler" warning suppressions; split compound conditions and state invariants positively; smallest scope; explicit options at call site (not library defaults).
- **Testing**: Test positive and negative space (valid and invalid data, boundaries, valid→invalid transitions); see `general-llm-anti-patterns.mdc` 6.2.
- **Documentation**: Comments explain why and how; commit body carries "why" (PR description is not stored in git).

## Python Standards

The `python-3-development-standards.mdc` file enforces:

- **PEP 8 & PEP 20** compliance.
- **Modern Python**: usage of `@dataclass`, `pathlib`, and type hints (`PEP 484`).
- **Performance**: Sets vs Lists for membership testing; proper use of generators.
- **Clean Code**: Explicit parameter naming; avoidance of `*args`/`**kwargs` abuse.

## iOS/Swift Standards

Use **one** Swift language-mode pair per project (`swift-5-9-*.mdc` or `swift-6-*.mdc`); list the choice in project `AGENTS.md`. See `RULE_COMPOSITION.md` Example 4.

**Swift 5.9** (`swift-5-9-development-standards.mdc`):

- Swift 5.9 language mode; platform minimum is project-defined.
- Architecture: UI, Domain, Data layers; Swift 6 readiness tracked in audit Section E.

**Swift 6** (`swift-6-development-standards.mdc`):

- Swift 6 language mode with **strict concurrency** (data-race safety at compile time).
- `sending`, region isolation, `@preconcurrency` for legacy interop; shared architecture cross-referenced from 5.9 rules.
- Platform minimum is project-defined (no hardcoded OS version in shared rules).

## Go Standards

The `go-1-21-development-standards.mdc` file enforces:

- **Effective Go** and Uber Go Style Guide compliance.
- **Error handling**: Explicit error checks; wrap errors with `%w` for context.
- **Concurrency**: No fire-and-forget goroutines; use `WaitGroup` or `errgroup` for lifecycle management.
- **Context propagation**: `context.Context` as first argument for blocking I/O.
- **Interface design**: Define interfaces at consumer, not producer; avoid interface pollution.

## Java Standards

The `java-17-development-standards.mdc` and `java-21-development-standards.mdc` files enforce:

- **Effective Java** principles and Google Java Style Guide.
- **Modern Java**: Records for immutable DTOs, pattern matching, sealed classes, switch expressions.
- **Java 17**: ExecutorService for I/O; tuned thread pools.
- **Java 21**: Virtual Threads for I/O-bound tasks; sequenced collections.
- **Immutability**: Records over POJOs; fail-fast with `Optional` over null.

## JavaScript/TypeScript Standards

The `javascript-3-development-standards.mdc` file enforces:

- **Modern ES6+**: `const`/`let` over `var`; async/await over callbacks; strict mode always.
- **Type safety**: Prefer TypeScript or JSDoc for types.
- **Style**: Airbnb/Google conventions; camelCase; explicit over implicit.
- **Security**: Input validation; no `eval()`; sanitize user input.
- **Modular**: ES6 modules; functional over imperative where appropriate.

## Rust Standards

The `rust-development-standards.mdc` file enforces:

- **Errors as values**: Result/Option; propagate with ?; no unwrap/expect in library code; propagate errors with context.
- **Ownership and borrowing**: Prefer references over clone; flexible API boundaries (impl AsRef, &[T]); no unbounded collects when streaming is possible.
- **Unsafe and concurrency**: unsafe only with // SAFETY: comment; Send/Sync correct; no blocking in async; no shared mutable state without sync (Arc<Mutex<T>>, channels).
- **API design**: Rust API Guidelines (naming as_/to_/into_, iter/iter_mut/into_iter, Debug and common traits); constructors and documentation.
- **Tooling**: rustfmt, clippy; run cargo build / cargo test before claiming success; verify crates (slopsquatting prevention).

## Extending

To add support for a new language (e.g., TypeScript/React):

1. Create a new file: `.cursor/rules/typescript-development-standards.mdc`.
2. Add the frontmatter:

    ```markdown
    ---
    description: TypeScript and React development standards
    globs: ["**/*.ts", "**/*.tsx"]
    alwaysApply: false
    ---
    ```

3. Define your specific rules, following the structure of existing files.

For **domain packs** (e.g., Obsidian): add a thin glob-scoped `.mdc` for anti-patterns in this repo; link to upstream Agent Skills for syntax (see [Obsidian Vault Projects](#obsidian-vault-projects) and `RULE_COMPOSITION.md`).

## Phase-Based Audit Workflows

The repository includes on-demand brutal audit workflows for comprehensive architectural reviews:

- **Swift/iOS (5.9)**: `.cursor/rules/swift-5-9-brutal-audit.mdc` - Swift 5.9 projects (deployment target is project-defined; includes Swift 6 readiness)
- **Swift/iOS (6)**: `.cursor/rules/swift-6-brutal-audit.mdc` - Swift 6 projects (concurrency compliance; deployment target is project-defined)
- **Python**: `.cursor/rules/python-3-brutal-audit.mdc` - Comprehensive audit for Python 3.13 projects
- **Java**: `.cursor/rules/java-brutal-audit.mdc` - Comprehensive audit for Java 17/21 LTS projects
- **Go**: `.cursor/rules/go-1-21-brutal-audit.mdc` - Comprehensive audit for Go 1.21+ projects (Effective Go, concurrency, testing)
- **JavaScript/TypeScript**: `.cursor/rules/javascript-3-brutal-audit.mdc` - Comprehensive audit for JS/TS projects (modern ES, tooling, testing)
- **Rust**: `.cursor/rules/rust-brutal-audit.mdc` - Comprehensive audit for Rust (edition 2021/2024) projects (error handling, ownership, concurrency, testing)

These audits are designed to run after phase completion to ensure code quality and architectural compliance. They complement the always-on rules by providing deep, milestone-based validation.

**Usage:** Mention "run the audit", "check for anti-patterns", or "verify phase completion" to invoke the appropriate audit workflow.

The audits use tools (`grep`, `codebase_search`) to verify checks rather than just reading files, ensuring thorough validation of codebase quality.

## Contributing

Contributions are welcome! If you identify new LLM anti-patterns or want to add rules for other languages, please submit a Pull Request.
