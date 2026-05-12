import argparse
import platform
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config_loader import load_policy
import remediation
import policy_engine
import report_generator
from logger import setup_logger

logger = setup_logger()

def get_system_utils(os_name):
    if os_name == "linux":
        from platforms.linux import system_utils
    elif os_name == "windows":
        from platforms.windows import system_utils
    elif os_name == "darwin":
        from platforms.macos import system_utils
    else:
        raise RuntimeError(f"Unsupported OS: {os_name}")
    return system_utils

def main():
    parser = argparse.ArgumentParser(description="Cross-Platform Hardening Agent")
    parser.add_argument('--policy', required=True, help='Path to YAML or JSON policy file')
    parser.add_argument('--remediate', action='store_true', help='Attempt to auto-remediate drift')
    args = parser.parse_args()

    logger.info("Starting Hardening Agent...")

    os_name = platform.system().lower()
    logger.info(f"Detected OS: {os_name}")

    try:
        system_utils = get_system_utils(os_name)
    except RuntimeError as e:
        logger.error(str(e))
        return

    policy = load_policy(args.policy)
    all_rules = policy.get("rules", [])
    filtered_rules = [
        rule for rule in all_rules
        if rule.get("os", "").lower() in [os_name, "any"]
    ]

    logger.info(f"Loaded {len(all_rules)} rules from: {args.policy}")
    logger.info(f"Filtered {len(filtered_rules)} applicable rules for {os_name}")

    results = []

    for rule in filtered_rules:
        try:
            compliant, actual = policy_engine.evaluate_rule(rule, system_utils)
            status = "compliant" if compliant else "drift"

            results.append({
                "id": rule.get("id"),
                "title": rule.get("title"),
                "type": rule.get("type"),
                "severity": rule.get("severity", "medium"),
                "category": rule.get("category", "general"),
                "status": status,
                "expected": rule.get("expected"),
                "actual": actual
            })

            if compliant:
                print(f"Compliant: {rule['id']} - {rule['title']}")
            else:
                print(f"Drift: {rule['id']} - {rule['title']} (actual: {actual})")
                if args.remediate:
                    success = remediation.remediate_rule(rule, system_utils)
                    if success:
                        print(f"    🔧 Remediated: {rule['id']}")
                    else:
                        logger.error(f"Remediation failed for {rule['id']}")
        except Exception as e:
            print(f"[!] Error evaluating {rule.get('id')}: {e}")
            logger.error(f"Exception in rule {rule.get('id')}: {e}")

    # Generate compliance report
    if results:
        report_path = report_generator.generate_report(results)
        logger.info(f"Compliance report written to: {report_path}")
    else:
        logger.warning("No applicable rules were processed.")

if __name__ == "__main__":
    main()
