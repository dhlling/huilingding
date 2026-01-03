"""Base classes and interfaces for the college planning system."""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from pydantic import BaseModel

from src.core.models import Student


T = TypeVar("T", bound=BaseModel)


class BaseModule(ABC):
    """Base class for all planning modules."""

    def __init__(self, ai_engine: "AIEngine"):
        self.ai_engine = ai_engine
        self._initialized = False

    @property
    @abstractmethod
    def name(self) -> str:
        """Module name for identification."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Module description."""
        pass

    async def initialize(self) -> None:
        """Initialize the module (load data, etc.)."""
        self._initialized = True

    def ensure_initialized(self) -> None:
        """Ensure module is initialized before use."""
        if not self._initialized:
            raise RuntimeError(f"Module {self.name} not initialized. Call initialize() first.")


class AIEngine(ABC):
    """Abstract base class for AI/LLM integration."""

    @abstractmethod
    async def generate_text(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Generate text using the AI model."""
        pass

    @abstractmethod
    async def generate_structured(
        self,
        prompt: str,
        response_model: type[T],
        system_prompt: str | None = None,
    ) -> T:
        """Generate structured output conforming to a Pydantic model."""
        pass

    @abstractmethod
    async def analyze_essay(
        self,
        essay_content: str,
        prompt: str,
        criteria: list[str],
    ) -> dict[str, Any]:
        """Analyze an essay based on given criteria."""
        pass

    @abstractmethod
    async def chat(
        self,
        messages: list[dict[str, str]],
        system_prompt: str | None = None,
    ) -> str:
        """Have a multi-turn conversation."""
        pass


class RecommendationEngine(ABC, Generic[T]):
    """Base class for recommendation engines."""

    @abstractmethod
    async def get_recommendations(
        self,
        student: Student,
        count: int = 5,
        filters: dict[str, Any] | None = None,
    ) -> list[T]:
        """Get personalized recommendations for a student."""
        pass

    @abstractmethod
    async def explain_recommendation(
        self,
        student: Student,
        recommendation: T,
    ) -> str:
        """Explain why a recommendation was made."""
        pass


class DataRepository(ABC, Generic[T]):
    """Base class for data repositories."""

    @abstractmethod
    async def get(self, id: str) -> T | None:
        """Get an item by ID."""
        pass

    @abstractmethod
    async def get_all(self) -> list[T]:
        """Get all items."""
        pass

    @abstractmethod
    async def create(self, item: T) -> T:
        """Create a new item."""
        pass

    @abstractmethod
    async def update(self, id: str, item: T) -> T:
        """Update an existing item."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete an item."""
        pass

    @abstractmethod
    async def search(self, query: dict[str, Any]) -> list[T]:
        """Search for items matching criteria."""
        pass
