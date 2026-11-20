# Career Development Agent

## Overview

The Career Development Agent is a Python-based application that helps students explore technology career paths based on their skills, interests, existing projects, and learning goals.

It provides career recommendations, skill-gap analysis, and a structured learning roadmap using locally stored data.

## Technologies Used

- Python 3.11+
- Streamlit
- Plotly
- Pydantic
- Pytest
- JSON

## Project Structure

```text
career-development-agent/
├── app.py
├── career_agent.py
├── models.py
├── data_loader.py
├── skill_engine.py
├── recommendation_engine.py
├── roadmap_engine.py
├── career_roles.json
├── students.json
├── requirements.txt
├── README.md
├── tests/
│   ├── conftest.py
│   ├── test_starter.py
│   ├── test_skill_engine.py
│   ├── test_recommendation_engine.py
│   └── test_roadmap_engine.py
└── .cursor/
    ├── rules/
    └── skills/
        └── career-advisor/
            └── SKILL.md
```

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows Command Prompt:

```cmd
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal.

## Run Automated Tests

```bash
pytest -q
```

## Sample Student Profile

The project includes a sample student profile named Harsha.

- Degree: B.Tech Computer Science
- Python: 7/10
- Cloud: 5/10
- Kubernetes: 3/10
- AI/LLM: 4/10
- Interests: Cloud and AI
- Existing project: Chatbot
- Learning availability: 8 hours per week

## Recommendation Scoring

The recommendation engine uses these weighted components:

| Component | Weight |
|---|---:|
| Skill Match | 50% |
| Interest Match | 20% |
| Project Match | 15% |
| Certification Match | 10% |
| Industry Match | 5% |

Scores represent learning recommendations, not probabilities of employment.

## Main Features

- Local student and career-role data loading
- Skill-name normalization
- Career recommendation and ranking
- Skill-gap analysis
- Learning roadmap generation
- Visual skill comparison
- Downloadable Markdown report
- Automated tests

## Reliability

The application uses local JSON data and does not require external API keys or external career-service integrations.

## Testing Result

The current automated test suite passes:

```text
15 passed
```

## Purpose

The goal is to help students understand their current skill levels, identify relevant career paths, and plan practical learning activities.
