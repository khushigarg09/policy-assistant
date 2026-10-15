# Policy Assistant

A small, offline question-answering assistant for merchant payment policies. It answers support questions across evolving policy documents, calculates fees deterministically in code, respects effective dates, and detects contradictions between FAQs and official circulars.

---

## Quickstart (How to Run)

Requires **Python 3.8+**. No third-party packages or API keys are required.

Run the test suite:
```bash
python evaluate.py
```
*(On macOS/Linux, use `python3 evaluate.py`)*

### Using It in Python

```python
from main import ask

# Example: Arithmetic calculation with cap and GST
result = ask("A large merchant receives a Rs.1,50,000 UPI payment", as_of_date="2026-08-15")
print(result)
# Output:
# {
#   'answer': 'For a ₹150,000.00 transaction, MDR is ₹25.00, GST is ₹4.50, and the total fee is ₹29.50.',
#   'citations': ['Master 2.2', 'Circular C / Master 2.3', 'Master 2.4'],
#   'status': 'ANSWERED'
# }
```

---

## Output Format

Every call to `ask(question, as_of_date)` returns a dictionary:

```python
{
    "answer": "Plain-English answer or calculation result",
    "citations": ["List of relevant document names and clause numbers"],
    "status": "ANSWERED" | "CONFLICT_RESOLVED" | "CANNOT_ANSWER"
}
```

- **`ANSWERED`**: Found an applicable rule for the specified date and answered it.
- **`CONFLICT_RESOLVED`**: Found a contradiction (e.g. stale FAQ vs. new circular amendment) and resolved it using policy precedence.
- **`CANNOT_ANSWER`**: The question is out of scope or cannot be safely answered from policy documents.

---

## What Works

1. **Temporal Awareness (`as_of_date`)**:
   - The same question returns different answers depending on the date:
     - **Refund MDR before 1 Sep 2026**: Reversible within 24 hours (Master 3.3).
     - **Refund MDR on/after 1 Sep 2026**: Not reversible (Circular MS/2026/17 Section D deleted Clause 3.3).
     - **Small merchant MDR**: 0.30% before 1 Aug 2026, 0.25% from 1 Aug 2026 onward (Circular Section B).

2. **Code-Calculated Arithmetic**:
   - Fee calculations (MDR, tiered caps, and 18% GST) are computed directly in Python, never guessed by a model.
   - Automatically applies the ₹15 cap (small merchants) or ₹25 cap (large merchants under Circular Section C).
   - Correctly handles GST outside of the MDR cap as mandated by Master Clause 2.4.

3. **Conflict Detection & Precedence**:
   - The March 2026 FAQ claims there is "no upper limit on the fee".
   - The system detects this contradiction against Circular Section C / Master 2.3, explains why the FAQ is outdated, cites both sources, and marks the status as `CONFLICT_RESOLVED`.

4. **Grounded Citations**:
   - Every citation links to real clauses in `policy_master_v1.md`, `circular_2026_08_amendment.md`, or `merchant_faq_2026-03.md`. It never invents clause numbers.

5. **Safe Fallbacks**:
   - Returns `CANNOT_ANSWER` for out-of-scope or ungrounded questions (e.g. unsupported questions or missing policy areas).

---

## Benchmark Questions (Q1 – Q8)

