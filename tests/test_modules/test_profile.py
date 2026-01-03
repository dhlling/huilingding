"""Tests for the Student Profile module."""

import pytest
from datetime import date, datetime

from src.modules.profile import (
    StudentProfileModule,
    PersonalityProfile,
    InterestInventory,
    AcademicAssessment,
    GoalFramework,
    ProfileAssessmentResult,
)
from src.core.enums import (
    SubjectArea,
    TestType,
    GradeLevel,
    InterestLevel,
    FinancialNeedLevel,
)
from tests.conftest import MockAIEngine


class TestStudentProfileModule:
    """Tests for StudentProfileModule."""

    @pytest.fixture
    def profile_module(self, mock_ai_engine):
        """Create a profile module for testing."""
        return StudentProfileModule(mock_ai_engine)

    @pytest.mark.asyncio
    async def test_module_properties(self, profile_module):
        """Test module name and description."""
        assert profile_module.name == "Student Profile & Assessment Engine"
        assert "profiling" in profile_module.description.lower()

    @pytest.mark.asyncio
    async def test_create_profile(self, profile_module):
        """Test creating a student profile."""
        student = await profile_module.create_profile(
            first_name="John",
            last_name="Smith",
            email="john.smith@example.com",
            date_of_birth=date(2008, 3, 20),
            high_school="Central High School",
            graduation_year=2026,
            state="TX",
        )

        assert student is not None
        assert student.personal_info.first_name == "John"
        assert student.personal_info.last_name == "Smith"
        assert student.personal_info.full_name == "John Smith"
        assert student.personal_info.graduation_year == 2026
        assert student.id is not None

    @pytest.mark.asyncio
    async def test_get_student(self, profile_module):
        """Test retrieving a student profile."""
        student = await profile_module.create_profile(
            first_name="Alice",
            last_name="Johnson",
            email="alice@example.com",
            date_of_birth=date(2008, 7, 10),
            high_school="West High",
            graduation_year=2026,
            state="CA",
        )

        retrieved = await profile_module.get_student(student.id)
        assert retrieved is not None
        assert retrieved.id == student.id
        assert retrieved.personal_info.first_name == "Alice"

    @pytest.mark.asyncio
    async def test_get_nonexistent_student(self, profile_module):
        """Test getting a student that doesn't exist."""
        result = await profile_module.get_student("nonexistent-id")
        assert result is None

    @pytest.mark.asyncio
    async def test_update_family_context(self, profile_module):
        """Test updating family context."""
        student = await profile_module.create_profile(
            first_name="Bob",
            last_name="Brown",
            email="bob@example.com",
            date_of_birth=date(2008, 1, 15),
            high_school="East High",
            graduation_year=2026,
            state="NY",
        )

        updated = await profile_module.update_family_context(
            student_id=student.id,
            parent_education="Master's degree",
            income_bracket="$150k+",
            first_generation=False,
            legacy_schools=["Harvard", "Yale"],
            geographic_preferences=["Northeast", "California"],
            financial_need=FinancialNeedLevel.PARTIAL_AID,
        )

        assert updated.family_context.parent_education_level == "Master's degree"
        assert "Harvard" in updated.family_context.legacy_schools
        assert updated.family_context.financial_need == FinancialNeedLevel.PARTIAL_AID

    @pytest.mark.asyncio
    async def test_update_family_context_invalid_student(self, profile_module):
        """Test updating family context for non-existent student."""
        with pytest.raises(ValueError, match="not found"):
            await profile_module.update_family_context(
                student_id="invalid-id",
                parent_education="Bachelor's",
            )

    @pytest.mark.asyncio
    async def test_add_test_score(self, profile_module):
        """Test adding a test score."""
        student = await profile_module.create_profile(
            first_name="Carol",
            last_name="Davis",
            email="carol@example.com",
            date_of_birth=date(2008, 5, 5),
            high_school="North High",
            graduation_year=2026,
            state="FL",
        )

        updated = await profile_module.add_test_score(
            student_id=student.id,
            test_type=TestType.SAT,
            score=1480,
            max_score=1600,
            date_taken=date(2025, 3, 15),
        )

        assert len(updated.academic_record.test_scores) == 1
        assert updated.academic_record.test_scores[0].score == 1480
        assert updated.academic_record.test_scores[0].test_type == TestType.SAT

    @pytest.mark.asyncio
    async def test_add_course(self, profile_module):
        """Test adding a course."""
        student = await profile_module.create_profile(
            first_name="Dan",
            last_name="Evans",
            email="dan@example.com",
            date_of_birth=date(2008, 9, 1),
            high_school="South High",
            graduation_year=2026,
            state="WA",
        )

        updated = await profile_module.add_course(
            student_id=student.id,
            name="AP Chemistry",
            subject_area=SubjectArea.CHEMISTRY,
            level="AP",
            grade_level=GradeLevel.JUNIOR,
            semester="Full Year",
            grade="A",
            credits=1.0,
        )

        assert len(updated.academic_record.courses) == 1
        assert updated.academic_record.courses[0].name == "AP Chemistry"
        assert updated.academic_record.courses[0].level == "AP"

    @pytest.mark.asyncio
    async def test_add_interest(self, profile_module):
        """Test adding an interest."""
        student = await profile_module.create_profile(
            first_name="Eve",
            last_name="Foster",
            email="eve@example.com",
            date_of_birth=date(2008, 11, 20),
            high_school="Central High",
            graduation_year=2026,
            state="CO",
        )

        updated = await profile_module.add_interest(
            student_id=student.id,
            area=SubjectArea.PHYSICS,
            level=InterestLevel.PASSIONATE,
            years_of_engagement=3,
            notes="Loves physics problems",
        )

        assert len(updated.interests) == 1
        assert updated.interests[0].area == SubjectArea.PHYSICS
        assert updated.interests[0].level == InterestLevel.PASSIONATE

    @pytest.mark.asyncio
    async def test_conduct_interest_inventory(self, profile_module):
        """Test conducting interest inventory assessment."""
        student = await profile_module.create_profile(
            first_name="Frank",
            last_name="Garcia",
            email="frank@example.com",
            date_of_birth=date(2008, 2, 28),
            high_school="Valley High",
            graduation_year=2026,
            state="AZ",
        )

        responses = {
            "favorite_subjects": ["Math", "Computer Science"],
            "hobbies": ["Programming", "Chess"],
            "dream_career": "Software Engineer",
        }

        result = await profile_module.conduct_interest_inventory(
            student_id=student.id,
            responses=responses,
        )

        assert isinstance(result, InterestInventory)
        assert len(result.top_academic_interests) > 0

    @pytest.mark.asyncio
    async def test_assess_personality(self, profile_module):
        """Test personality assessment."""
        student = await profile_module.create_profile(
            first_name="Grace",
            last_name="Harris",
            email="grace@example.com",
            date_of_birth=date(2008, 4, 12),
            high_school="Hill High",
            graduation_year=2026,
            state="OR",
        )

        responses = {
            "work_preference": "I prefer working in groups",
            "learning_style": "I learn best by seeing diagrams",
            "stress_response": "I work well under pressure",
        }

        result = await profile_module.assess_personality(
            student_id=student.id,
            questionnaire_responses=responses,
        )

        assert isinstance(result, PersonalityProfile)
        assert result.work_style is not None
        assert result.learning_style is not None

    @pytest.mark.asyncio
    async def test_assess_academics(self, profile_module):
        """Test academic assessment."""
        student = await profile_module.create_profile(
            first_name="Henry",
            last_name="Irwin",
            email="henry@example.com",
            date_of_birth=date(2008, 6, 30),
            high_school="Lake High",
            graduation_year=2026,
            state="MI",
        )

        # Add some courses and scores first
        await profile_module.add_course(
            student_id=student.id,
            name="AP Calculus AB",
            subject_area=SubjectArea.MATHEMATICS,
            level="AP",
            grade_level=GradeLevel.JUNIOR,
            semester="Full Year",
            grade="A",
        )

        await profile_module.add_test_score(
            student_id=student.id,
            test_type=TestType.PSAT,
            score=1400,
            max_score=1520,
            date_taken=date(2024, 10, 15),
        )

        result = await profile_module.assess_academics(student_id=student.id)

        assert isinstance(result, AcademicAssessment)
        assert len(result.strong_subjects) > 0

    @pytest.mark.asyncio
    async def test_set_goals(self, profile_module):
        """Test goal setting."""
        student = await profile_module.create_profile(
            first_name="Ivy",
            last_name="Jones",
            email="ivy@example.com",
            date_of_birth=date(2008, 8, 8),
            high_school="River High",
            graduation_year=2026,
            state="GA",
        )

        result = await profile_module.set_goals(
            student_id=student.id,
            dream_schools=["MIT", "Caltech", "Stanford"],
            intended_majors=["Computer Science", "Electrical Engineering"],
            career_aspirations=["Tech Entrepreneur", "AI Researcher"],
        )

        assert isinstance(result, GoalFramework)
        assert "MIT" in result.dream_schools
        assert "Computer Science" in result.intended_majors

    @pytest.mark.asyncio
    async def test_conduct_full_assessment(self, profile_module):
        """Test conducting full profile assessment."""
        student = await profile_module.create_profile(
            first_name="Jack",
            last_name="King",
            email="jack@example.com",
            date_of_birth=date(2008, 10, 10),
            high_school="Mountain High",
            graduation_year=2026,
            state="UT",
        )

        result = await profile_module.conduct_full_assessment(
            student_id=student.id,
            interest_responses={"favorite": "science"},
            personality_responses={"style": "visual"},
            goals={
                "dream_schools": ["Stanford"],
                "intended_majors": ["CS"],
                "career_aspirations": ["Engineer"],
            },
        )

        assert isinstance(result, ProfileAssessmentResult)
        assert result.personality is not None
        assert result.interests is not None
        assert result.academic is not None
        assert result.goals is not None
        assert len(result.initial_recommendations) > 0

    @pytest.mark.asyncio
    async def test_update_student(self, profile_module):
        """Test updating a student profile."""
        student = await profile_module.create_profile(
            first_name="Kate",
            last_name="Lee",
            email="kate@example.com",
            date_of_birth=date(2008, 12, 25),
            high_school="Ocean High",
            graduation_year=2026,
            state="HI",
        )

        original_updated_at = student.updated_at

        # Modify the student
        student.intended_majors = ["Biology", "Pre-Med"]

        import time
        time.sleep(0.01)  # Small delay to ensure time difference

        updated = await profile_module.update_student(student)

        assert updated.intended_majors == ["Biology", "Pre-Med"]
        assert updated.updated_at >= original_updated_at

    @pytest.mark.asyncio
    async def test_generate_profile_summary(self, profile_module):
        """Test generating a profile summary."""
        student = await profile_module.create_profile(
            first_name="Leo",
            last_name="Miller",
            email="leo@example.com",
            date_of_birth=date(2008, 7, 4),
            high_school="Star High",
            graduation_year=2026,
            state="NV",
        )

        summary = await profile_module.generate_profile_summary(student.id)

        assert isinstance(summary, str)
        assert len(summary) > 0
