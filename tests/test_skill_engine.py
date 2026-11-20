import pytest
from models import Skill, Student
from skill_engine import normalize_skill_name, compare_skills
from data_loader import load_students, load_career_roles


def test_skill_normalization():
    assert normalize_skill_name("K8s") == "Kubernetes"
    assert normalize_skill_name("AWS") == "Amazon Web Services"


@pytest.mark.parametrize("level", [-1, 11])
def test_invalid_skill_level(level):
    with pytest.raises(ValueError):
        Skill(name="Python", level=level)


def test_missing_skills():
    student = load_students()[0]
    role = load_career_roles()[0]

    result = compare_skills(student, role)

    assert "Docker" in result["missing_skills"]