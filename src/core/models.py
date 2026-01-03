"""Core data models for the college planning system."""

from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, computed_field

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
    RecommendationType,
    InterestLevel,
    ProgramType,
    CompetitionType,
    MilestoneCategory,
    FinancialNeedLevel,
)


# ============================================================================
# Student Profile Models
# ============================================================================


class PersonalInfo(BaseModel):
    """Basic personal information."""
    first_name: str
    last_name: str
    email: str
    date_of_birth: date
    high_school: str
    graduation_year: int
    state: str
    country: str = "USA"
    first_generation: bool = False
    international_student: bool = False

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class FamilyContext(BaseModel):
    """Family background and context."""
    parent_education_level: Optional[str] = None
    household_income_bracket: Optional[str] = None
    siblings_in_college: int = 0
    legacy_schools: list[str] = Field(default_factory=list)
    geographic_preferences: list[str] = Field(default_factory=list)
    financial_need: FinancialNeedLevel = FinancialNeedLevel.FULL_PAY


class Interest(BaseModel):
    """A student's interest in a particular area."""
    area: SubjectArea
    level: InterestLevel
    years_of_engagement: float = 0
    notes: str = ""


class TestScore(BaseModel):
    """Standardized test score."""
    test_type: TestType
    score: float
    max_score: float
    date_taken: date
    subject: Optional[str] = None  # For AP, SAT Subject tests

    @computed_field
    @property
    def percentile(self) -> float:
        """Approximate percentile based on score ratio."""
        return (self.score / self.max_score) * 100


class Course(BaseModel):
    """A single course."""
    name: str
    subject_area: SubjectArea
    level: str  # Regular, Honors, AP, IB
    grade: Optional[str] = None
    credits: float = 1.0
    grade_level: GradeLevel
    semester: str  # Fall, Spring, Full Year


class AcademicRecord(BaseModel):
    """Complete academic record."""
    courses: list[Course] = Field(default_factory=list)
    cumulative_gpa: float = 0.0
    weighted_gpa: float = 0.0
    class_rank: Optional[int] = None
    class_size: Optional[int] = None
    test_scores: list[TestScore] = Field(default_factory=list)

    @computed_field
    @property
    def rank_percentile(self) -> Optional[float]:
        if self.class_rank and self.class_size:
            return ((self.class_size - self.class_rank) / self.class_size) * 100
        return None


class Activity(BaseModel):
    """Extracurricular activity."""
    id: str
    name: str
    category: ActivityCategory
    description: str
    position: Optional[str] = None
    organization: Optional[str] = None
    hours_per_week: float
    weeks_per_year: float
    years_participated: list[GradeLevel]
    achievements: list[str] = Field(default_factory=list)
    achievement_level: AchievementLevel = AchievementLevel.PARTICIPANT
    is_primary: bool = False  # Part of main "spike"

    @computed_field
    @property
    def total_hours(self) -> float:
        return self.hours_per_week * self.weeks_per_year * len(self.years_participated)


class Competition(BaseModel):
    """Academic competition entry."""
    id: str
    name: str
    competition_type: CompetitionType
    year: int
    level_achieved: AchievementLevel
    award: Optional[str] = None
    description: str = ""


class SummerProgram(BaseModel):
    """Summer program or experience."""
    id: str
    name: str
    program_type: ProgramType
    institution: Optional[str] = None
    year: int
    duration_weeks: int
    description: str
    selective: bool = False
    paid: bool = False


class Student(BaseModel):
    """Complete student profile."""
    id: str
    personal_info: PersonalInfo
    family_context: FamilyContext
    academic_record: AcademicRecord
    interests: list[Interest] = Field(default_factory=list)
    activities: list[Activity] = Field(default_factory=list)
    competitions: list[Competition] = Field(default_factory=list)
    summer_programs: list[SummerProgram] = Field(default_factory=list)
    intended_majors: list[str] = Field(default_factory=list)
    career_interests: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @computed_field
    @property
    def current_grade(self) -> GradeLevel:
        """Calculate current grade based on graduation year."""
        current_year = datetime.now().year
        current_month = datetime.now().month
        # Assume school year starts in September
        academic_year = current_year if current_month >= 9 else current_year - 1
        years_until_grad = self.personal_info.graduation_year - academic_year
        grade_map = {4: GradeLevel.FRESHMAN, 3: GradeLevel.SOPHOMORE,
                     2: GradeLevel.JUNIOR, 1: GradeLevel.SENIOR}
        return grade_map.get(years_until_grad, GradeLevel.SENIOR)

    @computed_field
    @property
    def primary_interests(self) -> list[SubjectArea]:
        """Get top interests marked as passionate or committed."""
        return [
            i.area for i in self.interests
            if i.level in [InterestLevel.PASSIONATE, InterestLevel.COMMITTED]
        ]


# ============================================================================
# College Models
# ============================================================================


class AdmissionStats(BaseModel):
    """College admission statistics."""
    acceptance_rate: float
    early_acceptance_rate: Optional[float] = None
    avg_gpa: float
    gpa_25th: Optional[float] = None
    gpa_75th: Optional[float] = None
    sat_avg: Optional[int] = None
    sat_25th: Optional[int] = None
    sat_75th: Optional[int] = None
    act_avg: Optional[int] = None
    act_25th: Optional[int] = None
    act_75th: Optional[int] = None
    yield_rate: Optional[float] = None


