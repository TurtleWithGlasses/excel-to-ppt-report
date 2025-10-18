"""
Helper utility functions.
"""
from pathlib import Path
from typing import Any, Dict
import json
import uuid
from sqlalchemy import TypeDecorator, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB as PG_JSONB


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


class GUID(TypeDecorator):
    """
    Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses String(36).
    Handles SQLite and other databases that don't support native UUID.
    """
    impl = String
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(String(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value
        else:
            if isinstance(value, uuid.UUID):
                return str(value)
            return value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return value
        return uuid.UUID(value)


class JSONB(TypeDecorator):
    """
    Platform-independent JSONB type.
    Uses PostgreSQL's JSONB type, otherwise uses Text with JSON serialization.
    """
    impl = Text
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_JSONB())
        else:
            return dialect.type_descriptor(Text())

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if dialect.name == 'postgresql':
            return value
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if dialect.name == 'postgresql':
            return value
        else:
            return json.loads(value)

