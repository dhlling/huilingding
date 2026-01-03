"""Module 1: Student Profile & Assessment Engine.

This module handles:
- Initial student profile creation
- Interest inventory and personality assessment
- Academic strength/weakness identification
- Learning style analysis
- Goal setting framework
"""

from datetime import date, datetime
from typing import Any
from pydantic import BaseModel, Field
import uuid

from src.core.base import BaseModule, AIEngine
from src.core.models import (
    Student,
    PersonalInfo,
    FamilyContext,
    AcademicRecord,
    Interest,
    TestScore,
    Course,
)
from src.core.enums import (
    GradeLevel,
    SubjectArea,
    InterestLevel,
    FinancialNeedLevel,
    TestType,
)


class PersonalityProfile(BaseModel):
    """Result of personality assessment."""
    strengths: list[str]
    work_style: str  # Independent, Collaborative, Mixed
    learning_style: str  # Visual, Auditory, Kinesthetic, Reading/Writing
    risk_tolerance: str  # Conservative, Moderate, Ambitious
    time_management: str  # Structured, Flexible, Procrastinator
    leadership_tendency: str  # Leader, Collaborator, Independent
    creativity_level: str  # Analytical, Creative, Balanced
    stress_management: str  # Thrives under pressure, Steady pace, Needs calm


class InterestInventory(BaseModel):
    """Detailed interest inventory results."""
    top_academic_interests: list[SubjectArea]
    career_clusters: list[str]
    activity_preferences: list[str]
    passion_areas: list[str]
    aversions: list[str]


class AcademicAssessment(BaseModel):
    """Academic strength and weakness analysis."""
    strong_subjects: list[SubjectArea]
    developing_subjects: list[SubjectArea]
    recommended_focus_areas: list[str]
    gpa_trajectory: str  # Improving, Stable, Declining
    course_rigor_assessment: str
    testing_readiness: str


class GoalFramework(BaseModel):
    """Student goals and aspirations."""
    dream_schools: list[str] = Field(default_factory=list)
    intended_majors: list[str] = Field(default_factory=list)
    career_aspirations: list[str] = Field(default_factory=list)
    short_term_goals: list[str] = Field(default_factory=list)  # This semester
    medium_term_goals: list[str] = Field(default_factory=list)  # This year
    long_term_goals: list[str] = Field(default_factory=list)  # By graduation
    non_negotiables: list[str] = Field(default_factory=list)  # Must-haves in college


class ProfileAssessmentResult(BaseModel):
    """Complete assessment result."""
    personality: PersonalityProfile
    interests: InterestInventory
    academic: AcademicAssessment
    goals: GoalFramework
    initial_recommendations: list[str]
    areas_to_explore: list[str]


