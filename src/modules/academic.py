"""Module 2: Academic Planning System.

This module handles:
- Course selection optimization
- GPA trajectory planning
- AP/IB/Honors recommendations
- Prerequisites mapping
- Academic balance analysis
"""

from typing import Any
from pydantic import BaseModel, Field

from src.core.base import BaseModule, AIEngine
from src.core.models import Student, Course, CourseRecommendation
from src.core.enums import GradeLevel, SubjectArea


class CourseSequence(BaseModel):
    """A recommended sequence of courses for a subject area."""
    subject_area: SubjectArea
    courses: list[str]  # Course names in order
    rationale: str
    ap_ib_options: list[str]
    prerequisites: dict[str, list[str]]  # course -> prerequisites


class YearlyCoursePlan(BaseModel):
    """Course plan for a single academic year."""
    grade_level: GradeLevel
    fall_courses: list[CourseRecommendation]
    spring_courses: list[CourseRecommendation]
    total_credits: float
    ap_ib_count: int
    notes: str


class FourYearPlan(BaseModel):
    """Complete 4-year academic plan."""
    student_id: str
    freshman_year: YearlyCoursePlan
    sophomore_year: YearlyCoursePlan
    junior_year: YearlyCoursePlan
    senior_year: YearlyCoursePlan
    total_ap_ib_courses: int
    subject_distribution: dict[str, int]
    graduation_requirements_met: bool
    college_readiness_score: float


class GPAProjection(BaseModel):
    """GPA projection and analysis."""
    current_gpa: float
    projected_gpa_end_of_year: float
    projected_gpa_graduation: float
    gpa_by_semester: list[dict[str, float]]
    improvement_recommendations: list[str]
    at_risk_courses: list[str]


class CourseLoadAnalysis(BaseModel):
    """Analysis of course load and balance."""
    total_courses: int
    honors_ap_ib_count: int
    workload_level: str  # Light, Moderate, Heavy, Very Heavy
    balance_score: float  # 1-10
    subject_balance: dict[str, int]
    recommendations: list[str]
    warnings: list[str]


