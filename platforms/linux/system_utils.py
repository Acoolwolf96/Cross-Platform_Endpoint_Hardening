import subprocess
import os

def is_kernel_module_disabled(module_name):
    try:
        with open("/proc/modules", "r") as f:
            return "disabled" if module_name not in f.read() else "enabled"
    except Exception:
        return "unknown"

def disable_kernel_module(module_name):
    try:
        subprocess.run(["modprobe", "-r", module_name], check=True)
        with open(f"/etc/modprobe.d/{module_name}.conf", "w") as f:
            f.write(f"install {module_name} /bin/true\n")
        return True
    except Exception as e:
        return False

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
        result = subprocess.run(["systemctl", "is-enabled", service_name],
                                capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return "unknown"

def disable_service(service_name):
    try:
        subprocess.run(["systemctl", "disable", "--now", service_name],
                       capture_output=True, text=True, check=True)
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
        with open("/etc/sysctl.conf", "a") as f:
            f.write(f"\n{key} = {value}")
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
