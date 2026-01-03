"""Tests for core data models."""

import pytest
from datetime import date, datetime
from src.core.models import (
    PersonalInfo,
    FamilyContext,
    Interest,
    TestScore,
    Course,
    AcademicRecord,
    Activity,
    Competition,
    SummerProgram,
    Student,
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
    CompetitionType,
    ProgramType,
)


class TestPersonalInfo:
    """Tests for PersonalInfo model."""

    def test_create_personal_info(self, sample_personal_info):
        """Test creating PersonalInfo."""
        assert sample_personal_info.first_name == "Jane"
        assert sample_personal_info.last_name == "Doe"
        assert sample_personal_info.email == "jane.doe@example.com"

    def test_full_name_computed(self, sample_personal_info):
        """Test full_name computed property."""
        assert sample_personal_info.full_name == "Jane Doe"

    def test_default_values(self):
        """Test default values are set correctly."""
        info = PersonalInfo(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            date_of_birth=date(2008, 1, 1),
            high_school="Test High",
            graduation_year=2026,
            state="NY",
        )
        assert info.country == "USA"
        assert info.first_generation is False
        assert info.international_student is False


class TestTestScore:
    """Tests for TestScore model."""

    def test_create_test_score(self):
        """Test creating a test score."""
        score = TestScore(
            test_type=TestType.SAT,
            score=1500,
            max_score=1600,
            date_taken=date(2025, 6, 15),
        )
        assert score.score == 1500
        assert score.max_score == 1600

    def test_percentile_calculation(self):
        """Test percentile computed property."""
        score = TestScore(
            test_type=TestType.SAT,
            score=1200,
            max_score=1600,
            date_taken=date(2025, 6, 15),
        )
        assert score.percentile == 75.0

    def test_perfect_score_percentile(self):
        """Test percentile for perfect score."""
        score = TestScore(
            test_type=TestType.ACT,
            score=36,
            max_score=36,
            date_taken=date(2025, 6, 15),
        )
        assert score.percentile == 100.0


class TestCourse:
    """Tests for Course model."""

    def test_create_course(self):
        """Test creating a course."""
        course = Course(
            name="AP Calculus BC",
            subject_area=SubjectArea.MATHEMATICS,
            level="AP",
            grade="A",
            credits=1.0,
            grade_level=GradeLevel.JUNIOR,
            semester="Full Year",
        )
        assert course.name == "AP Calculus BC"
        assert course.level == "AP"
        assert course.credits == 1.0

    def test_course_without_grade(self):
        """Test course can be created without grade (in progress)."""
        course = Course(
            name="AP Physics C",
            subject_area=SubjectArea.PHYSICS,
            level="AP",
            grade_level=GradeLevel.SENIOR,
            semester="Fall",
        )
        assert course.grade is None


class TestAcademicRecord:
    """Tests for AcademicRecord model."""

    def test_empty_academic_record(self):
        """Test creating empty academic record."""
        record = AcademicRecord()
        assert record.courses == []
        assert record.test_scores == []
        assert record.cumulative_gpa == 0.0

    def test_rank_percentile_calculation(self):
        """Test rank percentile computation."""
        record = AcademicRecord(
            class_rank=10,
            class_size=100,
        )
        # (100 - 10) / 100 * 100 = 90
        assert record.rank_percentile == 90.0

    def test_rank_percentile_without_data(self):
        """Test rank percentile when data is missing."""
        record = AcademicRecord()
        assert record.rank_percentile is None


class TestActivity:
    """Tests for Activity model."""

    def test_create_activity(self, sample_activity):
        """Test creating an activity."""
        assert sample_activity.name == "Robotics Club"
        assert sample_activity.category == ActivityCategory.CLUB
        assert sample_activity.is_primary is True

    def test_total_hours_calculation(self, sample_activity):
        """Test total hours computed property."""
        # 10 hours/week * 40 weeks/year * 3 years = 1200 hours
        assert sample_activity.total_hours == 1200


class TestCompetition:
    """Tests for Competition model."""

    def test_create_competition(self):
        """Test creating a competition entry."""
        competition = Competition(
            id="comp-001",
            name="USACO",
            competition_type=CompetitionType.INFORMATICS_OLYMPIAD,
            year=2024,
            level_achieved=AchievementLevel.NATIONAL,
            award="Gold Division",
            description="USA Computing Olympiad",
        )
        assert competition.level_achieved == AchievementLevel.NATIONAL


