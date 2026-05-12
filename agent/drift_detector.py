def detect_drift(rule, actual_value):
    expected = rule.get("expected")
    is_drifted = actual_value != expected
    if is_drifted:
        drift = {
            "id": rule["id"],
            "title": rule["title"],
            "expected": expected,
            "actual": actual_value,
            "remediation": rule.get("remediation")
        }
        return drift
    return None
