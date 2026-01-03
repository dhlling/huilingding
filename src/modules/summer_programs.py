"""Module 4: Summer Programs & Opportunities Engine.

This module handles:
- Pre-college programs matching
- Research opportunities
- Internship recommendations
- Volunteer programs
- International experiences
"""

from datetime import date
from typing import Any
from pydantic import BaseModel, Field
import uuid

from src.core.base import BaseModule, AIEngine
from src.core.models import Student, SummerProgram
from src.core.enums import (
    ProgramType,
    GradeLevel,
    SubjectArea,
)


class ProgramDetails(BaseModel):
    """Detailed information about a summer program."""
    id: str
    name: str
    program_type: ProgramType
    institution: str
    location: str
    duration_weeks: int
    cost: int  # in USD, 0 for free
    financial_aid_available: bool
    selectivity: str  # Open, Selective, Highly Selective
    acceptance_rate: float | None
    application_deadline: str
    eligibility: str  # Grade levels
    subject_areas: list[SubjectArea]
    description: str
    benefits: list[str]
    application_requirements: list[str]
    website: str


class ProgramRecommendation(BaseModel):
    """A recommended program for a student."""
    program: ProgramDetails
    match_score: float
    reasons: list[str]
    considerations: list[str]
    application_tips: list[str]


class SummerPlan(BaseModel):
    """Recommended summer plan for a specific year."""
    year: int
    grade_after: GradeLevel
    primary_program: ProgramRecommendation | None
    backup_programs: list[ProgramRecommendation]
    self_directed_options: list[str]
    timeline: list[dict[str, str]]
    budget_estimate: int


class FourSummerStrategy(BaseModel):
    """Complete summer strategy across high school years."""
    student_id: str
    freshman_summer: SummerPlan
    sophomore_summer: SummerPlan
    junior_summer: SummerPlan
    overall_theme: str
    progression_narrative: str
    total_estimated_cost: int


