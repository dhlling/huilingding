"""Module 8: Timeline & Milestone Orchestrator.

This module handles:
- 4-year master calendar
- Deadline tracking
- Progress monitoring
- Adaptive recommendations
- Parent/counselor collaboration tools
"""

from datetime import date, datetime, timedelta
from typing import Any
from pydantic import BaseModel, Field
import uuid

from src.core.base import BaseModule, AIEngine
from src.core.models import Student, Timeline, Milestone
from src.core.enums import GradeLevel, MilestoneCategory


class MonthlyPlan(BaseModel):
    """Plan for a specific month."""
    month: int
    year: int
    milestones: list[Milestone]
    priorities: list[str]
    goals: list[str]


class YearlyOverview(BaseModel):
    """Overview of a single academic year."""
    grade_level: GradeLevel
    academic_year: str  # e.g., "2024-2025"
    themes: list[str]
    key_milestones: list[Milestone]
    monthly_plans: list[MonthlyPlan]
    success_metrics: list[str]


class FourYearTimeline(BaseModel):
    """Complete 4-year college prep timeline."""
    student_id: str
    freshman_year: YearlyOverview
    sophomore_year: YearlyOverview
    junior_year: YearlyOverview
    senior_year: YearlyOverview
    cross_cutting_goals: list[str]
    flexibility_notes: str


class ProgressReport(BaseModel):
    """Progress report on timeline completion."""
    student_id: str
    as_of_date: date
    overall_progress: float
    milestones_completed: int
    milestones_pending: int
    milestones_overdue: int
    on_track_status: str  # Ahead, On Track, Behind, At Risk
    completed_items: list[str]
    upcoming_items: list[str]
    overdue_items: list[str]
    recommendations: list[str]


class AdaptiveRecommendation(BaseModel):
    """Adaptive recommendation based on progress."""
    category: str
    recommendation: str
    priority: int
    reasoning: str
    action_items: list[str]
    deadline: date | None


class WeeklyDigest(BaseModel):
    """Weekly digest of tasks and progress."""
    week_of: date
    student_name: str
    this_week_priorities: list[str]
    upcoming_deadlines: list[dict[str, Any]]
    completed_last_week: list[str]
    progress_summary: str
    motivation_note: str


