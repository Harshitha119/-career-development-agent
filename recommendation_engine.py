"""Deterministic career recommendation engine."""

from models import Student, CareerRole
from skill_engine import (
    normalize_skill_name,
    get_student_skills,
    compare_skills,
)

WEIGHTS = {
    "skill": 0.50,
    "interest": 0.20,
    "project": 0.15,
    "certification": 0.10,
    "industry": 0.05,
}


def score_role(student: Student, role: CareerRole) -> dict:
    """Calculate an explainable career recommendation score."""

    student_skills = get_student_skills(student)

    total_weight = sum(
        skill.importance_weight
        for skill in role.required_skills
    )

    skill_score = (
        sum(
            skill.importance_weight
            * min(
                student_skills.get(
                    normalize_skill_name(skill.name), 0
                ) / max(skill.target_beginner_proficiency, 1),
                1.0,
            )
            for skill in role.required_skills
        ) / total_weight
        if total_weight else 0
    )

    role_interests = {
        item.lower() for item in role.interests
    }
    student_interests = {
        item.lower() for item in student.interests
    }

    interest_score = (
        len(role_interests & student_interests)
        / len(role_interests)
        if role_interests else 0
    )

    project_score = (
        1.0 if student.existing_projects else 0.0
    )

    certification_score = (
        1.0 if student.certifications else 0.0
    )

    # No industry preference is provided by the sample profile.
    industry_score = 0.0

    score = 100 * (
        WEIGHTS["skill"] * skill_score
        + WEIGHTS["interest"] * interest_score
        + WEIGHTS["project"] * project_score
        + WEIGHTS["certification"] * certification_score
        + WEIGHTS["industry"] * industry_score
    )

    comparison = compare_skills(student, role)

    return {
        "role_id": role.id,
        "title": role.title,
        "score": round(min(max(score, 0), 100), 2),
        **comparison,
        "explanation": (
            f"Skill match: {skill_score:.2%}; "
            f"interest match: {interest_score:.2%}; "
            f"project match: {project_score:.2%}; "
            f"certification match: {certification_score:.2%}; "
            f"industry match: {industry_score:.2%}."
        ),
    }


def recommend_careers(
    student: Student,
    roles: list[CareerRole],
) -> list[dict]:
    """Score and rank all career roles deterministically."""
    results = [
        score_role(student, role)
        for role in roles
    ]

    return sorted(
        results,
        key=lambda result: (-result["score"], result["title"]),
    )