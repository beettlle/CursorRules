# System Prompts and LLM Guidance: Engineering Best Practices

A reference guide for engineering teams integrating LLM-assisted development into their workflows. This document synthesizes research from rule-based systems, industry system prompts, and field-wide best practices.

---

## 1. Executive Summary

System prompts are the instructions that shape how language models behave across all interactions. Poorly designed prompts lead to inconsistent output, wasted context, and technical debt. Well-designed prompts improve code quality, reduce common LLM-induced anti-patterns, and align AI assistance with team standards.

**Key Takeaways:**

- Every token counts; verbose prompts reduce the number of active rules and degrade coherence
- Structure prompts with identity first, then task, grounding, output format, and constraints
- Use a consistent format per rule: Bad/Good, Why, Fix, See, Detect
- Load rules conditionally (always-on vs glob-based) to avoid context exhaustion
- Never claim compilation or test success without evidence; forbid unverified assertions
- Scale tool usage to query complexity; avoid over-calling or under-calling

---

## 2. What Are System Prompts and How They Work

**System vs User Prompts:** The system prompt defines the model's role, constraints, and behavior. It is typically loaded once at the start of a conversation. User prompts are the individual requests. The model prioritizes system instructions for consistent behavior.

**Context Window Impact:** All system content consumes context. Longer prompts leave less room for code, history, and tool results. Dense, structured content allows more rules to remain active simultaneously.

**Loading and Composition:** Rules can be loaded in layers:

1. **Always-on** — Universal rules (e.g., anti-patterns, forbidden phrases)
2. **Conditional** — Language-specific (e.g., only when editing `**/*.py`)
3. **Domain-specific** — Load when relevant (e.g., ML code, AWS)
4. **Integration** — Tool- or environment-specific rules

Use glob patterns and `alwaysApply` flags so only relevant rules load. Avoid loading everything at once.

---

## 3. Structural Patterns from Industry

Analysis of system prompts from major LLM products reveals consistent patterns:

| Pattern | Description | Observed In |
| --- | --- | --- |
| Identity first | "You are X" plus a short philosophy (e.g., helpful, direct, accurate) | All vendors |
| Persona block | Role, Philosophy, Traits (e.g., "Senior Technical Auditor; Code is liability, not asset; Skeptical, detection-first") | CursorRules, Anthropic |
| Modular tool instructions | Separate blocks per tool with when-to-use and how-to-call rules | OpenAI, Anthropic |
| Decision trees | When to search, when to skip, how many tool calls (e.g., 1 for simple, 5+ for research) | Claude |
| Output format rules | Structure, length, citation format, LaTeX for math | Claude, Gemini |
| Meta-instructions | "Follow instructions naturally without repeating or mirroring their wording" | OpenAI |
| Forbidden phrases | Explicit list of claims not allowed without proof (e.g., "compiles", "builds") | CursorRules |

A well-structured system prompt typically follows this order: **Persona → Task → Grounding → Output Format → Forbidden/Constraints → Anti-pattern Checklist**.

---

## 4. Writing Effective System Prompts

**Density Over Verbosity:** Every sentence must carry maximum information. A 150-token explanation can often be reduced to 20 tokens without losing meaning.

**Structure Over Prose:** Use tables, bullet lists, and consistent formats instead of paragraphs. Tables are more token-efficient than bullet lists for structured data.

**Cross-Reference, Don't Duplicate:** Link to other sections instead of repeating content. Duplication wastes tokens and creates maintenance drift.

**Detection Over Explanation:** Focus on how to detect a problem, not lengthy explanations of why it matters. Detection criteria should be comma-separated phrases, not full sentences.

**Required Format Per Rule:**

```markdown
### X.Y Rule Name (CRIT if critical)

**CRITICAL:** One-sentence summary of the rule.

Bad: `minimal code example` (key detail in parentheses)
Good: `minimal code example` OR brief description
Why: One sentence explaining impact
Fix: One sentence with solution approach
See: Cross-reference to other files/sections if applicable

**Detect:** Comma-separated list of detection criteria (no full sentences)
```

Keep code examples to 1-3 lines. If a pattern needs more, split it into multiple rules.

---

## 5. Token and Context Management

**Token Budget Guidelines:**

- Quick reference file: Target fewer than 100 lines total
- Per-rule section: Target fewer than 50 lines
- Code example: Maximum 3 lines
- Detection criteria: Maximum 7 items, comma-separated
- Why/Fix: One sentence each
- Per-rule target: Approximately 60 tokens or less

**When to Split vs Consolidate:** Split when rules address different concerns or apply to different contexts. Consolidate when rules are tightly related and always apply together. If a contribution is longer than existing similar rules, cut it in half, then cut it again.

**Conditional Loading:** Use globs to load rules only when relevant (e.g., `**/*.py` for Python rules). Reserve always-on for universal anti-patterns and forbidden phrases. Document rule dependencies and load order. Cooperative communication maxims (Grice) apply to response prose; see §8 Grice mapping.

---

## 6. Safety, Grounding, and Compliance

