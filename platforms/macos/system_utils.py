import subprocess
import os

def get_file_permission(path):
    try:
        return oct(os.stat(path).st_mode)[-3:]
    except:
        return "error"

def set_file_permission(path, permission):
    try:
        os.chmod(path, int(permission, 8))
        return True
    except:
        return False

def get_service_status(service_name):
    try:
        result = subprocess.run(["launchctl", "print-disabled", "system"],
                                capture_output=True, text=True)
        if f'"{service_name}" = true' in result.stdout:
            return "disabled"
        elif f'"{service_name}" = false' in result.stdout:
            return "enabled"
        else:
            return "unknown"
    except:
        return "unknown"

def disable_service(service_name):
    try:
        subprocess.run(["launchctl", "disable", f"system/{service_name}"],
                       capture_output=True, check=True)
        subprocess.run(["launchctl", "bootout", "system", f"/System/Library/LaunchDaemons/{service_name}.plist"],
                       capture_output=True)
        return True
    except:
        return False

def get_sysctl_value(key):
    try:
        result = subprocess.run(["sysctl", "-n", key],
                                capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return "unknown"

def set_sysctl_value(key, value):
    try:
        subprocess.run(["sysctl", f"{key}={value}"], check=True)
        return True
    except:
        return False

def run_custom_eval(rule):
    script = rule.get("script_eval")
    if not script or not os.path.exists(script):
        return False
    try:
        result = subprocess.run(["bash", script], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def run_custom_fix(rule):
    script = rule.get("script_fix")
    if not script or not os.path.exists(script):
        return False
    try:
        result = subprocess.run(["bash", script], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

# Unsupported in macOS
def is_kernel_module_disabled(module_name):
    return "unsupported"

def disable_kernel_module(module_name):
    return False

def get_registry_value(_):
    return "unsupported"
