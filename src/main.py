"""Main entry point for the AI College Planning System.

This module provides the CLI interface and orchestrates all modules.
"""

import asyncio
from datetime import date
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.core.ai_engine import create_ai_engine, AIEngine
from src.core.models import Student
from src.core.enums import GradeLevel, SubjectArea, InterestLevel
from src.modules.profile import StudentProfileModule
from src.modules.academic import AcademicPlanningModule
from src.modules.extracurricular import ExtracurricularAdvisorModule
from src.modules.summer_programs import SummerProgramsModule
from src.modules.college_research import CollegeResearchModule
from src.modules.essay import EssayWorkshopModule
from src.modules.application import ApplicationManagerModule
from src.modules.timeline import TimelineOrchestratorModule


app = typer.Typer(
    name="college-planner",
    help="AI-powered college planning system for high school students",
)
console = Console()


class CollegePlanningSystem:
    """Main orchestrator for the college planning system."""

    def __init__(self, ai_provider: str = "mock", api_key: str | None = None):
        self.ai_engine = create_ai_engine(provider=ai_provider, api_key=api_key)

        # Initialize all modules
        self.profile = StudentProfileModule(self.ai_engine)
        self.academic = AcademicPlanningModule(self.ai_engine)
        self.extracurricular = ExtracurricularAdvisorModule(self.ai_engine)
        self.summer = SummerProgramsModule(self.ai_engine)
        self.college = CollegeResearchModule(self.ai_engine)
        self.essay = EssayWorkshopModule(self.ai_engine)
        self.application = ApplicationManagerModule(self.ai_engine)
        self.timeline = TimelineOrchestratorModule(self.ai_engine)

        self._current_student: Student | None = None

    async def initialize(self) -> None:
        """Initialize all modules."""
        await self.profile.initialize()
        await self.academic.initialize()
        await self.extracurricular.initialize()
        await self.summer.initialize()
        await self.college.initialize()
        await self.essay.initialize()
        await self.application.initialize()
        await self.timeline.initialize()

    @property
    def current_student(self) -> Student | None:
        return self._current_student

    async def create_new_student(
        self,
        first_name: str,
        last_name: str,
        email: str,
        date_of_birth: date,
        high_school: str,
        graduation_year: int,
        state: str,
    ) -> Student:
        """Create a new student profile."""
        student = await self.profile.create_profile(
            first_name=first_name,
            last_name=last_name,
            email=email,
            date_of_birth=date_of_birth,
            high_school=high_school,
            graduation_year=graduation_year,
            state=state,
        )
        self._current_student = student

        # Create timeline
        await self.timeline.create_timeline(student)

        return student

    async def get_dashboard(self, student: Student) -> dict:
        """Get a comprehensive dashboard for the student."""
        # Gather data from all modules
        progress = await self.timeline.generate_progress_report(student)
        recommendations = await self.timeline.generate_adaptive_recommendations(student)

        return {
            "student": student,
            "progress": progress,
            "recommendations": recommendations,
        }

    async def run_full_assessment(
        self,
        student: Student,
        interest_responses: dict,
        personality_responses: dict,
        goals: dict,
    ) -> dict:
        """Run a full assessment across all modules."""
        # Profile assessment
        profile_assessment = await self.profile.conduct_full_assessment(
            student.id, interest_responses, personality_responses, goals
        )

        # Academic assessment
        academic_assessment = await self.academic.analyze_course_rigor(student)

        # Activity portfolio
        activity_analysis = await self.extracurricular.analyze_portfolio(student)

        return {
            "profile": profile_assessment,
            "academic": academic_assessment,
            "activities": activity_analysis,
        }


# Global system instance
_system: CollegePlanningSystem | None = None


def get_system() -> CollegePlanningSystem:
    """Get or create the global system instance."""
    global _system
    if _system is None:
        _system = CollegePlanningSystem(ai_provider="mock")
        asyncio.get_event_loop().run_until_complete(_system.initialize())
    return _system


@app.command()
def welcome():
    """Display welcome message and system overview."""
    console.print(Panel.fit(
        "[bold blue]🎓 AI College Planning System[/bold blue]\n\n"
        "Your comprehensive guide to college preparation.\n\n"
        "[dim]Modules:[/dim]\n"
        "• Student Profile & Assessment\n"
        "• Academic Planning\n"
        "• Extracurricular & Competitions\n"
        "• Summer Programs\n"
        "• College Research & Matching\n"
        "• Essay Development\n"
        "• Application Management\n"
        "• Timeline Orchestration",
        title="Welcome",
        border_style="blue"
    ))


