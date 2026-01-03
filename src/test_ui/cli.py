"""Interactive CLI for testing modules.

This CLI provides an interactive way to test the AI College Planning System modules.
Run with: python -m src.test_ui.cli
"""

import asyncio
import subprocess
import sys
from datetime import date
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.tree import Tree
from rich import print as rprint

from src.core.enums import (
    GradeLevel,
    SubjectArea,
    TestType,
    InterestLevel,
    FinancialNeedLevel,
    EssayType,
    CollegeTier,
)
from src.core.models import (
    Student,
    PersonalInfo,
    FamilyContext,
    AcademicRecord,
    Course,
    TestScore,
    Interest,
)

# Create Typer app
app = typer.Typer(
    name="module-tester",
    help="Interactive testing UI for AI College Planning System modules",
    add_completion=False,
)

console = Console()


# Mock AI Engine for interactive testing
class InteractiveTestEngine:
    """A mock AI engine that returns predictable results for testing."""

    async def generate_text(self, prompt: str, **kwargs) -> str:
        return f"[Mock Response] Analysis of: {prompt[:100]}..."

    async def generate_structured(self, prompt: str, response_model, **kwargs):
        from src.modules.profile import (
            PersonalityProfile,
            InterestInventory,
            AcademicAssessment,
            GoalFramework,
        )

        if response_model == PersonalityProfile:
            return PersonalityProfile(
                strengths=["analytical thinking", "creativity", "perseverance"],
                work_style="Collaborative",
                learning_style="Visual",
                risk_tolerance="Moderate",
                time_management="Structured",
                leadership_tendency="Leader",
                creativity_level="Balanced",
                stress_management="Thrives under pressure",
            )
        elif response_model == InterestInventory:
            return InterestInventory(
                top_academic_interests=[SubjectArea.COMPUTER_SCIENCE, SubjectArea.MATHEMATICS],
                career_clusters=["Technology", "Engineering"],
                activity_preferences=["coding", "robotics"],
                passion_areas=["artificial intelligence", "game development"],
                aversions=[],
            )
        elif response_model == AcademicAssessment:
            return AcademicAssessment(
                strong_subjects=[SubjectArea.MATHEMATICS, SubjectArea.PHYSICS],
                developing_subjects=[SubjectArea.ENGLISH],
                recommended_focus_areas=["writing skills"],
                gpa_trajectory="Improving",
                course_rigor_assessment="Strong rigor with AP courses",
                testing_readiness="Ready for SAT",
            )
        elif response_model == GoalFramework:
            return GoalFramework(
                dream_schools=["MIT", "Stanford"],
                intended_majors=["Computer Science"],
                career_aspirations=["Software Engineer"],
                short_term_goals=["Improve GPA"],
                medium_term_goals=["Take SAT"],
                long_term_goals=["Get into top CS program"],
                non_negotiables=["Strong CS program"],
            )
        raise NotImplementedError(f"No mock for {response_model}")

    async def analyze_essay(self, essay_content: str, prompt: str, criteria: list) -> dict:
        return {
            "overall_score": 85,
            "strengths": ["Clear narrative", "Strong voice"],
            "areas_for_improvement": ["More specific examples"],
        }

    async def chat(self, messages: list, **kwargs) -> str:
        return "[Mock Chat Response] Here's my advice..."


def create_sample_student() -> Student:
    """Create a sample student for testing."""
    return Student(
        id="test-student-001",
        personal_info=PersonalInfo(
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com",
            date_of_birth=date(2008, 5, 15),
            high_school="Springfield High School",
            graduation_year=2026,
            state="CA",
            country="USA",
        ),
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
            ],
        ),
        interests=[
            Interest(
                area=SubjectArea.COMPUTER_SCIENCE,
                level=InterestLevel.PASSIONATE,
                years_of_engagement=4,
            ),
        ],
        intended_majors=["Computer Science"],
        career_interests=["Software Engineer"],
    )


