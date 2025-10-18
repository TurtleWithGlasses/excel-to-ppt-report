"""
Helper utility functions.
"""
from pathlib import Path
from typing import Any, Dict
import json


def ensure_directory(directory: str) -> Path:
    """
    Ensure a directory exists, create if it doesn't.
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_json(data: Dict[str, Any], file_path: str) -> None:
    """
    Save dictionary to JSON file.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_json(file_path: str) -> Dict[str, Any]:
    """
    Load JSON file to dictionary.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def format_file_size(size_bytes: int) -> str:
    """
    Format bytes to human-readable file size.
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

