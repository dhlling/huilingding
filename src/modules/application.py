"""Module 7: Application Assembly & Submission Manager.

This module handles:
- Application timeline management
- Document checklist tracking
- Recommendation letter coordination
- Interview preparation
- Submission verification
"""

from datetime import date, datetime, timedelta
from typing import Any
from pydantic import BaseModel, Field
import uuid

from src.core.base import BaseModule, AIEngine
from src.core.models import (
    Student,
    Application,
    Essay,
    RecommendationLetter,
    College,
)
from src.core.enums import (
    ApplicationStatus,
    CollegeTier,
    EssayType,
    RecommendationType,
)


class ApplicationChecklist(BaseModel):
    """Checklist for a single application."""
    application_id: str
    college_name: str
    deadline: date
    days_remaining: int
    items: list[dict[str, Any]]
    completion_percentage: float
    blocking_items: list[str]
    next_action: str


class RecommenderStatus(BaseModel):
    """Status tracking for a recommender."""
    recommender_name: str
    recommender_email: str
    recommendation_type: RecommendationType
    schools_requested: list[str]
    date_requested: date | None
    reminder_sent: bool
    submitted_to: list[str]
    pending_for: list[str]


class InterviewPrep(BaseModel):
    """Interview preparation materials."""
    college_name: str
    interview_type: str  # Alumni, Admissions, Student
    interview_date: date | None
    preparation_topics: list[str]
    sample_questions: list[str]
    questions_to_ask: list[str]
    tips: list[str]
    mock_interview_feedback: str | None


class SubmissionStatus(BaseModel):
    """Status of an application submission."""
    application_id: str
    college_name: str
    submitted: bool
    submitted_date: date | None
    confirmation_number: str | None
    financial_aid_submitted: bool
    fafsa_submitted: bool
    css_profile_submitted: bool
    portal_access: bool
    missing_items: list[str]


class ApplicationDashboard(BaseModel):
    """Overview dashboard of all applications."""
    student_id: str
    total_applications: int
    submitted: int
    in_progress: int
    not_started: int
    upcoming_deadlines: list[dict[str, Any]]
    overall_progress: float
    action_items: list[str]
    by_tier: dict[str, int]


