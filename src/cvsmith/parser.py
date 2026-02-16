"""YAML parser for CV data"""

import yaml


def load_yaml(file_path: str) -> dict:
    """Load YAML file and return as dictionary."""
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)