class TestSummerProgram:
    """Tests for SummerProgram model."""

    def test_create_summer_program(self):
        """Test creating a summer program."""
        program = SummerProgram(
            id="program-001",
            name="Stanford AI4ALL",
            program_type=ProgramType.PRE_COLLEGE,
            institution="Stanford University",
            year=2025,
            duration_weeks=3,
            description="AI program for high school students",
            selective=True,
            paid=False,
        )
        assert program.selective is True
        assert program.institution == "Stanford University"


class TestStudent:
    """Tests for Student model."""

    def test_create_student(self, sample_student):
        """Test creating a student."""
        assert sample_student.id == "test-student-001"
        assert sample_student.personal_info.full_name == "Jane Doe"

    def test_primary_interests(self, sample_student):
        """Test primary_interests computed property."""
        primary = sample_student.primary_interests
        assert SubjectArea.COMPUTER_SCIENCE in primary
        assert SubjectArea.MATHEMATICS in primary

    def test_student_timestamps(self, sample_student):
        """Test timestamps are set."""
        assert sample_student.created_at is not None
        assert sample_student.updated_at is not None


class TestCollege:
    """Tests for College model."""

    def test_create_college(self, sample_college):
        """Test creating a college."""
        assert sample_college.name == "Tech University"
        assert sample_college.size == 15000

    def test_admission_stats(self, sample_college):
        """Test admission stats are accessible."""
        assert sample_college.admission_stats.acceptance_rate == 0.15
        assert sample_college.admission_stats.sat_avg == 1500

    def test_financial_info(self, sample_college):
        """Test financial info is accessible."""
        assert sample_college.financial_info.meets_full_need is True


class TestApplication:
    """Tests for Application model."""

    def test_create_application(self, sample_application):
        """Test creating an application."""
        assert sample_application.status == ApplicationStatus.IN_PROGRESS
        assert sample_application.tier == CollegeTier.REACH

    def test_days_until_deadline(self, sample_application):
        """Test days_until_deadline computation."""
        # This will vary based on current date
        days = sample_application.days_until_deadline
        assert isinstance(days, int)

    def test_is_complete_property(self, sample_application):
        """Test is_complete computed property."""
        # Essays not final, so should be incomplete
        assert sample_application.is_complete is False


class TestEssay:
    """Tests for Essay model."""

    def test_create_essay(self, sample_essay):
        """Test creating an essay."""
        assert sample_essay.essay_type == EssayType.COMMON_APP_PERSONAL
        assert sample_essay.word_limit == 650
        assert sample_essay.status == "drafting"

    def test_essay_drafts(self, sample_essay):
        """Test essay has drafts."""
        assert len(sample_essay.drafts) == 2


class TestTimeline:
    """Tests for Timeline model."""

    def test_create_timeline(self, sample_timeline):
        """Test creating a timeline."""
        assert len(sample_timeline.milestones) == 2

    def test_get_upcoming_milestones(self, sample_timeline):
        """Test getting upcoming milestones."""
        # Modify to have near-future deadline for testing
        from datetime import timedelta
        sample_timeline.milestones[0].due_date = date.today() + timedelta(days=7)
        upcoming = sample_timeline.get_upcoming(days=30)
        assert len(upcoming) >= 1

    def test_get_overdue_milestones(self, sample_timeline):
        """Test getting overdue milestones."""
        from datetime import timedelta
        sample_timeline.milestones[0].due_date = date.today() - timedelta(days=7)
        sample_timeline.milestones[0].completed = False
        overdue = sample_timeline.get_overdue()
        assert len(overdue) >= 1


class TestMilestone:
    """Tests for Milestone model."""

    def test_create_milestone(self):
        """Test creating a milestone."""
        milestone = Milestone(
            id="m-001",
            title="Complete SAT",
            description="Take the SAT exam",
            category=MilestoneCategory.TESTING,
            grade_level=GradeLevel.JUNIOR,
            due_date=date(2025, 10, 15),
            priority=1,
        )
        assert milestone.completed is False
        assert milestone.priority == 1

    def test_milestone_completion(self):
        """Test marking milestone as complete."""
        milestone = Milestone(
            id="m-002",
            title="Test",
            description="Test milestone",
            category=MilestoneCategory.ACADEMIC,
            grade_level=GradeLevel.JUNIOR,
            completed=True,
            completed_date=date.today(),
        )
        assert milestone.completed is True
        assert milestone.completed_date == date.today()
