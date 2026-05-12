import subprocess
import os
import winreg

def get_registry_value(reg_path):
    try:
        hive_map = {
            "HKLM": winreg.HKEY_LOCAL_MACHINE,
            "HKCU": winreg.HKEY_CURRENT_USER
        }
        parts = reg_path.split("\\")
        hive_str = parts[0]
        key_path = "\\".join(parts[1:-1])
        value_name = parts[-1]
        hive = hive_map[hive_str]

        key = winreg.OpenKey(hive, key_path)
        value, _ = winreg.QueryValueEx(key, value_name)
        return str(value)
    except:
        return "error"

def set_registry_value(reg_path, value):
    try:
        parts = reg_path.split("\\")
        hive_str = parts[0]
        key_path = "\\".join(parts[1:-1])
        value_name = parts[-1]
        hive = {
            "HKLM": winreg.HKEY_LOCAL_MACHINE,
            "HKCU": winreg.HKEY_CURRENT_USER
        }.get(hive_str)

        key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, str(value))
        return True
    except:
        return False

def get_service_status(service_name):
    try:
        result = subprocess.run(["sc", "query", service_name], capture_output=True, text=True)
        if "RUNNING" in result.stdout:
            return "running"
        return "stopped"
    except:
        return "unknown"

def disable_service(service_name):
    try:
        subprocess.run(["sc", "config", service_name, "start=", "disabled"], check=True)
        subprocess.run(["sc", "stop", service_name], check=False)
        return True
    except:
        return False

def get_file_permission(path):
    try:
        result = subprocess.run(["icacls", path], capture_output=True, text=True)
        return result.stdout
    except:
        return "error"

def set_file_permission(path, permissions):
    try:
        result = subprocess.run(["icacls", path, "/grant", permissions], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def get_sysctl_value(key):
    return "unsupported"

def set_sysctl_value(key, value):
    return False

def is_kernel_module_disabled(module_name):
    return "unsupported"

def disable_kernel_module(module_name):
    return False

def run_custom_eval(rule):
    script = rule.get("script_eval")
    if not script or not os.path.exists(script):
        return False
    try:
        result = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", script],
                                capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def run_custom_fix(rule):
    script = rule.get("script_fix")
    if not script or not os.path.exists(script):
        return False
    try:
        result = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", script],
                                capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False
