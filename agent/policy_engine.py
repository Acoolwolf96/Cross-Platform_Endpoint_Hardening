import platform

def evaluate_rule(rule, system_utils):
    rule_type = rule.get("type")
    target = rule.get("target")
    expected = rule.get("expected")

    if rule_type == "kernel_module":
        actual = system_utils.is_kernel_module_disabled(target)
        return actual == expected, actual

    elif rule_type == "file_permission":
        actual = system_utils.get_file_permission(target)
        return actual == expected, actual

    elif rule_type == "service_status":
        actual = system_utils.get_service_status(target)
        return actual == expected, actual

    elif rule_type == "registry_key":
        if platform.system().lower() != "windows":
            return False, "unsupported"
        actual = system_utils.get_registry_value(target)
        return actual == expected, actual

    elif rule_type == "sysctl":
        actual = system_utils.get_sysctl_value(target)
        return actual == expected, actual

    elif rule_type == "custom_script":
        passed = system_utils.run_custom_eval(rule)
        return passed, None

    else:
        print(f"[!] Unsupported rule type: {rule_type}")
        return False, None
