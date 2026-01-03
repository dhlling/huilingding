"""Tests for the Essay Workshop module."""

import pytest
from datetime import datetime

from src.modules.essay import (
    EssayWorkshopModule,
    StoryElement,
    PersonalNarrative,
    EssayOutline,
    EssayDraft,
    DetailedFeedback,
    EssayStrategy,
)
from src.core.models import Essay
from src.core.enums import EssayType
from tests.conftest import MockAIEngine


class TestEssayWorkshopModule:
    """Tests for EssayWorkshopModule."""

    @pytest.fixture
    def essay_module(self, mock_ai_engine):
        """Create an essay module for testing."""
        return EssayWorkshopModule(mock_ai_engine)

    def test_module_properties(self, essay_module):
        """Test module name and description."""
        assert essay_module.name == "Essay Development Workshop"
        assert "essay" in essay_module.description.lower()

    @pytest.mark.asyncio
    async def test_module_initialization(self, essay_module):
        """Test module can be initialized."""
        await essay_module.initialize()
        assert essay_module._initialized is True


class TestStoryElement:
    """Tests for StoryElement model."""

    def test_create_story_element(self):
        """Test creating a story element."""
        element = StoryElement(
            title="Learning to code at age 12",
            description="My journey into programming started with building a simple game",
            emotional_core="Discovery and passion",
            potential_themes=["perseverance", "curiosity", "self-directed learning"],
            essay_types_fit=[EssayType.COMMON_APP_PERSONAL, EssayType.SUPPLEMENTAL],
            uniqueness_score=0.85,
        )
        assert element.title == "Learning to code at age 12"
        assert element.uniqueness_score == 0.85
        assert EssayType.COMMON_APP_PERSONAL in element.essay_types_fit


class TestPersonalNarrative:
    """Tests for PersonalNarrative model."""

    def test_create_personal_narrative(self):
        """Test creating a personal narrative."""
        story = StoryElement(
            title="Test Story",
            description="Description",
            emotional_core="Core",
            potential_themes=["theme1"],
            essay_types_fit=[EssayType.COMMON_APP_PERSONAL],
            uniqueness_score=0.8,
        )
        narrative = PersonalNarrative(
            core_values=["integrity", "curiosity", "empathy"],
            defining_moments=[story],
            unique_perspectives=["First-gen tech entrepreneur in family"],
            growth_stories=[story],
            passions=["technology", "education access"],
            challenges_overcome=[story],
            recommended_main_essay_topic=story,
            backup_topics=[story],
        )
        assert "integrity" in narrative.core_values
        assert narrative.recommended_main_essay_topic is not None


class TestEssayOutline:
    """Tests for EssayOutline model."""

    def test_create_essay_outline(self):
        """Test creating an essay outline."""
        outline = EssayOutline(
            essay_type=EssayType.COMMON_APP_PERSONAL,
            prompt="Some students have a background, identity, interest, or talent...",
            thesis_statement="My journey with robotics shaped my understanding of failure",
            opening_hook="The robot's arm fell off during the state championship",
            main_points=[
                "Initial failure and disappointment",
                "Learning to iterate and improve",
                "Applying lessons beyond robotics",
            ],
            supporting_details={
                "Initial failure": ["The moment of failure", "Team reaction"],
                "Learning": ["Research phase", "Mentor guidance"],
            },
            conclusion_direction="Connect to future goals in engineering",
            word_target=650,
        )
        assert outline.essay_type == EssayType.COMMON_APP_PERSONAL
        assert outline.word_target == 650


class TestEssayDraft:
    """Tests for EssayDraft model."""

    def test_create_essay_draft(self):
        """Test creating an essay draft."""
        draft = EssayDraft(
            id="draft-001",
            essay_id="essay-001",
            version=1,
            content="My journey began on a cold November morning...",
            word_count=450,
            created_at=datetime.now(),
            notes="First draft - focus on narrative flow",
        )
        assert draft.version == 1
        assert draft.word_count == 450


class TestDetailedFeedback:
    """Tests for DetailedFeedback model."""

    def test_create_detailed_feedback(self):
        """Test creating detailed feedback."""
        feedback = DetailedFeedback(
            essay_id="essay-001",
            overall_score=82.5,
            category_scores={
                "narrative": 85,
                "authenticity": 90,
                "writing_quality": 75,
                "theme_clarity": 80,
            },
            strengths=[
                "Strong opening hook",
                "Authentic voice",
                "Clear growth narrative",
            ],
            areas_for_improvement=[
                "Conclusion could be stronger",
                "Some transitions are abrupt",
            ],
            line_by_line_suggestions=[
                {"line": 5, "suggestion": "Consider stronger verb here"},
            ],
            revised_sentences=[
                {"original": "I was happy", "revised": "Joy overwhelmed me"},
            ],
            authenticity_analysis="Voice feels genuine and personal",
            admissions_officer_perspective="Would stand out for its unique perspective",
            next_steps=["Revise conclusion", "Polish transitions"],
        )
        assert feedback.overall_score == 82.5
        assert len(feedback.strengths) == 3


class TestEssayStrategy:
    """Tests for EssayStrategy model."""

    def test_create_essay_strategy(self):
        """Test creating an essay strategy."""
        strategy = EssayStrategy(
            student_id="student-001",
            main_essay_topic="Robotics failure and growth",
            main_essay_theme="Learning from failure",
            supplemental_themes=[
                "Community impact",
                "Intellectual curiosity",
                "Leadership development",
            ],
            topics_to_avoid_repeating=[
                "robotics",
                "failure",
            ],
            schools_requiring_unique_content=["MIT", "Stanford", "CMU"],
            essay_calendar=[
                {"deadline": "Nov 1", "essays": "Stanford EA"},
                {"deadline": "Jan 1", "essays": "MIT, CMU"},
            ],
        )
        assert strategy.main_essay_theme == "Learning from failure"
        assert "MIT" in strategy.schools_requiring_unique_content
