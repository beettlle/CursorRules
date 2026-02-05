# Prompt: Add Language Addenda to CursorRules Modelfiles

Use this prompt with any LLM to produce Modelfiles customized for your project's language.

## Instructions for the LLM

You are helping a user customize CursorRules Ollama Modelfiles for their project.

**User's project language:** [Replace with: Go | Python | Java | Swift | JavaScript]

**Task:**

1. Read the base Modelfiles in this directory:
   - `cursorrules-review.Modelfile`
   - `cursorrules-refine.Modelfile`
   - `cursorrules-code.Modelfile`
   - `cursorrules-refactor.Modelfile`

2. Read the language addenda for the user's language:
   - `addenda/review-[lang].txt` (e.g., `addenda/review-go.txt`)
   - `addenda/refine-[lang].txt` (e.g., `addenda/refine-go.txt`)
   - `addenda/code-[lang].txt` (e.g., `addenda/code-go.txt`)
   - `addenda/refactor-[lang].txt` (e.g., `addenda/refactor-go.txt`)

3. Merge the addendum content into each Modelfile:
   - Append the addendum text to the end of the SYSTEM block, before the closing `"""`.
   - Ensure the addendum flows naturally after the existing SYSTEM content (add a space or newline if needed).

4. Output the four complete modified Modelfile contents, ready to save as `cursorrules-review-[lang].Modelfile`, `cursorrules-refine-[lang].Modelfile`, `cursorrules-code-[lang].Modelfile`, and `cursorrules-refactor-[lang].Modelfile`.

**Available languages:** Go, Python, Java, Swift, JavaScript. Choose the addenda matching your project's primary language.

**Optional:** If the user requests only a subset (e.g. "only review and refine"), read and output only those base Modelfiles and their corresponding addenda (e.g. two Modelfiles and two addenda).
