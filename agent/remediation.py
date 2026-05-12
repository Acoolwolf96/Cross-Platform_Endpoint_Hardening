import subprocess
import os
import platform

def remediate_rule(rule, system_utils):
    rule_type = rule.get("type")
    target = rule.get("target")
    expected = rule.get("expected")

    if rule_type == "kernel_module":
        return system_utils.disable_kernel_module(target)

    elif rule_type == "file_permission":
        return system_utils.set_file_permission(target, expected)

    elif rule_type == "service_status":
        return system_utils.disable_service(target)

    elif rule_type == "sysctl":
        return system_utils.set_sysctl_value(target, expected)

    elif rule_type == "custom_script":
        return system_utils.run_custom_fix(rule)

    elif rule_type == "registry_key":
        return False  

    else:
        print(f"[!] Unknown remediation type: {rule_type}")
        return False
