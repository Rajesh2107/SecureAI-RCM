
from app.security_lab.security_tests import (
    run_security_tests,
    calculate_security_score,
)

results = run_security_tests()

print("\n===== SECUREAI-RCM SECURITY TEST RESULTS =====\n")

for result in results:
    print(
        f"{result['test_id']} | "
        f"{result['test_name']} | "
        f"{result['status']} | "
        f"{result['actual_result']}"
    )

print("\n===== SECURITY SCORE =====")
print(f"{calculate_security_score(results)}%")

print("\n===== DETAILS =====")

for result in results:
    print(f"\n{result['test_id']}: {result['details']}")
