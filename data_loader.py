"""Load local JSON files into Pydantic models.

This module only reads files from disk. It does not score skills, recommend
careers, or build roadmaps, and it does not call any network service.
"""

import json
from pathlib import Path

from models import CareerRole, Student

PROJECT_ROOT = Path(__file__).resolve().parent
STUDENTS_FILE = PROJECT_ROOT / "students.json"
CAREER_ROLES_FILE = PROJECT_ROOT / "career_roles.json"


def load_json(path: Path) -> list | dict:
    """Read one JSON file and return the parsed value."""
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_students(path: Path | None = None) -> list[Student]:
    """Load students from students.json, or from path when one is given."""
    payload = load_json(path or STUDENTS_FILE)
    if not isinstance(payload, list):
        raise ValueError("students.json must contain a list of students.")
    return [Student.model_validate(item) for item in payload]


def load_career_roles(path: Path | None = None) -> list[CareerRole]:
    """Load career roles from career_roles.json, or from path when one is given."""
    payload = load_json(path or CAREER_ROLES_FILE)
    if not isinstance(payload, list):
        raise ValueError("career_roles.json must contain a list of career roles.")
    return [CareerRole.model_validate(item) for item in payload]
