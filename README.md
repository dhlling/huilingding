# AI College Planning System

A comprehensive AI-powered platform that guides high school students through their 4-year journey from freshman year to college applications.

## Overview

This system provides personalized guidance through every phase of college preparation:

- **Freshman Year**: Foundation building, interest exploration, activity discovery
- **Sophomore Year**: Skill development, deeper engagement, initial competition exposure
- **Junior Year**: Leadership roles, standardized testing, college research
- **Senior Year**: Applications, essays, decisions

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     AI College Planning System                   │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Orchestration Layer (Module 8)              │   │
│  │         Timeline & Milestone Management                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐      │
│  │Module 1  │Module 2  │Module 3  │Module 4  │Module 5  │      │
│  │Profile & │Academic  │Extra-    │Summer    │College   │      │
│  │Assess    │Planning  │curricular│Programs  │Research  │      │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘      │
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Application Layer (Modules 6-7)             │   │
│  │         Essay Workshop + Application Manager             │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Modules

### Module 1: Student Profile & Assessment Engine
- Initial interest inventory and personality assessment
- Academic strength/weakness identification
- Learning style analysis
- Goal setting framework

### Module 2: Academic Planning System
- Course selection optimization
- GPA trajectory planning
- AP/IB/Honors recommendations
- Prerequisites mapping

### Module 3: Extracurricular & Competition Advisor
- Activity recommendations based on interests
- Competition matching (Olympiads, Science Fairs, Debate)
- Leadership opportunity identification
- "Spike" development strategy

### Module 4: Summer Programs & Opportunities Engine
- Pre-college programs matching
- Research opportunities
- Internship recommendations
- Selective program application guidance

### Module 5: College Research & Matching System
- College database with smart filtering
- Admission statistics analysis
- School culture matching
- Financial aid estimation
- Balanced list building (reach/match/safety)

### Module 6: Essay Development Workshop
- Personal narrative discovery
- Common App essay guidance
- Supplemental essay strategies
- AI-powered feedback and revision

### Module 7: Application Assembly & Submission Manager
- Application timeline management
- Document checklist tracking
- Recommendation letter coordination
- Interview preparation

### Module 8: Timeline & Milestone Orchestrator
- 4-year master calendar
- Deadline tracking
- Progress monitoring
- Adaptive recommendations

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd ai-college-planner

# Install dependencies
pip install -e .

# For development
pip install -e ".[dev]"
```

## Usage

### Command Line Interface

```bash
# Display welcome message
college-planner welcome

# Create a new student profile
college-planner create-student

# View dashboard
college-planner dashboard

# Add interests
college-planner add-interest mathematics --level passionate

# Get activity recommendations
college-planner recommend-activities

# Get college recommendations
college-planner recommend-colleges --count 15

# Build balanced college list
college-planner build-college-list

# View timeline and milestones
college-planner timeline

# Get summer program recommendations
college-planner summer-programs --year 2025 --budget 5000

# Start essay brainstorming
college-planner essay-brainstorm
```

### Python API

```python
import asyncio
from src.main import CollegePlanningSystem
from datetime import date

async def main():
    # Initialize the system
    system = CollegePlanningSystem(ai_provider="anthropic", api_key="your-key")
    await system.initialize()

    # Create a student profile
    student = await system.create_new_student(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        date_of_birth=date(2008, 5, 15),
        high_school="Springfield High",
        graduation_year=2026,
        state="CA",
    )

    # Get activity recommendations
    activities = await system.extracurricular.recommend_activities(student)

    # Get college matches
    matches = await system.college.match_colleges(student, count=10)

    # Build college list
    college_list = await system.college.build_college_list(student)

    # Get timeline progress
    progress = await system.timeline.generate_progress_report(student)

asyncio.run(main())
```

## Configuration

### AI Provider

The system supports multiple AI providers:

```python
# Anthropic Claude (recommended)
system = CollegePlanningSystem(ai_provider="anthropic", api_key="sk-...")

# OpenAI GPT
system = CollegePlanningSystem(ai_provider="openai", api_key="sk-...")

# Mock (for testing without API)
system = CollegePlanningSystem(ai_provider="mock")
```

### Environment Variables

```bash
# Set API keys via environment
export ANTHROPIC_API_KEY="sk-..."
export OPENAI_API_KEY="sk-..."
```

## Project Structure

```
ai-college-planner/
├── src/
│   ├── __init__.py
│   ├── main.py              # CLI and main orchestrator
│   ├── core/
│   │   ├── __init__.py
│   │   ├── base.py          # Base classes and interfaces
│   │   ├── models.py        # Pydantic data models
│   │   ├── enums.py         # Enumerations
│   │   └── ai_engine.py     # AI/LLM integration
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── profile.py       # Module 1: Student Profile
│   │   ├── academic.py      # Module 2: Academic Planning
│   │   ├── extracurricular.py  # Module 3: Activities
│   │   ├── summer_programs.py  # Module 4: Summer Programs
│   │   ├── college_research.py # Module 5: College Matching
│   │   ├── essay.py         # Module 6: Essay Workshop
│   │   ├── application.py   # Module 7: Applications
│   │   └── timeline.py      # Module 8: Timeline
│   ├── data/                # Data layer
│   ├── utils/               # Utility functions
│   └── api/                 # API endpoints
├── tests/                   # Test suite
├── config/                  # Configuration files
├── data/                    # Static data files
│   ├── colleges/
│   ├── activities/
│   └── programs/
├── pyproject.toml
├── ARCHITECTURE.md
└── README.md
```

## Key Features

### Personalized Recommendations
AI-driven suggestions based on individual student profiles, interests, and goals.

### Timeline Automation
Smart deadline tracking and milestone management across all four years.

### Progress Analytics
Visual dashboards showing growth, achievements, and areas for improvement.

### Essay Intelligence
NLP-powered writing assistance with feedback and revision suggestions.

### College Matching
Data-driven school recommendations with admission probability estimates.

### Activity Optimization
Strategic extracurricular planning for "spike" development.

## Development

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src

# Format code
black src tests

# Lint
ruff src tests

# Type check
mypy src
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For questions or issues, please open a GitHub issue.
