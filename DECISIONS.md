
# Design Decisions

## 1. Rule-Based Approach
The prototype uses explicit Python rules instead of an LLM or RAG pipeline. This keeps policy selection and calculations predictable.

## 2. Policy Precedence
When an amendment conflicts with an older policy or FAQ, the applicable newer amendment takes precedence according to its effective date and recorded precedence.

## 3. Effective Dates
Rules are selected using the requested date. Expired rules should not apply, and future rules should not apply before their effective dates.

## 4. Calculations
MDR, applicable caps, GST, and total fees are calculated using Python rather than generated text.

## 5. Citations
Answers include references to the policy clauses or source sections used.

## 6. Response Status
- ANSWERED: A policy answer was produced.
- CONFLICT_RESOLVED: Conflicting policy information was identified and resolved.
- CANNOT_ANSWER: The system could not answer from its supported rules.

## 7. Scope
The prototype uses keyword-based topic detection and a manually maintained rule table. It does not use embeddings, a vector database, or an external LLM.