| # | Question | Date | Status | How It Is Handled |
| :--- | :--- | :--- | :--- | :--- |
| **Q1** | When does a small merchant receive UPI money? | 2026-08-15 | `ANSWERED` | Settle by 11:59 PM same day with Instant Settlement add-on, otherwise T+1 (Circular Section A / Master 1.1). |
| **Q2** | Large merchant receives ₹4,000 UPI. What MDR & GST? | 2026-08-15 | `ANSWERED` | 0.50% MDR = ₹20.00, GST = ₹3.60, Total = ₹23.60 (Master 2.2, Circular C, Master 2.4). |
| **Q3** | Large merchant receives ₹1,50,000 UPI. What do they pay? | 2026-08-15 | `ANSWERED` | 0.50% uncapped is ₹750, capped at ₹25.00. GST = ₹4.50, Total = ₹29.50 (Master 2.2, Circular C, Master 2.4). |
| **Q4a** | Refund 3 hours after sale on 20 Aug 2026: MDR back? | 2026-08-20 | `ANSWERED` | Yes, full reversal within 24 hours under Master 3.2 and 3.3. |
| **Q4b** | Same refund question asked on 5 Sep 2026: MDR back? | 2026-09-05 | `ANSWERED` | No, Clause 3.3 deleted from 1 Sep 2026 by Circular Section D. |
| **Q5** | What does FAQ say about MDR cap, and is it right? | 2026-08-15 | `CONFLICT_RESOLVED` | FAQ says no cap; that is incorrect under Circular Section C (cap is ₹15 / ₹25). |
| **Q6** | Can customer pay ₹1,00,000 twice in one day? | 2026-08-15 | `ANSWERED` | No, daily aggregate limit per customer is ₹1,00,000 or customer bank limit (Master 4.3 & Circular E). |
| **Q7** | Closed account yesterday. When will I get money? | 2026-08-15 | `ANSWERED` | Released within 10 working days, subject to 30 days notice (Master 5.1 & 5.2). |
| **Q8** | Can card payments settle same day? | 2026-08-15 | `ANSWERED` | No, cards settle on T+2 (Master 1.2). Same-day is UPI only with add-on. |

---

## What Doesn't Work (Limitations)

- **Keyword Sensitivity**: Uses rule/keyword detection. Rephrasing with unusual synonyms or complex compound sentences can cause the system to miss the topic and return `CANNOT_ANSWER`.
- **Pre-Configured Conflicts Only**: Specifically resolves known discrepancies (like the FAQ cap claim); does not automatically discover arbitrary new document conflicts without added rules.
- **Single-Intent Focus**: Does not split multi-part questions (e.g. asking settlement time and fee in a single sentence).
- **Manual Maintenance**: New policies or circular amendments must be added to `policy_rules.py`.

*(See [`WHERE_IT_BREAKS.md`](file:///c:/Users/gargp/Downloads/policy-assistant/policy-assistant/WHERE_IT_BREAKS.md) for concrete failure examples.)*

---

## Project Files

- [`main.py`](file:///c:/Users/gargp/Downloads/policy-assistant/policy-assistant/main.py): Main entrypoint (`ask`) and fee calculator.
- [`policy_rules.py`](file:///c:/Users/gargp/Downloads/policy-assistant/policy-assistant/policy_rules.py): Structured policy rules with validity dates and precedence.
- [`evaluate.py`](file:///c:/Users/gargp/Downloads/policy-assistant/policy-assistant/evaluate.py): Test runner for `eval.json`.
- [`eval.json`](file:///c:/Users/gargp/Downloads/policy-assistant/policy-assistant/eval.json): Evaluation dataset with standard, temporal, and adversarial test cases.
- [`DECISIONS.md`](file:///c:/Users/gargp/Downloads/policy-assistant/policy-assistant/DECISIONS.md): Key design decisions and handling of policy ambiguities.
- [`WHERE_IT_BREAKS.md`](file:///c:/Users/gargp/Downloads/policy-assistant/policy-assistant/WHERE_IT_BREAKS.md): Detailed edge cases where the system fails.
- [`AI_USAGE.md`](file:///c:/Users/gargp/Downloads/policy-assistant/policy-assistant/AI_USAGE.md): Transparent disclosure of AI assistance.
- [`ai-2-data/`](file:///c:/Users/gargp/Downloads/policy-assistant/policy-assistant/ai-2-data): Source policy documents (`policy_master_v1.md`, `circular_2026_08_amendment.md`, `merchant_faq_2026-03.md`).
