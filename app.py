
"""Streamlit interface for the Career Development Agent."""

import streamlit as st
import plotly.graph_objects as go

from pydantic import ValidationError

from data_loader import load_students, load_career_roles
from models import Student
from recommendation_engine import recommend_careers
from roadmap_engine import generate_roadmap, generate_quick_start
from skill_engine import normalize_skill_name


st.set_page_config(
    page_title="Career Development Agent",
    page_icon="🎯",
    layout="wide",
)

st.title("🎯 AI Career Development Agent")
st.write("Discover suitable technology careers and build your learning roadmap.")

students = load_students()
roles = load_career_roles()

if "student" not in st.session_state:
    st.session_state.student = students[0]

if "has_generated" not in st.session_state:
    st.session_state.has_generated = True

student = st.session_state.student

# --------------------------------------------------
# Student profile controls
# --------------------------------------------------

st.sidebar.header("Student Profile")

profile_keys = [
    "profile_name",
    "profile_degree",
    "profile_skills",
    "profile_interests",
    "profile_projects",
    "profile_certifications",
    "profile_hours",
    "profile_timeframe",
]


def reset_profile(profile):
    """Clear old form values and load the selected profile."""
    for key in profile_keys:
        st.session_state.pop(key, None)

    st.session_state.student = profile
    st.session_state.has_generated = True
    st.rerun()


button_col1, button_col2 = st.sidebar.columns(2)

with button_col1:
    if st.button("Load Sample Profile", use_container_width=True):
        reset_profile(students[0])

with button_col2:
    if st.button("Reset", use_container_width=True):
        reset_profile(students[0])

st.sidebar.caption("Edit your details and generate an updated career plan.")

with st.sidebar.form("student_profile_form"):

    st.subheader("Personal Details")

    profile_name = st.text_input(
        "Student Name",
        value=student.name,
        key="profile_name",
    )

    profile_degree = st.text_input(
        "Degree",
        value=student.degree,
        key="profile_degree",
    )

    st.subheader("Current Skills")

    default_skills = "\n".join(
        f"{skill.name}:{skill.level}"
        for skill in student.skills
    )

    profile_skills = st.text_area(
        "Enter one skill per line as Skill:Level (0–10)",
        value=default_skills,
        key="profile_skills",
        height=130,
        help="Example: Python:7",
    )

    profile_interests = st.text_input(
        "Interests (comma-separated)",
        value=", ".join(student.interests),
        key="profile_interests",
    )

    profile_projects = st.text_area(
        "Existing Projects (comma-separated)",
        value=", ".join(student.existing_projects),
        key="profile_projects",
    )

    profile_certifications = st.text_area(
        "Certifications (comma-separated)",
        value=", ".join(student.certifications),
        key="profile_certifications",
    )

    profile_hours = st.number_input(
        "Learning Hours Per Week",
        min_value=0.5,
        max_value=80.0,
        value=float(student.weekly_learning_hours),
        step=0.5,
        key="profile_hours",
    )

    profile_timeframe = st.number_input(
        "Learning Timeframe (months)",
        min_value=1,
        max_value=24,
        value=int(student.learning_timeframe_months),
        step=1,
        key="profile_timeframe",
    )

    generate_clicked = st.form_submit_button(
        "Generate Career Plan",
        use_container_width=True,
        type="primary",
    )

if generate_clicked:
    try:
        parsed_skills = []

        for line in profile_skills.splitlines():
            line = line.strip()

            if not line:
                continue

            if ":" not in line:
                raise ValueError(
                    f"Invalid skill entry: '{line}'. Use Skill:Level format."
                )

            skill_name, skill_level = line.rsplit(":", 1)

            if not skill_name.strip():
                raise ValueError("Skill names cannot be empty.")

            try:
                level = int(skill_level.strip())
            except ValueError:
                raise ValueError(
                    f"Invalid level for '{skill_name}'. Enter a whole number."
                )

            parsed_skills.append({
                "name": skill_name.strip(),
                "level": level,
            })

        updated_student = Student.model_validate({
            "id": student.id,
            "name": profile_name.strip(),
            "degree": profile_degree.strip(),
            "skills": parsed_skills,
            "interests": [
                item.strip()
                for item in profile_interests.split(",")
                if item.strip()
            ],
            "existing_projects": [
                item.strip()
                for item in profile_projects.split(",")
                if item.strip()
            ],
            "certifications": [
                item.strip()
                for item in profile_certifications.split(",")
                if item.strip()
            ],
            "weekly_learning_hours": profile_hours,
            "learning_timeframe_months": profile_timeframe,
        })

        if not updated_student.name:
            raise ValueError("Student name cannot be empty.")

        if not updated_student.degree:
            raise ValueError("Degree cannot be empty.")

        st.session_state.student = updated_student
        st.session_state.has_generated = True
        st.rerun()

    except (ValidationError, ValueError) as error:
        st.sidebar.error(f"Please correct your profile: {error}")

# Use the latest profile after form submission.
student = st.session_state.student

