# Stet dismiss reasons — quick reference

How to choose a dismiss reason when triaging stet findings. Prefer always giving a reason: it feeds optimize/shadowing and improves future reviews.

See also: `.cursor/rules/stet-integration.mdc` for commands and the reason table.

## When to use each reason

### `false_positive`

The finding is not a real issue: the model misread the code, duplicated an existing check, or flagged style noise.

**Example:** Stet reports a missing null check, but the caller already validates the value two lines above.

```bash
stet dismiss abc123 false_positive
```

### `already_correct`

The code already addresses the concern, or the finding targets removed lines that the diff already fixes.

**Example:** Finding says "add error handling" but the added lines in the same hunk already wrap the call in try/except.

```bash
stet dismiss def456 already_correct
```

### `wrong_suggestion`

The suggested fix is incorrect or harmful: wrong tool, inconsistent with project patterns, or would regress behavior.

**Example:** Stet suggests switching to a sync HTTP client inside an async handler; project standards require `httpx.AsyncClient`.

```bash
stet dismiss ghi789 wrong_suggestion
```

### `out_of_scope`

The finding applies to the wrong scope: generated files, vendored assets, meta/curated docs, or files outside the review intent.

**Example:** Nit on `package-lock.json` or a rule file in a curated rules repo where the change is intentional policy.

```bash
stet dismiss jkl012 out_of_scope
```

## Quick pick

| Situation | Reason |
|-----------|--------|
| Suggestion would make code worse or inconsistent | `wrong_suggestion` |
| Wrong file type or generated/meta content | `out_of_scope` |
| Code or diff already correct | `already_correct` |
| Otherwise noise or misread | `false_positive` |

## Bad vs good

❌ **Bad:** `stet dismiss abc123` with no reason when the user said the finding was not useful.

✅ **Good:** `stet dismiss abc123 false_positive` (or the reason that matches the situation).
