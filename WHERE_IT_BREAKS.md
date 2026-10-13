
# Where It Breaks

## 1. Keyword Detection
Questions phrased in unexpected ways may not map to the correct topic.

## 2. Policy Coverage
Only explicitly implemented policy topics can be answered. Missing rules may result in CANNOT_ANSWER.

## 3. Effective Dates
Date comparisons depend on correct rule dates and precedence data.

## 4. Conflict Detection
Conflict handling is currently narrow and manually implemented. Not every contradiction is detected automatically.

## 5. Calculations
MDR rates, caps, and GST assumptions must match the applicable policy version. Unsupported merchant categories or invalid inputs may not be handled comprehensively.

## 6. Citations
Citations are manually assigned in the answer logic and may become inaccurate if source documents change.

## 7. Evaluation
The 12 test cases cover only a small set of scenarios. A passing result does not guarantee correctness for all questions.

## 8. No RAG
The system does not retrieve arbitrary passages from documents at runtime. New policy content must be added to the structured rules and answer logic.

## 9. Production Readiness
The prototype has no authentication, audit logging, user interface, automated document ingestion, or production monitoring.
