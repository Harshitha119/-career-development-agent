"""Pydantic models for the Career Development Agent."""

from pydantic import BaseModel, Field


class Skill(BaseModel):
    """Student skill and proficiency."""

    name: str
    level: int = Field(ge=0, le=10)


class RoleSkill(BaseModel):
    """Required skill for a career role."""

    name: str
    importance_weight: float = Field(gt=0)
    target_beginner_proficiency: int = Field(ge=0, le=10)


class Student(BaseModel):
    """Student learning profile."""

    id: str = "student-1"
    name: str
    degree: str
    skills: list[Skill] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)
    existing_projects: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    weekly_learning_hours: float = Field(gt=0)
    learning_timeframe_months: int = Field(ge=1, le=24)


class CareerRole(BaseModel):
    """Technology career role information."""

    id: str
    title: str
    description: str
    interests: list[str] = Field(default_factory=list)
    industries: list[str] = Field(default_factory=list)
    required_skills: list[RoleSkill] = Field(default_factory=list)
    optional_certifications: list[str] = Field(default_factory=list)
    hands_on_projects: list[str] = Field(default_factory=list)
    six_month_learning_sequence: list[str] = Field(
        default_factory=list
    )


class SkillGap(BaseModel):
    """Comparison between current and target proficiency."""

    skill_name: str
    current_level: int = Field(ge=0, le=10)
    required_level: int = Field(ge=0, le=10)


class CareerRecommendation(BaseModel):
    """Career recommendation result."""

    role_id: str
    title: str
    score: float = Field(ge=0, le=100)
    reasons: list[str] = Field(default_factory=list)


class RoadmapStep(BaseModel):
    """One learning roadmap step."""

    order: int = Field(ge=1)
    title: str
    detail: str


class LearningRoadmap(BaseModel):
    """Generated learning roadmap."""

    role_id: str
    steps: list[RoadmapStep] = Field(default_factory=list)