class SummerProgramsModule(BaseModule):
    """Module for summer program recommendations and planning."""

    @property
    def name(self) -> str:
        return "Summer Programs & Opportunities Engine"

    @property
    def description(self) -> str:
        return "Pre-college programs, research, internships, and summer opportunity matching"

    # Sample program database
    PROGRAMS_DATABASE: list[dict[str, Any]] = [
        # STEM Research Programs
        {
            "id": "rsi",
            "name": "Research Science Institute (RSI)",
            "program_type": ProgramType.RESEARCH,
            "institution": "MIT/CEE",
            "location": "Cambridge, MA",
            "duration_weeks": 6,
            "cost": 0,
            "financial_aid_available": True,
            "selectivity": "Highly Selective",
            "acceptance_rate": 0.03,
            "application_deadline": "January",
            "eligibility": "Rising Seniors",
            "subject_areas": [SubjectArea.PHYSICS, SubjectArea.MATHEMATICS, SubjectArea.BIOLOGY,
                              SubjectArea.CHEMISTRY, SubjectArea.COMPUTER_SCIENCE],
            "description": "Prestigious free summer research program at MIT",
            "benefits": ["Conduct original research", "Top tier mentorship", "Strong alumni network"],
            "application_requirements": ["Transcripts", "Essays", "Recommendations", "Test scores"],
        },
        {
            "id": "ssp",
            "name": "Summer Science Program",
            "program_type": ProgramType.RESEARCH,
            "institution": "SSP",
            "location": "Multiple (CO, NM, NC)",
            "duration_weeks": 5,
            "cost": 7500,
            "financial_aid_available": True,
            "selectivity": "Highly Selective",
            "acceptance_rate": 0.10,
            "application_deadline": "February",
            "eligibility": "Rising Juniors and Seniors",
            "subject_areas": [SubjectArea.PHYSICS, SubjectArea.MATHEMATICS, SubjectArea.BIOLOGY],
            "description": "Rigorous research program in astrophysics, biochemistry, or genomics",
            "benefits": ["Hands-on research", "Strong community", "College prep"],
            "application_requirements": ["Application", "Essays", "Transcripts", "Recommendations"],
        },
        {
            "id": "cosmos",
            "name": "COSMOS (California)",
            "program_type": ProgramType.PRE_COLLEGE,
            "institution": "UC System",
            "location": "California (multiple UC campuses)",
            "duration_weeks": 4,
            "cost": 4000,
            "financial_aid_available": True,
            "selectivity": "Selective",
            "acceptance_rate": 0.25,
            "application_deadline": "February",
            "eligibility": "Grades 8-12",
            "subject_areas": [SubjectArea.PHYSICS, SubjectArea.MATHEMATICS, SubjectArea.BIOLOGY,
                              SubjectArea.ENGINEERING, SubjectArea.COMPUTER_SCIENCE],
            "description": "UC summer STEM program for California residents",
            "benefits": ["UC experience", "Research exposure", "STEM community"],
            "application_requirements": ["Application", "Essays", "Transcripts"],
        },
        # Pre-College Programs
        {
            "id": "yale_yygs",
            "name": "Yale Young Global Scholars (YYGS)",
            "program_type": ProgramType.PRE_COLLEGE,
            "institution": "Yale University",
            "location": "New Haven, CT",
            "duration_weeks": 2,
            "cost": 6500,
            "financial_aid_available": True,
            "selectivity": "Selective",
            "acceptance_rate": 0.20,
            "application_deadline": "Rolling",
            "eligibility": "Rising Juniors and Seniors",
            "subject_areas": [SubjectArea.HISTORY, SubjectArea.ECONOMICS, SubjectArea.BIOLOGY],
            "description": "Interdisciplinary academic program at Yale",
            "benefits": ["Seminars with Yale faculty", "Global peer network", "Ivy exposure"],
            "application_requirements": ["Application", "Essays", "Transcripts"],
        },
        {
            "id": "stanford_sumac",
            "name": "Stanford SUMAC",
            "program_type": ProgramType.PRE_COLLEGE,
            "institution": "Stanford University",
            "location": "Stanford, CA",
            "duration_weeks": 3,
            "cost": 0,
            "financial_aid_available": True,
            "selectivity": "Highly Selective",
            "acceptance_rate": 0.08,
            "application_deadline": "February",
            "eligibility": "Rising Seniors",
            "subject_areas": [SubjectArea.MATHEMATICS],
            "description": "Intensive mathematics program at Stanford",
            "benefits": ["Advanced math", "Stanford experience", "Free program"],
            "application_requirements": ["Application", "Math background", "Essays"],
        },
        # Internships
        {
            "id": "google_cssi",
            "name": "Google CSSI",
            "program_type": ProgramType.INTERNSHIP,
            "institution": "Google",
            "location": "Various US locations",
            "duration_weeks": 4,
            "cost": 0,
            "financial_aid_available": True,
            "selectivity": "Selective",
            "acceptance_rate": 0.15,
            "application_deadline": "March",
            "eligibility": "Rising College Freshmen (apply senior year)",
            "subject_areas": [SubjectArea.COMPUTER_SCIENCE],
            "description": "Computer science intensive for underrepresented groups",
            "benefits": ["Industry experience", "Google mentorship", "Stipend provided"],
            "application_requirements": ["Application", "Coding experience", "Essays"],
        },
        # Volunteer/Service
        {
            "id": "habitat",
            "name": "Habitat for Humanity",
            "program_type": ProgramType.VOLUNTEER,
            "institution": "Habitat for Humanity",
            "location": "Various",
            "duration_weeks": 1,
            "cost": 1500,
            "financial_aid_available": True,
            "selectivity": "Open",
            "acceptance_rate": 0.90,
            "application_deadline": "Rolling",
            "eligibility": "Ages 16+",
            "subject_areas": [],
            "description": "Service-learning building homes for families in need",
            "benefits": ["Community impact", "Teamwork skills", "Meaningful service"],
            "application_requirements": ["Application"],
        },
    ]

    def __init__(self, ai_engine: AIEngine):
        super().__init__(ai_engine)
        self._programs = {p["id"]: ProgramDetails(**{**p, "website": ""})
                          for p in self.PROGRAMS_DATABASE}

    async def get_all_programs(
        self,
        filters: dict[str, Any] | None = None,
    ) -> list[ProgramDetails]:
        """Get all programs, optionally filtered."""
        programs = list(self._programs.values())

        if filters:
            if "program_type" in filters:
                programs = [p for p in programs if p.program_type == filters["program_type"]]
            if "subject_area" in filters:
                programs = [p for p in programs
                            if filters["subject_area"] in p.subject_areas]
            if "max_cost" in filters:
                programs = [p for p in programs if p.cost <= filters["max_cost"]]
            if "selectivity" in filters:
                programs = [p for p in programs if p.selectivity == filters["selectivity"]]

        return programs

    async def recommend_programs(
        self,
        student: Student,
        summer_year: int,
        count: int = 5,
        budget: int | None = None,
    ) -> list[ProgramRecommendation]:
        """Recommend summer programs for a student."""
        # Calculate which grade they'll be after this summer
        years_until_grad = student.personal_info.graduation_year - summer_year
        grade_after_map = {3: GradeLevel.SOPHOMORE, 2: GradeLevel.JUNIOR,
                          1: GradeLevel.SENIOR, 0: GradeLevel.SENIOR}
        grade_after = grade_after_map.get(years_until_grad, GradeLevel.FRESHMAN)

        # Get student's strong subjects
        strong_subjects = [
            i.area for i in student.interests
            if i.level.value in ['passionate', 'committed']
        ]

        recommendations = []

        for program in self._programs.values():
            # Check budget constraint
            if budget and program.cost > budget and not program.financial_aid_available:
                continue

            # Calculate match score
            score = 0.0

            # Subject alignment
            matching_subjects = set(program.subject_areas) & set(strong_subjects)
            score += len(matching_subjects) * 15

            # Academic strength match
            if student.academic_record.cumulative_gpa >= 3.8:
                if program.selectivity == "Highly Selective":
                    score += 20
            elif student.academic_record.cumulative_gpa >= 3.5:
                if program.selectivity in ["Selective", "Highly Selective"]:
                    score += 15
            else:
                if program.selectivity == "Open":
                    score += 20

            # Program type preference based on grade
            if grade_after == GradeLevel.SOPHOMORE:
                if program.program_type in [ProgramType.CAMP, ProgramType.PRE_COLLEGE]:
                    score += 10
            elif grade_after == GradeLevel.JUNIOR:
                if program.program_type in [ProgramType.PRE_COLLEGE, ProgramType.RESEARCH]:
                    score += 10
            elif grade_after == GradeLevel.SENIOR:
                if program.program_type in [ProgramType.RESEARCH, ProgramType.INTERNSHIP]:
                    score += 10

            # Free programs bonus
            if program.cost == 0:
                score += 10

            if score > 0:
                recommendations.append(ProgramRecommendation(
                    program=program,
                    match_score=min(score, 100),
                    reasons=[
                        f"Aligns with your interest in {', '.join(s.value for s in matching_subjects)}"
                        if matching_subjects else "Provides valuable experience",
                        f"Appropriate selectivity for your profile",
                    ],
                    considerations=[
                        f"Cost: ${program.cost}" if program.cost > 0 else "Free program",
                        f"Application deadline: {program.application_deadline}",
                    ],
                    application_tips=[
                        "Start application early",
                        "Highlight relevant experience and passion",
                    ],
                ))

        # Sort by match score and return top N
        recommendations.sort(key=lambda x: x.match_score, reverse=True)
        return recommendations[:count]

    async def find_research_opportunities(
        self,
        student: Student,
        local_only: bool = False,
    ) -> list[dict[str, Any]]:
        """Find research opportunities for a student."""
        prompt = f"""Find research opportunities for this student:

Student Profile:
- Grade: {student.current_grade.value}
- GPA: {student.academic_record.cumulative_gpa}
- Interests: {[i.area.value for i in student.interests if i.level.value in ['passionate', 'committed']]}
- Intended Major: {student.intended_majors}
- Location: {student.personal_info.state}

Types of research opportunities to consider:
1. University summer research programs
2. Local professor mentorship
3. Hospital/lab internships
4. Online research programs
5. Independent research projects

For each opportunity type, provide:
- How to find opportunities
- How to approach professors/mentors
- What to prepare
- Timeline for applications
- Tips for success
"""

        response = await self.ai_engine.generate_text(prompt)

        return [
            {
                "type": "University Research Programs",
                "examples": ["RSI", "SSP", "COSMOS"],
                "how_to_apply": "Formal applications typically due January-February",
                "tips": ["Start early", "Strong recommendations needed"],
            },
            {
                "type": "Local Professor Mentorship",
                "examples": ["Cold email professors at nearby universities"],
                "how_to_apply": "Email professors directly with your interests",
                "tips": ["Be specific about interests", "Show prior knowledge"],
            },
            {
                "type": "Independent Research",
                "examples": ["Science fair projects", "Original investigations"],
                "how_to_apply": "Self-directed with mentor guidance",
                "tips": ["Start with a question you're passionate about"],
            },
        ]

    async def create_summer_plan(
        self,
        student: Student,
        year: int,
        budget: int | None = None,
    ) -> SummerPlan:
        """Create a detailed summer plan for a specific year."""
        recommendations = await self.recommend_programs(student, year, count=5, budget=budget)

        years_until_grad = student.personal_info.graduation_year - year
        grade_map = {3: GradeLevel.SOPHOMORE, 2: GradeLevel.JUNIOR,
                     1: GradeLevel.SENIOR, 0: GradeLevel.SENIOR}
        grade_after = grade_map.get(years_until_grad, GradeLevel.FRESHMAN)

        primary = recommendations[0] if recommendations else None
        backups = recommendations[1:3] if len(recommendations) > 1 else []

        return SummerPlan(
            year=year,
            grade_after=grade_after,
            primary_program=primary,
            backup_programs=backups,
            self_directed_options=[
                "Start an independent project related to your interests",
                "Read widely in your field of interest",
                "Take online courses (Coursera, edX, etc.)",
                "Work part-time for real-world experience",
                "Volunteer in your community",
            ],
            timeline=[
                {"month": "January", "action": "Submit applications for competitive programs"},
                {"month": "February", "action": "Apply to backup programs"},
                {"month": "March", "action": "Wait for decisions, prepare backup plans"},
                {"month": "April-May", "action": "Confirm enrollment, make travel arrangements"},
                {"month": "June-August", "action": "Participate in programs"},
            ],
            budget_estimate=primary.program.cost if primary else 0,
        )

    async def create_four_summer_strategy(
        self,
        student: Student,
        annual_budget: int | None = None,
    ) -> FourSummerStrategy:
        """Create a comprehensive summer strategy for all four years."""
        grad_year = student.personal_info.graduation_year

        freshman_summer = await self.create_summer_plan(
            student, grad_year - 3, annual_budget)
        sophomore_summer = await self.create_summer_plan(
            student, grad_year - 2, annual_budget)
        junior_summer = await self.create_summer_plan(
            student, grad_year - 1, annual_budget)

        # Calculate total cost
        total_cost = (
            (freshman_summer.primary_program.program.cost if freshman_summer.primary_program else 0) +
            (sophomore_summer.primary_program.program.cost if sophomore_summer.primary_program else 0) +
            (junior_summer.primary_program.program.cost if junior_summer.primary_program else 0)
        )

        prompt = f"""Create a narrative explaining this student's summer strategy:

Student: {student.personal_info.full_name}
Interests: {[i.area.value for i in student.interests]}
Intended Major: {student.intended_majors}

Freshman Summer: {freshman_summer.primary_program.program.name if freshman_summer.primary_program else 'Self-directed exploration'}
Sophomore Summer: {sophomore_summer.primary_program.program.name if sophomore_summer.primary_program else 'Building skills'}
Junior Summer: {junior_summer.primary_program.program.name if junior_summer.primary_program else 'Advanced experience'}

Write:
1. An overall theme connecting these experiences
2. A narrative explaining the progression
"""

        response = await self.ai_engine.generate_text(prompt)

        return FourSummerStrategy(
            student_id=student.id,
            freshman_summer=freshman_summer,
            sophomore_summer=sophomore_summer,
            junior_summer=junior_summer,
            overall_theme="Progressive deepening of expertise and experience",
            progression_narrative=response,
            total_estimated_cost=total_cost,
        )

    async def add_program_to_student(
        self,
        student: Student,
        program_id: str,
        year: int,
    ) -> SummerProgram:
        """Add a completed program to the student's profile."""
        program_details = self._programs.get(program_id)
        if not program_details:
            raise ValueError(f"Program {program_id} not found")

        summer_program = SummerProgram(
            id=str(uuid.uuid4()),
            name=program_details.name,
            program_type=program_details.program_type,
            institution=program_details.institution,
            year=year,
            duration_weeks=program_details.duration_weeks,
            description=program_details.description,
            selective=program_details.selectivity in ["Selective", "Highly Selective"],
            paid=program_details.cost > 0,
        )

        student.summer_programs.append(summer_program)
        return summer_program

    async def generate_application_strategy(
        self,
        student: Student,
        target_programs: list[str],
    ) -> dict[str, Any]:
        """Generate an application strategy for target programs."""
        prompt = f"""Create an application strategy for these summer programs:

Student Profile:
- Name: {student.personal_info.full_name}
- GPA: {student.academic_record.cumulative_gpa}
- Interests: {[i.area.value for i in student.interests]}
- Activities: {[a.name for a in student.activities[:5]]}

Target Programs: {target_programs}

For each program, provide:
1. Key application components
2. How to make the application stand out
3. Common mistakes to avoid
4. Timeline for preparation
5. How to approach essays/short answers
"""

        response = await self.ai_engine.generate_text(prompt)

        return {
            "overall_strategy": response,
            "timeline": [
                {"deadline": "October", "action": "Research programs and requirements"},
                {"deadline": "November", "action": "Request recommendations"},
                {"deadline": "December", "action": "Draft essays"},
                {"deadline": "January", "action": "Submit applications"},
                {"deadline": "March-April", "action": "Await decisions"},
            ],
            "tips": [
                "Start essays early and revise multiple times",
                "Ask teachers for recommendations well in advance",
                "Have someone review your application",
                "Apply to a mix of selectivity levels",
            ],
        }
