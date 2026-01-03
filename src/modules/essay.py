"""Module 6: Essay Development Workshop.

This module handles:
- Personal narrative discovery
- Common App essay guidance
- Supplemental essay strategies
- Story arc development
- Revision and feedback system
"""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field
import uuid

from src.core.base import BaseModule, AIEngine
from src.core.models import Student, Essay, EssayFeedback
from src.core.enums import EssayType


class StoryElement(BaseModel):
    """An element of the student's personal story."""
    title: str
    description: str
    emotional_core: str
    potential_themes: list[str]
    essay_types_fit: list[EssayType]
    uniqueness_score: float


class PersonalNarrative(BaseModel):
    """The student's personal narrative exploration."""
    core_values: list[str]
    defining_moments: list[StoryElement]
    unique_perspectives: list[str]
    growth_stories: list[StoryElement]
    passions: list[str]
    challenges_overcome: list[StoryElement]
    recommended_main_essay_topic: StoryElement | None
    backup_topics: list[StoryElement]


class EssayOutline(BaseModel):
    """Outline for an essay."""
    essay_type: EssayType
    prompt: str
    thesis_statement: str
    opening_hook: str
    main_points: list[str]
    supporting_details: dict[str, list[str]]
    conclusion_direction: str
    word_target: int


class EssayDraft(BaseModel):
    """An essay draft with metadata."""
    id: str
    essay_id: str
    version: int
    content: str
    word_count: int
    created_at: datetime
    notes: str


class DetailedFeedback(BaseModel):
    """Detailed feedback on an essay."""
    essay_id: str
    overall_score: float
    category_scores: dict[str, float]
    strengths: list[str]
    areas_for_improvement: list[str]
    line_by_line_suggestions: list[dict[str, str]]
    revised_sentences: list[dict[str, str]]
    authenticity_analysis: str
    admissions_officer_perspective: str
    next_steps: list[str]


class EssayStrategy(BaseModel):
    """Overall essay strategy for applications."""
    student_id: str
    main_essay_topic: str
    main_essay_theme: str
    supplemental_themes: list[str]
    topics_to_avoid_repeating: list[str]
    schools_requiring_unique_content: list[str]
    essay_calendar: list[dict[str, str]]