st.sidebar.divider()
st.sidebar.write(f"**Name:** {student.name}")
st.sidebar.write(f"**Degree:** {student.degree}")
st.sidebar.write(
    f"**Weekly Learning Hours:** {student.weekly_learning_hours}"
)

# --------------------------------------------------
# Career recommendations
# --------------------------------------------------

st.header("Career Recommendations")

recommendations = recommend_careers(student, roles)

if not recommendations:
    st.warning("No career recommendations are currently available.")
    st.stop()

for item in recommendations[:3]:
    st.subheader(item["title"])
    st.metric("Career Match Score", f'{item["score"]:.2f}/100')
    st.write(item["explanation"])
    st.write(
        "**Matched skills:**",
        ", ".join(item["matched_skills"]) or "None",
    )
    st.write(
        "**Partially matched skills:**",
        ", ".join(item["partially_matched_skills"]) or "None",
    )
    st.write(
        "**Missing skills:**",
        ", ".join(item["missing_skills"]) or "None",
    )
    st.divider()

# --------------------------------------------------
# Select career role
# --------------------------------------------------

recommended_index = next(
    (
        index
        for index, role in enumerate(roles)
        if role.title == recommendations[0]["title"]
    ),
    0,
)

selected_title = st.selectbox(
    "Choose a career for your learning roadmap",
    [role.title for role in roles],
    index=recommended_index,
)

selected_role = next(
    role for role in roles
    if role.title == selected_title
)

# --------------------------------------------------
# Skill gap analysis
# --------------------------------------------------

st.header("Skill Gap Analysis")

current = {
    normalize_skill_name(skill.name): skill.level
    for skill in student.skills
}

skill_names = [
    normalize_skill_name(skill.name)
    for skill in selected_role.required_skills
]

current_values = [
    current.get(name, 0)
    for name in skill_names
]

target_values = [
    skill.target_beginner_proficiency
    for skill in selected_role.required_skills
]

gap_rows = []

for name, current_level, target_level in zip(
    skill_names,
    current_values,
    target_values,
):
    gap_rows.append({
        "Skill": name,
        "Current Level": current_level,
        "Target Level": target_level,
        "Gap": max(0, target_level - current_level),
    })

st.table(gap_rows)

fig = go.Figure()

fig.add_trace(
    go.Bar(
        name="Current Level",
        x=skill_names,
        y=current_values,
    )
)

fig.add_trace(
    go.Bar(
        name="Target Level",
        x=skill_names,
        y=target_values,
    )
)

fig.update_layout(
    title="Current Skills vs Target Skills",
    yaxis_title="Proficiency (0–10)",
    yaxis=dict(range=[0, 10]),
    barmode="group",
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Seven-day quick-start plan
# --------------------------------------------------

st.header("Seven-Day Quick-Start Plan")

quick_start = generate_quick_start(student, selected_role)

for day in quick_start:
    with st.expander(f"Day {day['day']}: {day['skill']}"):
        st.write(day["activity"])
        st.write("**Deliverable:**", day["deliverable"])

# --------------------------------------------------
# Learning roadmap
# --------------------------------------------------

st.header("Learning Roadmap")

roadmap = generate_roadmap(student, selected_role)

for month in roadmap:
    with st.expander(
        f"Month {month['month']}: {month['objective']}"
    ):
        st.write(
            "**Skills:**",
            ", ".join(month["skills"]) or "Portfolio development",
        )

        st.write("**Exercises:**")

        for exercise in month["exercises"]:
            st.write(f"- {exercise}")

        st.write("**Deliverable:**", month["deliverable"])
        st.write(
            "**Available hours per week:**",
            month["hours_per_week"],
        )
        st.write(
            "**Completion criteria:**",
            month["completion_criteria"],
        )

# --------------------------------------------------
# Career resources
# --------------------------------------------------

st.header("Career Resources")

st.write("**Suggested hands-on projects:**")

for project in selected_role.hands_on_projects:
    st.write(f"- {project}")

st.write("**Optional certifications:**")

for certification in selected_role.optional_certifications:
    st.write(f"- {certification}")

# --------------------------------------------------
# Downloadable report
# --------------------------------------------------

report = f"""# Career Development Report

Student: {student.name}
Degree: {student.degree}
Weekly Learning Hours: {student.weekly_learning_hours}
Learning Timeframe: {student.learning_timeframe_months} months

## Current Skills

""" + "\n".join(
    f"- {skill.name}: {skill.level}/10"
    for skill in student.skills
)

report += "\n\n## Top Career Recommendations\n"

report += "\n".join(
    f"- {item['title']}: {item['score']:.2f}/100"
    for item in recommendations[:3]
)

report += f"\n\n## Selected Career Roadmap\n{selected_role.title}\n"

report += "\n".join(
    f"- Month {month['month']}: {month['objective']}"
    for month in roadmap
)

st.download_button(
    "Download Career Report",
    data=report,
    file_name="career_development_report.md",
    mime="text/markdown",
)

st.success("Career analysis completed successfully!")