class TimelineOrchestratorModule(BaseModule):
    """Module for timeline management and orchestration."""

    @property
    def name(self) -> str:
        return "Timeline & Milestone Orchestrator"

    @property
    def description(self) -> str:
        return "4-year planning, deadline tracking, and progress monitoring"

    # Standard milestone templates by grade and month
    MILESTONE_TEMPLATES = {
        GradeLevel.FRESHMAN: {
            9: [  # September
                ("Start high school strong", MilestoneCategory.ACADEMIC),
                ("Join 2-3 extracurricular activities", MilestoneCategory.EXTRACURRICULAR),
            ],
            10: [
                ("First quarter grade check", MilestoneCategory.ACADEMIC),
            ],
            12: [
                ("Reflect on first semester", MilestoneCategory.ACADEMIC),
            ],
            1: [
                ("Take PSAT 8/9 if offered", MilestoneCategory.TESTING),
            ],
            3: [
                ("Research summer opportunities", MilestoneCategory.EXTRACURRICULAR),
            ],
            5: [
                ("Plan summer activities", MilestoneCategory.EXTRACURRICULAR),
                ("Request course recommendations for next year", MilestoneCategory.ACADEMIC),
            ],
        },
        GradeLevel.SOPHOMORE: {
            9: [
                ("Take PSAT 10", MilestoneCategory.TESTING),
                ("Increase activity involvement", MilestoneCategory.EXTRACURRICULAR),
            ],
            10: [
                ("Register for PSAT/NMSQT", MilestoneCategory.TESTING),
            ],
            11: [
                ("Consider SAT Subject Tests", MilestoneCategory.TESTING),
            ],
            1: [
                ("Begin college research", MilestoneCategory.VISIT),
                ("Plan campus visits", MilestoneCategory.VISIT),
            ],
            3: [
                ("Research competitive summer programs", MilestoneCategory.EXTRACURRICULAR),
            ],
            5: [
                ("Plan challenging junior year courses", MilestoneCategory.ACADEMIC),
            ],
        },
        GradeLevel.JUNIOR: {
            9: [
                ("Take PSAT/NMSQT", MilestoneCategory.TESTING),
                ("Begin SAT/ACT prep", MilestoneCategory.TESTING),
            ],
            10: [
                ("Take PSAT/NMSQT", MilestoneCategory.TESTING),
                ("Attend college fairs", MilestoneCategory.VISIT),
            ],
            12: [
                ("Register for spring SAT/ACT", MilestoneCategory.TESTING),
            ],
            1: [
                ("Finalize testing plan", MilestoneCategory.TESTING),
                ("Start college list", MilestoneCategory.APPLICATION),
            ],
            3: [
                ("Take SAT/ACT", MilestoneCategory.TESTING),
                ("Plan college visits for spring break", MilestoneCategory.VISIT),
            ],
            4: [
                ("Visit colleges during spring break", MilestoneCategory.VISIT),
            ],
            5: [
                ("Take AP exams", MilestoneCategory.TESTING),
                ("Retake SAT/ACT if needed", MilestoneCategory.TESTING),
                ("Ask for recommendation letters", MilestoneCategory.RECOMMENDATION),
            ],
            6: [
                ("Finalize college list", MilestoneCategory.APPLICATION),
                ("Begin Common App essay brainstorming", MilestoneCategory.ESSAY),
            ],
        },
        GradeLevel.SENIOR: {
            8: [
                ("Common App opens", MilestoneCategory.APPLICATION),
                ("Finalize Common App essay", MilestoneCategory.ESSAY),
            ],
            9: [
                ("Complete EA/ED applications", MilestoneCategory.APPLICATION),
                ("Request transcripts", MilestoneCategory.APPLICATION),
            ],
            10: [
                ("Submit EA/ED applications", MilestoneCategory.APPLICATION),
            ],
            11: [
                ("Submit EA applications", MilestoneCategory.APPLICATION),
                ("Work on RD essays", MilestoneCategory.ESSAY),
            ],
            12: [
                ("Submit FAFSA and CSS Profile", MilestoneCategory.FINANCIAL_AID),
                ("Complete RD applications", MilestoneCategory.APPLICATION),
            ],
            1: [
                ("Submit all RD applications", MilestoneCategory.APPLICATION),
            ],
            3: [
                ("Receive EA/RD decisions", MilestoneCategory.DECISION),
            ],
            4: [
                ("Compare financial aid offers", MilestoneCategory.FINANCIAL_AID),
                ("Visit accepted schools", MilestoneCategory.VISIT),
            ],
            5: [
                ("Make final decision by May 1", MilestoneCategory.DECISION),
                ("Submit enrollment deposit", MilestoneCategory.DECISION),
            ],
        },
    }

    def __init__(self, ai_engine: AIEngine):
        super().__init__(ai_engine)
        self._timelines: dict[str, Timeline] = {}

    async def create_timeline(
        self,
        student: Student,
    ) -> Timeline:
        """Create a personalized timeline for a student."""
        milestones = []

        # Generate milestones for remaining high school years
        current_grade = student.current_grade
        graduation_year = student.personal_info.graduation_year

        for grade in [GradeLevel.FRESHMAN, GradeLevel.SOPHOMORE,
                      GradeLevel.JUNIOR, GradeLevel.SENIOR]:
            if grade.year_number < current_grade.year_number:
                continue  # Skip past grades

            # Calculate academic year
            years_until_grad = graduation_year - datetime.now().year
            grade_year = graduation_year - (12 - grade.year_number)

            templates = self.MILESTONE_TEMPLATES.get(grade, {})

            for month, items in templates.items():
                for title, category in items:
                    # Calculate due date
                    if month >= 9:  # Fall semester
                        due_year = grade_year - 1
                    else:  # Spring semester
                        due_year = grade_year

                    milestone = Milestone(
                        id=str(uuid.uuid4()),
                        title=title,
                        description=f"Standard milestone for {grade.value} year",
                        category=category,
                        grade_level=grade,
                        month=month,
                        due_date=date(due_year, month, 15),
                        priority=1,
                    )
                    milestones.append(milestone)

        timeline = Timeline(
            student_id=student.id,
            milestones=milestones,
        )

        self._timelines[student.id] = timeline
        return timeline

    async def add_custom_milestone(
        self,
        student_id: str,
        title: str,
        description: str,
        category: MilestoneCategory,
        due_date: date,
        priority: int = 2,
    ) -> Milestone:
        """Add a custom milestone to the timeline."""
        timeline = self._timelines.get(student_id)
        if not timeline:
            raise ValueError(f"Timeline for student {student_id} not found")

        # Determine grade level based on due date
        grade_level = GradeLevel.SENIOR  # Default

        milestone = Milestone(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            category=category,
            grade_level=grade_level,
            due_date=due_date,
            priority=priority,
        )

        timeline.custom_events.append(milestone)
        return milestone

    async def complete_milestone(
        self,
        student_id: str,
        milestone_id: str,
        notes: str = "",
    ) -> Milestone:
        """Mark a milestone as completed."""
        timeline = self._timelines.get(student_id)
        if not timeline:
            raise ValueError(f"Timeline for student {student_id} not found")

        for milestone in timeline.milestones + timeline.custom_events:
            if milestone.id == milestone_id:
                milestone.completed = True
                milestone.completed_date = date.today()
                milestone.notes = notes
                return milestone

        raise ValueError(f"Milestone {milestone_id} not found")

    async def get_upcoming_milestones(
        self,
        student_id: str,
        days: int = 30,
    ) -> list[Milestone]:
        """Get upcoming milestones for a student."""
        timeline = self._timelines.get(student_id)
        if not timeline:
            return []

        return timeline.get_upcoming(days)

    async def get_overdue_milestones(
        self,
        student_id: str,
    ) -> list[Milestone]:
        """Get overdue milestones for a student."""
        timeline = self._timelines.get(student_id)
        if not timeline:
            return []

        return timeline.get_overdue()

    async def generate_progress_report(
        self,
        student: Student,
    ) -> ProgressReport:
        """Generate a progress report for a student."""
        timeline = self._timelines.get(student.id)
        if not timeline:
            timeline = await self.create_timeline(student)

        all_milestones = timeline.milestones + timeline.custom_events

        completed = [m for m in all_milestones if m.completed]
        pending = [m for m in all_milestones if not m.completed and
                   (not m.due_date or m.due_date >= date.today())]
        overdue = [m for m in all_milestones if not m.completed and
                   m.due_date and m.due_date < date.today()]

        # Determine status
        if len(overdue) > 3:
            status = "At Risk"
        elif len(overdue) > 0:
            status = "Behind"
        elif len(completed) > len(pending) * 0.5:
            status = "Ahead"
        else:
            status = "On Track"

        total = len(all_milestones)
        progress = (len(completed) / total * 100) if total > 0 else 0

        return ProgressReport(
            student_id=student.id,
            as_of_date=date.today(),
            overall_progress=progress,
            milestones_completed=len(completed),
            milestones_pending=len(pending),
            milestones_overdue=len(overdue),
            on_track_status=status,
            completed_items=[m.title for m in completed[-5:]],
            upcoming_items=[m.title for m in pending[:5]],
            overdue_items=[m.title for m in overdue[:5]],
            recommendations=[
                f"Complete overdue item: {overdue[0].title}" if overdue else "Stay on track!",
                "Focus on upcoming deadlines",
            ],
        )

    async def generate_four_year_timeline(
        self,
        student: Student,
    ) -> FourYearTimeline:
        """Generate a complete 4-year timeline."""
        grad_year = student.personal_info.graduation_year

        async def create_yearly_overview(grade: GradeLevel) -> YearlyOverview:
            grade_year = grad_year - (12 - grade.year_number)
            academic_year = f"{grade_year - 1}-{grade_year}"

            templates = self.MILESTONE_TEMPLATES.get(grade, {})
            milestones = []

            for month, items in templates.items():
                for title, category in items:
                    milestone = Milestone(
                        id=str(uuid.uuid4()),
                        title=title,
                        description=f"{grade.value} year milestone",
                        category=category,
                        grade_level=grade,
                        month=month,
                        priority=1,
                    )
                    milestones.append(milestone)

            themes = {
                GradeLevel.FRESHMAN: ["Exploration", "Foundation Building", "Adjustment"],
                GradeLevel.SOPHOMORE: ["Skill Development", "Interest Deepening", "Testing Introduction"],
                GradeLevel.JUNIOR: ["Leadership", "Testing Focus", "College Research"],
                GradeLevel.SENIOR: ["Applications", "Decision Making", "Transition"],
            }

            return YearlyOverview(
                grade_level=grade,
                academic_year=academic_year,
                themes=themes.get(grade, []),
                key_milestones=milestones,
                monthly_plans=[],
                success_metrics=[
                    f"Complete all {grade.value} year milestones",
                    "Maintain strong academic performance",
                    "Develop extracurricular depth",
                ],
            )

        freshman = await create_yearly_overview(GradeLevel.FRESHMAN)
        sophomore = await create_yearly_overview(GradeLevel.SOPHOMORE)
        junior = await create_yearly_overview(GradeLevel.JUNIOR)
        senior = await create_yearly_overview(GradeLevel.SENIOR)

        return FourYearTimeline(
            student_id=student.id,
            freshman_year=freshman,
            sophomore_year=sophomore,
            junior_year=junior,
            senior_year=senior,
            cross_cutting_goals=[
                "Maintain high academic performance",
                "Develop a clear 'spike' or area of expertise",
                "Build meaningful relationships with teachers",
                "Explore and confirm interests",
                "Prepare compelling college applications",
            ],
            flexibility_notes="This timeline is a guide - adjust based on individual circumstances and opportunities.",
        )

    async def generate_adaptive_recommendations(
        self,
        student: Student,
    ) -> list[AdaptiveRecommendation]:
        """Generate adaptive recommendations based on progress."""
        timeline = self._timelines.get(student.id)
        progress = await self.generate_progress_report(student)

        recommendations = []

        # Check for overdue items
        if progress.milestones_overdue > 0:
            recommendations.append(AdaptiveRecommendation(
                category="Urgent",
                recommendation="Address overdue milestones immediately",
                priority=1,
                reasoning=f"You have {progress.milestones_overdue} overdue items",
                action_items=progress.overdue_items[:3],
                deadline=date.today() + timedelta(days=7),
            ))

        # Grade-specific recommendations
        current_grade = student.current_grade
        current_month = datetime.now().month

        if current_grade == GradeLevel.JUNIOR and current_month >= 1 and current_month <= 5:
            recommendations.append(AdaptiveRecommendation(
                category="Testing",
                recommendation="Focus on SAT/ACT preparation",
                priority=2,
                reasoning="Spring of junior year is prime testing season",
                action_items=[
                    "Complete practice tests weekly",
                    "Register for upcoming test dates",
                    "Focus on weakest areas",
                ],
                deadline=date.today() + timedelta(days=30),
            ))

        if current_grade == GradeLevel.SENIOR and current_month >= 8 and current_month <= 10:
            recommendations.append(AdaptiveRecommendation(
                category="Applications",
                recommendation="Finalize Early Applications",
                priority=1,
                reasoning="EA/ED deadlines are approaching",
                action_items=[
                    "Complete Common App essay",
                    "Finalize supplemental essays",
                    "Confirm recommendation letters",
                ],
                deadline=date(datetime.now().year, 11, 1),
            ))

        # Academic recommendations
        if student.academic_record.cumulative_gpa < 3.5:
            recommendations.append(AdaptiveRecommendation(
                category="Academic",
                recommendation="Focus on GPA improvement",
                priority=2,
                reasoning="Higher GPA will strengthen college applications",
                action_items=[
                    "Identify challenging courses",
                    "Seek tutoring if needed",
                    "Meet with teachers regularly",
                ],
                deadline=None,
            ))

        return recommendations

    async def generate_weekly_digest(
        self,
        student: Student,
    ) -> WeeklyDigest:
        """Generate a weekly digest for the student."""
        timeline = self._timelines.get(student.id)
        if not timeline:
            timeline = await self.create_timeline(student)

        upcoming = timeline.get_upcoming(days=14)
        overdue = timeline.get_overdue()

        # Get recently completed
        all_milestones = timeline.milestones + timeline.custom_events
        completed_recently = [
            m for m in all_milestones
            if m.completed and m.completed_date and
            (date.today() - m.completed_date).days <= 7
        ]

        priorities = []
        if overdue:
            priorities.append(f"⚠️ Complete overdue: {overdue[0].title}")
        for m in upcoming[:3]:
            priorities.append(f"📅 {m.title}")

        prompt = f"""Write a brief, encouraging motivation note for a {student.current_grade.value}
student working on college prep. They have {len(upcoming)} upcoming tasks and
completed {len(completed_recently)} tasks last week. Keep it to 2-3 sentences."""

        motivation = await self.ai_engine.generate_text(prompt)

        return WeeklyDigest(
            week_of=date.today() - timedelta(days=date.today().weekday()),
            student_name=student.personal_info.first_name,
            this_week_priorities=priorities[:5],
            upcoming_deadlines=[
                {"task": m.title, "due": m.due_date.isoformat() if m.due_date else "TBD"}
                for m in upcoming[:5]
            ],
            completed_last_week=[m.title for m in completed_recently],
            progress_summary=f"Completed {len(completed_recently)} tasks, {len(upcoming)} upcoming",
            motivation_note=motivation,
        )

    async def sync_with_applications(
        self,
        student_id: str,
        applications: list[dict[str, Any]],
    ) -> list[Milestone]:
        """Sync timeline with application deadlines."""
        timeline = self._timelines.get(student_id)
        if not timeline:
            raise ValueError(f"Timeline for student {student_id} not found")

        new_milestones = []

        for app in applications:
            # Add application deadline
            deadline_milestone = Milestone(
                id=str(uuid.uuid4()),
                title=f"Submit {app['college_name']} application",
                description=f"{app['application_type']} application deadline",
                category=MilestoneCategory.APPLICATION,
                grade_level=GradeLevel.SENIOR,
                due_date=app["deadline"],
                priority=1,
            )
            timeline.custom_events.append(deadline_milestone)
            new_milestones.append(deadline_milestone)

            # Add essay milestones (2 weeks before deadline)
            essay_deadline = app["deadline"] - timedelta(days=14)
            essay_milestone = Milestone(
                id=str(uuid.uuid4()),
                title=f"Complete {app['college_name']} essays",
                description="Finalize all essays for this application",
                category=MilestoneCategory.ESSAY,
                grade_level=GradeLevel.SENIOR,
                due_date=essay_deadline,
                priority=1,
            )
            timeline.custom_events.append(essay_milestone)
            new_milestones.append(essay_milestone)

        return new_milestones

    async def get_timeline(self, student_id: str) -> Timeline | None:
        """Get timeline for a student."""
        return self._timelines.get(student_id)

    async def export_to_calendar(
        self,
        student_id: str,
        format: str = "ical",
    ) -> str:
        """Export timeline to calendar format."""
        timeline = self._timelines.get(student_id)
        if not timeline:
            raise ValueError(f"Timeline for student {student_id} not found")

        if format == "ical":
            # Generate iCal format
            events = []
            events.append("BEGIN:VCALENDAR")
            events.append("VERSION:2.0")
            events.append("PRODID:-//College Planning System//EN")

            for milestone in timeline.milestones + timeline.custom_events:
                if milestone.due_date and not milestone.completed:
                    events.append("BEGIN:VEVENT")
                    events.append(f"DTSTART:{milestone.due_date.strftime('%Y%m%d')}")
                    events.append(f"SUMMARY:{milestone.title}")
                    events.append(f"DESCRIPTION:{milestone.description}")
                    events.append(f"CATEGORIES:{milestone.category.value}")
                    events.append("END:VEVENT")

            events.append("END:VCALENDAR")
            return "\n".join(events)

        else:
            raise ValueError(f"Unknown format: {format}")