@app.command()
def create_student(
    first_name: str = typer.Option(..., prompt="First name"),
    last_name: str = typer.Option(..., prompt="Last name"),
    email: str = typer.Option(..., prompt="Email"),
    birth_year: int = typer.Option(..., prompt="Birth year"),
    birth_month: int = typer.Option(..., prompt="Birth month"),
    birth_day: int = typer.Option(..., prompt="Birth day"),
    high_school: str = typer.Option(..., prompt="High school name"),
    graduation_year: int = typer.Option(..., prompt="Graduation year"),
    state: str = typer.Option(..., prompt="State"),
):
    """Create a new student profile."""
    system = get_system()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Creating student profile...", total=None)

        student = asyncio.get_event_loop().run_until_complete(
            system.create_new_student(
                first_name=first_name,
                last_name=last_name,
                email=email,
                date_of_birth=date(birth_year, birth_month, birth_day),
                high_school=high_school,
                graduation_year=graduation_year,
                state=state,
            )
        )

    console.print(f"\n[green]✓[/green] Created profile for {student.personal_info.full_name}")
    console.print(f"  Student ID: {student.id}")
    console.print(f"  Current Grade: {student.current_grade.value}")


@app.command()
def dashboard():
    """Show the student dashboard."""
    system = get_system()

    if not system.current_student:
        console.print("[red]No student profile loaded. Run 'create-student' first.[/red]")
        raise typer.Exit(1)

    student = system.current_student

    # Create dashboard table
    table = Table(title=f"Dashboard: {student.personal_info.full_name}")

    table.add_column("Category", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Details")

    table.add_row(
        "Profile",
        "Complete" if student.interests else "Incomplete",
        f"{len(student.interests)} interests, {len(student.activities)} activities"
    )
    table.add_row(
        "Academic",
        f"GPA: {student.academic_record.cumulative_gpa:.2f}",
        f"{len(student.academic_record.courses)} courses"
    )
    table.add_row(
        "Testing",
        f"{len(student.academic_record.test_scores)} scores",
        ", ".join(t.test_type.value for t in student.academic_record.test_scores[:3])
    )
    table.add_row(
        "Activities",
        f"{len(student.activities)} total",
        ", ".join(a.name for a in student.activities[:3]) or "None yet"
    )

    console.print(table)


@app.command()
def add_interest(
    area: str = typer.Argument(..., help="Subject area (e.g., mathematics, physics)"),
    level: str = typer.Option("interested", help="Interest level: exploring/interested/passionate/committed"),
):
    """Add an interest to the current student's profile."""
    system = get_system()

    if not system.current_student:
        console.print("[red]No student profile loaded.[/red]")
        raise typer.Exit(1)

    try:
        subject = SubjectArea(area.lower())
        interest_level = InterestLevel(level.lower())
    except ValueError as e:
        console.print(f"[red]Invalid value: {e}[/red]")
        raise typer.Exit(1)

    asyncio.get_event_loop().run_until_complete(
        system.profile.add_interest(
            system.current_student.id,
            subject,
            interest_level,
        )
    )

    console.print(f"[green]✓[/green] Added interest: {area} ({level})")


@app.command()
def recommend_activities():
    """Get activity recommendations for the current student."""
    system = get_system()

    if not system.current_student:
        console.print("[red]No student profile loaded.[/red]")
        raise typer.Exit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Generating recommendations...", total=None)

        recommendations = asyncio.get_event_loop().run_until_complete(
            system.extracurricular.recommend_activities(system.current_student)
        )

    table = Table(title="Recommended Activities")
    table.add_column("Activity", style="cyan")
    table.add_column("Category")
    table.add_column("Time")
    table.add_column("Match", style="green")

    for rec in recommendations:
        table.add_row(
            rec.activity_name,
            rec.category.value,
            rec.time_commitment,
            f"{rec.alignment_score:.1f}/10"
        )

    console.print(table)


@app.command()
def recommend_colleges(
    count: int = typer.Option(10, help="Number of colleges to recommend"),
):
    """Get college recommendations for the current student."""
    system = get_system()

    if not system.current_student:
        console.print("[red]No student profile loaded.[/red]")
        raise typer.Exit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Matching colleges...", total=None)

        matches = asyncio.get_event_loop().run_until_complete(
            system.college.match_colleges(system.current_student, count=count)
        )

    table = Table(title="College Matches")
    table.add_column("College", style="cyan")
    table.add_column("Tier")
    table.add_column("Match Score", style="green")
    table.add_column("Admission %")

    for match in matches:
        tier_color = {"reach": "red", "target": "yellow", "likely": "green"}.get(
            match.tier.value, "white"
        )
        table.add_row(
            match.college.name,
            f"[{tier_color}]{match.tier.value.upper()}[/{tier_color}]",
            f"{match.overall_match_score:.1f}",
            f"{match.admission_probability:.1f}%"
        )

    console.print(table)


@app.command()
def build_college_list():
    """Build a balanced college list for the current student."""
    system = get_system()

    if not system.current_student:
        console.print("[red]No student profile loaded.[/red]")
        raise typer.Exit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Building college list...", total=None)

        college_list = asyncio.get_event_loop().run_until_complete(
            system.college.build_college_list(system.current_student)
        )

    console.print(Panel.fit(
        f"[bold]Total Schools:[/bold] {college_list.total_schools}\n"
        f"[red]Reach:[/red] {len(college_list.reach_schools)}\n"
        f"[yellow]Target:[/yellow] {len(college_list.target_schools)}\n"
        f"[green]Likely:[/green] {len(college_list.likely_schools)}",
        title="College List Summary"
    ))

    for tier, schools in [
        ("REACH", college_list.reach_schools),
        ("TARGET", college_list.target_schools),
        ("LIKELY", college_list.likely_schools),
    ]:
        if schools:
            console.print(f"\n[bold]{tier}:[/bold]")
            for school in schools:
                console.print(f"  • {school.college.name}")


@app.command()
def timeline():
    """View the timeline and upcoming milestones."""
    system = get_system()

    if not system.current_student:
        console.print("[red]No student profile loaded.[/red]")
        raise typer.Exit(1)

    progress = asyncio.get_event_loop().run_until_complete(
        system.timeline.generate_progress_report(system.current_student)
    )

    console.print(Panel.fit(
        f"[bold]Overall Progress:[/bold] {progress.overall_progress:.1f}%\n"
        f"[bold]Status:[/bold] {progress.on_track_status}\n"
        f"[green]Completed:[/green] {progress.milestones_completed}\n"
        f"[yellow]Pending:[/yellow] {progress.milestones_pending}\n"
        f"[red]Overdue:[/red] {progress.milestones_overdue}",
        title="Timeline Progress"
    ))

    if progress.upcoming_items:
        console.print("\n[bold]Upcoming:[/bold]")
        for item in progress.upcoming_items:
            console.print(f"  📅 {item}")

    if progress.overdue_items:
        console.print("\n[bold red]Overdue:[/bold red]")
        for item in progress.overdue_items:
            console.print(f"  ⚠️  {item}")


@app.command()
def summer_programs(
    year: int = typer.Option(None, help="Summer year (defaults to next summer)"),
    budget: int = typer.Option(None, help="Maximum budget in USD"),
):
    """Get summer program recommendations."""
    system = get_system()

    if not system.current_student:
        console.print("[red]No student profile loaded.[/red]")
        raise typer.Exit(1)

    if year is None:
        year = date.today().year if date.today().month < 6 else date.today().year + 1

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Finding programs...", total=None)

        recommendations = asyncio.get_event_loop().run_until_complete(
            system.summer.recommend_programs(
                system.current_student,
                summer_year=year,
                budget=budget,
            )
        )

    table = Table(title=f"Summer {year} Program Recommendations")
    table.add_column("Program", style="cyan")
    table.add_column("Type")
    table.add_column("Duration")
    table.add_column("Cost")
    table.add_column("Match", style="green")

    for rec in recommendations:
        table.add_row(
            rec.program.name,
            rec.program.program_type.value,
            f"{rec.program.duration_weeks} weeks",
            f"${rec.program.cost:,}" if rec.program.cost > 0 else "Free",
            f"{rec.match_score:.1f}/100"
        )

    console.print(table)


@app.command()
def essay_brainstorm():
    """Start essay brainstorming session."""
    system = get_system()

    if not system.current_student:
        console.print("[red]No student profile loaded.[/red]")
        raise typer.Exit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Discovering your story...", total=None)

        narrative = asyncio.get_event_loop().run_until_complete(
            system.essay.discover_personal_narrative(system.current_student)
        )

    console.print(Panel.fit(
        f"[bold]Core Values:[/bold] {', '.join(narrative.core_values)}\n\n"
        f"[bold]Passions:[/bold] {', '.join(narrative.passions)}\n\n"
        f"[bold]Unique Perspectives:[/bold]\n" +
        "\n".join(f"  • {p}" for p in narrative.unique_perspectives),
        title="Your Personal Narrative"
    ))

    if narrative.recommended_main_essay_topic:
        console.print(f"\n[bold green]Recommended Main Essay Topic:[/bold green]")
        console.print(f"  {narrative.recommended_main_essay_topic.title}")
        console.print(f"  Themes: {', '.join(narrative.recommended_main_essay_topic.potential_themes)}")


@app.command()
def version():
    """Display version information."""
    from src import __version__
    console.print(f"AI College Planning System v{__version__}")


def main():
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
