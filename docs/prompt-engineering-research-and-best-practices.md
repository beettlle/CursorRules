# Prompt Engineering: Research Findings and Best Practices for Engineering Teams

## Executive Summary

Large Language Models (LLMs) are increasingly central to software products, from coding assistants and chatbots to agentic workflows and RAG systems. Their performance depends heavily on how they are prompted. Research shows that systematic prompt design significantly improves accuracy, consistency, and safety—and that automated prompt optimization (APO) can match or exceed human-designed prompts across diverse tasks.

This document consolidates findings from academic research, industry documentation, and practitioner experience into actionable guidance for Engineering teams. It covers system prompt design principles, model-specific considerations, evaluation practices, security, and concrete steps to integrate prompt engineering into development workflows. Use it as a reference when designing prompts, as a how-to guide when adopting new practices, and as a shared vocabulary for cross-team collaboration.

**Key takeaway:** Treat prompts as first-class artifacts. Structure them consistently, evaluate them systematically, version them alongside code, and consider automation (APO) when scaling prompt iteration.

---

## 1. Research Landscape

### Surveys and Taxonomies

| Source | Scope | Key Deliverables |
|--------|-------|------------------|
| **The Prompt Report** (Schulhoff et al., 2024) | 4,797 records → 1,565 papers (PRISMA) | 58 text-based techniques, 40 multimodal/multilingual techniques, 33 standardized vocabulary terms, best practices for SOTA LLMs |
| **Automatic Prompt Optimization Survey** (ACL/EMNLP 2025) | APO methods | Formal APO definition, 5-part unifying framework, categorization by optimization approach |
| **Optimization-Theoretic Survey** (arXiv:2502.11560) | Automated prompt engineering | Formalization as discrete/continuous/hybrid optimization; methods by variable (instructions, soft prompts, exemplars) |

### Key Research Papers

| Paper | arXiv | Contribution |
|-------|-------|--------------|
| **SPRIG** (Zhang et al., 2024) | 2410.14826 | Edit-based genetic algorithm for system prompt optimization; single optimized system prompt performs on par with task-specific prompts; generalizes across models, sizes, languages |
| **OPRO – Large Language Models as Optimizers** (Yang et al., 2024) | 2309.03409 | LLMs as optimizers; up to 8% gain on GSM8K, 50% on Big-Bench Hard over human prompts; code at github.com/google-deepmind/opro |
| **APE – Automatic Prompt Engineer** (Zhou et al., ICLR 2023) | — | LLM-generated prompts outperform human prompts on 24/24 Instruction Induction, 17/21 BIG-Bench tasks |
| **Chain-of-Thought Prompting** (Wei et al., 2022) | 2201.11903 | Intermediate reasoning steps improve performance; foundational for reasoning-heavy tasks |
| **CAPO** (2025) | — | Cost-aware prompt optimization; AutoML + evolutionary search; outperforms discrete methods in 11/15 benchmarks, up to 21% improvement |

### Industry Documentation

