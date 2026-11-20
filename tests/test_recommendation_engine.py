from data_loader import load_students, load_career_roles
from recommendation_engine import recommend_careers, score_role
from models import Skill


def test_scores_between_zero_and_hundred():
    student = load_students()[0]
    roles = load_career_roles()

    results = recommend_careers(student, roles)

    assert all(0 <= item["score"] <= 100 for item in results)


def test_increasing_relevant_skill_does_not_reduce_score():
    student = load_students()[0]
    role = load_career_roles()[0]

    original = score_role(student, role)["score"]

    student.skills.append(Skill(name="Docker", level=5))
    updated = score_role(student, role)["score"]

    assert updated >= original


def test_ai_platform_engineer_is_top_recommendation():
    student = load_students()[0]
    roles = load_career_roles()

    results = recommend_careers(student, roles)

    assert results[0]["title"] == "AI Platform Engineer"


def test_recommendations_are_deterministic():
    student = load_students()[0]
    roles = load_career_roles()

    first = recommend_careers(student, roles)
    second = recommend_careers(student, roles)

    assert first == second