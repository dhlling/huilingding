"""Module 3: Extracurricular & Competition Advisor.

This module handles:
- Activity recommendations based on interests
- Competition matching (Olympiads, Science Fairs, Debate, etc.)
- Leadership opportunity identification
- Time commitment balancing
- Spike development strategy
"""

from typing import Any
from pydantic import BaseModel, Field
import uuid

from src.core.base import BaseModule, AIEngine
from src.core.models import Student, Activity, Competition, ActivityRecommendation
from src.core.enums import (
    ActivityCategory,
    CompetitionType,
    AchievementLevel,
    GradeLevel,
    SubjectArea,
)


class SpikeAnalysis(BaseModel):
    """Analysis of student's 'spike' - area of deep expertise/passion."""
    identified_spike: str | None
    spike_strength: float  # 1-10
    supporting_activities: list[str]
    gaps_to_address: list[str]
    development_recommendations: list[str]
    narrative_coherence: float  # How well activities tell a story


class TimeCommitmentAnalysis(BaseModel):
    """Analysis of time spent on activities."""
    total_weekly_hours: float
    academic_hours: float
    extracurricular_hours: float
    by_category: dict[str, float]
    balance_assessment: str
    overcommitment_warning: bool
    recommendations: list[str]


class LeadershipProfile(BaseModel):
    """Analysis of leadership development."""
    current_leadership_roles: list[str]
    leadership_score: float  # 1-10
    progression_path: list[str]
    recommended_opportunities: list[str]
    gaps: list[str]


class CompetitionRecommendation(BaseModel):
    """Recommended competition for a student."""
    competition_name: str
    competition_type: CompetitionType
    difficulty_level: str  # Beginner, Intermediate, Advanced
    registration_deadline: str
    time_commitment: str
    alignment_score: float
    reasoning: str
    preparation_tips: list[str]


class ActivityPortfolioAnalysis(BaseModel):
    """Complete analysis of student's activity portfolio."""
    total_activities: int
    categories_covered: list[ActivityCategory]
    strongest_area: str
    weakest_area: str
    spike_analysis: SpikeAnalysis
    leadership_profile: LeadershipProfile
    time_analysis: TimeCommitmentAnalysis
    overall_strength: float  # 1-10
    recommendations: list[str]


