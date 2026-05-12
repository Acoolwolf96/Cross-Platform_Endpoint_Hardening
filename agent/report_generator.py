import json
import os
from datetime import datetime

def generate_report(results, output_path="reports/compliance_report.json"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    summary = {
        "total_rules": len(results),
        "compliant": sum(1 for r in results if r["status"] == "compliant"),
        "non_compliant": sum(1 for r in results if r["status"] == "drift"),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "results": results
    }

    with open(output_path, "w") as f:
        json.dump(summary, f, indent=4)

    return output_path