@app.command()
def run_tests(
    module: Optional[str] = typer.Option(None, "--module", "-m", help="Specific module to test"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    coverage: bool = typer.Option(False, "--coverage", "-c", help="Run with coverage report"),
):
    """Run pytest tests for the modules."""
    console.print(Panel.fit("[bold blue]Running Module Tests[/bold blue]"))

    cmd = ["python", "-m", "pytest"]

    if module:
        if module == "core":
            cmd.append("tests/test_core/")
        elif module == "profile":
            cmd.append("tests/test_modules/test_profile.py")
        elif module == "academic":
            cmd.append("tests/test_modules/test_academic.py")
        elif module == "essay":
            cmd.append("tests/test_modules/test_essay.py")
        elif module == "all-modules":
            cmd.append("tests/test_modules/test_all_modules.py")
        else:
            cmd.append(f"tests/test_modules/test_{module}.py")
    else:
        cmd.append("tests/")

    if verbose:
        cmd.append("-v")

    if coverage:
        cmd.extend(["--cov=src", "--cov-report=term-missing"])

    console.print(f"[dim]Running: {' '.join(cmd)}[/dim]\n")

    try:
        result = subprocess.run(cmd, cwd="/home/user/huilingding")
        if result.returncode == 0:
            console.print("\n[bold green]All tests passed![/bold green]")
        else:
            console.print("\n[bold red]Some tests failed.[/bold red]")
    except FileNotFoundError:
        console.print("[red]Error: pytest not found. Install with: pip install pytest[/red]")


@app.command()
def list_modules():
    """List all available modules."""
    console.print(Panel.fit("[bold blue]Available Modules[/bold blue]"))

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Module", style="cyan")
    table.add_column("Description")
    table.add_column("Test File")

    modules = [
        ("StudentProfileModule", "Student profiling and assessment", "test_profile.py"),
        ("AcademicPlanningModule", "Course selection and GPA planning", "test_academic.py"),
        ("ExtracurricularAdvisorModule", "Activity recommendations", "test_all_modules.py"),
        ("SummerProgramsModule", "Summer program matching", "test_all_modules.py"),
        ("CollegeResearchModule", "College matching and research", "test_all_modules.py"),
        ("EssayWorkshopModule", "Essay development and feedback", "test_essay.py"),
        ("ApplicationManagerModule", "Application tracking", "test_all_modules.py"),
        ("TimelineOrchestratorModule", "Timeline and milestone management", "test_all_modules.py"),
    ]

    for name, desc, test_file in modules:
        table.add_row(name, desc, test_file)

    console.print(table)


@app.command()
def test_profile():
    """Interactively test the Student Profile module."""
    console.print(Panel.fit("[bold blue]Student Profile Module - Interactive Test[/bold blue]"))

    asyncio.run(_test_profile_interactive())


async def _test_profile_interactive():
    """Interactive testing for profile module."""
    from src.modules.profile import StudentProfileModule

    engine = InteractiveTestEngine()
    module = StudentProfileModule(engine)

    console.print("\n[bold]Creating a new student profile...[/bold]")

    # Create profile
    first_name = Prompt.ask("First name", default="Jane")
    last_name = Prompt.ask("Last name", default="Doe")
    email = Prompt.ask("Email", default="jane.doe@example.com")
    graduation_year = int(Prompt.ask("Graduation year", default="2026"))
    state = Prompt.ask("State", default="CA")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Creating profile...", total=None)

        student = await module.create_profile(
            first_name=first_name,
            last_name=last_name,
            email=email,
            date_of_birth=date(2008, 5, 15),
            high_school="Test High School",
            graduation_year=graduation_year,
            state=state,
        )

    console.print(f"\n[green]Profile created![/green] ID: {student.id}")
    console.print(f"Full name: {student.personal_info.full_name}")

    # Add test score
    if Confirm.ask("\nAdd a test score?"):
        score = int(Prompt.ask("SAT Score", default="1450"))

        student = await module.add_test_score(
            student_id=student.id,
            test_type=TestType.SAT,
            score=score,
            max_score=1600,
            date_taken=date.today(),
        )
        console.print(f"[green]Test score added![/green] Percentile: {student.academic_record.test_scores[0].percentile:.1f}%")

    # Run assessment
    if Confirm.ask("\nRun personality assessment?"):
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task("Running AI assessment...", total=None)

            result = await module.assess_personality(
                student_id=student.id,
                questionnaire_responses={"sample": "response"},
            )

        console.print("\n[bold]Personality Assessment Results:[/bold]")
        table = Table(show_header=False)
        table.add_column("Trait", style="cyan")
        table.add_column("Value")
        table.add_row("Strengths", ", ".join(result.strengths))
        table.add_row("Work Style", result.work_style)
        table.add_row("Learning Style", result.learning_style)
        table.add_row("Risk Tolerance", result.risk_tolerance)
        console.print(table)

    console.print("\n[bold green]Profile module test completed![/bold green]")


@app.command()
def test_all():
    """Run all interactive module tests."""
    console.print(Panel.fit("[bold blue]Running All Module Tests[/bold blue]"))

    modules = [
        "profile",
        "academic",
        "extracurricular",
        "summer_programs",
        "college_research",
        "essay",
        "application",
        "timeline",
    ]

    asyncio.run(_test_all_modules(modules))


async def _test_all_modules(modules: list):
    """Test all modules with mock data."""
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

    engine = InteractiveTestEngine()

    module_classes = [
        ("Student Profile", StudentProfileModule),
        ("Academic Planning", AcademicPlanningModule),
        ("Extracurricular Advisor", ExtracurricularAdvisorModule),
        ("Summer Programs", SummerProgramsModule),
        ("College Research", CollegeResearchModule),
        ("Essay Workshop", EssayWorkshopModule),
        ("Application Manager", ApplicationManagerModule),
        ("Timeline Orchestrator", TimelineOrchestratorModule),
    ]

    results = Table(show_header=True, header_style="bold magenta")
    results.add_column("Module", style="cyan")
    results.add_column("Status")
    results.add_column("Details")

    for name, cls in module_classes:
        try:
            module = cls(engine)
            await module.initialize()
            results.add_row(name, "[green]OK[/green]", f"Initialized: {module._initialized}")
        except Exception as e:
            results.add_row(name, "[red]FAIL[/red]", str(e)[:50])

    console.print(results)


@app.command()
def show_coverage():
    """Show test coverage report."""
    console.print(Panel.fit("[bold blue]Test Coverage Report[/bold blue]"))

    cmd = [
        "python", "-m", "pytest",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-report=html",
        "tests/",
        "-q",
    ]

    console.print(f"[dim]Running: {' '.join(cmd)}[/dim]\n")

    try:
        subprocess.run(cmd, cwd="/home/user/huilingding")
        console.print("\n[green]HTML coverage report generated in htmlcov/[/green]")
    except FileNotFoundError:
        console.print("[red]Error: pytest-cov not found. Install with: pip install pytest-cov[/red]")


@app.command()
def show_structure():
    """Show the test directory structure."""
    console.print(Panel.fit("[bold blue]Test Directory Structure[/bold blue]"))

    tree = Tree("[bold]tests/[/bold]")

    conftest = tree.add("[cyan]conftest.py[/cyan] - Shared fixtures and mock AI engine")

    core = tree.add("[bold]test_core/[/bold]")
    core.add("[cyan]test_enums.py[/cyan] - Enum tests")
    core.add("[cyan]test_models.py[/cyan] - Data model tests")

    modules = tree.add("[bold]test_modules/[/bold]")
    modules.add("[cyan]test_profile.py[/cyan] - Student Profile module tests")
    modules.add("[cyan]test_academic.py[/cyan] - Academic Planning module tests")
    modules.add("[cyan]test_essay.py[/cyan] - Essay Workshop module tests")
    modules.add("[cyan]test_all_modules.py[/cyan] - All modules basic tests")

    console.print(tree)


@app.command()
def demo():
    """Run a quick demo of the testing system."""
    console.print(Panel.fit("[bold blue]Module Testing Demo[/bold blue]"))

    console.print("\n[bold]1. Creating a sample student...[/bold]")
    student = create_sample_student()

    table = Table(show_header=False, title="Sample Student")
    table.add_column("Field", style="cyan")
    table.add_column("Value")
    table.add_row("ID", student.id)
    table.add_row("Name", student.personal_info.full_name)
    table.add_row("School", student.personal_info.high_school)
    table.add_row("GPA", str(student.academic_record.cumulative_gpa))
    table.add_row("Graduation Year", str(student.personal_info.graduation_year))
    table.add_row("Primary Interests", ", ".join(s.value for s in student.primary_interests))
    console.print(table)

    console.print("\n[bold]2. Testing modules with mock AI engine...[/bold]")
    asyncio.run(_demo_modules())


async def _demo_modules():
    """Demo module functionality."""
    from src.modules.profile import StudentProfileModule

    engine = InteractiveTestEngine()
    module = StudentProfileModule(engine)

    # Create and test
    student = await module.create_profile(
        first_name="Demo",
        last_name="User",
        email="demo@test.com",
        date_of_birth=date(2008, 1, 1),
        high_school="Demo High",
        graduation_year=2026,
        state="CA",
    )

    console.print(f"[green]Created student:[/green] {student.personal_info.full_name}")

    # Run assessment
    assessment = await module.assess_personality(
        student_id=student.id,
        questionnaire_responses={"demo": True},
    )

    console.print(f"[green]Personality assessment complete![/green]")
    console.print(f"  Work Style: {assessment.work_style}")
    console.print(f"  Learning Style: {assessment.learning_style}")

    console.print("\n[bold green]Demo completed successfully![/bold green]")


def main():
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
