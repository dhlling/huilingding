"""Enumerations used throughout the college planning system."""

from enum import Enum, auto


class GradeLevel(str, Enum):
    """High school grade levels."""
    FRESHMAN = "freshman"
    SOPHOMORE = "sophomore"
    JUNIOR = "junior"
    SENIOR = "senior"

    @property
    def year_number(self) -> int:
        """Return numeric year (9-12)."""
        return {"freshman": 9, "sophomore": 10, "junior": 11, "senior": 12}[self.value]


class ActivityCategory(str, Enum):
    """Categories for extracurricular activities."""
    ACADEMIC = "academic"
    ARTS = "arts"
    ATHLETICS = "athletics"
    COMMUNITY_SERVICE = "community_service"
    LEADERSHIP = "leadership"
    WORK_EXPERIENCE = "work_experience"
    RESEARCH = "research"
    COMPETITION = "competition"
    CLUB = "club"
    PERSONAL_PROJECT = "personal_project"


class CompetitionType(str, Enum):
    """Types of academic competitions."""
    MATH_OLYMPIAD = "math_olympiad"
    SCIENCE_OLYMPIAD = "science_olympiad"
    PHYSICS_OLYMPIAD = "physics_olympiad"
    CHEMISTRY_OLYMPIAD = "chemistry_olympiad"
    BIOLOGY_OLYMPIAD = "biology_olympiad"
    INFORMATICS_OLYMPIAD = "informatics_olympiad"
    DEBATE = "debate"
    MODEL_UN = "model_un"
    SCIENCE_FAIR = "science_fair"
    ESSAY_COMPETITION = "essay_competition"
    ROBOTICS = "robotics"
    HACKATHON = "hackathon"
    BUSINESS = "business"
    ECONOMICS = "economics"
    LINGUISTICS = "linguistics"
    HISTORY = "history"


class AchievementLevel(str, Enum):
    """Levels of achievement in activities and competitions."""
    PARTICIPANT = "participant"
    SCHOOL_LEVEL = "school_level"
    REGIONAL = "regional"
    STATE = "state"
    NATIONAL = "national"
    INTERNATIONAL = "international"


class ApplicationStatus(str, Enum):
    """Status of college applications."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WAITLISTED = "waitlisted"
    DEFERRED = "deferred"
    WITHDRAWN = "withdrawn"


class CollegeType(str, Enum):
    """Types of colleges/universities."""
    RESEARCH_UNIVERSITY = "research_university"
    LIBERAL_ARTS = "liberal_arts"
    STATE_UNIVERSITY = "state_university"
    COMMUNITY_COLLEGE = "community_college"
    TECHNICAL_INSTITUTE = "technical_institute"
    ART_SCHOOL = "art_school"
    CONSERVATORY = "conservatory"


class CollegeTier(str, Enum):
    """College tiers for list building."""
    REACH = "reach"
    TARGET = "target"
    LIKELY = "likely"


class SubjectArea(str, Enum):
    """Academic subject areas."""
    MATHEMATICS = "mathematics"
    PHYSICS = "physics"
    CHEMISTRY = "chemistry"
    BIOLOGY = "biology"
    COMPUTER_SCIENCE = "computer_science"
    ENGLISH = "english"
    HISTORY = "history"
    FOREIGN_LANGUAGE = "foreign_language"
    ECONOMICS = "economics"
    PSYCHOLOGY = "psychology"
    ART = "art"
    MUSIC = "music"
    ENGINEERING = "engineering"
    BUSINESS = "business"
    MEDICINE = "medicine"
    LAW = "law"


class TestType(str, Enum):
    """Standardized test types."""
    SAT = "sat"
    ACT = "act"
    SAT_SUBJECT = "sat_subject"
    AP = "ap"
    IB = "ib"
    TOEFL = "toefl"
    IELTS = "ielts"
    PSAT = "psat"


class EssayType(str, Enum):
    """Types of college application essays."""
    COMMON_APP_PERSONAL = "common_app_personal"
    COALITION_PERSONAL = "coalition_personal"
    SUPPLEMENTAL = "supplemental"
    WHY_US = "why_us"
    ACTIVITY_DESCRIPTION = "activity_description"
    ADDITIONAL_INFO = "additional_info"
    SHORT_ANSWER = "short_answer"


class RecommendationType(str, Enum):
    """Types of recommendation letters."""
    COUNSELOR = "counselor"
    CORE_TEACHER = "core_teacher"
    ADDITIONAL_TEACHER = "additional_teacher"
    PEER = "peer"
    COACH = "coach"
    MENTOR = "mentor"
    EMPLOYER = "employer"


class InterestLevel(str, Enum):
    """Level of interest in a subject or activity."""
    EXPLORING = "exploring"
    INTERESTED = "interested"
    PASSIONATE = "passionate"
    COMMITTED = "committed"


class ProgramType(str, Enum):
    """Types of summer/enrichment programs."""
    PRE_COLLEGE = "pre_college"
    RESEARCH = "research"
    INTERNSHIP = "internship"
    CAMP = "camp"
    VOLUNTEER = "volunteer"
    TRAVEL = "travel"
    ONLINE_COURSE = "online_course"


class FinancialNeedLevel(str, Enum):
    """Financial need categories."""
    FULL_PAY = "full_pay"
    PARTIAL_AID = "partial_aid"
    SIGNIFICANT_AID = "significant_aid"
    FULL_AID = "full_aid"


class MilestoneCategory(str, Enum):
    """Categories for timeline milestones."""
    ACADEMIC = "academic"
    TESTING = "testing"
    EXTRACURRICULAR = "extracurricular"
    APPLICATION = "application"
    ESSAY = "essay"
    RECOMMENDATION = "recommendation"
    FINANCIAL_AID = "financial_aid"
    VISIT = "visit"
    DECISION = "decision"
