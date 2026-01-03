"""Shared fixtures and configuration for tests."""

import pytest
from datetime import date, datetime
from typing import Any, TypeVar
from pydantic import BaseModel

from src.core.base import AIEngine
from src.core.models import (
    Student,
    PersonalInfo,
    FamilyContext,
    AcademicRecord,
    Course,
    TestScore,
    Activity,
    Interest,
    College,
    AdmissionStats,
    FinancialInfo,
    Application,
    Essay,
    Timeline,
    Milestone,
)
from src.core.enums import (
    GradeLevel,
    SubjectArea,
    TestType,
    InterestLevel,
    CollegeType,
    CollegeTier,
    ActivityCategory,
    AchievementLevel,
    EssayType,
    ApplicationStatus,
    MilestoneCategory,
    FinancialNeedLevel,
)


T = TypeVar("T", bound=BaseModel)


class MockAIEngine(AIEngine):
    """Mock AI engine for testing without actual API calls."""

    def __init__(self):
        self.call_history: list[dict[str, Any]] = []
        self.responses: dict[str, Any] = {}

    def set_response(self, method: str, response: Any) -> None:
        """Set a predefined response for a method."""
        self.responses[method] = response

    async def generate_text(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Generate mock text response."""
        self.call_history.append({
            "method": "generate_text",
            "prompt": prompt,
            "system_prompt": system_prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
        })
        return self.responses.get("generate_text", "Mock AI response for testing purposes.")

    async def generate_structured(
        self,
        prompt: str,
        response_model: type[T],
        system_prompt: str | None = None,
    ) -> T:
        """Generate mock structured response."""
        self.call_history.append({
            "method": "generate_structured",
            "prompt": prompt,
            "response_model": response_model.__name__,
            "system_prompt": system_prompt,
        })

        # Return predefined response or create mock data based on model
        if "generate_structured" in self.responses:
            return self.responses["generate_structured"]

        # Create default mock data for common models
        return self._create_mock_model(response_model)

    def _create_mock_model(self, model_class: type[T]) -> T:
        """Create a mock instance of a Pydantic model."""
        from src.modules.profile import (
            PersonalityProfile,
            InterestInventory,
            AcademicAssessment,
            GoalFramework,
        )
        from src.modules.academic import CourseRecommendationResult
        from src.modules.extracurricular import ActivityRecommendationResult
        from src.modules.college_research import CollegeMatch
        from src.modules.essay import EssayAnalysis

        mock_data = {
            PersonalityProfile: {
                "strengths": ["analytical thinking", "creativity", "perseverance"],
                "work_style": "Collaborative",
                "learning_style": "Visual",
                "risk_tolerance": "Moderate",
                "time_management": "Structured",
                "leadership_tendency": "Leader",
                "creativity_level": "Balanced",
                "stress_management": "Thrives under pressure",
            },
            InterestInventory: {
                "top_academic_interests": [SubjectArea.COMPUTER_SCIENCE, SubjectArea.MATHEMATICS],
                "career_clusters": ["Technology", "Engineering"],
                "activity_preferences": ["coding", "robotics"],
                "passion_areas": ["artificial intelligence", "game development"],
                "aversions": [],
            },
            AcademicAssessment: {
                "strong_subjects": [SubjectArea.MATHEMATICS, SubjectArea.PHYSICS],
                "developing_subjects": [SubjectArea.ENGLISH],
                "recommended_focus_areas": ["writing skills", "verbal communication"],
                "gpa_trajectory": "Improving",
                "course_rigor_assessment": "Strong rigor with AP courses",
                "testing_readiness": "Ready for SAT",
            },
            GoalFramework: {
                "dream_schools": ["MIT", "Stanford"],
                "intended_majors": ["Computer Science"],
                "career_aspirations": ["Software Engineer"],
                "short_term_goals": ["Improve GPA"],
                "medium_term_goals": ["Take SAT"],
                "long_term_goals": ["Get into top CS program"],
                "non_negotiables": ["Strong CS program"],
            },
        }

        if model_class in mock_data:
            return model_class(**mock_data[model_class])

        # For unknown models, raise an error to be explicit
        raise NotImplementedError(f"No mock data defined for {model_class.__name__}")

    async def analyze_essay(
        self,
        essay_content: str,
        prompt: str,
        criteria: list[str],
    ) -> dict[str, Any]:
        """Analyze an essay with mock feedback."""
        self.call_history.append({
            "method": "analyze_essay",
            "essay_content": essay_content[:100],
            "prompt": prompt,
            "criteria": criteria,
        })
        return self.responses.get("analyze_essay", {
            "overall_score": 85,
            "strengths": ["Clear narrative", "Strong voice"],
            "areas_for_improvement": ["Could use more specific examples"],
            "specific_suggestions": ["Add a concrete anecdote"],
            "theme_clarity": 0.9,
            "authenticity_score": 0.85,
        })

    async def chat(
        self,
        messages: list[dict[str, str]],
        system_prompt: str | None = None,
    ) -> str:
        """Have a mock conversation."""
        self.call_history.append({
            "method": "chat",
            "messages": messages,
            "system_prompt": system_prompt,
        })
        return self.responses.get("chat", "Mock chat response.")

    def reset(self) -> None:
        """Reset call history and responses."""
        self.call_history = []
        self.responses = {}


@pytest.fixture
def mock_ai_engine() -> MockAIEngine:
    """Provide a mock AI engine for testing."""
    return MockAIEngine()


@pytest.fixture
def sample_personal_info() -> PersonalInfo:
    """Create sample personal info for testing."""
    return PersonalInfo(
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        date_of_birth=date(2008, 5, 15),
        high_school="Springfield High School",
        graduation_year=2026,
        state="CA",
        country="USA",
    )


@pytest.fixture
def sample_student(sample_personal_info) -> Student:
    """Create a sample student for testing."""
    return Student(
        id="test-student-001",
        personal_info=sample_personal_info,
        family_context=FamilyContext(
            parent_education_level="Bachelor's degree",
            household_income_bracket="$100k-$150k",
            financial_need=FinancialNeedLevel.PARTIAL_AID,
        ),
        academic_record=AcademicRecord(
            cumulative_gpa=3.8,
            weighted_gpa=4.2,
            class_rank=15,
            class_size=300,
            courses=[
                Course(
                    name="AP Calculus BC",
                    subject_area=SubjectArea.MATHEMATICS,
                    level="AP",
                    grade="A",
                    credits=1.0,
                    grade_level=GradeLevel.JUNIOR,
                    semester="Full Year",
                ),
                Course(
                    name="AP Physics C",
                    subject_area=SubjectArea.PHYSICS,
                    level="AP",
                    grade="A-",
                    credits=1.0,
                    grade_level=GradeLevel.JUNIOR,
                    semester="Full Year",
                ),
                Course(
                    name="AP Computer Science A",
                    subject_area=SubjectArea.COMPUTER_SCIENCE,
                    level="AP",
                    grade="A",
                    credits=1.0,
                    grade_level=GradeLevel.JUNIOR,
                    semester="Full Year",
                ),
            ],
            test_scores=[
                TestScore(
                    test_type=TestType.PSAT,
                    score=1400,
                    max_score=1520,
                    date_taken=date(2024, 10, 15),
                ),
            ],
        ),
        interests=[
            Interest(
                area=SubjectArea.COMPUTER_SCIENCE,
                level=InterestLevel.PASSIONATE,
                years_of_engagement=4,
            ),
            Interest(
                area=SubjectArea.MATHEMATICS,
                level=InterestLevel.COMMITTED,
                years_of_engagement=3,
            ),
        ],
        intended_majors=["Computer Science", "Applied Mathematics"],
        career_interests=["Software Engineer", "Data Scientist"],
    )


@pytest.fixture
def sample_college() -> College:
    """Create a sample college for testing."""
    return College(
        id="test-college-001",
        name="Tech University",
        location="San Jose, CA",
        state="CA",
        college_type=CollegeType.RESEARCH_UNIVERSITY,
        size=15000,
        setting="Urban",
        admission_stats=AdmissionStats(
            acceptance_rate=0.15,
            avg_gpa=3.9,
            sat_avg=1500,
            act_avg=34,
        ),
        financial_info=FinancialInfo(
            tuition_in_state=15000,
            tuition_out_of_state=45000,
            room_and_board=18000,
            avg_financial_aid=30000,
            percent_receiving_aid=0.60,
            meets_full_need=True,
        ),
        application_deadlines={
            "EA": date(2025, 11, 1),
            "RD": date(2026, 1, 1),
        },
        essays_required=2,
        interview_offered=True,
    )


@pytest.fixture
def sample_activity() -> Activity:
    """Create a sample activity for testing."""
    return Activity(
        id="test-activity-001",
        name="Robotics Club",
        category=ActivityCategory.CLUB,
        description="Member and lead programmer of the school robotics team",
        position="Lead Programmer",
        organization="Springfield High Robotics",
        hours_per_week=10,
        weeks_per_year=40,
        years_participated=[GradeLevel.FRESHMAN, GradeLevel.SOPHOMORE, GradeLevel.JUNIOR],
        achievements=["State Championship 2nd Place", "Best Programming Award"],
        achievement_level=AchievementLevel.STATE,
        is_primary=True,
    )


@pytest.fixture
def sample_essay() -> Essay:
    """Create a sample essay for testing."""
    return Essay(
        id="test-essay-001",
        essay_type=EssayType.COMMON_APP_PERSONAL,
        prompt="Share a story about a challenge you've faced.",
        word_limit=650,
        content="My journey into robotics began when I was just twelve years old...",
        drafts=["First draft...", "Second draft..."],
        status="drafting",
        themes=["perseverance", "technology", "teamwork"],
    )


@pytest.fixture
def sample_application(sample_student, sample_college, sample_essay) -> Application:
    """Create a sample application for testing."""
    return Application(
        id="test-application-001",
        student_id=sample_student.id,
        college_id=sample_college.id,
        college_name=sample_college.name,
        tier=CollegeTier.REACH,
        application_type="EA",
        status=ApplicationStatus.IN_PROGRESS,
        deadline=date(2025, 11, 1),
        essays=[sample_essay],
    )


@pytest.fixture
def sample_timeline(sample_student) -> Timeline:
    """Create a sample timeline for testing."""
    return Timeline(
        student_id=sample_student.id,
        milestones=[
            Milestone(
                id="milestone-001",
                title="Take PSAT",
                description="Complete PSAT test",
                category=MilestoneCategory.TESTING,
                grade_level=GradeLevel.JUNIOR,
                due_date=date(2025, 10, 15),
                priority=1,
            ),
            Milestone(
                id="milestone-002",
                title="Submit Common App",
                description="Complete and submit Common Application",
                category=MilestoneCategory.APPLICATION,
                grade_level=GradeLevel.SENIOR,
                due_date=date(2025, 11, 1),
                priority=1,
            ),
        ],
    )
