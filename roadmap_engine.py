
"""Generate prioritized career learning roadmaps."""

from models import Student, CareerRole
from skill_engine import normalize_skill_name, get_student_skills


def _get_prioritized_gaps(student: Student, role: CareerRole) -> list[dict]:
    """Return skill gaps ordered by importance and proficiency difference."""

    current_skills = get_student_skills(student)
    gaps = []

    for skill in role.required_skills:
        name = normalize_skill_name(skill.name)
        current = current_skills.get(name, 0)
        target = skill.target_beginner_proficiency

        if current < target:
            gaps.append({
                "skill": name,
                "current": current,
                "target": target,
                "importance": skill.importance_weight,
                "priority": (target - current) * skill.importance_weight,
            })

    return sorted(
        gaps,
        key=lambda item: (-item["priority"], item["skill"]),
    )


def generate_quick_start(student: Student, role: CareerRole) -> list[dict]:
    """Generate a practical seven-day career preparation plan."""

    gaps = _get_prioritized_gaps(student, role)

    activities = [
        "Review the selected career role and its required skills",
        "Study the fundamentals of the highest-priority skill",
        "Complete beginner-level practical exercises",
        "Practice the selected skill using a small coding task",
        "Study another important skill gap",
        "Build a small hands-on project",
        "Review progress and document completed work",
    ]

    result = []

    for day, activity in enumerate(activities, start=1):
        if gaps:
            skill = gaps[min((day - 1) // 2, len(gaps) - 1)]["skill"]
        else:
            skill = "Portfolio"

        result.append({
            "day": day,
            "skill": skill,
            "activity": activity,
            "deliverable": f"Day {day} progress note or practical output",
        })

    return result


def generate_roadmap(
    student: Student,
    role: CareerRole,
) -> list[dict]:
    """Create a deterministic monthly roadmap without repeating skill gaps."""

    gaps = _get_prioritized_gaps(student, role)
    roadmap = []
    months = student.learning_timeframe_months

    project_phases = [
        {
            "objective": "Plan and design a career-focused portfolio project",
            "exercises": [
                "Identify a practical problem related to the selected role",
                "Define project requirements and features",
                "Design the architecture and development milestones",
            ],
            "deliverable": "Project proposal and architecture document",
            "criteria": "Requirements, architecture, and milestones are documented",
        },
        {
            "objective": "Develop the core functionality of the portfolio project",
            "exercises": [
                "Implement the main project components",
                "Apply the required technical concepts",
                "Test individual components",
            ],
            "deliverable": "Working core project implementation",
            "criteria": "Core features work and basic tests pass",
        },
        {
            "objective": "Integrate components and improve project reliability",
            "exercises": [
                "Integrate the project components",
                "Handle errors and edge cases",
                "Perform integration and functional testing",
            ],
            "deliverable": "Integrated and tested project",
            "criteria": "Major components work together successfully",
        },
        {
            "objective": "Deploy and document the portfolio project",
            "exercises": [
                "Prepare the project for deployment",
                "Configure the required environment",
                "Write setup and usage documentation",
            ],
            "deliverable": "Deployable project with README documentation",
            "criteria": "Project setup instructions work and documentation is complete",
        },
        {
            "objective": "Prepare and present the completed career portfolio",
            "exercises": [
                "Review code quality and project completeness",
                "Prepare a project demonstration",
                "Document technical decisions and lessons learned",
            ],
            "deliverable": "Final portfolio presentation and project demonstration",
            "criteria": "Project is demonstrable and its design can be explained",
        },
    ]

    for month in range(1, months + 1):

        if month <= len(gaps):
            selected = gaps[month - 1]
            skill = selected["skill"]
            target = selected["target"]

            roadmap.append({
                "month": month,
                "objective": (
                    f"Develop {skill} proficiency toward level {target}"
                ),
                "skills": [skill],
                "exercises": [
                    f"Study the core concepts of {skill}",
                    f"Complete practical exercises using {skill}",
                    f"Build a focused mini-project using {skill}",
                ],
                "deliverable": f"Completed {skill} mini-project",
                "hours_per_week": student.weekly_learning_hours,
                "completion_criteria": (
                    f"Demonstrate understanding of {skill} "
                    f"and document progress toward level {target}"
                ),
            })

        else:
            phase_index = (month - len(gaps) - 1) % len(project_phases)
            phase = project_phases[phase_index]
            cycle = (month - len(gaps) - 1) // len(project_phases) + 1

            objective = phase["objective"]

            if cycle > 1:
                objective = f"Iteration {cycle}: {objective}"

            roadmap.append({
                "month": month,
                "objective": objective,
                "skills": [gap["skill"] for gap in gaps],
                "exercises": phase["exercises"],
                "deliverable": phase["deliverable"],
                "hours_per_week": student.weekly_learning_hours,
                "completion_criteria": phase["criteria"],
            })

    return roadmap
