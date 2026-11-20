
"""Integration tests for the Career Development Agent."""

import json
from pathlib import Path

from career_agent import CareerAgent
from data_loader import load_career_roles, load_students

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_json_files_are_valid():
    for filename in ("students.json", "career_roles.json"):
        payload = json.loads(
            (PROJECT_ROOT / filename).read_text(encoding="utf-8")
        )
        assert isinstance(payload, list)
        assert payload


def test_data_loader_returns_expected_sample():
    students = load_students()
    roles = load_career_roles()

    assert students[0].name == "Harsha"
    assert roles[0].title == "AI Platform Engineer"
    assert len(roles) == 10


def test_agent_can_look_up_local_records():
    agent = CareerAgent(PROJECT_ROOT)

    assert agent.get_student("student-1").name == "Harsha"
    assert agent.get_role("ai-platform-engineer").title == "AI Platform Engineer"


def test_agent_recommendations_and_roadmap():
    agent = CareerAgent(PROJECT_ROOT)
    student = agent.get_student("student-1")
    role = agent.get_role("ai-platform-engineer")

    assert agent.skill_gaps(student.id, role.id)["missing_skills"]
    assert agent.recommendations(student.id)[0]["title"] == "AI Platform Engineer"
    assert len(agent.roadmap(student.id, role.id)) == student.learning_timeframe_months
