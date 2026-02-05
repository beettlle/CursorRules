# Proposal: Add Code Complexity and Quality Metrics to Cursor Rules

This document proposes how to integrate code complexity and quality metrics into the CursorRules project so that agents and contributors can use measurable criteria for maintainability, bug reduction, and production stability.

## Goals

- **Maintainability**: Codify thresholds (cyclomatic complexity, cognitive complexity, Maintainability Index) so rules discourage unmaintainable code.
- **Bug reduction**: Align rules with metrics that correlate with defects (CK metrics, churn, file size).
- **Production stability**: Connect existing anti-patterns (no I/O in loops, no silent failures) to complexity and quality metrics where relevant.
- **Consistency**: Follow existing rule format (CONTRIBUTING.md), composition (RULE_COMPOSITION.md), and density guidelines.

## Summary of Metrics to Encode

| Metric | Scope | Use in rules |
|--------|--------|--------------|
| **Cyclomatic complexity** | Per function/method | Cap per function (e.g. ≤10–15); basis for test count |
| **Cognitive complexity** | Per function/class | Prefer over cyclomatic for "understandability"; nesting/linearity |
| **Maintainability Index (MI)** | Per module | 0–100; gate "no new code below 20" |
| **File/module size (LOC)** | Per file | Already implied by file size limit ~250 lines in `general-llm-anti-patterns.mdc` 1.7 |
| **CK metrics (OO)** | Per class | WMC, CBO, LCOM as design smells; high values → refactor |
| **Code churn / hotspots** | Process | Mention in audits: high churn + high complexity = priority |

References: [GeeksforGeeks – Complexity Metrics](https://www.geeksforgeeks.org/dsa/complexity-metrics/), [SonarSource – Cognitive Complexity](https://www.sonarsource.com/resources/cognitive-complexity/), [Microsoft – Maintainability Index](https://learn.microsoft.com/en-us/visualstudio/code-quality/code-metrics-maintainability-index-range-and-meaning), SEI risk bands for cyclomatic complexity.

---

## Option A: New Rule File (Recommended)

**File:** `.cursor/rules/code-complexity-quality-metrics.mdc`

**Rationale:** Keeps complexity/quality in one place; language-agnostic; can be loaded for any codebase. Does not bloat `general-llm-anti-patterns.mdc` or the quick reference.

**Frontmatter (draft):**

```yaml
---
description: "Code complexity and quality metrics - cyclomatic, cognitive, MI, CK metrics for maintainability and defect reduction"
globs: ["**/*.py", "**/*.go", "**/*.java", "**/*.kt", "**/*.swift", "**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx"]
alwaysApply: false
---
```

**Content structure (dense, CONTRIBUTING-compliant):**

- **Cyclomatic complexity** – Cap per function (e.g. ≤10 or ≤15); above = refactor or split; reference SEI bands (1–10 simple, 11–20 moderate, 21–50 high, 50+ untestable).
- **Cognitive complexity** – Prefer lowering nesting and breaks in linear flow; consider "understandability" when reviewing.
- **Maintainability Index** – Aim MI ≥20 for new/modified code; below 10 = refactor priority.
- **File/module size** – Cross-reference only: general-llm-anti-patterns.mdc section 1.7.
- **OO design (CK)** – High WMC/CBO/LCOM → refactor/split class; DIT/NOC deep or wide → consider design.
- **Churn and hotspots** – In audits: high churn + high complexity = priority areas.

**Format:** Each rule follows CONTRIBUTING.md: ❌ Bad / ✅ Good / ⚠️ Why / 🔧 Fix / 📍 See / **Detect**; 1–3 line examples; comma-separated detection; cross-reference, no duplication.

## Option B: Integrate Into Existing Rules

- **general-llm-anti-patterns.mdc:** Add a category (e.g. "Category 12: Complexity and Quality Metrics") with 3–5 short rules.
- **critical-rules-quick-reference.mdc:** Add 1–2 lines (e.g. cyclomatic ≤10–15, MI ≥20, churn+complexity priority).
- **Brutal audits:** Add a "Complexity and quality metrics" check that references the new rule file.

**Recommendation:** Do Option A and light Option B: new file + one short bullet in the quick reference + audit workflow/brutal audits reference the new file.

---

## Proposed README.md Changes

- **Repository Structure** – In the `.cursor/rules/` listing, add:
  - `code-complexity-quality-metrics.mdc` – Code complexity and quality metrics (cyclomatic, cognitive, MI, CK) for maintainability and defect reduction.
- **Core Principles** – Add one bullet:
  - Complexity and quality metrics: Cyclomatic complexity per function (e.g. ≤10–15), Maintainability Index ≥20 for new code, OO design metrics (CK); see code-complexity-quality-metrics.mdc.
- **Phase-Based Audit Workflows** – Add:
  - Audits may include complexity and quality checks; see code-complexity-quality-metrics.mdc and language-specific brutal audit files.
- **Table of Contents** – Add "Complexity and quality metrics" if you add a dedicated subsection.

## Proposed CONTRIBUTING.md Changes

- **Review Checklist** – Add:
  - [ ] If adding or changing rules that affect complexity or maintainability, consider aligning with code-complexity-quality-metrics.mdc.
- **Content Validation** – Add (optional):
  - When the rule relates to complexity or design, consider consistency with thresholds in code-complexity-quality-metrics.mdc.
- **See Also** – Add:
  - docs/proposal-complexity-quality-metrics.md – Proposal for complexity and quality metrics rules.

## Implementation Order

1. Create `.cursor/rules/code-complexity-quality-metrics.mdc`.
2. Update critical-rules-quick-reference.mdc with one short reference and pointer to the new file.
3. Update audit-workflow.mdc and optionally brutal audits to reference complexity/quality checks.
4. Update README.md (structure, core principles, audits, TOC).
5. Update CONTRIBUTING.md (checklist, validation, See Also).
6. Optionally update AGENTS.md under Phase Verification to mention the new rule file.

## References

- [GeeksforGeeks – Complexity Metrics](https://www.geeksforgeeks.org/dsa/complexity-metrics/)
- [SonarSource – Cognitive Complexity](https://www.sonarsource.com/resources/cognitive-complexity/)
- [Microsoft – Maintainability Index](https://learn.microsoft.com/en-us/visualstudio/code-quality/code-metrics-maintainability-index-range-and-meaning)
- SEI/SonarSource cyclomatic complexity risk bands; Chidamber–Kemerer (CK) metrics.

---

## Summary

- **New doc:** `docs/proposal-complexity-quality-metrics.md` (this file).
- **New rule (recommended):** `.cursor/rules/code-complexity-quality-metrics.mdc` (Option A), with a short mention in the quick reference and in audit workflows.
- **README.md:** Add the new rule to the repo structure, one bullet under Core Principles, and a sentence under Phase-Based Audit Workflows (and TOC if needed).
- **CONTRIBUTING.md:** Add one checklist item, one optional validation bullet, and one See Also link.
