# CursorRules Ollama Modelfiles

Ollama Modelfiles that apply CursorRules anti-pattern standards to local LLM code review and refinement workflows.

## Overview

- **cursorrules-review**: Reviews git commit diffs. Strict grounding (diff-only, no invented paths/lines). Flags universal and language-specific anti-patterns. Use with RoboRev or similar.
- **cursorrules-refine**: Addresses review findings with minimal edits. Runs build and tests. Outputs "Changes:" list for commit message. Use with RoboRev or similar.
- **cursorrules-code**: Implements features and fixes bugs from specs; minimal scope; CursorRules-aware. Use with CLI or IDE (standalone).
- **cursorrules-refactor**: Refactors and simplifies code in a file, group of files, or folder; preserves behavior. Use with CLI or IDE (standalone).

## Requirements

- [Ollama](https://ollama.com) installed
- Minimum Ollama version: 0.3.0+ (or recent; see [Ollama docs](https://github.com/ollama/ollama))

## Tested Configuration

- **Base model**: `qwen3-coder:30b` (tested)
- Base model and parameters are configurable via FROM and PARAMETER in the Modelfile.

## Quick Start

```bash
ollama pull qwen3-coder:30b
ollama create cursorrules-review -f ollama/cursorrules-review.Modelfile
ollama create cursorrules-refine -f ollama/cursorrules-refine.Modelfile
ollama create cursorrules-code -f ollama/cursorrules-code.Modelfile
ollama create cursorrules-refactor -f ollama/cursorrules-refactor.Modelfile
```

## Context Size and RAM

Default `num_ctx` is 32768 (fits most machines). Adjust for your hardware:

| num_ctx | Typical RAM | Use Case |
|---------|-------------|----------|
| 16384   | 16GB+       | Smaller context, faster |
| 32768   | 32GB+       | Default; balanced |
| 65536   | 64GB+       | Large commits, full context |

Edit the Modelfile and change `PARAMETER num_ctx` before creating the model.

## Typical Workflow

1. Provide a git diff or commit to the review model.
2. Review model outputs findings (or "No issues found").
3. Provide the review findings to the refine model.
4. Refine model suggests edits, runs build/tests, outputs "Changes:" list.
5. Apply edits and commit (caller commits; models do not).

Tool-agnostic: use any wrapper that can pipe diffs and findings to the models. For implement or refactor tasks, use cursorrules-code or cursorrules-refactor with a CLI or IDE; provide the task and relevant files or scope.

## Language Addenda

Base Modelfiles are language-agnostic. For language-specific anti-patterns and build/test commands, use the addenda.

**Available languages:** Go, Python, Java, Swift, JavaScript, Rust.

Addenda exist for all four models: `review-*.txt`, `refine-*.txt`, `code-*.txt`, `refactor-*.txt`. See [PROMPT-add-addenda.md](PROMPT-add-addenda.md) for the LLM prompt to merge addenda into the base Modelfiles (produces customized Modelfiles for any of the four models). Addenda files are in `addenda/`.

## Modelfile prompt design

When editing the SYSTEM block in a Modelfile:

- **Structure**: Use the order Persona → Task → Grounding → Output format → Forbidden → Anti-pattern/Detect.
- **Density**: No filler; use tables or lists over paragraphs. One or two minimal examples per output type are fine.
- **Placement**: Put static content (identity, instructions, format) at the start of SYSTEM; dynamic content (diff, review text) stays in the user message.
- **Examples**: Use language-agnostic examples in base Modelfiles (e.g. neutral paths like `path/to/module/file.ext` and generic descriptions) so behavior does not bias toward a specific language.
- **Addenda**: Prefer one base Modelfile per role plus addenda for language-specific content; avoid maintaining full per-language Modelfiles unless you need a frozen snapshot (use PROMPT-add-addenda to generate).

For full principles see [docs/SYSTEM_PROMPTS_ENGINEERING_GUIDE.md](../docs/SYSTEM_PROMPTS_ENGINEERING_GUIDE.md) and [docs/prompt-engineering-research-and-best-practices.md](../docs/prompt-engineering-research-and-best-practices.md).

## Customization

- **FROM**: Change to another base model (e.g., `qwen3-coder:7b` for lighter hardware).
- **PARAMETER**: Adjust `temperature`, `num_ctx`, `top_p`, `top_k` as needed. Code and refactor models use slightly higher temperature than review/refine for more variety in outputs.