class FinancialInfo(BaseModel):
    """College financial information."""
    tuition_in_state: int
    tuition_out_of_state: int
    room_and_board: int
    avg_financial_aid: int
    percent_receiving_aid: float
    meets_full_need: bool = False
    merit_scholarships: bool = True


class CollegeProgram(BaseModel):
    """Academic program at a college."""
    name: str
    department: str
    degree_type: str  # BA, BS, etc.
    ranking: Optional[int] = None
    notable_features: list[str] = Field(default_factory=list)


class College(BaseModel):
    """College/University profile."""
    id: str
    name: str
    location: str
    state: str
    college_type: CollegeType
    size: int  # Undergraduate enrollment
    setting: str  # Urban, Suburban, Rural
    admission_stats: AdmissionStats
    financial_info: FinancialInfo
    programs: list[CollegeProgram] = Field(default_factory=list)
    notable_features: list[str] = Field(default_factory=list)
    application_deadlines: dict[str, date] = Field(default_factory=dict)
    essays_required: int = 0
    interview_offered: bool = False
    demonstrated_interest: bool = False


# ============================================================================
# Application Models
# ============================================================================


class Essay(BaseModel):
    """College application essay."""
    id: str
    essay_type: EssayType
    college_id: Optional[str] = None  # None for Common App main essay
    prompt: str
    word_limit: int
    content: str = ""
    drafts: list[str] = Field(default_factory=list)
    feedback: list[str] = Field(default_factory=list)
    status: str = "not_started"  # not_started, drafting, reviewing, final
    themes: list[str] = Field(default_factory=list)


class RecommendationLetter(BaseModel):
    """Recommendation letter tracking."""
    id: str
    recommender_name: str
    recommender_title: str
    recommender_email: str
    recommendation_type: RecommendationType
    subject_taught: Optional[str] = None
    relationship_description: str = ""
    date_requested: Optional[date] = None
    date_submitted: Optional[date] = None
    status: str = "not_requested"  # not_requested, requested, in_progress, submitted


class Application(BaseModel):
    """College application."""
    id: str
    student_id: str
    college_id: str
    college_name: str
    tier: CollegeTier
    application_type: str  # EA, ED, ED2, RD, Rolling
    status: ApplicationStatus = ApplicationStatus.NOT_STARTED
    deadline: date
    essays: list[Essay] = Field(default_factory=list)
    recommendations: list[RecommendationLetter] = Field(default_factory=list)
    interview_date: Optional[date] = None
    interview_notes: str = ""
    submitted_date: Optional[date] = None
    decision_date: Optional[date] = None
    notes: str = ""

    @computed_field
    @property
    def days_until_deadline(self) -> int:
        return (self.deadline - date.today()).days

    @computed_field
    @property
    def is_complete(self) -> bool:
        essays_done = all(e.status == "final" for e in self.essays)
        recs_done = all(r.status == "submitted" for r in self.recommendations)
        return essays_done and recs_done


# ============================================================================
# Timeline Models
# ============================================================================


class Milestone(BaseModel):
    """A milestone in the college planning timeline."""
    id: str
    title: str
    description: str
    category: MilestoneCategory
    grade_level: GradeLevel
    due_date: Optional[date] = None
    month: Optional[int] = None  # 1-12 for recurring milestones
    priority: int = 1  # 1 = highest
    completed: bool = False
    completed_date: Optional[date] = None
    notes: str = ""
    dependencies: list[str] = Field(default_factory=list)  # IDs of prerequisite milestones


class Timeline(BaseModel):
    """Complete 4-year college planning timeline."""
    student_id: str
    milestones: list[Milestone] = Field(default_factory=list)
    custom_events: list[Milestone] = Field(default_factory=list)

    def get_upcoming(self, days: int = 30) -> list[Milestone]:
        """Get milestones due in the next N days."""
        today = date.today()
        upcoming = []
        for m in self.milestones + self.custom_events:
            if m.due_date and not m.completed:
                days_until = (m.due_date - today).days
                if 0 <= days_until <= days:
                    upcoming.append(m)
        return sorted(upcoming, key=lambda x: x.due_date or date.max)

    def get_overdue(self) -> list[Milestone]:
        """Get overdue milestones."""
        today = date.today()
        return [
            m for m in self.milestones + self.custom_events
            if m.due_date and not m.completed and m.due_date < today
        ]


# ============================================================================
# Recommendation Models (AI Output)
# ============================================================================


class CourseRecommendation(BaseModel):
    """AI-generated course recommendation."""
    course_name: str
    subject_area: SubjectArea
    level: str
    reasoning: str
    priority: int
    prerequisites: list[str] = Field(default_factory=list)


class ActivityRecommendation(BaseModel):
    """AI-generated activity recommendation."""
    activity_name: str
    category: ActivityCategory
    description: str
    reasoning: str
    time_commitment: str
    alignment_score: float  # How well it aligns with student's goals


class CollegeRecommendation(BaseModel):
    """AI-generated college recommendation."""
    college: College
    tier: CollegeTier
    match_score: float
    strengths: list[str]
    considerations: list[str]
    recommended_programs: list[str]


class EssayFeedback(BaseModel):
    """AI-generated essay feedback."""
    essay_id: str
    overall_score: float
    strengths: list[str]
    areas_for_improvement: list[str]
    specific_suggestions: list[str]
    theme_clarity: float
    authenticity_score: float
    grammar_issues: list[str] = Field(default_factory=list)
