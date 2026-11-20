
# 🎯 AI Career Development Agent

An intelligent career guidance application that helps students identify suitable technology career paths based on their current skills, interests, projects, certifications, and learning availability.

The application provides career recommendations, skill-gap analysis, personalized learning roadmaps, and practical project suggestions.

## 1. Problem Statement

Students often find it difficult to identify suitable technology careers and understand which technical skills they need to develop.

This project addresses the problem by analyzing student profiles and comparing them with the skill requirements of different technology roles.

## 2. Objectives

- Analyze student skills and proficiency levels.
- Recommend suitable technology career paths.
- Identify missing and partially developed skills.
- Prioritize skill gaps.
- Generate personalized learning roadmaps.
- Provide practical project and certification suggestions.
- Generate downloadable career reports.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive user interface |
| Plotly | Skill comparison visualization |
| Pydantic | Data validation |
| JSON | Local student and career-role data |
| Pytest | Automated testing |

## 4. System Architecture

The application follows a modular architecture.

- `app.py`: Streamlit interface.
- `career_agent.py`: Coordinates career analysis.
- `models.py`: Pydantic data models.
- `data_loader.py`: Loads local JSON data.
- `skill_engine.py`: Skill normalization and comparison.
- `recommendation_engine.py`: Career scoring and ranking.
- `roadmap_engine.py`: Learning roadmap generation.

## 5. Main Features

### Student Profile Management
- Enter student name and degree.
- Add technical skills and proficiency levels.
- Specify interests, projects, and certifications.
- Set weekly learning hours and learning timeframe.

### Career Recommendations
- Rank technology career roles.
- Display the top three recommendations.
- Explain recommendation scores.

### Skill-Gap Analysis
- Identify matched skills.
- Identify partially matched skills.
- Identify missing skills.
- Compare current and target proficiency levels.

### Personalized Learning Roadmap
- Seven-day quick-start plan.
- Monthly learning objectives.
- Practical exercises.
- Measurable deliverables.
- Completion criteria.

### Career Resources
- Suggested hands-on projects.
- Optional certifications.
- Downloadable Markdown career report.

## 6. Recommendation Scoring

The recommendation engine uses a weighted scoring approach.

| Component | Weight |
|---|---:|
| Skill Match | 50% |
| Interest Match | 20% |
| Project Match | 15% |
| Certification Match | 10% |
| Industry Match | 5% |

The final recommendation score is bounded between 0 and 100.

These scores represent career-learning suitability, not employment probabilities.

## 7. Installation

Clone the repository:

```bash
git clone https://github.com/Harshitha119/-career-development-agent.git
cd -career-development-agent
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```cmd
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 8. Run the Application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal.

## 9. Run Automated Tests

```bash
pytest -q
```

Current test result:

```text
15 passed
```

## 10. Screenshots

Application screenshots will be added here.

## 11. Reliability

- Uses local JSON datasets.
- Does not require external API keys.
- Uses Pydantic for input validation.
- Uses deterministic recommendation and roadmap logic.
- Includes automated tests.

## 12. Future Enhancements

- Integration with real-time job-market information.
- More detailed student progress tracking.
- Additional technology career paths.
- Advanced skill assessment.
- Personalized project difficulty recommendations.

## Author

Career Development Agent Project
