import yaml
import json
import os

def load_policy(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Policy file not found: {path}")
    
    with open(path, 'r') as f:
        if path.endswith('.yaml') or path.endswith('.yml'):
            return yaml.safe_load(f)
        elif path.endswith('.json'):
            return json.load(f)
        else:
            raise ValueError("Unsupported policy file format (must be .yaml or .json)")