class EssayWorkshopModule(BaseModule):
    """Module for essay development and refinement."""

    @property
    def name(self) -> str:
        return "Essay Development Workshop"

    @property
    def description(self) -> str:
        return "Personal narrative discovery, essay writing, and revision support"

    # Common App prompts (2024-2025)
    COMMON_APP_PROMPTS = [
        "Some students have a background, identity, interest, or talent that is so meaningful they believe their application would be incomplete without it. If this sounds like you, then please share your story.",
        "The lessons we take from obstacles we encounter can be fundamental to later success. Recount a time when you faced a challenge, setback, or failure. How did it affect you, and what did you learn from the experience?",
        "Reflect on a time when you questioned or challenged a belief or idea. What prompted your thinking? What was the outcome?",
        "Reflect on something that someone has done for you that has made you happy or thankful in a surprising way. How has this gratitude affected or motivated you?",
        "Discuss an accomplishment, event, or realization that sparked a period of personal growth and a new understanding of yourself or others.",
        "Describe a topic, idea, or concept you find so engaging that it makes you lose all track of time. Why does it captivate you? What or who do you turn to when you want to learn more?",
        "Share an essay on any topic of your choice. It can be one you've already written, one that responds to a different prompt, or one of your own design.",
    ]

    def __init__(self, ai_engine: AIEngine):
        super().__init__(ai_engine)
        self._essays: dict[str, Essay] = {}
        self._drafts: dict[str, list[EssayDraft]] = {}

    async def discover_personal_narrative(
        self,
        student: Student,
        brainstorm_responses: dict[str, Any] | None = None,
    ) -> PersonalNarrative:
        """Guide student through personal narrative discovery."""
        prompt = f"""Help this student discover their personal narrative for college essays:

Student Profile:
- Background: {student.personal_info.state}, {student.personal_info.country}
- First Generation: {student.personal_info.first_generation}
- Interests: {[(i.area.value, i.level.value) for i in student.interests]}
- Activities: {[(a.name, a.description, a.achievements) for a in student.activities]}
- Intended Major: {student.intended_majors}
- Career Goals: {student.career_interests}

Brainstorm Responses: {brainstorm_responses or 'Not provided'}

Help identify:
1. Core values (3-5 that define who they are)
2. Defining moments (pivotal experiences)
3. Unique perspectives (what makes them see the world differently)
4. Growth stories (times they changed or developed)
5. Passions (what they truly care about)
6. Challenges overcome (obstacles they've faced)

For each story element, evaluate:
- Emotional resonance
- Uniqueness
- Growth/reflection potential
- Which essay types it fits

Recommend the best main essay topic and backup options.
"""

        response = await self.ai_engine.generate_text(prompt)

        # Create story elements from activities and interests (simplified)
        defining_moments = []
        for activity in student.activities[:3]:
            if activity.achievements:
                defining_moments.append(StoryElement(
                    title=activity.name,
                    description=activity.description,
                    emotional_core="Passion and dedication",
                    potential_themes=["Growth", "Perseverance"],
                    essay_types_fit=[EssayType.COMMON_APP_PERSONAL, EssayType.SUPPLEMENTAL],
                    uniqueness_score=7.0,
                ))

        return PersonalNarrative(
            core_values=["Curiosity", "Perseverance", "Community"],
            defining_moments=defining_moments,
            unique_perspectives=[
                "Intersection of multiple interests",
                "Unique cultural background",
            ],
            growth_stories=[],
            passions=[i.area.value for i in student.interests if i.level.value == "passionate"],
            challenges_overcome=[],
            recommended_main_essay_topic=defining_moments[0] if defining_moments else None,
            backup_topics=defining_moments[1:] if len(defining_moments) > 1 else [],
        )

    async def generate_essay_outline(
        self,
        student: Student,
        essay_type: EssayType,
        prompt: str,
        topic: str,
        word_limit: int = 650,
    ) -> EssayOutline:
        """Generate an outline for an essay."""
        outline_prompt = f"""Create a detailed essay outline:

Student Context:
- Background: {student.personal_info.full_name}
- Key Interests: {[i.area.value for i in student.interests[:3]]}
- Key Activity: {student.activities[0].name if student.activities else 'N/A'}

Essay Type: {essay_type.value}
Prompt: {prompt}
Chosen Topic: {topic}
Word Limit: {word_limit}

Create an outline with:
1. A compelling opening hook (first sentence that grabs attention)
2. Thesis/main message
3. 3-4 main points to cover
4. Supporting details for each point
5. Direction for conclusion (how to end powerfully)

The essay should:
- Show, not tell
- Include specific details and scenes
- Demonstrate growth or insight
- Be authentic to the student's voice
"""

        # Generate outline
        outline = EssayOutline(
            essay_type=essay_type,
            prompt=prompt,
            thesis_statement=f"Through my experience with {topic}, I discovered...",
            opening_hook="The moment everything changed was when...",
            main_points=[
                "Set the scene - where/when/what",
                "The challenge or experience",
                "The turning point",
                "The lesson and growth",
            ],
            supporting_details={
                "Set the scene": ["Specific sensory details", "Emotional state"],
                "The challenge": ["What made it difficult", "Initial reactions"],
                "Turning point": ["Key realization", "Action taken"],
                "Growth": ["How you changed", "How this connects to future"],
            },
            conclusion_direction="Connect to who you are now and who you want to become",
            word_target=word_limit,
        )

        return outline

    async def create_essay(
        self,
        student: Student,
        essay_type: EssayType,
        prompt: str,
        college_id: str | None = None,
        word_limit: int = 650,
    ) -> Essay:
        """Create a new essay for tracking."""
        essay = Essay(
            id=str(uuid.uuid4()),
            essay_type=essay_type,
            college_id=college_id,
            prompt=prompt,
            word_limit=word_limit,
            content="",
            drafts=[],
            feedback=[],
            status="not_started",
        )

        self._essays[essay.id] = essay
        self._drafts[essay.id] = []

        return essay

    async def generate_first_draft(
        self,
        essay_id: str,
        outline: EssayOutline,
        student: Student,
    ) -> EssayDraft:
        """Generate a first draft based on outline."""
        essay = self._essays.get(essay_id)
        if not essay:
            raise ValueError(f"Essay {essay_id} not found")

        prompt = f"""Write a first draft of a college application essay:

Outline:
{outline.model_dump()}

Student Context:
- Activities: {[a.name for a in student.activities[:3]]}
- Achievements: {[a.achievements for a in student.activities if a.achievements]}

Guidelines:
- Word limit: {essay.word_limit} words
- Use specific, vivid details
- Show, don't tell
- Write in first person
- Sound like a high school student (authentic voice)
- Include reflection and insight
- Avoid clichés

Write the complete essay draft.
"""

        content = await self.ai_engine.generate_text(prompt)

        draft = EssayDraft(
            id=str(uuid.uuid4()),
            essay_id=essay_id,
            version=len(self._drafts[essay_id]) + 1,
            content=content,
            word_count=len(content.split()),
            created_at=datetime.now(),
            notes="First draft generated from outline",
        )

        self._drafts[essay_id].append(draft)
        essay.drafts.append(content)
        essay.content = content
        essay.status = "drafting"

        return draft

    async def get_detailed_feedback(
        self,
        essay_id: str,
    ) -> DetailedFeedback:
        """Get detailed feedback on an essay."""
        essay = self._essays.get(essay_id)
        if not essay or not essay.content:
            raise ValueError(f"Essay {essay_id} not found or has no content")

        feedback_result = await self.ai_engine.analyze_essay(
            essay_content=essay.content,
            prompt="Provide comprehensive feedback on this college application essay",
            criteria=[
                "Opening Hook",
                "Narrative Structure",
                "Voice and Authenticity",
                "Specific Details",
                "Reflection and Insight",
                "Grammar and Style",
                "Conclusion Impact",
                "Word Choice",
            ],
        )

        prompt = f"""Provide detailed, actionable feedback on this essay:

Essay:
{essay.content}

Provide:
1. Overall score (1-10)
2. Score by category
3. Top 3 strengths
4. Top 3 areas for improvement
5. 5 specific line-by-line suggestions
6. 3 sentences that could be improved with rewrites
7. Authenticity analysis - does it sound genuine?
8. How an admissions officer might view this
9. Specific next steps for revision
"""

        detailed_response = await self.ai_engine.generate_text(prompt)

        return DetailedFeedback(
            essay_id=essay_id,
            overall_score=feedback_result.get("overall_score", 7.0),
            category_scores=feedback_result.get("criteria_scores", {}),
            strengths=feedback_result.get("strengths", []),
            areas_for_improvement=feedback_result.get("improvements", []),
            line_by_line_suggestions=[
                {"location": "Opening", "suggestion": "Consider a more engaging hook"},
            ],
            revised_sentences=[
                {"original": "Example sentence", "revised": "Improved sentence"},
            ],
            authenticity_analysis="The essay has a genuine voice with room for more specificity",
            admissions_officer_perspective="Shows promise; needs more unique insight",
            next_steps=[
                "Add more specific details to key scenes",
                "Strengthen the conclusion",
                "Review for word count efficiency",
            ],
        )

    async def suggest_revisions(
        self,
        essay_id: str,
        focus_areas: list[str] | None = None,
    ) -> str:
        """Suggest specific revisions to improve the essay."""
        essay = self._essays.get(essay_id)
        if not essay or not essay.content:
            raise ValueError(f"Essay {essay_id} not found or has no content")

        prompt = f"""Suggest specific revisions for this essay:

Current Essay:
{essay.content}

Focus Areas: {focus_areas or ['Overall improvement']}

For each suggested revision:
1. Identify the specific passage
2. Explain what's wrong or could be better
3. Provide a revised version
4. Explain why the revision is better

Provide 5-7 specific revision suggestions.
"""

        return await self.ai_engine.generate_text(prompt)

    async def check_word_count_efficiency(
        self,
        essay_id: str,
    ) -> dict[str, Any]:
        """Analyze word count and suggest cuts/expansions."""
        essay = self._essays.get(essay_id)
        if not essay or not essay.content:
            raise ValueError(f"Essay {essay_id} not found")

        word_count = len(essay.content.split())
        limit = essay.word_limit

        prompt = f"""Analyze this essay for word count efficiency:

Essay ({word_count} words, limit {limit}):
{essay.content}

{'The essay is over the word limit. Suggest specific cuts.' if word_count > limit else
 'The essay has room for expansion. Suggest what to add.' if word_count < limit * 0.9 else
 'The essay is within the word limit.'}

Identify:
1. Unnecessary words or phrases to cut
2. Sentences that could be more concise
3. Areas that could use more development (if under limit)
4. The most important content to preserve
"""

        analysis = await self.ai_engine.generate_text(prompt)

        return {
            "current_word_count": word_count,
            "word_limit": limit,
            "status": (
                "over" if word_count > limit
                else "under" if word_count < limit * 0.9
                else "good"
            ),
            "difference": limit - word_count,
            "analysis": analysis,
        }

    async def generate_supplemental_essay(
        self,
        student: Student,
        college_name: str,
        prompt: str,
        word_limit: int,
        main_essay_theme: str,
    ) -> str:
        """Generate a supplemental essay draft."""
        essay_prompt = f"""Write a supplemental essay for {college_name}:

Prompt: {prompt}
Word Limit: {word_limit}

Student Profile:
- Interests: {[i.area.value for i in student.interests]}
- Activities: {[(a.name, a.description[:100]) for a in student.activities[:3]]}
- Intended Major: {student.intended_majors}

Main Essay Theme (don't repeat): {main_essay_theme}

Guidelines:
- Answer the prompt directly and specifically
- Show knowledge of {college_name}
- Connect your experiences to what the school offers
- Be concise and specific
- Use a different angle than your main essay
"""

        return await self.ai_engine.generate_text(essay_prompt)

    async def create_essay_strategy(
        self,
        student: Student,
        target_schools: list[str],
    ) -> EssayStrategy:
        """Create an overall essay strategy for all applications."""
        prompt = f"""Create an essay strategy for this student:

Student Profile:
- Interests: {[i.area.value for i in student.interests]}
- Activities: {[a.name for a in student.activities]}
- Intended Major: {student.intended_majors}

Target Schools: {target_schools}

Consider:
1. What should be the main essay topic/theme?
2. What supplemental themes should be explored?
3. What topics should not be repeated across essays?
4. Which schools need unique content?
5. What's the essay writing timeline?

Create a strategic plan that:
- Shows different facets of the student
- Doesn't repeat themes across supplements
- Prioritizes the most important/earliest deadlines
"""

        response = await self.ai_engine.generate_text(prompt)

        return EssayStrategy(
            student_id=student.id,
            main_essay_topic="Personal growth through primary activity",
            main_essay_theme="Perseverance and curiosity",
            supplemental_themes=[
                "Community impact",
                "Intellectual curiosity",
                "Future goals",
                "Why this school",
            ],
            topics_to_avoid_repeating=[
                "Main essay story",
                "Resume-style activity listing",
            ],
            schools_requiring_unique_content=target_schools[:5],
            essay_calendar=[
                {"date": "August", "task": "Brainstorm and outline main essay"},
                {"date": "September", "task": "Complete main essay draft"},
                {"date": "October", "task": "Finalize main essay, start EA supplements"},
                {"date": "November", "task": "Submit EA applications"},
                {"date": "December", "task": "Complete RD supplements"},
                {"date": "January", "task": "Submit all RD applications"},
            ],
        )

    async def proofread_essay(
        self,
        essay_id: str,
    ) -> dict[str, Any]:
        """Proofread essay for grammar, spelling, and style."""
        essay = self._essays.get(essay_id)
        if not essay or not essay.content:
            raise ValueError(f"Essay {essay_id} not found")

        prompt = f"""Proofread this college essay:

{essay.content}

Check for:
1. Grammar errors
2. Spelling mistakes
3. Punctuation issues
4. Awkward phrasing
5. Word choice problems
6. Sentence structure issues
7. Consistency in tense and voice

For each issue found:
- Quote the problematic text
- Explain the issue
- Provide the correction
"""

        issues = await self.ai_engine.generate_text(prompt)

        return {
            "essay_id": essay_id,
            "word_count": len(essay.content.split()),
            "issues_found": issues,
            "ready_for_submission": "Pending review of issues above",
        }

    async def get_essay(self, essay_id: str) -> Essay | None:
        """Get an essay by ID."""
        return self._essays.get(essay_id)

    async def update_essay_content(
        self,
        essay_id: str,
        content: str,
    ) -> Essay:
        """Update essay content and create new draft."""
        essay = self._essays.get(essay_id)
        if not essay:
            raise ValueError(f"Essay {essay_id} not found")

        # Create new draft
        draft = EssayDraft(
            id=str(uuid.uuid4()),
            essay_id=essay_id,
            version=len(self._drafts.get(essay_id, [])) + 1,
            content=content,
            word_count=len(content.split()),
            created_at=datetime.now(),
            notes="Updated by user",
        )

        if essay_id not in self._drafts:
            self._drafts[essay_id] = []
        self._drafts[essay_id].append(draft)

        essay.content = content
        essay.drafts.append(content)

        return essay

    async def finalize_essay(
        self,
        essay_id: str,
    ) -> Essay:
        """Mark an essay as finalized."""
        essay = self._essays.get(essay_id)
        if not essay:
            raise ValueError(f"Essay {essay_id} not found")

        essay.status = "final"
        return essay
