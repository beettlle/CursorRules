# Cursor Rules for LLM-Assisted Development

This repository provides a centralized collection of **Cursor Rules** (`.mdc` files) designed to enforce best practices and mitigate common "bad habits" often introduced by LLM-assisted coding.

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

```
.cursor/rules/
├── critical-rules-quick-reference.mdc  # Top 11 universal rules for fast context loading
├── general-llm-anti-patterns.mdc       # Comprehensive guide to LLM behavioral smells
├── python-development-standards.mdc    # Python-specific standards (PEP 8, Zen of Python)
├── ios-development-standards.mdc       # iOS/Swift 5 development standards
├── ui-development-focus.mdc            # UI/UX best practices
├── ios-build-automation.mdc            # CI/CD and build automation rules
└── documentation-policy.mdc            # Rules for creating/editing documentation
```

## Installation

To use these rules in your project:

1.  **Copy the `.cursor` folder** from this repository into the root of your project.
    ```bash
    cp -r /path/to/CursorRules/.cursor /path/to/your/project/
    ```
2.  **Restart Cursor** or reload the window to ensure the rules are indexed.

## Core Principles (Universal)

The `general-llm-anti-patterns.mdc` file is language-agnostic and enforces:

-   **Zero-Hallucination Policy**: Verify every API call; no "imaginary" libraries.
-   **No Ghost Layers**: Services must add value, not just pass calls through.
-   **Performance-First**: No database or network calls inside loops.
-   **Security**: No hardcoded secrets; strict input validation.
-   **Code Quality**: No commented-out dead code; no "Shut Up, Compiler" warning suppressions.

## Python Standards

The `python-development-standards.mdc` file enforces:
-   **PEP 8 & PEP 20** compliance.
-   **Modern Python**: usage of `@dataclass`, `pathlib`, and type hints (`PEP 484`).
-   **Performance**: Sets vs Lists for membership testing; proper use of generators.
-   **Clean Code**: Explicit parameter naming; avoidance of `*args`/`**kwargs` abuse.

## iOS/Swift Standards

The `ios-development-standards.mdc` file focuses on:
-   **Swift 5+** modern concurrency features.
-   **Architecture**: Clean separation of UI, Domain, and Data layers.
-   **UI**: SwiftUI/UIKit best practices.

## Extending

To add support for a new language (e.g., TypeScript/React):

1.  Create a new file: `.cursor/rules/typescript-development-standards.mdc`.
2.  Add the frontmatter:
    ```markdown
    ---
    description: TypeScript and React development standards
    globs: "**/*.ts", "**/*.tsx"
    alwaysApply: false
    ---
    ```
3.  Define your specific rules, following the structure of existing files.

## Contributing

Contributions are welcome! If you identify new LLM anti-patterns or want to add rules for other languages, please submit a Pull Request.