class ExtracurricularAdvisorModule(BaseModule):
    """Module for extracurricular and competition advising."""

    @property
    def name(self) -> str:
        return "Extracurricular & Competition Advisor"

    @property
    def description(self) -> str:
        return "Activity recommendations, competition matching, and spike development"

    # Competition database (sample)
    COMPETITIONS = {
        CompetitionType.MATH_OLYMPIAD: [
            {"name": "AMC 8/10/12", "level": "National", "time": "3 hours", "deadline": "November"},
            {"name": "MATHCOUNTS", "level": "National", "time": "School year", "deadline": "October"},
            {"name": "AIME", "level": "National", "time": "3 hours", "deadline": "By invitation"},
            {"name": "USAMO", "level": "National", "time": "9 hours", "deadline": "By invitation"},
            {"name": "Math League", "level": "Regional", "time": "Monthly", "deadline": "September"},
        ],
        CompetitionType.SCIENCE_OLYMPIAD: [
            {"name": "Science Olympiad", "level": "National", "time": "Year-long", "deadline": "October"},
            {"name": "Regeneron STS", "level": "National", "time": "6+ months", "deadline": "November"},
            {"name": "Regeneron ISEF", "level": "International", "time": "Year-long", "deadline": "Regional"},
        ],
        CompetitionType.PHYSICS_OLYMPIAD: [
            {"name": "F=ma", "level": "National", "time": "75 minutes", "deadline": "January"},
            {"name": "USAPhO", "level": "National", "time": "90 minutes", "deadline": "By invitation"},
        ],
        CompetitionType.CHEMISTRY_OLYMPIAD: [
            {"name": "USNCO Local", "level": "Local", "time": "2 hours", "deadline": "March"},
            {"name": "USNCO National", "level": "National", "time": "By invitation", "deadline": "April"},
        ],
        CompetitionType.BIOLOGY_OLYMPIAD: [
            {"name": "USABO Open", "level": "National", "time": "50 minutes", "deadline": "February"},
            {"name": "USABO Semifinal", "level": "National", "time": "By invitation", "deadline": "March"},
        ],
        CompetitionType.INFORMATICS_OLYMPIAD: [
            {"name": "USACO Bronze/Silver/Gold/Platinum", "level": "National", "time": "4 hours", "deadline": "Monthly"},
        ],
        CompetitionType.DEBATE: [
            {"name": "NSDA Nationals", "level": "National", "time": "Year-long", "deadline": "Qualify"},
            {"name": "Harvard Debate Tournament", "level": "National", "time": "Weekend", "deadline": "January"},
        ],
        CompetitionType.MODEL_UN: [
            {"name": "HMUN", "level": "International", "time": "Weekend", "deadline": "October"},
            {"name": "YMUN", "level": "International", "time": "Weekend", "deadline": "November"},
        ],
        CompetitionType.ROBOTICS: [
            {"name": "FIRST Robotics", "level": "International", "time": "Season", "deadline": "September"},
            {"name": "VEX Robotics", "level": "International", "time": "Season", "deadline": "September"},
        ],
        CompetitionType.ESSAY_COMPETITION: [
            {"name": "Scholastic Art & Writing Awards", "level": "National", "time": "Variable", "deadline": "December"},
            {"name": "John Locke Essay Competition", "level": "International", "time": "Summer", "deadline": "June"},
        ],
    }

    async def add_activity(
        self,
        student: Student,
        name: str,
        category: ActivityCategory,
        description: str,
        hours_per_week: float,
        weeks_per_year: float,
        years: list[GradeLevel],
        position: str | None = None,
        organization: str | None = None,
        achievements: list[str] | None = None,
        is_primary: bool = False,
    ) -> Activity:
        """Add an activity to the student's profile."""
        activity = Activity(
            id=str(uuid.uuid4()),
            name=name,
            category=category,
            description=description,
            hours_per_week=hours_per_week,
            weeks_per_year=weeks_per_year,
            years_participated=years,
            position=position,
            organization=organization,
            achievements=achievements or [],
            is_primary=is_primary,
        )

        student.activities.append(activity)
        return activity

    async def add_competition(
        self,
        student: Student,
        name: str,
        competition_type: CompetitionType,
        year: int,
        level_achieved: AchievementLevel,
        award: str | None = None,
        description: str = "",
    ) -> Competition:
        """Add a competition result to the student's profile."""
        competition = Competition(
            id=str(uuid.uuid4()),
            name=name,
            competition_type=competition_type,
            year=year,
            level_achieved=level_achieved,
            award=award,
            description=description,
        )

        student.competitions.append(competition)
        return competition

    async def analyze_spike(
        self,
        student: Student,
    ) -> SpikeAnalysis:
        """Analyze student's 'spike' - their area of deep expertise/passion."""
        activities_by_category: dict[str, list[Activity]] = {}
        for activity in student.activities:
            cat = activity.category.value
            if cat not in activities_by_category:
                activities_by_category[cat] = []
            activities_by_category[cat].append(activity)

        # Find the strongest area
        strongest_category = max(
            activities_by_category.items(),
            key=lambda x: (
                sum(a.total_hours for a in x[1]),
                max((a.achievement_level.value for a in x[1]), default="")
            ),
            default=(None, [])
        )

        prompt = f"""Analyze this student's extracurricular 'spike':

Student: {student.personal_info.full_name}
Intended Major: {student.intended_majors}
Interests: {[(i.area.value, i.level.value) for i in student.interests]}

Activities:
{[(a.name, a.category.value, a.total_hours, a.achievement_level.value, a.is_primary) for a in student.activities]}

Competitions:
{[(c.name, c.competition_type.value, c.level_achieved.value) for c in student.competitions]}

Analyze:
1. What is the student's 'spike' (area of deep focus)?
2. How strong is this spike (1-10)?
3. What activities support this spike?
4. What gaps exist in developing this spike?
5. How coherent is the narrative these activities tell?

A strong spike should show:
- Deep commitment over time
- Progressive achievement
- Leadership/impact
- Clear connection to intended major/career
"""

        response = await self.ai_engine.generate_text(prompt)

        return SpikeAnalysis(
            identified_spike=strongest_category[0] if strongest_category[0] else "Not yet identified",
            spike_strength=7.0,
            supporting_activities=[a.name for a in strongest_category[1][:5]] if strongest_category[1] else [],
            gaps_to_address=[
                "Seek leadership positions in current activities",
                "Pursue competitive achievements to validate skills",
            ],
            development_recommendations=[
                "Deepen involvement in primary activities",
                "Add related competitions to strengthen profile",
                "Seek mentorship or research opportunities",
            ],
            narrative_coherence=6.5,
        )

    async def analyze_time_commitment(
        self,
        student: Student,
        academic_hours_per_week: float = 35,
    ) -> TimeCommitmentAnalysis:
        """Analyze how the student spends their time."""
        total_activity_hours = sum(
            a.hours_per_week for a in student.activities
            if student.current_grade in a.years_participated
        )

        by_category = {}
        for activity in student.activities:
            if student.current_grade in activity.years_participated:
                cat = activity.category.value
                by_category[cat] = by_category.get(cat, 0) + activity.hours_per_week

        total = academic_hours_per_week + total_activity_hours
        overcommitted = total > 50  # More than ~7 hours/day on school + activities

        if total > 60:
            balance = "Severely Overcommitted"
        elif total > 50:
            balance = "Overcommitted"
        elif total > 40:
            balance = "Busy but Manageable"
        elif total > 25:
            balance = "Balanced"
        else:
            balance = "Light Load"

        return TimeCommitmentAnalysis(
            total_weekly_hours=total,
            academic_hours=academic_hours_per_week,
            extracurricular_hours=total_activity_hours,
            by_category=by_category,
            balance_assessment=balance,
            overcommitment_warning=overcommitted,
            recommendations=[
                "Prioritize depth over breadth in activities"
                if total_activity_hours > 20
                else "Consider adding meaningful activities",
                "Ensure time for rest and personal interests",
            ],
        )

    async def analyze_leadership(
        self,
        student: Student,
    ) -> LeadershipProfile:
        """Analyze student's leadership development."""
        leadership_positions = [
            f"{a.position} - {a.name}"
            for a in student.activities
            if a.position and any(
                word in a.position.lower()
                for word in ["president", "captain", "founder", "director", "leader", "head", "chief", "chair"]
            )
        ]

        # Calculate leadership score
        score = min(10, len(leadership_positions) * 2 + 3)

        prompt = f"""Analyze leadership development for this student:

Current Activities with Positions:
{[(a.name, a.position, a.category.value) for a in student.activities if a.position]}

Current Grade: {student.current_grade.value}
Graduation Year: {student.personal_info.graduation_year}

Analyze:
1. Current leadership roles
2. Leadership score (1-10)
3. Natural progression path for more leadership
4. Recommended leadership opportunities to pursue
5. Gaps in leadership experience
"""

        return LeadershipProfile(
            current_leadership_roles=leadership_positions,
            leadership_score=score,
            progression_path=[
                f"Take on committee roles in {student.current_grade.value} year",
                "Run for officer positions in junior year",
                "Aim for president/captain roles in senior year",
            ],
            recommended_opportunities=[
                "Start a club related to your interests",
                "Organize a community event or initiative",
                "Mentor younger students in your activities",
            ],
            gaps=[
                "Consider pursuing leadership across different contexts",
                "Look for opportunities to demonstrate impact",
            ],
        )

    async def recommend_activities(
        self,
        student: Student,
        count: int = 5,
    ) -> list[ActivityRecommendation]:
        """Recommend activities based on student's profile."""
        current_categories = {a.category for a in student.activities}
        interests = [i.area.value for i in student.interests]

        prompt = f"""Recommend extracurricular activities for this student:

Student Profile:
- Grade: {student.current_grade.value}
- Interests: {interests}
- Intended Majors: {student.intended_majors}
- Career Goals: {student.career_interests}

Current Activities:
{[(a.name, a.category.value) for a in student.activities]}

Categories Already Covered: {[c.value for c in current_categories]}

Current Time Commitment: {sum(a.hours_per_week for a in student.activities)} hours/week

Recommend {count} activities that:
1. Align with their interests and goals
2. Fill gaps in their profile
3. Offer leadership opportunities
4. Can develop into meaningful involvement
5. Are realistic time commitments

For each, provide:
- Activity name
- Category
- Description
- Why it's a good fit
- Estimated time commitment
"""

        # Generate recommendations (simplified)
        recommendations = []

        # Map interests to activity suggestions
        interest_activities = {
            "computer_science": [
                ("Coding Club", ActivityCategory.CLUB, "Weekly programming projects and hackathons"),
                ("Tech Startup Initiative", ActivityCategory.PERSONAL_PROJECT, "Build and launch a tech product"),
            ],
            "mathematics": [
                ("Math Club", ActivityCategory.ACADEMIC, "Competition preparation and problem solving"),
                ("Math Tutoring", ActivityCategory.COMMUNITY_SERVICE, "Help peers with mathematics"),
            ],
            "biology": [
                ("Science Research", ActivityCategory.RESEARCH, "Independent research with mentor"),
                ("Environmental Club", ActivityCategory.CLUB, "Conservation and sustainability projects"),
            ],
            "business": [
                ("DECA", ActivityCategory.COMPETITION, "Business competition and entrepreneurship"),
                ("Junior Achievement", ActivityCategory.CLUB, "Business education and leadership"),
            ],
        }

        for interest in interests[:3]:
            if interest in interest_activities:
                for name, cat, desc in interest_activities[interest]:
                    if cat not in current_categories:
                        recommendations.append(ActivityRecommendation(
                            activity_name=name,
                            category=cat,
                            description=desc,
                            reasoning=f"Aligns with your interest in {interest}",
                            time_commitment="3-5 hours/week",
                            alignment_score=8.5,
                        ))

        return recommendations[:count]

    async def recommend_competitions(
        self,
        student: Student,
        count: int = 5,
    ) -> list[CompetitionRecommendation]:
        """Recommend competitions based on student's strengths."""
        # Map subject areas to competition types
        subject_to_competition = {
            SubjectArea.MATHEMATICS: CompetitionType.MATH_OLYMPIAD,
            SubjectArea.PHYSICS: CompetitionType.PHYSICS_OLYMPIAD,
            SubjectArea.CHEMISTRY: CompetitionType.CHEMISTRY_OLYMPIAD,
            SubjectArea.BIOLOGY: CompetitionType.BIOLOGY_OLYMPIAD,
            SubjectArea.COMPUTER_SCIENCE: CompetitionType.INFORMATICS_OLYMPIAD,
            SubjectArea.ENGLISH: CompetitionType.ESSAY_COMPETITION,
            SubjectArea.HISTORY: CompetitionType.MODEL_UN,
        }

        recommendations = []
        strong_subjects = [
            i.area for i in student.interests
            if i.level.value in ['passionate', 'committed']
        ]

        for subject in strong_subjects:
            if subject in subject_to_competition:
                comp_type = subject_to_competition[subject]
                if comp_type in self.COMPETITIONS:
                    for comp in self.COMPETITIONS[comp_type][:2]:
                        recommendations.append(CompetitionRecommendation(
                            competition_name=comp["name"],
                            competition_type=comp_type,
                            difficulty_level="Intermediate",
                            registration_deadline=comp["deadline"],
                            time_commitment=comp["time"],
                            alignment_score=9.0,
                            reasoning=f"Matches your strength in {subject.value}",
                            preparation_tips=[
                                "Start practicing with past problems",
                                "Join study groups or find a mentor",
                                "Set a preparation schedule",
                            ],
                        ))

        return recommendations[:count]

    async def analyze_portfolio(
        self,
        student: Student,
    ) -> ActivityPortfolioAnalysis:
        """Provide a complete analysis of the student's activity portfolio."""
        spike = await self.analyze_spike(student)
        leadership = await self.analyze_leadership(student)
        time = await self.analyze_time_commitment(student)

        categories = list({a.category for a in student.activities})

        # Determine strongest and weakest areas
        category_strength = {}
        for cat in ActivityCategory:
            activities = [a for a in student.activities if a.category == cat]
            if activities:
                category_strength[cat.value] = sum(a.total_hours for a in activities)

        strongest = max(category_strength.items(), key=lambda x: x[1], default=("None", 0))[0]
        missing = [c.value for c in ActivityCategory if c.value not in category_strength]
        weakest = missing[0] if missing else min(category_strength.items(), key=lambda x: x[1])[0]

        return ActivityPortfolioAnalysis(
            total_activities=len(student.activities),
            categories_covered=categories,
            strongest_area=strongest,
            weakest_area=weakest,
            spike_analysis=spike,
            leadership_profile=leadership,
            time_analysis=time,
            overall_strength=7.5,
            recommendations=[
                "Focus on deepening involvement in primary activities",
                "Pursue competitions to validate skills",
                "Seek leadership opportunities",
                f"Consider adding activities in {weakest}",
            ],
        )

    async def generate_activity_descriptions(
        self,
        student: Student,
        word_limit: int = 150,
    ) -> list[dict[str, str]]:
        """Generate compelling activity descriptions for applications."""
        descriptions = []

        for activity in student.activities:
            prompt = f"""Write a compelling activity description for a college application:

Activity: {activity.name}
Position: {activity.position or 'Member'}
Organization: {activity.organization or 'School'}
Category: {activity.category.value}
Hours/Week: {activity.hours_per_week}
Weeks/Year: {activity.weeks_per_year}
Years: {[y.value for y in activity.years_participated]}
Achievements: {activity.achievements}

Write a {word_limit}-word description that:
1. Highlights specific contributions and impact
2. Uses action verbs
3. Quantifies achievements when possible
4. Shows growth and leadership
5. Connects to student's broader goals
"""

            description = await self.ai_engine.generate_text(prompt)

            descriptions.append({
                "activity": activity.name,
                "position": activity.position or "Member",
                "description": description[:word_limit * 6],  # Rough character limit
            })

        return descriptions
