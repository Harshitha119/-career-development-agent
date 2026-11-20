
"""Coordinate local data loading and career analysis."""

from pathlib import Path

from data_loader import load_career_roles, load_students
from models import Student, CareerRole
from recommendation_engine import recommend_careers
from roadmap_engine import generate_roadmap
from skill_engine import compare_skills


class CareerAgent:
    """Coordinate the career recommendation workflow."""

    def __init__(self, project_root: Path | None = None) -> None:
        students_path = (
            None if project_root is None
            else project_root / "students.json"
        )
        roles_path = (
            None if project_root is None
            else project_root / "career_roles.json"
        )

        self.students = load_students(students_path)
        self.roles = load_career_roles(roles_path)

    def get_student(self, student_id: str) -> Student:
        for student in self.students:
            if student.id == student_id:
                return student
        raise KeyError(f"Student not found: {student_id}")

    def get_role(self, role_id: str) -> CareerRole:
        for role in self.roles:
            if role.id == role_id:
                return role
        raise KeyError(f"Career role not found: {role_id}")

    def skill_gaps(self, student_id: str, role_id: str) -> dict:
        return compare_skills(
            self.get_student(student_id),
            self.get_role(role_id),
        )

    def recommendations(self, student_id: str) -> list[dict]:
        return recommend_careers(
            self.get_student(student_id),
            self.roles,
        )

    def roadmap(self, student_id: str, role_id: str) -> list[dict]:
        return generate_roadmap(
            self.get_student(student_id),
            self.get_role(role_id),
        )
