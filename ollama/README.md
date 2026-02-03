# CursorRules Ollama Modelfiles

Ollama Modelfiles that apply CursorRules anti-pattern standards to local LLM code review and refinement workflows.

## Overview

- **cursorrules-review**: Reviews git commit diffs. Strict grounding (diff-only, no invented paths/lines). Flags universal and language-specific anti-patterns.
- **cursorrules-refine**: Addresses review findings with minimal edits. Runs build and tests. Outputs "Changes:" list for commit message.

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

Tool-agnostic: use any wrapper that can pipe diffs and findings to the models.

## Language Addenda

Base Modelfiles are language-agnostic. For language-specific anti-patterns and build/test commands, use the addenda.

**Available languages:** Go, Python, Java, Swift, JavaScript.

See [PROMPT-add-addenda.md](PROMPT-add-addenda.md) for the LLM prompt to merge addenda into the base Modelfiles. Addenda files are in `addenda/` (e.g., `review-go.txt`, `refine-go.txt`).

## Customization

- **FROM**: Change to another base model (e.g., `qwen3-coder:7b` for lighter hardware).
- **PARAMETER**: Adjust `temperature`, `num_ctx`, `top_p`, `top_k` as needed.