class ApplicationManagerModule(BaseModule):
    """Module for managing college applications."""

    @property
    def name(self) -> str:
        return "Application Assembly & Submission Manager"

    @property
    def description(self) -> str:
        return "Application tracking, document management, and submission coordination"

    def __init__(self, ai_engine: AIEngine):
        super().__init__(ai_engine)
        self._applications: dict[str, Application] = {}
        self._recommenders: dict[str, list[RecommenderStatus]] = {}

    async def create_application(
        self,
        student: Student,
        college: College,
        tier: CollegeTier,
        application_type: str,  # EA, ED, ED2, RD, Rolling
        deadline: date,
    ) -> Application:
        """Create a new application."""
        application = Application(
            id=str(uuid.uuid4()),
            student_id=student.id,
            college_id=college.id,
            college_name=college.name,
            tier=tier,
            application_type=application_type,
            deadline=deadline,
            essays=[],
            recommendations=[],
        )

        self._applications[application.id] = application
        return application

    async def add_essay_to_application(
        self,
        application_id: str,
        essay: Essay,
    ) -> Application:
        """Add an essay to an application."""
        application = self._applications.get(application_id)
        if not application:
            raise ValueError(f"Application {application_id} not found")

        application.essays.append(essay)
        return application

    async def add_recommendation(
        self,
        application_id: str,
        recommender_name: str,
        recommender_title: str,
        recommender_email: str,
        recommendation_type: RecommendationType,
        subject_taught: str | None = None,
    ) -> RecommendationLetter:
        """Add a recommendation letter to an application."""
        application = self._applications.get(application_id)
        if not application:
            raise ValueError(f"Application {application_id} not found")

        rec = RecommendationLetter(
            id=str(uuid.uuid4()),
            recommender_name=recommender_name,
            recommender_title=recommender_title,
            recommender_email=recommender_email,
            recommendation_type=recommendation_type,
            subject_taught=subject_taught,
        )

        application.recommendations.append(rec)
        return rec

    async def request_recommendation(
        self,
        application_id: str,
        recommendation_id: str,
    ) -> RecommendationLetter:
        """Mark a recommendation as requested."""
        application = self._applications.get(application_id)
        if not application:
            raise ValueError(f"Application {application_id} not found")

        for rec in application.recommendations:
            if rec.id == recommendation_id:
                rec.date_requested = date.today()
                rec.status = "requested"
                return rec

        raise ValueError(f"Recommendation {recommendation_id} not found")

    async def generate_recommendation_request(
        self,
        student: Student,
        recommender_name: str,
        recommender_title: str,
        subject: str,
        relationship_context: str,
    ) -> str:
        """Generate a recommendation request email."""
        prompt = f"""Write a polite, professional email requesting a recommendation letter:

Student: {student.personal_info.full_name}
Recommender: {recommender_name}, {recommender_title}
Subject: {subject}
Relationship: {relationship_context}

The email should:
1. Be respectful of their time
2. Explain why you're asking them specifically
3. Provide context about your college goals
4. Offer to provide supporting materials (resume, brag sheet)
5. Give a clear deadline
6. Express gratitude

Keep it concise but warm.
"""

        return await self.ai_engine.generate_text(prompt)

    async def get_application_checklist(
        self,
        application_id: str,
    ) -> ApplicationChecklist:
        """Get a detailed checklist for an application."""
        application = self._applications.get(application_id)
        if not application:
            raise ValueError(f"Application {application_id} not found")

        items = []

        # Common App / Coalition completion
        items.append({
            "category": "Application Form",
            "item": "Complete personal information",
            "status": "complete",  # Would be tracked
            "priority": 1,
        })
        items.append({
            "category": "Application Form",
            "item": "Complete activities section",
            "status": "complete",
            "priority": 1,
        })

        # Essays
        for essay in application.essays:
            items.append({
                "category": "Essays",
                "item": f"{essay.essay_type.value}: {essay.prompt[:50]}...",
                "status": essay.status,
                "priority": 1 if essay.status != "final" else 3,
            })

        # If no essays added yet
        if not application.essays:
            items.append({
                "category": "Essays",
                "item": "Main essay required",
                "status": "not_started",
                "priority": 1,
            })

        # Recommendations
        for rec in application.recommendations:
            items.append({
                "category": "Recommendations",
                "item": f"{rec.recommendation_type.value}: {rec.recommender_name}",
                "status": rec.status,
                "priority": 2 if rec.status != "submitted" else 3,
            })

        # Test scores
        items.append({
            "category": "Test Scores",
            "item": "Send official test scores",
            "status": "pending",
            "priority": 2,
        })

        # Transcripts
        items.append({
            "category": "Documents",
            "item": "Request transcript",
            "status": "pending",
            "priority": 2,
        })

        # Financial aid
        items.append({
            "category": "Financial Aid",
            "item": "Submit FAFSA",
            "status": "not_started",
            "priority": 2,
        })

        # Calculate completion
        completed = sum(1 for i in items if i["status"] in ["complete", "final", "submitted"])
        total = len(items)
        completion = (completed / total * 100) if total > 0 else 0

        blocking = [i["item"] for i in items if i["status"] not in ["complete", "final", "submitted"] and i["priority"] == 1]

        return ApplicationChecklist(
            application_id=application_id,
            college_name=application.college_name,
            deadline=application.deadline,
            days_remaining=application.days_until_deadline,
            items=items,
            completion_percentage=completion,
            blocking_items=blocking,
            next_action=blocking[0] if blocking else "Ready to submit!",
        )

    async def prepare_for_interview(
        self,
        student: Student,
        application_id: str,
        interview_date: date | None = None,
    ) -> InterviewPrep:
        """Prepare interview materials for a student."""
        application = self._applications.get(application_id)
        if not application:
            raise ValueError(f"Application {application_id} not found")

        prompt = f"""Prepare interview materials for this student applying to {application.college_name}:

Student Profile:
- Name: {student.personal_info.full_name}
- Interests: {[i.area.value for i in student.interests]}
- Activities: {[(a.name, a.position) for a in student.activities[:5]]}
- Intended Major: {student.intended_majors}
- Why this school: Based on their profile

Generate:
1. Key topics to prepare to discuss
2. 10 common interview questions
3. 5 thoughtful questions to ask the interviewer
4. Tips for success at this specific school's interview
"""

        response = await self.ai_engine.generate_text(prompt)

        return InterviewPrep(
            college_name=application.college_name,
            interview_type="Alumni",
            interview_date=interview_date,
            preparation_topics=[
                "Your biggest academic passion and why",
                "A challenge you overcame",
                "Why this specific college",
                "Your activities and leadership",
                "Future goals and aspirations",
            ],
            sample_questions=[
                "Tell me about yourself.",
                "Why are you interested in [College]?",
                "What would you contribute to our community?",
                "Describe a challenge you've overcome.",
                "What are you most proud of?",
                "What do you do outside of school?",
                "Where do you see yourself in 10 years?",
                "What books have you read recently?",
                "Tell me about your favorite class.",
                "Do you have any questions for me?",
            ],
            questions_to_ask=[
                "What do you wish you had known before attending?",
                "How did [College] prepare you for your career?",
                "What's your favorite memory from your time there?",
                "What makes the community special?",
                "How accessible were professors?",
            ],
            tips=[
                "Research the interviewer on LinkedIn if possible",
                "Prepare specific examples for common questions",
                "Practice but don't memorize - be conversational",
                "Dress business casual",
                "Arrive 10 minutes early",
                "Bring a copy of your resume",
                "Send a thank-you email within 24 hours",
            ],
            mock_interview_feedback=None,
        )

    async def conduct_mock_interview(
        self,
        student: Student,
        application_id: str,
        responses: dict[str, str],
    ) -> str:
        """Conduct a mock interview and provide feedback."""
        application = self._applications.get(application_id)
        if not application:
            raise ValueError(f"Application {application_id} not found")

        prompt = f"""Evaluate these mock interview responses for {application.college_name}:

Student: {student.personal_info.full_name}
Applying for: {student.intended_majors}

Questions and Responses:
{responses}

Provide detailed feedback on:
1. Overall impression (1-10)
2. Strengths in the responses
3. Areas for improvement
4. Specific suggestions for each answer
5. Body language/delivery tips (general)
6. How well they conveyed fit with {application.college_name}
"""

        return await self.ai_engine.generate_text(prompt)

    async def check_submission_status(
        self,
        application_id: str,
    ) -> SubmissionStatus:
        """Check the submission status of an application."""
        application = self._applications.get(application_id)
        if not application:
            raise ValueError(f"Application {application_id} not found")

        missing = []

        # Check essays
        for essay in application.essays:
            if essay.status != "final":
                missing.append(f"Essay: {essay.essay_type.value}")

        # Check recommendations
        for rec in application.recommendations:
            if rec.status != "submitted":
                missing.append(f"Recommendation: {rec.recommender_name}")

        return SubmissionStatus(
            application_id=application_id,
            college_name=application.college_name,
            submitted=application.status == ApplicationStatus.SUBMITTED,
            submitted_date=application.submitted_date,
            confirmation_number=None,
            financial_aid_submitted=False,
            fafsa_submitted=False,
            css_profile_submitted=False,
            portal_access=False,
            missing_items=missing,
        )

    async def submit_application(
        self,
        application_id: str,
    ) -> Application:
        """Mark an application as submitted."""
        application = self._applications.get(application_id)
        if not application:
            raise ValueError(f"Application {application_id} not found")

        # Check if ready
        status = await self.check_submission_status(application_id)
        if status.missing_items:
            raise ValueError(f"Cannot submit - missing items: {status.missing_items}")

        application.status = ApplicationStatus.SUBMITTED
        application.submitted_date = date.today()

        return application

    async def update_application_status(
        self,
        application_id: str,
        status: ApplicationStatus,
        decision_date: date | None = None,
    ) -> Application:
        """Update application status (e.g., after receiving decision)."""
        application = self._applications.get(application_id)
        if not application:
            raise ValueError(f"Application {application_id} not found")

        application.status = status
        if decision_date:
            application.decision_date = decision_date

        return application

    async def get_dashboard(
        self,
        student_id: str,
    ) -> ApplicationDashboard:
        """Get application dashboard for a student."""
        student_apps = [
            app for app in self._applications.values()
            if app.student_id == student_id
        ]

        submitted = sum(1 for a in student_apps if a.status == ApplicationStatus.SUBMITTED)
        in_progress = sum(1 for a in student_apps if a.status == ApplicationStatus.IN_PROGRESS)
        not_started = sum(1 for a in student_apps if a.status == ApplicationStatus.NOT_STARTED)

        # Upcoming deadlines
        upcoming = []
        for app in student_apps:
            if app.status not in [ApplicationStatus.SUBMITTED, ApplicationStatus.WITHDRAWN]:
                upcoming.append({
                    "college": app.college_name,
                    "deadline": app.deadline.isoformat(),
                    "days_remaining": app.days_until_deadline,
                    "type": app.application_type,
                })

        upcoming.sort(key=lambda x: x["days_remaining"])

        # By tier
        by_tier = {
            "Reach": sum(1 for a in student_apps if a.tier == CollegeTier.REACH),
            "Target": sum(1 for a in student_apps if a.tier == CollegeTier.TARGET),
            "Likely": sum(1 for a in student_apps if a.tier == CollegeTier.LIKELY),
        }

        # Action items
        action_items = []
        for app in student_apps[:3]:  # Top 3 most urgent
            if app.status != ApplicationStatus.SUBMITTED:
                checklist = await self.get_application_checklist(app.id)
                if checklist.blocking_items:
                    action_items.append(
                        f"{app.college_name}: {checklist.blocking_items[0]}"
                    )

        total = len(student_apps)
        progress = (submitted / total * 100) if total > 0 else 0

        return ApplicationDashboard(
            student_id=student_id,
            total_applications=total,
            submitted=submitted,
            in_progress=in_progress,
            not_started=not_started,
            upcoming_deadlines=upcoming[:5],
            overall_progress=progress,
            action_items=action_items,
            by_tier=by_tier,
        )

    async def generate_activity_description(
        self,
        activity_name: str,
        position: str,
        description: str,
        achievements: list[str],
        character_limit: int = 150,
    ) -> str:
        """Generate a compelling activity description for the Common App."""
        prompt = f"""Write a compelling activity description for a college application:

Activity: {activity_name}
Position: {position}
Description: {description}
Achievements: {achievements}
Character Limit: {character_limit}

Guidelines:
- Start with an action verb
- Be specific and quantify when possible
- Highlight impact and leadership
- Fit within the character limit
- Avoid generic descriptions

Write the description.
"""

        response = await self.ai_engine.generate_text(prompt)

        # Ensure it fits within limit
        if len(response) > character_limit:
            response = response[:character_limit - 3] + "..."

        return response

    async def review_activities_section(
        self,
        activities: list[dict[str, str]],
    ) -> dict[str, Any]:
        """Review and provide feedback on the activities section."""
        prompt = f"""Review this Common App activities section:

Activities:
{activities}

Evaluate:
1. Overall strength (1-10)
2. Order optimization (are most impactful activities first?)
3. Description quality
4. Variety and depth balance
5. Red flags or concerns
6. Specific improvement suggestions

Provide actionable feedback.
"""

        feedback = await self.ai_engine.generate_text(prompt)

        return {
            "activities_count": len(activities),
            "feedback": feedback,
            "suggested_order": [a["name"] for a in activities],  # Would be reordered
            "improvement_priority": ["Strengthen descriptions", "Add quantifiable achievements"],
        }

    async def get_application(self, application_id: str) -> Application | None:
        """Get an application by ID."""
        return self._applications.get(application_id)

    async def get_all_applications(self, student_id: str) -> list[Application]:
        """Get all applications for a student."""
        return [
            app for app in self._applications.values()
            if app.student_id == student_id
        ]