- **OpenAI:** [Prompt Engineering](https://platform.openai.com/docs/guides/prompt-engineering), [GPT Best Practices](https://platform.openai.com/docs/guides/gpt-best-practices)
- **Anthropic:** [System Prompts](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts), [Claude 4 Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)
- **Google AI:** [Gemini Prompt Design Strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)

### Staying Updated

| Source | Focus |
|--------|-------|
| arXiv cs.CL | Computation and Language |
| OpenReview | ICLR, peer review, discussions |
| Papers with Code | Implementations, benchmarks |
| The Prompt Report | trigaten.github.io/Prompt_Survey_Site |
| Provider changelogs | Model and API updates |

---

## 2. System Prompt Design: Core Principles

Principles supported by research and aligned across major providers:

### Structure

System prompts should follow a consistent order:

1. **Identity/Role** — Purpose, communication style, high-level goals
2. **Instructions** — Rules, constraints, what to do and not do
3. **Examples** — Input/output pairs that demonstrate desired behavior
4. **Context** — Additional information (documents, data); place near the end

Context placement matters: for long context, put the data first and instructions last. Anchor with phrases like "Based on the information above..."

### Clarity

- Be explicit. Vague prompts underperform.
- Specify format, length, tone, and constraints.
- Reduce ambiguity; avoid "fix it" or "make it better" without criteria.

### Positive Framing

- Prefer "do X" over "don't do Y."
- Use positive patterns (show good examples) rather than anti-patterns alone.
- Example: "Write in flowing prose" instead of "Do not use bullet points."

### Examples (Few-Shot)

- Include 2–5 diverse examples that match desired output.
- Ensure consistent formatting across examples.
- Examples strongly influence behavior; quality matters more than quantity.
- Balance: too few under-specify; too many may overfit.

### Formatting

- **Markdown:** Headers and lists for hierarchy and readability.
- **XML tags:** Boundaries between sections (e.g., `<context>`, `<task>`).
- **Consistency:** Use one style per prompt.
- **Metadata:** XML attributes for labels (e.g., `id="example-1"`).

### Token Efficiency

- Put reusable content (identity, instructions, examples) at the beginning for prompt caching.
- Density over verbosity; every token counts in the context window.
- Cross-reference instead of duplicating long content.

### Chain of Command

Provider APIs give different authority to message roles:

- **Developer/System messages:** Highest priority; define behavior.
- **User messages:** Lower priority; task-specific input.
- Model outputs follow this hierarchy when roles conflict.

---

## 3. Model-Specific Considerations

### Reasoning Models vs. GPT-Style Models

| Model Type | Analogy | Prompting Approach |
|------------|---------|-------------------|
| **Reasoning models** | Senior colleague | Give high-level goals; trust them on implementation details |
| **GPT-style models** | Junior colleague | Give explicit step-by-step instructions |

Reasoning models often perform better with less prescriptive prompts; GPT-style models benefit from very specific instructions.

### Temperature and Sampling

- **Lower temperature:** More deterministic, better for factual or structured outputs.
- **Higher temperature:** More varied, creative outputs.
- **Caution:** Some models (e.g., Gemini 3) recommend keeping default temperature; changing it can cause looping or degraded reasoning.

### Versioning

- Pin production applications to specific model snapshots (e.g., `gpt-4.1-2025-04-14`).
- Behavior can drift across model versions.
- Run evals when upgrading models or prompts.

---

## 4. Best Practices by Use Case

### Coding Agents

- Define the agent's role (e.g., "software engineering agent").
- Provide concrete tool-use examples.
- Require testing (unit tests, commands) before considering work complete.
- Specify output format (Markdown, code fences, file paths with backticks).
- Instruct to investigate files before answering questions about code.

### Agentic Workflows

- Instruct to resolve the full query before yielding.
- Decompose tasks and reflect after each tool call.
- Use TODO tools or rubrics for progress tracking.
- Ask for confirmation before destructive actions (force push, delete, shared writes).
- Balance autonomy and safety; avoid aggressive "MUST use tool" language if it causes over-triggering.

### RAG and Grounding

- State explicitly: "Rely only on the provided context."
- Add: "If the answer is not in the context, state that the information is not available."
- Avoid asking the model to use external knowledge when context should be authoritative.
- Place context first, then the question or instruction.

### Long-Horizon Tasks

- Use structured state (e.g., `tests.json`, `progress.txt`).
- Inform the model about context compaction or multi-window workflows.
- Encourage incremental progress and persistence.
- Use git for checkpoints; models can recover state from the filesystem.

### Avoiding Overengineering

- Scope changes to what was requested.
- Do not add features, refactors, or abstractions beyond the ask.
- Do not add docstrings or validation for unchanged code.
- Avoid speculative "future-proof" design.

---

## 5. Automatic Prompt Optimization (APO)

### When to Use APO

- Scaling prompt iteration across many tasks
- Exploring large prompt spaces
- Reducing manual tuning effort
- Optimizing for accuracy, token count, or cost

### Methods

| Method | Approach | Use Case |
|--------|----------|----------|
| **SPRIG** | Genetic algorithm over prompt components | System-level optimization |
| **OPRO** | LLM generates new prompts from scored candidates | Task-specific and general optimization |
| **APE** | LLM proposes candidates; select by task metrics | Instruction optimization |
| **CAPO** | AutoML + evolutionary search; cost-aware | Multi-objective (accuracy, tokens) |

### Research Findings

- A single optimized system prompt can perform on par with task-specific prompts.
- Combining system-level and task-level optimization yields further gains.
- Optimized prompts generalize across model families, sizes, and languages.

---

## 6. Evaluation and Iteration

### The Prompt Engineering Loop

```text
Infer on dataset → Evaluate performance → Modify prompt → Repeat
```

### Metrics

- **Accuracy:** Task correctness (exact match, F1, etc.)
- **Token count:** Cost and latency
- **Consistency:** Variance across runs or phrasings
- **Safety:** Refusal rates, injection resistance

### Tools and Practices

| Tool | Purpose |
|------|---------|
| **OpenAI Evals** | Custom evals, benchmark registry, dashboard integration |
| **Provider dashboards** | Playground, eval runs, prompt versioning |
| **Custom benchmarks** | HELM, MMLU, BIG-Bench, domain-specific datasets |

### Production Guidance

- Build evals before shipping new prompts.
- Run evals before and after model or prompt changes.
- Create evals for critical user-facing flows.
- Monitor prompt performance as part of model upgrade processes.

---

## 7. Security and Robustness

### Prompt Injection

- **Risk:** Malicious or accidental text in user/retrieved content can override instructions.
- **Mitigations:**
  - Design patterns for prompt injection resistance (e.g., clear separation of trusted vs. untrusted content)
  - Training-based defenses (e.g., SecAlign) to prefer secure outputs
  - Detection (e.g., PromptShield) for injection attempts
- **Limitation:** Injection is not fully solvable via training alone; use layered defenses.

### Prompt Leak

- Reduce risk of system prompt exposure in outputs.
- Follow provider guidance for reducing prompt leak (e.g., Anthropic guardrails).
- Avoid including secrets or PII in prompts.

### Jailbreaking

- Use provider guardrail and safety documentation.
- Avoid overly permissive instructions.
- Monitor refusal patterns and adjust prompts as needed.

---

## 8. Integration into Engineering Workflows

### Process

- Add prompt review to PR checklists for features that use LLMs.
- Version prompts (dashboard, LangChain Hub, or version-controlled files).
- Treat prompts as code: review, test, and document changes.

### Standards

- Adopt a shared structure (Identity → Instructions → Examples → Context).
- Document forbidden phrases and anti-patterns (e.g., no unverified "compiles" or "build succeeded" claims).
- Maintain a prompt library or template collection for common patterns.

### Evaluation

- Create evals for critical prompts.
- Run evals before/after model or prompt changes.
- Integrate evals into CI/CD where feasible.

### Tooling

- Use provider Prompt Optimizer or evals frameworks.
- Consider APO methods for high-stakes or frequently updated prompts.
- Leverage prompt caching and efficient context placement for cost and latency.

### Training and Sharing

- Share this document and provider guides with teams.
- Link to The Prompt Report and curated resources (e.g., promptingguide.ai).
- Establish a shared vocabulary for prompt engineering discussions.

---

## 9. References and Further Reading

### Academic

| Source | URL / ID |
|--------|----------|
| The Prompt Report | arXiv:2406.06608; trigaten.github.io/Prompt_Survey_Site |
| SPRIG | arXiv:2410.14826 |
| OPRO | arXiv:2309.03409; github.com/google-deepmind/opro |
| Chain-of-Thought | arXiv:2201.11903 |
| APO Survey | ACL Anthology, EMNLP 2025 |
| Optimization-Theoretic Survey | arXiv:2502.11560 |

### Provider Documentation

| Provider | Prompting Guides |
|----------|------------------|
| OpenAI | platform.openai.com/docs/guides/prompt-engineering |
| Anthropic | docs.anthropic.com/en/docs/build-with-claude/prompt-engineering |
| Google AI | ai.google.dev/gemini-api/docs/prompting-strategies |

### Curated Resources

| Resource | URL | Focus |
|----------|-----|-------|
| Prompting Guide | promptingguide.ai | Techniques, model-specific guides, agents |
| Awesome Prompt Engineering | github.com/promptslab/Awesome-Prompt-Engineering | Papers, tools, platforms |
| LangChain Hub | smith.langchain.com/hub | Community prompts, versioning |
| OpenAI Cookbook | cookbook.openai.com | Examples, related resources |

### Conferences and Workshops

- **PromptEng'24:** Workshop on Prompt Engineering for Pre-Trained Language Models (TheWebConf 2024)
- **EMNLP / ACL:** Tutorials and papers on prompting, agents, evaluation
- **ICLR:** OPRO, APE, and related optimization work
