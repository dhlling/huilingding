"""Module 5: College Research & Matching System.

This module handles:
- College database with filtering
- Admission statistics analysis
- School culture matching
- Financial aid estimation
- College list building (reach/match/safety)
"""

from datetime import date
from typing import Any
from pydantic import BaseModel, Field

from src.core.base import BaseModule, AIEngine
from src.core.models import (
    Student,
    College,
    AdmissionStats,
    FinancialInfo,
    CollegeProgram,
    CollegeRecommendation,
)
from src.core.enums import CollegeType, CollegeTier, SubjectArea, FinancialNeedLevel


class CollegeMatch(BaseModel):
    """A college match with detailed analysis."""
    college: College
    tier: CollegeTier
    overall_match_score: float  # 0-100
    academic_fit: float
    interest_alignment: float
    culture_fit: float
    financial_fit: float
    admission_probability: float  # Estimated chance of admission
    strengths: list[str]
    considerations: list[str]
    why_apply: str


class CollegeList(BaseModel):
    """A curated college list for a student."""
    student_id: str
    reach_schools: list[CollegeMatch]
    target_schools: list[CollegeMatch]
    likely_schools: list[CollegeMatch]
    total_schools: int
    strategy_notes: str
    recommended_early_decision: CollegeMatch | None
    recommended_early_action: list[CollegeMatch]


class AdmissionChanceAnalysis(BaseModel):
    """Analysis of admission chances at a specific school."""
    college_name: str
    base_probability: float  # Based on stats alone
    adjusted_probability: float  # With hooks, essays, etc.
    tier: CollegeTier
    factors_helping: list[str]
    factors_hurting: list[str]
    how_to_improve: list[str]
    similar_schools: list[str]


class FinancialAidEstimate(BaseModel):
    """Estimated financial aid package."""
    college_name: str
    total_cost: int
    estimated_grant_aid: int
    estimated_loan: int
    estimated_net_cost: int
    work_study: int
    merit_scholarship_chance: float
    notes: list[str]


class CollegeComparison(BaseModel):
    """Comparison of multiple colleges."""
    colleges: list[str]
    comparison_matrix: dict[str, dict[str, Any]]
    winner_by_category: dict[str, str]
    overall_recommendation: str
    personalized_analysis: str


