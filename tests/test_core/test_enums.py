"""Tests for core enumerations."""

import pytest
from src.core.enums import (
    GradeLevel,
    ActivityCategory,
    AchievementLevel,
    ApplicationStatus,
    CollegeType,
    CollegeTier,
    SubjectArea,
    TestType,
    EssayType,
    InterestLevel,
    ProgramType,
    FinancialNeedLevel,
    MilestoneCategory,
    CompetitionType,
    RecommendationType,
)


class TestGradeLevel:
    """Tests for GradeLevel enum."""

    def test_grade_level_values(self):
        """Test that all grade levels have correct values."""
        assert GradeLevel.FRESHMAN.value == "freshman"
        assert GradeLevel.SOPHOMORE.value == "sophomore"
        assert GradeLevel.JUNIOR.value == "junior"
        assert GradeLevel.SENIOR.value == "senior"

    def test_year_number_property(self):
        """Test year_number property returns correct grade number."""
        assert GradeLevel.FRESHMAN.year_number == 9
        assert GradeLevel.SOPHOMORE.year_number == 10
        assert GradeLevel.JUNIOR.year_number == 11
        assert GradeLevel.SENIOR.year_number == 12

    def test_grade_level_is_string_enum(self):
        """Test that GradeLevel values can be used as strings."""
        assert str(GradeLevel.JUNIOR) == "GradeLevel.JUNIOR"
        assert GradeLevel.JUNIOR.value == "junior"


class TestActivityCategory:
    """Tests for ActivityCategory enum."""

    def test_all_categories_exist(self):
        """Test all expected activity categories are defined."""
        expected = [
            "academic", "arts", "athletics", "community_service",
            "leadership", "work_experience", "research", "competition",
            "club", "personal_project"
        ]
        actual = [c.value for c in ActivityCategory]
        assert set(expected) == set(actual)

    def test_category_membership(self):
        """Test checking category membership."""
        assert ActivityCategory.RESEARCH in ActivityCategory
        assert "research" not in ActivityCategory  # String not in enum


class TestAchievementLevel:
    """Tests for AchievementLevel enum."""

    def test_achievement_level_ordering(self):
        """Test that achievement levels are properly defined."""
        levels = list(AchievementLevel)
        values = [l.value for l in levels]
        expected_order = [
            "participant", "school_level", "regional",
            "state", "national", "international"
        ]
        assert values == expected_order


class TestApplicationStatus:
    """Tests for ApplicationStatus enum."""

    def test_all_statuses_exist(self):
        """Test all application statuses are defined."""
        statuses = [s.value for s in ApplicationStatus]
        assert "not_started" in statuses
        assert "submitted" in statuses
        assert "accepted" in statuses
        assert "rejected" in statuses
        assert "waitlisted" in statuses

    def test_status_transitions_are_valid(self):
        """Test that common status values are correct."""
        assert ApplicationStatus.NOT_STARTED.value == "not_started"
        assert ApplicationStatus.IN_PROGRESS.value == "in_progress"
        assert ApplicationStatus.SUBMITTED.value == "submitted"


class TestCollegeTier:
    """Tests for CollegeTier enum."""

    def test_tier_values(self):
        """Test college tier values."""
        assert CollegeTier.REACH.value == "reach"
        assert CollegeTier.TARGET.value == "target"
        assert CollegeTier.LIKELY.value == "likely"

    def test_tier_count(self):
        """Test there are exactly 3 tiers."""
        assert len(CollegeTier) == 3


class TestSubjectArea:
    """Tests for SubjectArea enum."""

    def test_core_subjects_exist(self):
        """Test core academic subjects are defined."""
        subjects = [s.value for s in SubjectArea]
        core = ["mathematics", "physics", "chemistry", "biology",
                "computer_science", "english", "history"]
        for subj in core:
            assert subj in subjects

    def test_stem_subjects(self):
        """Test STEM subjects are properly defined."""
        stem = [
            SubjectArea.MATHEMATICS,
            SubjectArea.PHYSICS,
            SubjectArea.CHEMISTRY,
            SubjectArea.BIOLOGY,
            SubjectArea.COMPUTER_SCIENCE,
            SubjectArea.ENGINEERING,
        ]
        for subj in stem:
            assert subj in SubjectArea


class TestTestType:
    """Tests for TestType enum."""

    def test_standardized_tests(self):
        """Test standardized test types are defined."""
        assert TestType.SAT.value == "sat"
        assert TestType.ACT.value == "act"
        assert TestType.PSAT.value == "psat"
        assert TestType.AP.value == "ap"

    def test_english_proficiency_tests(self):
        """Test English proficiency tests are defined."""
        assert TestType.TOEFL.value == "toefl"
        assert TestType.IELTS.value == "ielts"


class TestEssayType:
    """Tests for EssayType enum."""

    def test_essay_types(self):
        """Test essay types are defined."""
        types = [e.value for e in EssayType]
        assert "common_app_personal" in types
        assert "supplemental" in types
        assert "why_us" in types


class TestInterestLevel:
    """Tests for InterestLevel enum."""

    def test_interest_level_progression(self):
        """Test interest levels represent progression."""
        levels = [l.value for l in InterestLevel]
        expected = ["exploring", "interested", "passionate", "committed"]
        assert levels == expected


class TestFinancialNeedLevel:
    """Tests for FinancialNeedLevel enum."""

    def test_financial_need_levels(self):
        """Test financial need levels are defined."""
        assert FinancialNeedLevel.FULL_PAY.value == "full_pay"
        assert FinancialNeedLevel.FULL_AID.value == "full_aid"
        assert len(FinancialNeedLevel) == 4
