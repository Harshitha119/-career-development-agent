"""Skill normalization and comparison utilities."""

from models import Student, CareerRole

SKILL_ALIASES = {
    "aws": "Amazon Web Services",
    "k8s": "Kubernetes",
    "js": "JavaScript",
    "ml": "Machine Learning",
    "ai": "Artificial Intelligence",
    "gcp": "Google Cloud Platform",
}


def normalize_skill_name(name: str) -> str:
    """Normalize equivalent skill names."""
    cleaned = name.strip()
    return SKILL_ALIASES.get(cleaned.lower(), cleaned)


def get_student_skills(student: Student) -> dict[str, int]:
    """Return normalized student skills."""
    return {
        normalize_skill_name(skill.name): skill.level
        for skill in student.skills
    }


def compare_skills(
    student: Student,
    role: CareerRole,
) -> dict:
    """Compare student skills with role requirements."""
    student_skills = get_student_skills(student)

    matched = []
    partial = []
    missing = []

    for skill in role.required_skills:
        name = normalize_skill_name(skill.name)
        current = student_skills.get(name, 0)
        target = skill.target_beginner_proficiency

        if current >= target:
            matched.append(name)
        elif current > 0:
            partial.append(name)
        else:
            missing.append(name)

    return {
        "matched_skills": matched,
        "partially_matched_skills": partial,
        "missing_skills": missing,
    }