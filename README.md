
# Policy Assistant

A rule-based policy assistant that answers merchant questions using policy documents, amendments, effective dates, and precedence rules.

## Features
- Detects policy topics from questions.
- Selects rules based on effective dates.
- Calculates MDR, GST, and total fees.
- Provides policy citations.
- Identifies conflicts between FAQ information and official policy.
- Returns ANSWERED, CONFLICT_RESOLVED, or CANNOT_ANSWER.

## Project Structure

- `ai-2-data/` — Source policy documents.
- `policy_rules.py` — Structured policy rules and date filtering.
- `main.py` — Question handling and fee calculations.
- `eval.json` — Evaluation questions.
- `evaluate.py` — Evaluation runner.
- `DECISIONS.md` — Design decisions.
- `AI_USAGE.md` — AI usage disclosure.
- `WHERE_IT_BREAKS.md` — Known limitations.

## Requirements
Python 3. No external packages are currently required.

## Run

```bash
python3 evaluate.py
```

## Evaluation
The initial evaluation dataset contains 12 test cases covering policy questions, calculations, conflicting information, and unsupported questions.

## Limitations
This is a prototype. Answers and calculations must be validated against the source documents before production use.
