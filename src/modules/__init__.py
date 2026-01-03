"""College Planning System Modules."""

from src.modules.profile import StudentProfileModule
from src.modules.academic import AcademicPlanningModule
from src.modules.extracurricular import ExtracurricularAdvisorModule
from src.modules.summer_programs import SummerProgramsModule
from src.modules.college_research import CollegeResearchModule
from src.modules.essay import EssayWorkshopModule
from src.modules.application import ApplicationManagerModule
from src.modules.timeline import TimelineOrchestratorModule

__all__ = [
    "StudentProfileModule",
    "AcademicPlanningModule",
    "ExtracurricularAdvisorModule",
    "SummerProgramsModule",
    "CollegeResearchModule",
    "EssayWorkshopModule",
    "ApplicationManagerModule",
    "TimelineOrchestratorModule",
]
