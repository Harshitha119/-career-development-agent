
---
name: career-advisor
description: Evaluates student profiles, recommends suitable technology careers, identifies skill gaps, and creates evidence-based learning roadmaps using the Career Development Agent.
---

# Career Advisor Skill

## Objective

Provide transparent, evidence-based career guidance using the project's local student and career-role data.

## Required Workflow

Perform these steps in order:

1. Validate student information, skill levels, weekly learning hours, and learning timeframe.
2. Normalize equivalent skill names using skill_engine.py.
3. Separate evidence supplied by the student from inferred analysis.
4. Score all available career roles using recommendation_engine.py.
5. Select the highest-scoring primary career role.
6. Identify the top three alternative career roles.
7. Calculate and prioritize skill gaps using target proficiency, current proficiency, and importance.
8. Generate a measurable learning roadmap using roadmap_engine.py.
9. Recommend practical projects supported by the available role data.
10. Recommend optional certifications only when present in the supplied role data.
11. Explain the reasoning behind every major recommendation.
12. Perform safety, consistency, and quality checks before presenting results.

## Evidence and Safety Requirements

Never fabricate:
- Student skills
- Projects
- Certifications
- Education
- Achievements

Never:
- Guarantee employment or hiring outcomes.
- Infer protected personal characteristics.
- Make unsupported assumptions.
- Present learning recommendation scores as hiring probabilities.
- Claim current job-market trends without reliable evidence.

Clearly distinguish supplied evidence from career analysis.

## Required Output

Present the results in this order:

1. Evidence supplied by student
2. Career analysis
3. Recommended primary role
4. Three alternative roles
5. Skill gaps
6. Learning roadmap
7. Practical projects
8. Optional certifications
9. Explanation and limitations

## Project Architecture

- app.py: Streamlit user interface.
- career_agent.py: Workflow coordination.
- models.py: Pydantic data models.
- data_loader.py: Local JSON loading.
- skill_engine.py: Skill normalization and comparison.
- recommendation_engine.py: Career scoring.
- roadmap_engine.py: Learning roadmap generation.

Do not duplicate business logic inside app.py.

## Quality Checks

- Validate all input data.
- Keep recommendation scores between 0 and 100.
- Maintain deterministic results.
- Respect available weekly learning hours.
- Use only supplied student evidence.
- Run pytest -q after relevant implementation changes.