class CollegeResearchModule(BaseModule):
    """Module for college research and matching."""

    @property
    def name(self) -> str:
        return "College Research & Matching System"

    @property
    def description(self) -> str:
        return "College database, admission analysis, and list building"

    # Sample college database
    COLLEGES_DATABASE: list[dict[str, Any]] = [
        {
            "id": "mit",
            "name": "Massachusetts Institute of Technology",
            "location": "Cambridge, MA",
            "state": "MA",
            "college_type": CollegeType.RESEARCH_UNIVERSITY,
            "size": 4500,
            "setting": "Urban",
            "admission_stats": {
                "acceptance_rate": 0.04,
                "early_acceptance_rate": 0.05,
                "avg_gpa": 3.97,
                "sat_avg": 1545,
                "sat_25th": 1510,
                "sat_75th": 1580,
                "act_avg": 35,
            },
            "financial_info": {
                "tuition_in_state": 57986,
                "tuition_out_of_state": 57986,
                "room_and_board": 18830,
                "avg_financial_aid": 52000,
                "percent_receiving_aid": 0.58,
                "meets_full_need": True,
            },
            "notable_features": ["Top engineering", "UROP research", "Entrepreneurship"],
        },
        {
            "id": "stanford",
            "name": "Stanford University",
            "location": "Stanford, CA",
            "state": "CA",
            "college_type": CollegeType.RESEARCH_UNIVERSITY,
            "size": 7700,
            "setting": "Suburban",
            "admission_stats": {
                "acceptance_rate": 0.04,
                "early_acceptance_rate": 0.08,
                "avg_gpa": 3.96,
                "sat_avg": 1550,
                "sat_25th": 1500,
                "sat_75th": 1580,
                "act_avg": 35,
            },
            "financial_info": {
                "tuition_in_state": 56169,
                "tuition_out_of_state": 56169,
                "room_and_board": 18619,
                "avg_financial_aid": 56000,
                "percent_receiving_aid": 0.50,
                "meets_full_need": True,
            },
            "notable_features": ["Silicon Valley", "Cardinal Quarter", "D-School"],
        },
        {
            "id": "harvard",
            "name": "Harvard University",
            "location": "Cambridge, MA",
            "state": "MA",
            "college_type": CollegeType.RESEARCH_UNIVERSITY,
            "size": 7100,
            "setting": "Urban",
            "admission_stats": {
                "acceptance_rate": 0.035,
                "early_acceptance_rate": 0.08,
                "avg_gpa": 3.95,
                "sat_avg": 1550,
                "sat_25th": 1480,
                "sat_75th": 1580,
                "act_avg": 35,
            },
            "financial_info": {
                "tuition_in_state": 54269,
                "tuition_out_of_state": 54269,
                "room_and_board": 19502,
                "avg_financial_aid": 55000,
                "percent_receiving_aid": 0.55,
                "meets_full_need": True,
            },
            "notable_features": ["Liberal arts", "Houses system", "Extensive resources"],
        },
        {
            "id": "berkeley",
            "name": "UC Berkeley",
            "location": "Berkeley, CA",
            "state": "CA",
            "college_type": CollegeType.STATE_UNIVERSITY,
            "size": 32000,
            "setting": "Urban",
            "admission_stats": {
                "acceptance_rate": 0.12,
                "avg_gpa": 3.92,
                "sat_avg": 1440,
                "sat_25th": 1330,
                "sat_75th": 1530,
                "act_avg": 32,
            },
            "financial_info": {
                "tuition_in_state": 14312,
                "tuition_out_of_state": 44066,
                "room_and_board": 18642,
                "avg_financial_aid": 20000,
                "percent_receiving_aid": 0.65,
                "meets_full_need": False,
            },
            "notable_features": ["Top public", "Research opportunities", "Diverse"],
        },
        {
            "id": "williams",
            "name": "Williams College",
            "location": "Williamstown, MA",
            "state": "MA",
            "college_type": CollegeType.LIBERAL_ARTS,
            "size": 2000,
            "setting": "Rural",
            "admission_stats": {
                "acceptance_rate": 0.10,
                "early_acceptance_rate": 0.30,
                "avg_gpa": 3.95,
                "sat_avg": 1505,
                "sat_25th": 1440,
                "sat_75th": 1560,
                "act_avg": 34,
            },
            "financial_info": {
                "tuition_in_state": 60660,
                "tuition_out_of_state": 60660,
                "room_and_board": 16480,
                "avg_financial_aid": 60000,
                "percent_receiving_aid": 0.50,
                "meets_full_need": True,
            },
            "notable_features": ["Tutorial system", "Small classes", "Close community"],
        },
        {
            "id": "gatech",
            "name": "Georgia Institute of Technology",
            "location": "Atlanta, GA",
            "state": "GA",
            "college_type": CollegeType.RESEARCH_UNIVERSITY,
            "size": 18000,
            "setting": "Urban",
            "admission_stats": {
                "acceptance_rate": 0.16,
                "avg_gpa": 3.95,
                "sat_avg": 1480,
                "sat_25th": 1390,
                "sat_75th": 1540,
                "act_avg": 33,
            },
            "financial_info": {
                "tuition_in_state": 12852,
                "tuition_out_of_state": 33794,
                "room_and_board": 12360,
                "avg_financial_aid": 14000,
                "percent_receiving_aid": 0.45,
                "meets_full_need": False,
            },
            "notable_features": ["Top engineering", "Co-op programs", "Atlanta tech hub"],
        },
    ]

    def __init__(self, ai_engine: AIEngine):
        super().__init__(ai_engine)
        self._colleges: dict[str, College] = {}
        self._load_colleges()

    def _load_colleges(self) -> None:
        """Load college database."""
        for data in self.COLLEGES_DATABASE:
            admission_stats = AdmissionStats(**data["admission_stats"])
            financial_info = FinancialInfo(**data["financial_info"])

            college = College(
                id=data["id"],
                name=data["name"],
                location=data["location"],
                state=data["state"],
                college_type=data["college_type"],
                size=data["size"],
                setting=data["setting"],
                admission_stats=admission_stats,
                financial_info=financial_info,
                notable_features=data["notable_features"],
            )
            self._colleges[data["id"]] = college

    async def search_colleges(
        self,
        filters: dict[str, Any] | None = None,
    ) -> list[College]:
        """Search colleges with filters."""
        colleges = list(self._colleges.values())

        if filters:
            if "min_acceptance_rate" in filters:
                colleges = [c for c in colleges
                            if c.admission_stats.acceptance_rate >= filters["min_acceptance_rate"]]
            if "max_acceptance_rate" in filters:
                colleges = [c for c in colleges
                            if c.admission_stats.acceptance_rate <= filters["max_acceptance_rate"]]
            if "state" in filters:
                colleges = [c for c in colleges if c.state == filters["state"]]
            if "college_type" in filters:
                colleges = [c for c in colleges if c.college_type == filters["college_type"]]
            if "min_size" in filters:
                colleges = [c for c in colleges if c.size >= filters["min_size"]]
            if "max_size" in filters:
                colleges = [c for c in colleges if c.size <= filters["max_size"]]
            if "setting" in filters:
                colleges = [c for c in colleges if c.setting == filters["setting"]]
            if "meets_full_need" in filters:
                colleges = [c for c in colleges
                            if c.financial_info.meets_full_need == filters["meets_full_need"]]

        return colleges

    async def get_college(self, college_id: str) -> College | None:
        """Get a specific college by ID."""
        return self._colleges.get(college_id)

    async def calculate_admission_chance(
        self,
        student: Student,
        college: College,
    ) -> AdmissionChanceAnalysis:
        """Calculate admission chances for a student at a specific college."""
        stats = college.admission_stats
        gpa = student.academic_record.cumulative_gpa

        # Get best test score
        sat_score = None
        act_score = None
        for test in student.academic_record.test_scores:
            if test.test_type.value == "sat":
                sat_score = test.score
            elif test.test_type.value == "act":
                act_score = test.score

        # Base probability from acceptance rate
        base = stats.acceptance_rate * 100

        # Adjust for GPA
        if gpa >= stats.avg_gpa:
            base += 5
        elif gpa >= stats.avg_gpa - 0.2:
            base += 0
        else:
            base -= 10

        # Adjust for test scores
        if sat_score and stats.sat_avg:
            if sat_score >= stats.sat_75th:
                base += 10
            elif sat_score >= stats.sat_avg:
                base += 5
            elif sat_score >= stats.sat_25th:
                base += 0
            else:
                base -= 10

        # Adjust for activities (simplified)
        strong_activities = [a for a in student.activities if a.achievement_level.value in ['national', 'international']]
        base += len(strong_activities) * 2

        # Cap at reasonable limits
        base = max(1, min(base, stats.acceptance_rate * 100 * 3))

        # Determine tier
        if base < stats.acceptance_rate * 100 * 0.8:
            tier = CollegeTier.REACH
        elif base < stats.acceptance_rate * 100 * 1.5:
            tier = CollegeTier.TARGET
        else:
            tier = CollegeTier.LIKELY

        factors_helping = []
        factors_hurting = []

        if gpa >= stats.avg_gpa:
            factors_helping.append(f"GPA above average ({gpa:.2f} vs {stats.avg_gpa:.2f})")
        else:
            factors_hurting.append(f"GPA below average ({gpa:.2f} vs {stats.avg_gpa:.2f})")

        if strong_activities:
            factors_helping.append(f"{len(strong_activities)} national/international achievements")

        return AdmissionChanceAnalysis(
            college_name=college.name,
            base_probability=stats.acceptance_rate * 100,
            adjusted_probability=base,
            tier=tier,
            factors_helping=factors_helping,
            factors_hurting=factors_hurting,
            how_to_improve=[
                "Strengthen essays to convey unique perspective",
                "Get strong, specific recommendations",
                "Demonstrate genuine interest in the school",
            ],
            similar_schools=[],
        )

    async def estimate_financial_aid(
        self,
        student: Student,
        college: College,
    ) -> FinancialAidEstimate:
        """Estimate financial aid package."""
        total_cost = (college.financial_info.tuition_out_of_state +
                      college.financial_info.room_and_board)

        # Estimate based on financial need level
        need = student.family_context.financial_need

        if need == FinancialNeedLevel.FULL_AID:
            grant_aid = int(total_cost * 0.85) if college.financial_info.meets_full_need else int(total_cost * 0.50)
        elif need == FinancialNeedLevel.SIGNIFICANT_AID:
            grant_aid = int(total_cost * 0.60) if college.financial_info.meets_full_need else int(total_cost * 0.35)
        elif need == FinancialNeedLevel.PARTIAL_AID:
            grant_aid = int(total_cost * 0.30) if college.financial_info.meets_full_need else int(total_cost * 0.15)
        else:
            grant_aid = 0

        # Merit scholarship estimate
        merit_chance = 0.0
        if student.academic_record.cumulative_gpa >= 3.9:
            merit_chance = 0.3 if college.financial_info.merit_scholarships else 0
        elif student.academic_record.cumulative_gpa >= 3.7:
            merit_chance = 0.15 if college.financial_info.merit_scholarships else 0

        loan = min(5500, total_cost - grant_aid)  # Federal loan limit for freshmen
        work_study = 3000 if grant_aid > 0 else 0
        net_cost = total_cost - grant_aid - work_study

        return FinancialAidEstimate(
            college_name=college.name,
            total_cost=total_cost,
            estimated_grant_aid=grant_aid,
            estimated_loan=loan,
            estimated_net_cost=max(0, net_cost),
            work_study=work_study,
            merit_scholarship_chance=merit_chance,
            notes=[
                "Estimates are approximate - actual aid varies",
                "Run the Net Price Calculator on the college website for more accuracy",
                f"This school {'meets' if college.financial_info.meets_full_need else 'does not meet'} full demonstrated need",
            ],
        )

    async def match_colleges(
        self,
        student: Student,
        count: int = 15,
    ) -> list[CollegeMatch]:
        """Match student with colleges based on profile."""
        matches = []

        for college in self._colleges.values():
            # Calculate various fit scores
            admission_analysis = await self.calculate_admission_chance(student, college)

            # Academic fit
            academic_fit = min(100, admission_analysis.adjusted_probability * 5)

            # Interest alignment
            interest_score = 50  # Base score
            student_interests = [i.area for i in student.interests]
            # Would match against college programs in full implementation

            # Culture fit (simplified)
            culture_fit = 70  # Would be based on preferences

            # Financial fit
            financial = await self.estimate_financial_aid(student, college)
            financial_fit = 100 - (financial.estimated_net_cost / 1000)
            financial_fit = max(0, min(100, financial_fit))

            # Overall score
            overall = (academic_fit * 0.3 + interest_score * 0.3 +
                       culture_fit * 0.2 + financial_fit * 0.2)

            matches.append(CollegeMatch(
                college=college,
                tier=admission_analysis.tier,
                overall_match_score=overall,
                academic_fit=academic_fit,
                interest_alignment=interest_score,
                culture_fit=culture_fit,
                financial_fit=financial_fit,
                admission_probability=admission_analysis.adjusted_probability,
                strengths=admission_analysis.factors_helping,
                considerations=admission_analysis.factors_hurting + financial.notes[:1],
                why_apply=f"Strong match in {college.notable_features[0] if college.notable_features else 'academics'}",
            ))

        # Sort by overall match score
        matches.sort(key=lambda x: x.overall_match_score, reverse=True)
        return matches[:count]

    async def build_college_list(
        self,
        student: Student,
        total_schools: int = 12,
    ) -> CollegeList:
        """Build a balanced college list."""
        all_matches = await self.match_colleges(student, count=30)

        # Separate by tier
        reaches = [m for m in all_matches if m.tier == CollegeTier.REACH]
        targets = [m for m in all_matches if m.tier == CollegeTier.TARGET]
        likelies = [m for m in all_matches if m.tier == CollegeTier.LIKELY]

        # Build balanced list
        reach_count = min(4, len(reaches), total_schools // 3)
        target_count = min(5, len(targets), total_schools // 2)
        likely_count = min(3, len(likelies), total_schools // 4)

        selected_reaches = reaches[:reach_count]
        selected_targets = targets[:target_count]
        selected_likelies = likelies[:likely_count]

        # ED recommendation - highest match score reach school
        ed_rec = selected_reaches[0] if selected_reaches else None

        # EA recommendations - schools offering EA
        ea_recs = selected_targets[:2] + selected_likelies[:1]

        prompt = f"""Provide strategic notes for this college list:

Student Profile:
- GPA: {student.academic_record.cumulative_gpa}
- Interests: {[i.area.value for i in student.interests]}
- Intended Major: {student.intended_majors}

Reach Schools: {[r.college.name for r in selected_reaches]}
Target Schools: {[t.college.name for t in selected_targets]}
Likely Schools: {[l.college.name for l in selected_likelies]}

Provide:
1. Overall list strategy
2. Any gaps to address
3. Application timeline recommendations
"""

        strategy_notes = await self.ai_engine.generate_text(prompt)

        return CollegeList(
            student_id=student.id,
            reach_schools=selected_reaches,
            target_schools=selected_targets,
            likely_schools=selected_likelies,
            total_schools=len(selected_reaches) + len(selected_targets) + len(selected_likelies),
            strategy_notes=strategy_notes,
            recommended_early_decision=ed_rec,
            recommended_early_action=ea_recs,
        )

    async def compare_colleges(
        self,
        student: Student,
        college_ids: list[str],
    ) -> CollegeComparison:
        """Compare multiple colleges for a student."""
        colleges = [self._colleges[cid] for cid in college_ids if cid in self._colleges]

        if not colleges:
            raise ValueError("No valid colleges found")

        comparison_matrix = {}
        for college in colleges:
            admission = await self.calculate_admission_chance(student, college)
            financial = await self.estimate_financial_aid(student, college)

            comparison_matrix[college.name] = {
                "Acceptance Rate": f"{college.admission_stats.acceptance_rate * 100:.1f}%",
                "Your Admission Chance": f"{admission.adjusted_probability:.1f}%",
                "Total Cost": f"${college.financial_info.tuition_out_of_state + college.financial_info.room_and_board:,}",
                "Est. Net Cost": f"${financial.estimated_net_cost:,}",
                "Size": f"{college.size:,}",
                "Setting": college.setting,
                "Meets Full Need": "Yes" if college.financial_info.meets_full_need else "No",
            }

        prompt = f"""Compare these colleges for this student:

Student:
- Intended Major: {student.intended_majors}
- Interests: {[i.area.value for i in student.interests]}

Colleges: {[c.name for c in colleges]}

Comparison Data:
{comparison_matrix}

Provide:
1. Winner by each category
2. Overall recommendation
3. Personalized analysis for this student
"""

        response = await self.ai_engine.generate_text(prompt)

        return CollegeComparison(
            colleges=[c.name for c in colleges],
            comparison_matrix=comparison_matrix,
            winner_by_category={
                "Admission Chances": max(colleges, key=lambda c: c.admission_stats.acceptance_rate).name,
                "Financial Aid": max(colleges, key=lambda c: c.financial_info.avg_financial_aid).name,
            },
            overall_recommendation=colleges[0].name,  # Simplified
            personalized_analysis=response,
        )

    async def generate_why_us_research(
        self,
        student: Student,
        college_id: str,
    ) -> dict[str, Any]:
        """Generate research points for 'Why Us' essays."""
        college = self._colleges.get(college_id)
        if not college:
            raise ValueError(f"College {college_id} not found")

        prompt = f"""Help this student research {college.name} for their 'Why Us' essay:

Student Profile:
- Intended Major: {student.intended_majors}
- Interests: {[i.area.value for i in student.interests]}
- Activities: {[a.name for a in student.activities[:5]]}
- Career Goals: {student.career_interests}

College Info:
- Notable Features: {college.notable_features}
- Setting: {college.setting}
- Size: {college.size}

Provide:
1. Specific programs or opportunities to mention
2. Unique aspects of the school culture
3. How to connect student's background to the school
4. Professors or research to reference
5. Specific clubs or organizations
6. What NOT to mention (too generic)
"""

        response = await self.ai_engine.generate_text(prompt)

        return {
            "college": college.name,
            "research_points": response,
            "key_programs": college.notable_features,
            "tips": [
                "Be specific - avoid generic statements that apply to any school",
                "Show you've done your research by mentioning specific details",
                "Connect your goals to what this school uniquely offers",
                "Explain how you'll contribute to the community",
            ],
        }
