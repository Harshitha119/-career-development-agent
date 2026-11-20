from data_loader import load_students, load_career_roles
from roadmap_engine import generate_roadmap


def test_roadmap_length():
    student = load_students()[0]
    role = load_career_roles()[0]

    roadmap = generate_roadmap(student, role)

    assert len(roadmap) == student.learning_timeframe_months


def test_roadmap_is_deterministic():
    student = load_students()[0]
    role = load_career_roles()[0]

    first = generate_roadmap(student, role)
    second = generate_roadmap(student, role)

    assert first == second


def test_roadmap_has_deliverables():
    student = load_students()[0]
    role = load_career_roles()[0]

    roadmap = generate_roadmap(student, role)

    assert all(item["deliverable"] for item in roadmap)
    assert all(item["completion_criteria"] for item in roadmap)