"""Tests for all planning modules - basic functionality."""

import pytest

from src.modules import (
    StudentProfileModule,
    AcademicPlanningModule,
    ExtracurricularAdvisorModule,
    SummerProgramsModule,
    CollegeResearchModule,
    EssayWorkshopModule,
    ApplicationManagerModule,
    TimelineOrchestratorModule,
)
from tests.conftest import MockAIEngine


class TestAllModulesBasic:
    """Basic tests for all modules."""

    @pytest.fixture
    def mock_engine(self):
        """Create mock AI engine."""
        return MockAIEngine()

    def test_student_profile_module_creation(self, mock_engine):
        """Test StudentProfileModule can be created."""
        module = StudentProfileModule(mock_engine)
        assert module.name == "Student Profile & Assessment Engine"
        assert module.ai_engine is not None

    def test_academic_planning_module_creation(self, mock_engine):
        """Test AcademicPlanningModule can be created."""
        module = AcademicPlanningModule(mock_engine)
        assert module.name == "Academic Planning System"
        assert module.ai_engine is not None

    def test_extracurricular_advisor_module_creation(self, mock_engine):
        """Test ExtracurricularAdvisorModule can be created."""
        module = ExtracurricularAdvisorModule(mock_engine)
        assert module.name == "Extracurricular & Competition Advisor"
        assert module.ai_engine is not None

    def test_summer_programs_module_creation(self, mock_engine):
        """Test SummerProgramsModule can be created."""
        module = SummerProgramsModule(mock_engine)
        assert module.name == "Summer Programs & Opportunities Engine"
        assert module.ai_engine is not None

    def test_college_research_module_creation(self, mock_engine):
        """Test CollegeResearchModule can be created."""
        module = CollegeResearchModule(mock_engine)
        assert module.name == "College Research & Matching System"
        assert module.ai_engine is not None

    def test_essay_workshop_module_creation(self, mock_engine):
        """Test EssayWorkshopModule can be created."""
        module = EssayWorkshopModule(mock_engine)
        assert module.name == "Essay Development Workshop"
        assert module.ai_engine is not None

    def test_application_manager_module_creation(self, mock_engine):
        """Test ApplicationManagerModule can be created."""
        module = ApplicationManagerModule(mock_engine)
        assert module.name == "Application Assembly & Submission Manager"
        assert module.ai_engine is not None

    def test_timeline_orchestrator_module_creation(self, mock_engine):
        """Test TimelineOrchestratorModule can be created."""
        module = TimelineOrchestratorModule(mock_engine)
        assert module.name == "Timeline & Milestone Orchestrator"
        assert module.ai_engine is not None


class TestModuleInitialization:
    """Tests for module initialization."""

    @pytest.fixture
    def mock_engine(self):
        """Create mock AI engine."""
        return MockAIEngine()

    @pytest.mark.asyncio
    async def test_all_modules_initialize(self, mock_engine):
        """Test all modules can be initialized."""
        modules = [
            StudentProfileModule(mock_engine),
            AcademicPlanningModule(mock_engine),
            ExtracurricularAdvisorModule(mock_engine),
            SummerProgramsModule(mock_engine),
            CollegeResearchModule(mock_engine),
            EssayWorkshopModule(mock_engine),
            ApplicationManagerModule(mock_engine),
            TimelineOrchestratorModule(mock_engine),
        ]

        for module in modules:
            assert module._initialized is False
            await module.initialize()
            assert module._initialized is True

    @pytest.mark.asyncio
    async def test_module_not_initialized_error(self, mock_engine):
        """Test modules raise error when not initialized."""
        modules = [
            StudentProfileModule(mock_engine),
            AcademicPlanningModule(mock_engine),
            ExtracurricularAdvisorModule(mock_engine),
            SummerProgramsModule(mock_engine),
            CollegeResearchModule(mock_engine),
            EssayWorkshopModule(mock_engine),
            ApplicationManagerModule(mock_engine),
            TimelineOrchestratorModule(mock_engine),
        ]

        for module in modules:
            with pytest.raises(RuntimeError, match="not initialized"):
                module.ensure_initialized()


class TestModuleDescriptions:
    """Tests for module descriptions and metadata."""

    @pytest.fixture
    def mock_engine(self):
        """Create mock AI engine."""
        return MockAIEngine()

    def test_all_modules_have_unique_names(self, mock_engine):
        """Test all modules have unique names."""
        modules = [
            StudentProfileModule(mock_engine),
            AcademicPlanningModule(mock_engine),
            ExtracurricularAdvisorModule(mock_engine),
            SummerProgramsModule(mock_engine),
            CollegeResearchModule(mock_engine),
            EssayWorkshopModule(mock_engine),
            ApplicationManagerModule(mock_engine),
            TimelineOrchestratorModule(mock_engine),
        ]

        names = [m.name for m in modules]
        assert len(names) == len(set(names)), "Module names should be unique"

    def test_all_modules_have_descriptions(self, mock_engine):
        """Test all modules have non-empty descriptions."""
        modules = [
            StudentProfileModule(mock_engine),
            AcademicPlanningModule(mock_engine),
            ExtracurricularAdvisorModule(mock_engine),
            SummerProgramsModule(mock_engine),
            CollegeResearchModule(mock_engine),
            EssayWorkshopModule(mock_engine),
            ApplicationManagerModule(mock_engine),
            TimelineOrchestratorModule(mock_engine),
        ]

        for module in modules:
            assert module.description is not None
            assert len(module.description) > 10, f"{module.name} description too short"
