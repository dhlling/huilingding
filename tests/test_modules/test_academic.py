"""Tests for the Academic Planning module."""

import pytest
from datetime import date

from src.modules.academic import (
    AcademicPlanningModule,
    CourseSequence,
    YearlyCoursePlan,
    FourYearPlan,
    GPAProjection,
    CourseLoadAnalysis,
)
from src.core.models import Student, Course
from src.core.enums import GradeLevel, SubjectArea
from tests.conftest import MockAIEngine


class TestAcademicPlanningModule:
    """Tests for AcademicPlanningModule."""

    @pytest.fixture
    def academic_module(self, mock_ai_engine):
        """Create an academic module for testing."""
        return AcademicPlanningModule(mock_ai_engine)

    def test_module_properties(self, academic_module):
        """Test module name and description."""
        assert academic_module.name == "Academic Planning System"
        assert "course" in academic_module.description.lower()

    def test_graduation_requirements_defined(self, academic_module):
        """Test graduation requirements are properly defined."""
        reqs = academic_module.GRADUATION_REQUIREMENTS
        assert "english" in reqs
        assert "mathematics" in reqs
        assert reqs["english"] == 4
        assert reqs["mathematics"] == 4

    def test_ap_courses_defined(self, academic_module):
        """Test AP course lists are defined."""
        ap_courses = academic_module.AP_COURSES
        assert SubjectArea.MATHEMATICS in ap_courses
        assert "AP Calculus BC" in ap_courses[SubjectArea.MATHEMATICS]

    @pytest.mark.asyncio
    async def test_module_initialization(self, academic_module):
        """Test module can be initialized."""
        await academic_module.initialize()
        assert academic_module._initialized is True

    @pytest.mark.asyncio
    async def test_ensure_initialized_raises_error(self, academic_module):
        """Test that using module without initialization raises error."""
        with pytest.raises(RuntimeError, match="not initialized"):
            academic_module.ensure_initialized()


class TestCourseSequence:
    """Tests for CourseSequence model."""

    def test_create_course_sequence(self):
        """Test creating a course sequence."""
        sequence = CourseSequence(
            subject_area=SubjectArea.MATHEMATICS,
            courses=["Algebra 1", "Geometry", "Algebra 2", "Pre-Calculus", "AP Calculus BC"],
            rationale="Standard math progression for advanced students",
            ap_ib_options=["AP Calculus AB", "AP Calculus BC", "AP Statistics"],
            prerequisites={"AP Calculus BC": ["Pre-Calculus"]},
        )
        assert sequence.subject_area == SubjectArea.MATHEMATICS
        assert len(sequence.courses) == 5


class TestYearlyCoursePlan:
    """Tests for YearlyCoursePlan model."""

    def test_create_yearly_plan(self):
        """Test creating a yearly course plan."""
        from src.core.models import CourseRecommendation

        plan = YearlyCoursePlan(
            grade_level=GradeLevel.JUNIOR,
            fall_courses=[],
            spring_courses=[],
            total_credits=7.0,
            ap_ib_count=3,
            notes="Rigorous schedule for college prep",
        )
        assert plan.grade_level == GradeLevel.JUNIOR
        assert plan.ap_ib_count == 3


class TestGPAProjection:
    """Tests for GPAProjection model."""

    def test_create_gpa_projection(self):
        """Test creating a GPA projection."""
        projection = GPAProjection(
            current_gpa=3.7,
            projected_gpa_end_of_year=3.8,
            projected_gpa_graduation=3.85,
            gpa_by_semester=[
                {"semester": "Fall Junior", "gpa": 3.8},
                {"semester": "Spring Junior", "gpa": 3.9},
            ],
            improvement_recommendations=["Focus on writing skills"],
            at_risk_courses=["AP English Literature"],
        )
        assert projection.current_gpa == 3.7
        assert projection.projected_gpa_graduation > projection.current_gpa


class TestCourseLoadAnalysis:
    """Tests for CourseLoadAnalysis model."""

    def test_create_course_load_analysis(self):
        """Test creating a course load analysis."""
        analysis = CourseLoadAnalysis(
            total_courses=7,
            honors_ap_ib_count=4,
            workload_level="Heavy",
            balance_score=7.5,
            subject_balance={
                "STEM": 4,
                "Humanities": 2,
                "Arts": 1,
            },
            recommendations=["Consider dropping one AP if overwhelmed"],
            warnings=["Very heavy course load - monitor stress levels"],
        )
        assert analysis.workload_level == "Heavy"
        assert len(analysis.warnings) > 0