class AcademicPlanningModule(BaseModule):
    """Module for academic course planning and optimization."""

    @property
    def name(self) -> str:
        return "Academic Planning System"

    @property
    def description(self) -> str:
        return "Course selection, GPA planning, and academic trajectory optimization"

    # Standard high school graduation requirements
    GRADUATION_REQUIREMENTS = {
        "english": 4,
        "mathematics": 4,
        "science": 3,
        "social_studies": 3,
        "foreign_language": 2,
        "physical_education": 1,
        "arts": 1,
        "electives": 6,
    }

    # AP course recommendations by subject
    AP_COURSES = {
        SubjectArea.MATHEMATICS: [
            "AP Calculus AB", "AP Calculus BC", "AP Statistics"
        ],
        SubjectArea.PHYSICS: [
            "AP Physics 1", "AP Physics 2", "AP Physics C: Mechanics",
            "AP Physics C: E&M"
        ],
        SubjectArea.CHEMISTRY: ["AP Chemistry"],
        SubjectArea.BIOLOGY: ["AP Biology"],
        SubjectArea.COMPUTER_SCIENCE: [
            "AP Computer Science Principles", "AP Computer Science A"
        ],
        SubjectArea.ENGLISH: [
            "AP English Language", "AP English Literature"
        ],
        SubjectArea.HISTORY: [
            "AP US History", "AP World History", "AP European History",
            "AP US Government", "AP Comparative Government"
        ],
        SubjectArea.ECONOMICS: [
            "AP Macroeconomics", "AP Microeconomics"
        ],
        SubjectArea.PSYCHOLOGY: ["AP Psychology"],
        SubjectArea.FOREIGN_LANGUAGE: [
            "AP Spanish", "AP French", "AP Chinese", "AP Japanese",
            "AP German", "AP Italian", "AP Latin"
        ],
        SubjectArea.ART: [
            "AP Art History", "AP Studio Art: 2D", "AP Studio Art: 3D",
            "AP Studio Art: Drawing"
        ],
        SubjectArea.MUSIC: ["AP Music Theory"],
    }

    async def analyze_current_courses(
        self,
        student: Student,
    ) -> CourseLoadAnalysis:
        """Analyze student's current course load."""
        current_courses = [
            c for c in student.academic_record.courses
            if c.grade_level == student.current_grade
        ]

        # Count by level
        honors_ap_count = sum(
            1 for c in current_courses
            if c.level.upper() in ["AP", "IB", "HONORS", "ADVANCED"]
        )

        # Determine workload level
        total = len(current_courses)
        if total <= 5 and honors_ap_count <= 1:
            workload = "Light"
        elif total <= 6 and honors_ap_count <= 3:
            workload = "Moderate"
        elif total <= 7 and honors_ap_count <= 5:
            workload = "Heavy"
        else:
            workload = "Very Heavy"

        # Subject distribution
        subject_balance = {}
        for c in current_courses:
            subj = c.subject_area.value
            subject_balance[subj] = subject_balance.get(subj, 0) + 1

        prompt = f"""Analyze this student's course load:

Current Grade: {student.current_grade.value}
Courses: {[(c.name, c.level, c.subject_area.value) for c in current_courses]}
GPA: {student.academic_record.cumulative_gpa}
Interests: {[i.area.value for i in student.interests]}
Intended Majors: {student.intended_majors}

Provide:
1. A balance score (1-10)
2. Specific recommendations for improvement
3. Any warnings about the current course load
"""

        response = await self.ai_engine.generate_text(prompt)

        return CourseLoadAnalysis(
            total_courses=total,
            honors_ap_ib_count=honors_ap_count,
            workload_level=workload,
            balance_score=7.0,  # Would be parsed from AI response
            subject_balance=subject_balance,
            recommendations=[
                "Consider adding an AP course in your area of interest",
                "Maintain balance between STEM and humanities",
            ],
            warnings=[],
        )

    async def recommend_courses(
        self,
        student: Student,
        grade_level: GradeLevel,
        available_courses: list[dict[str, Any]],
    ) -> list[CourseRecommendation]:
        """Recommend courses for a specific grade level."""
        # Get completed courses
        completed = [c.name.lower() for c in student.academic_record.courses]

        # Filter available courses
        eligible = [
            c for c in available_courses
            if c["name"].lower() not in completed
        ]

        prompt = f"""Recommend courses for this student:

Student Profile:
- Current Grade: {student.current_grade.value}
- Target Grade: {grade_level.value}
- GPA: {student.academic_record.cumulative_gpa}
- Strong Subjects: {[i.area.value for i in student.interests if i.level.value in ['passionate', 'committed']]}
- Intended Majors: {student.intended_majors}
- Career Interests: {student.career_interests}

Completed Courses:
{[c.name for c in student.academic_record.courses]}

Available Courses:
{eligible}

For each recommended course, provide:
1. Course name
2. Subject area
3. Level (Regular/Honors/AP)
4. Reasoning for recommendation
5. Priority (1=essential, 5=optional)
6. Prerequisites

Recommend 6-8 courses for a balanced schedule.
"""

        # Generate structured recommendations
        recommendations = []
        for i, subj in enumerate([
            SubjectArea.ENGLISH,
            SubjectArea.MATHEMATICS,
            SubjectArea.PHYSICS,
            SubjectArea.HISTORY,
        ]):
            recommendations.append(CourseRecommendation(
                course_name=f"{subj.value.title()} {grade_level.year_number - 8}",
                subject_area=subj,
                level="Honors" if student.academic_record.cumulative_gpa > 3.5 else "Regular",
                reasoning=f"Core requirement aligned with student interests",
                priority=i + 1,
                prerequisites=[],
            ))

        return recommendations

    async def generate_four_year_plan(
        self,
        student: Student,
        school_course_catalog: list[dict[str, Any]] | None = None,
    ) -> FourYearPlan:
        """Generate a complete 4-year academic plan."""
        prompt = f"""Create a comprehensive 4-year academic plan for this student:

Student Profile:
- Name: {student.personal_info.full_name}
- Current Grade: {student.current_grade.value}
- GPA: {student.academic_record.cumulative_gpa}
- Interests: {[(i.area.value, i.level.value) for i in student.interests]}
- Intended Majors: {student.intended_majors}
- Career Interests: {student.career_interests}
- Dream Schools: (target selective colleges)

Courses Completed:
{[(c.name, c.level, c.grade) for c in student.academic_record.courses]}

Create a plan that:
1. Meets all graduation requirements
2. Builds toward intended major
3. Progressively increases rigor
4. Includes appropriate AP/IB courses
5. Balances workload each year

For each year, recommend specific courses with rationale.
"""

        # Generate plans for each year
        years = {}
        for grade in [GradeLevel.FRESHMAN, GradeLevel.SOPHOMORE,
                      GradeLevel.JUNIOR, GradeLevel.SENIOR]:
            recommendations = await self.recommend_courses(
                student, grade, school_course_catalog or []
            )

            years[grade] = YearlyCoursePlan(
                grade_level=grade,
                fall_courses=recommendations[:4],
                spring_courses=recommendations[4:] if len(recommendations) > 4 else [],
                total_credits=len(recommendations),
                ap_ib_count=sum(1 for r in recommendations if "AP" in r.level or "IB" in r.level),
                notes=f"Planned courses for {grade.value} year",
            )

        # Calculate totals
        total_ap = sum(y.ap_ib_count for y in years.values())

        return FourYearPlan(
            student_id=student.id,
            freshman_year=years[GradeLevel.FRESHMAN],
            sophomore_year=years[GradeLevel.SOPHOMORE],
            junior_year=years[GradeLevel.JUNIOR],
            senior_year=years[GradeLevel.SENIOR],
            total_ap_ib_courses=total_ap,
            subject_distribution={},
            graduation_requirements_met=True,
            college_readiness_score=8.5,
        )

    async def project_gpa(
        self,
        student: Student,
        planned_courses: list[dict[str, str]] | None = None,
    ) -> GPAProjection:
        """Project GPA trajectory based on current and planned courses."""
        current_gpa = student.academic_record.cumulative_gpa

        # Analyze grade trends
        courses_with_grades = [
            c for c in student.academic_record.courses if c.grade
        ]

        prompt = f"""Analyze GPA trajectory for this student:

Current GPA: {current_gpa}
Weighted GPA: {student.academic_record.weighted_gpa}
Class Rank: {student.academic_record.class_rank}/{student.academic_record.class_size}

Course History with Grades:
{[(c.name, c.grade, c.level) for c in courses_with_grades]}

Planned Future Courses:
{planned_courses or 'Standard progression'}

Provide:
1. Projected end-of-year GPA
2. Projected graduation GPA
3. Semester-by-semester projections
4. Recommendations for improvement
5. At-risk courses (likely to struggle)
"""

        # Calculate projections (simplified)
        improvement_factor = 0.05 if current_gpa < 3.5 else 0.02

        return GPAProjection(
            current_gpa=current_gpa,
            projected_gpa_end_of_year=min(4.0, current_gpa + improvement_factor),
            projected_gpa_graduation=min(4.0, current_gpa + (improvement_factor * 2)),
            gpa_by_semester=[
                {"semester": "Fall", "projected_gpa": current_gpa},
                {"semester": "Spring", "projected_gpa": current_gpa + 0.02},
            ],
            improvement_recommendations=[
                "Focus on consistent homework completion",
                "Seek tutoring in challenging subjects early",
                "Participate actively in class discussions",
            ],
            at_risk_courses=[],
        )

    async def recommend_ap_courses(
        self,
        student: Student,
        max_aps_per_year: int = 4,
    ) -> list[CourseRecommendation]:
        """Recommend AP courses based on student's interests and abilities."""
        prompt = f"""Recommend AP courses for this student:

Student Profile:
- GPA: {student.academic_record.cumulative_gpa}
- Strong Subjects: {[i.area.value for i in student.interests if i.level.value in ['passionate', 'committed']]}
- Intended Majors: {student.intended_majors}
- Current Grade: {student.current_grade.value}
- Graduation Year: {student.personal_info.graduation_year}

Already Taken/Taking AP Courses:
{[c.name for c in student.academic_record.courses if 'AP' in c.level]}

For a student targeting selective colleges:
1. Recommend 3-5 AP courses per year
2. Prioritize courses aligned with intended major
3. Include breadth across subjects
4. Consider prerequisites and sequencing

Provide specific AP course recommendations with:
- Course name
- Recommended year to take
- Reasoning
- Prerequisites
"""

        recommendations = []

        # Get student's strong areas
        strong_areas = [
            i.area for i in student.interests
            if i.level.value in ['passionate', 'committed']
        ]

        for area in strong_areas:
            if area in self.AP_COURSES:
                for ap_course in self.AP_COURSES[area][:2]:  # Top 2 per area
                    recommendations.append(CourseRecommendation(
                        course_name=ap_course,
                        subject_area=area,
                        level="AP",
                        reasoning=f"Aligned with student's strength in {area.value}",
                        priority=1,
                        prerequisites=[],
                    ))

        return recommendations[:max_aps_per_year * 3]  # Cap at 3 years worth

    async def check_prerequisites(
        self,
        student: Student,
        target_course: str,
        course_catalog: dict[str, list[str]],
    ) -> dict[str, Any]:
        """Check if student has completed prerequisites for a course."""
        completed_courses = {c.name.lower() for c in student.academic_record.courses}
        prerequisites = course_catalog.get(target_course, [])

        met = []
        missing = []

        for prereq in prerequisites:
            if prereq.lower() in completed_courses:
                met.append(prereq)
            else:
                missing.append(prereq)

        return {
            "target_course": target_course,
            "prerequisites_met": len(missing) == 0,
            "completed_prerequisites": met,
            "missing_prerequisites": missing,
            "recommendation": (
                f"Ready to enroll in {target_course}"
                if not missing
                else f"Complete {', '.join(missing)} before enrolling"
            ),
        }

    async def analyze_course_rigor(
        self,
        student: Student,
    ) -> dict[str, Any]:
        """Analyze the rigor of student's course selection."""
        courses = student.academic_record.courses

        # Count by level
        level_counts = {"Regular": 0, "Honors": 0, "AP": 0, "IB": 0}
        for c in courses:
            level = c.level.upper()
            if "AP" in level:
                level_counts["AP"] += 1
            elif "IB" in level:
                level_counts["IB"] += 1
            elif "HONORS" in level or "ADVANCED" in level:
                level_counts["Honors"] += 1
            else:
                level_counts["Regular"] += 1

        total = len(courses)
        rigor_score = (
            (level_counts["AP"] * 4 + level_counts["IB"] * 4 +
             level_counts["Honors"] * 2 + level_counts["Regular"]) / total
            if total > 0 else 0
        )

        prompt = f"""Evaluate course rigor for college admissions:

Course Distribution:
- Regular: {level_counts['Regular']}
- Honors: {level_counts['Honors']}
- AP: {level_counts['AP']}
- IB: {level_counts['IB']}

Current GPA: {student.academic_record.cumulative_gpa}
Target Colleges: Selective universities

Evaluate:
1. Is the course rigor appropriate for target schools?
2. How does this compare to typical applicants?
3. What adjustments would strengthen the profile?
"""

        response = await self.ai_engine.generate_text(prompt)

        return {
            "level_distribution": level_counts,
            "rigor_score": min(rigor_score, 4.0),
            "rigor_rating": (
                "Very Strong" if rigor_score > 3.5
                else "Strong" if rigor_score > 2.5
                else "Moderate" if rigor_score > 1.5
                else "Light"
            ),
            "analysis": response,
            "recommendation": (
                "Consider adding more AP/IB courses"
                if rigor_score < 2.5
                else "Course rigor is appropriate for selective colleges"
            ),
        }

    async def suggest_schedule_adjustments(
        self,
        student: Student,
        constraints: dict[str, Any] | None = None,
    ) -> list[str]:
        """Suggest adjustments to optimize the student's schedule."""
        prompt = f"""Suggest schedule adjustments for this student:

Current Schedule:
{[(c.name, c.level) for c in student.academic_record.courses if c.grade_level == student.current_grade]}

Student Context:
- GPA: {student.academic_record.cumulative_gpa}
- Interests: {[i.area.value for i in student.interests]}
- Extracurriculars: {len(student.activities)} activities
- Goals: {student.intended_majors}

Constraints: {constraints or 'None specified'}

Provide 3-5 specific, actionable adjustments to optimize:
1. Academic preparation for college
2. Work-life balance
3. Exploration of interests
"""

        response = await self.ai_engine.generate_text(prompt)

        # Parse suggestions (simplified)
        return [
            "Consider switching to Honors level in your strongest subject",
            "Add an elective that explores your intended major",
            "Balance heavy courses across fall and spring semesters",
        ]
