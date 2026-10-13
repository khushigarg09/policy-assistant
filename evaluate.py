
import json
from main import ask

with open("eval.json", "r", encoding="utf-8") as file:
    tests = json.load(file)

passed = 0

for i, test in enumerate(tests, 1):
    result = ask(test["question"], test["date"])
    expected = test["expected_status"]
    actual = result["status"]

    success = actual == expected
    passed += success

    print(f"\nTest {i}: {'PASS' if success else 'FAIL'}")
    print(f"Question: {test['question']}")
    print(f"Expected: {expected} | Actual: {actual}")
    print(f"Answer: {result['answer']}")
    print(f"Citations: {result['citations']}")

print(f"\nRESULT: {passed}/{len(tests)} tests passed")