class StudentProfileModule(BaseModule):
    """Module for student profile creation and assessment."""

    @property
    def name(self) -> str:
        return "Student Profile & Assessment Engine"

    @property
    def description(self) -> str:
        return "Comprehensive student profiling, assessment, and goal-setting system"

    def __init__(self, ai_engine: AIEngine):
        super().__init__(ai_engine)
        self._students: dict[str, Student] = {}

    async def create_profile(
        self,
        first_name: str,
        last_name: str,
        email: str,
        date_of_birth: date,
        high_school: str,
        graduation_year: int,
        state: str,
        country: str = "USA",
    ) -> Student:
        """Create a new student profile with basic information."""
        student_id = str(uuid.uuid4())

        personal_info = PersonalInfo(
            first_name=first_name,
            last_name=last_name,
            email=email,
            date_of_birth=date_of_birth,
            high_school=high_school,
            graduation_year=graduation_year,
            state=state,
            country=country,
        )

        student = Student(
            id=student_id,
            personal_info=personal_info,
            family_context=FamilyContext(),
            academic_record=AcademicRecord(),
        )

        self._students[student_id] = student
        return student

    async def update_family_context(
        self,
        student_id: str,
        parent_education: str | None = None,
        income_bracket: str | None = None,
        first_generation: bool = False,
        legacy_schools: list[str] | None = None,
        geographic_preferences: list[str] | None = None,
        financial_need: FinancialNeedLevel = FinancialNeedLevel.FULL_PAY,
    ) -> Student:
        """Update student's family context."""
        student = self._students.get(student_id)
        if not student:
            raise ValueError(f"Student {student_id} not found")

        student.family_context = FamilyContext(
            parent_education_level=parent_education,
            household_income_bracket=income_bracket,
            legacy_schools=legacy_schools or [],
            geographic_preferences=geographic_preferences or [],
            financial_need=financial_need,
        )
        student.personal_info.first_generation = first_generation
        student.updated_at = datetime.now()

        return student

    async def add_test_score(
        self,
        student_id: str,
        test_type: TestType,
        score: float,
        max_score: float,
        date_taken: date,
        subject: str | None = None,
    ) -> Student:
        """Add a test score to the student's record."""
        student = self._students.get(student_id)
        if not student:
            raise ValueError(f"Student {student_id} not found")

        test_score = TestScore(
            test_type=test_type,
            score=score,
            max_score=max_score,
            date_taken=date_taken,
            subject=subject,
        )
        student.academic_record.test_scores.append(test_score)
        student.updated_at = datetime.now()

        return student

    async def add_course(
        self,
        student_id: str,
        name: str,
        subject_area: SubjectArea,
        level: str,
        grade_level: GradeLevel,
        semester: str,
        grade: str | None = None,
        credits: float = 1.0,
    ) -> Student:
        """Add a course to the student's academic record."""
        student = self._students.get(student_id)
        if not student:
            raise ValueError(f"Student {student_id} not found")

        course = Course(
            name=name,
            subject_area=subject_area,
            level=level,
            grade=grade,
            credits=credits,
            grade_level=grade_level,
            semester=semester,
        )
        student.academic_record.courses.append(course)
        student.updated_at = datetime.now()

        return student

    async def add_interest(
        self,
        student_id: str,
        area: SubjectArea,
        level: InterestLevel,
        years_of_engagement: float = 0,
        notes: str = "",
    ) -> Student:
        """Add an interest to the student's profile."""
        student = self._students.get(student_id)
        if not student:
            raise ValueError(f"Student {student_id} not found")

        interest = Interest(
            area=area,
            level=level,
            years_of_engagement=years_of_engagement,
            notes=notes,
        )
        student.interests.append(interest)
        student.updated_at = datetime.now()

        return student

    async def conduct_interest_inventory(
        self,
        student_id: str,
        responses: dict[str, Any],
    ) -> InterestInventory:
        """Conduct an AI-powered interest inventory assessment."""
        student = self._students.get(student_id)
        if not student:
            raise ValueError(f"Student {student_id} not found")

        prompt = f"""Based on the following student information and responses,
analyze their interests and create a comprehensive interest inventory.

Student: {student.personal_info.full_name}
Current Grade: {student.current_grade.value}
Current Courses: {[c.name for c in student.academic_record.courses]}
Existing Interests: {[(i.area.value, i.level.value) for i in student.interests]}

Survey Responses:
{responses}

Identify:
1. Top 3-5 academic subject areas they are drawn to
2. Career clusters that align with their interests
3. Types of activities they would enjoy
4. Passion areas - topics they could talk about for hours
5. Areas they actively avoid or dislike
"""

        result = await self.ai_engine.generate_structured(
            prompt=prompt,
            response_model=InterestInventory,
            system_prompt="You are an expert educational psychologist specializing in student interest assessment.",
        )

        return result

    async def assess_personality(
        self,
        student_id: str,
        questionnaire_responses: dict[str, Any],
    ) -> PersonalityProfile:
        """Conduct personality assessment for learning and planning."""
        student = self._students.get(student_id)
        if not student:
            raise ValueError(f"Student {student_id} not found")

        prompt = f"""Based on the following questionnaire responses, create a personality
profile focused on learning style, work habits, and college readiness.

Student: {student.personal_info.full_name}
Responses: {questionnaire_responses}

Analyze:
1. Key strengths (3-5 traits)
2. Work style preference (Independent/Collaborative/Mixed)
3. Learning style (Visual/Auditory/Kinesthetic/Reading-Writing)
4. Risk tolerance in college choices (Conservative/Moderate/Ambitious)
5. Time management style
6. Leadership tendency
7. Creativity vs analytical balance
8. Stress management approach
"""

        result = await self.ai_engine.generate_structured(
            prompt=prompt,
            response_model=PersonalityProfile,
            system_prompt="You are an expert in educational psychology and personality assessment.",
        )

        return result

    async def assess_academics(
        self,
        student_id: str,
    ) -> AcademicAssessment:
        """Analyze academic strengths and weaknesses."""
        student = self._students.get(student_id)
        if not student:
            raise ValueError(f"Student {student_id} not found")

        courses_info = [
            {
                "name": c.name,
                "subject": c.subject_area.value,
                "level": c.level,
                "grade": c.grade,
                "year": c.grade_level.value,
            }
            for c in student.academic_record.courses
        ]

        test_info = [
            {
                "test": t.test_type.value,
                "score": t.score,
                "max": t.max_score,
                "subject": t.subject,
            }
            for t in student.academic_record.test_scores
        ]

        prompt = f"""Analyze this student's academic profile:

GPA: {student.academic_record.cumulative_gpa} (Weighted: {student.academic_record.weighted_gpa})
Class Rank: {student.academic_record.class_rank} of {student.academic_record.class_size}

Courses Taken:
{courses_info}

Test Scores:
{test_info}

Provide:
1. Strong subjects (where they excel)
2. Developing subjects (need improvement)
3. Recommended focus areas for improvement
4. GPA trajectory assessment
5. Course rigor evaluation
6. Testing readiness evaluation
"""

        result = await self.ai_engine.generate_structured(
            prompt=prompt,
            response_model=AcademicAssessment,
            system_prompt="You are an expert academic counselor analyzing student performance.",
        )

        return result

    async def set_goals(
        self,
        student_id: str,
        dream_schools: list[str] | None = None,
        intended_majors: list[str] | None = None,
        career_aspirations: list[str] | None = None,
    ) -> GoalFramework:
        """Help student set goals with AI-powered suggestions."""
        student = self._students.get(student_id)
        if not student:
            raise ValueError(f"Student {student_id} not found")

        if dream_schools:
            student.intended_majors = intended_majors or student.intended_majors
        if career_aspirations:
            student.career_interests = career_aspirations

        prompt = f"""Help this student develop a goal framework:

Student: {student.personal_info.full_name}
Grade: {student.current_grade.value}
Graduation Year: {student.personal_info.graduation_year}
Interests: {[i.area.value for i in student.interests if i.level in [InterestLevel.PASSIONATE, InterestLevel.COMMITTED]]}
Dream Schools: {dream_schools or 'Not specified'}
Intended Majors: {intended_majors or 'Exploring'}
Career Aspirations: {career_aspirations or 'Exploring'}

Create:
1. Realistic short-term goals (this semester)
2. Medium-term goals (this academic year)
3. Long-term goals (by graduation)
4. Non-negotiables for college selection
"""

        result = await self.ai_engine.generate_structured(
            prompt=prompt,
            response_model=GoalFramework,
            system_prompt="You are an expert college counselor helping students set achievable goals.",
        )

        # Update with provided values
        result.dream_schools = dream_schools or []
        result.intended_majors = intended_majors or []
        result.career_aspirations = career_aspirations or []

        return result

    async def conduct_full_assessment(
        self,
        student_id: str,
        interest_responses: dict[str, Any],
        personality_responses: dict[str, Any],
        goals: dict[str, list[str]],
    ) -> ProfileAssessmentResult:
        """Conduct a complete profile assessment."""
        student = self._students.get(student_id)
        if not student:
            raise ValueError(f"Student {student_id} not found")

        # Run all assessments
        interests = await self.conduct_interest_inventory(student_id, interest_responses)
        personality = await self.assess_personality(student_id, personality_responses)
        academic = await self.assess_academics(student_id)
        goal_framework = await self.set_goals(
            student_id,
            dream_schools=goals.get("dream_schools"),
            intended_majors=goals.get("intended_majors"),
            career_aspirations=goals.get("career_aspirations"),
        )

        # Generate recommendations
        prompt = f"""Based on this complete student assessment, provide initial recommendations:

Interests: {interests.model_dump()}
Personality: {personality.model_dump()}
Academic Assessment: {academic.model_dump()}
Goals: {goal_framework.model_dump()}

Provide:
1. 5-7 initial recommendations for immediate action
2. 3-5 areas they should explore further
"""

        response = await self.ai_engine.generate_text(prompt)

        # Parse recommendations from response (simplified)
        recommendations = [
            "Focus on strengthening core academic performance",
            "Begin exploring extracurricular activities aligned with interests",
            "Start researching potential colleges and programs",
            "Develop a standardized testing preparation plan",
            "Build relationships with potential recommenders",
        ]

        areas_to_explore = [
            "Summer programs in areas of interest",
            "Leadership opportunities in current activities",
            "Research or project opportunities",
        ]

        return ProfileAssessmentResult(
            personality=personality,
            interests=interests,
            academic=academic,
            goals=goal_framework,
            initial_recommendations=recommendations,
            areas_to_explore=areas_to_explore,
        )

    async def get_student(self, student_id: str) -> Student | None:
        """Retrieve a student profile."""
        return self._students.get(student_id)

    async def update_student(self, student: Student) -> Student:
        """Update a student profile."""
        student.updated_at = datetime.now()
        self._students[student.id] = student
        return student

    async def generate_profile_summary(self, student_id: str) -> str:
        """Generate a narrative summary of the student's profile."""
        student = self._students.get(student_id)
        if not student:
            raise ValueError(f"Student {student_id} not found")

        prompt = f"""Create a comprehensive summary of this student's profile:

Personal Info:
- Name: {student.personal_info.full_name}
- School: {student.personal_info.high_school}
- Grade: {student.current_grade.value}
- Graduation: {student.personal_info.graduation_year}

Academic Record:
- GPA: {student.academic_record.cumulative_gpa}
- Courses: {len(student.academic_record.courses)} total
- Test Scores: {[(t.test_type.value, t.score) for t in student.academic_record.test_scores]}

Interests: {[(i.area.value, i.level.value) for i in student.interests]}

Activities: {len(student.activities)} activities
Competitions: {len(student.competitions)} competitions
Summer Programs: {len(student.summer_programs)} programs

Goals:
- Intended Majors: {student.intended_majors}
- Career Interests: {student.career_interests}

Write a 2-3 paragraph narrative summary highlighting key strengths,
areas for development, and strategic recommendations.
"""

        return await self.ai_engine.generate_text(
            prompt=prompt,
            system_prompt="You are an expert college counselor writing a student profile summary.",
        )