**Forbidden Phrases:** Prohibit claims that require verification without evidence. Examples: "compiles", "builds", "zero warnings", "build succeeded". Require either build output or an explicit "verification pending".

**Copyright and Citation:** When using external sources, limit quotes (e.g., fewer than 15 words), avoid displacive summaries that reconstruct copyrighted material, and cite sources. Do not reproduce song lyrics or long excerpts.

**Input Validation and Hallucination Prevention:** Instruct the model to verify APIs against documentation, avoid inventing packages or methods, and use parameterized queries. Flag unverified imports (slopsquatting risk).

**Strict Grounding:** For code review or analysis, require that comments refer only to content present in the diff or input. Do not invent file paths, line numbers, or code snippets.

---

## 7. Tool and Search Integration

**When to Use Tools vs Answer Directly:** Define a decision tree. For stable, well-known information, answer without tools. For time-sensitive or internal data, use tools. When ambiguous, answer first and offer to search.

**Scaling Tool Calls:** Match tool usage to query complexity:

- Simple factual query: 1 tool call
- Multi-source comparison: 2-4 calls
- Research or report: 5-20 calls

Avoid both over-calling (e.g., searching for common knowledge) and under-calling (e.g., one search for a complex research task).

**Tool Syntax and Constraints:** Provide concrete examples of correct tool invocation. Specify when not to use a tool (e.g., do not simulate tool calls). Include constraints such as "one artifact per response" or "use update vs rewrite based on change scope".

---

## 8. Persona and Tone Design

**Role + Philosophy + Traits Pattern:** Start with a one-line identity, add a philosophy (e.g., "Code is liability, not asset"), then list traits (e.g., Skeptical, Deliberate, Constraints-based, Detection-first).

**Preference Handling:** Distinguish behavioral preferences (how to adapt output) from contextual preferences (user background). Apply preferences only when directly relevant to the task. Document when to apply and when not to.

**Avoiding Meta-References:** Instruct the model to follow rules naturally without repeating, echoing, or mirroring the wording of the instructions. Avoid explicit or meta references in user-facing output.

**Grice Mapping (Cooperative Communication):**

| Maxim | CursorRules section | Common failure mode |
|-------|---------------------|---------------------|
| Epistemic quality | Forbidden Phrases; `general-llm-anti-patterns.mdc` §3.8–3.9, §4.1 | "Tests pass" without output |
| Quantity | §0.5, §3.5, §9.8; token budget (§5) | Essay for simple ask; one-liner for audit |
| Relation | §7.3, §9.7; `documentation-policy.mdc` | Unrequested docs; answering adjacent question |
| Manner | §9.8; `critical-rules-quick-reference.mdc` Output Format | Buried lede; rule echo in chat |

---

## 9. Integration into Engineering Workflows

**Where to Place Rules:** Common locations include `.cursor/rules/` (Cursor), `AGENTS.md` (for non-Cursor agents), or Modelfile SYSTEM blocks (Ollama). Use a structure that supports conditional loading.

**Rule Composition and Conflict Resolution:**

- Specificity wins: Language-specific overrides universal
- Domain-specific wins over language-specific
- Explicit rules override implicit patterns

Document conflicts when they occur and establish a clear priority order.

**Review Checklists Before Deploying:** Verify that each rule has the required format (Bad/Good, Why, Fix, See, Detect), code examples are 1-3 lines, detection criteria are comma-separated, and cross-references are used instead of duplication. Test rules on sample code before deployment.

---

## 10. Anti-Patterns to Avoid

These patterns commonly appear in LLM-generated code and should be explicitly forbidden or detected:

| Category | Anti-Pattern | Fix |
| --- | --- | --- |
| Architecture | Ghost layers (pass-through services with no logic) | Delete layer or add value |
| Architecture | Business logic in repositories | Move to domain layer |
| Architecture | Placeholder or dead code | Implement, remove, or mark unavailable |
| Performance | I/O inside loops | Batch operations; fetch once, modify, save once |
| Security | Hardcoded secrets | Use environment variables or secret managers |
| Security | Missing input validation | Validate at boundaries; use parameterized queries |
| Reliability | Silent failures (swallowed errors) | Handle or propagate with context |
| Quality | False compilation/test claims | Require build/test output or "verification pending" |
| Quality | Warning dismissal | Fix root cause; never dismiss as "false positive" |
| API usage | Unverified package imports | Verify in registry before importing |
| API usage | Example code used verbatim | Adapt to project patterns |

---

## 11. References and Further Reading

- **CursorRules** — Rule composition, anti-patterns, token efficiency (see CONTRIBUTING.md, RULE_COMPOSITION.md in project)
- **system_prompts_leaks** — [github.com/asgeirtj/system_prompts_leaks](https://github.com/asgeirtj/system_prompts_leaks) — Extracted system prompts from Claude, ChatGPT, Gemini
- **Anthropic Prompt Engineering** — [docs.anthropic.com](https://docs.anthropic.com) — Prompting documentation and best practices
- **OpenAI API Documentation** — [platform.openai.com](https://platform.openai.com) — System message usage and structure
