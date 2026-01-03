"""AI Engine implementations for LLM integration."""

import json
from typing import Any, TypeVar

from pydantic import BaseModel

from src.core.base import AIEngine


T = TypeVar("T", bound=BaseModel)


class AnthropicEngine(AIEngine):
    """AI Engine using Anthropic's Claude API."""

    def __init__(self, api_key: str | None = None, model: str = "claude-sonnet-4-20250514"):
        self.model = model
        self._api_key = api_key
        self._client = None

    async def _get_client(self):
        """Lazy initialization of the Anthropic client."""
        if self._client is None:
            try:
                import anthropic
                self._client = anthropic.AsyncAnthropic(api_key=self._api_key)
            except ImportError:
                raise ImportError("anthropic package not installed. Run: pip install anthropic")
        return self._client

    async def generate_text(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Generate text using Claude."""
        client = await self._get_client()

        message = await client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt or "You are an expert college admissions counselor.",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )

        return message.content[0].text

    async def generate_structured(
        self,
        prompt: str,
        response_model: type[T],
        system_prompt: str | None = None,
    ) -> T:
        """Generate structured output conforming to a Pydantic model."""
        schema = response_model.model_json_schema()

        structured_prompt = f"""{prompt}

Please respond with valid JSON matching this schema:
{json.dumps(schema, indent=2)}

Respond ONLY with the JSON object, no additional text."""

        response = await self.generate_text(
            prompt=structured_prompt,
            system_prompt=system_prompt,
            temperature=0.3,  # Lower temperature for structured output
        )

        # Parse JSON from response
        try:
            # Handle potential markdown code blocks
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]

            data = json.loads(response.strip())
            return response_model.model_validate(data)
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Failed to parse structured response: {e}")

    async def analyze_essay(
        self,
        essay_content: str,
        prompt: str,
        criteria: list[str],
    ) -> dict[str, Any]:
        """Analyze an essay based on given criteria."""
        criteria_list = "\n".join(f"- {c}" for c in criteria)

        analysis_prompt = f"""{prompt}

Essay to analyze:
---
{essay_content}
---

Please evaluate based on these criteria:
{criteria_list}

Provide your analysis as a JSON object with:
- "overall_score": float 1-10
- "criteria_scores": dict of criterion -> score
- "strengths": list of strengths
- "improvements": list of areas for improvement
- "specific_feedback": detailed feedback string
"""
        response = await self.generate_text(
            prompt=analysis_prompt,
            system_prompt="You are an expert college essay reviewer with decades of experience.",
            temperature=0.4,
        )

        try:
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
            return json.loads(response.strip())
        except json.JSONDecodeError:
            return {
                "overall_score": 0,
                "error": "Failed to parse analysis",
                "raw_response": response,
            }

    async def chat(
        self,
        messages: list[dict[str, str]],
        system_prompt: str | None = None,
    ) -> str:
        """Have a multi-turn conversation."""
        client = await self._get_client()

        message = await client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=system_prompt or "You are an expert college admissions counselor.",
            messages=messages,
        )

        return message.content[0].text


class OpenAIEngine(AIEngine):
    """AI Engine using OpenAI's API."""

    def __init__(self, api_key: str | None = None, model: str = "gpt-4"):
        self.model = model
        self._api_key = api_key
        self._client = None

    async def _get_client(self):
        """Lazy initialization of the OpenAI client."""
        if self._client is None:
            try:
                import openai
                self._client = openai.AsyncOpenAI(api_key=self._api_key)
            except ImportError:
                raise ImportError("openai package not installed. Run: pip install openai")
        return self._client

    async def generate_text(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Generate text using OpenAI."""
        client = await self._get_client()

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content

    async def generate_structured(
        self,
        prompt: str,
        response_model: type[T],
        system_prompt: str | None = None,
    ) -> T:
        """Generate structured output conforming to a Pydantic model."""
        schema = response_model.model_json_schema()

        structured_prompt = f"""{prompt}

Please respond with valid JSON matching this schema:
{json.dumps(schema, indent=2)}

Respond ONLY with the JSON object, no additional text."""

        response = await self.generate_text(
            prompt=structured_prompt,
            system_prompt=system_prompt,
            temperature=0.3,
        )

        try:
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]

            data = json.loads(response.strip())
            return response_model.model_validate(data)
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Failed to parse structured response: {e}")

    async def analyze_essay(
        self,
        essay_content: str,
        prompt: str,
        criteria: list[str],
    ) -> dict[str, Any]:
        """Analyze an essay based on given criteria."""
        criteria_list = "\n".join(f"- {c}" for c in criteria)

        analysis_prompt = f"""{prompt}

Essay to analyze:
---
{essay_content}
---

Please evaluate based on these criteria:
{criteria_list}

Provide your analysis as a JSON object with:
- "overall_score": float 1-10
- "criteria_scores": dict of criterion -> score
- "strengths": list of strengths
- "improvements": list of areas for improvement
- "specific_feedback": detailed feedback string
"""
        response = await self.generate_text(
            prompt=analysis_prompt,
            system_prompt="You are an expert college essay reviewer.",
            temperature=0.4,
        )

        try:
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
            return json.loads(response.strip())
        except json.JSONDecodeError:
            return {
                "overall_score": 0,
                "error": "Failed to parse analysis",
                "raw_response": response,
            }

    async def chat(
        self,
        messages: list[dict[str, str]],
        system_prompt: str | None = None,
    ) -> str:
        """Have a multi-turn conversation."""
        client = await self._get_client()

        all_messages = []
        if system_prompt:
            all_messages.append({"role": "system", "content": system_prompt})
        all_messages.extend(messages)

        response = await client.chat.completions.create(
            model=self.model,
            messages=all_messages,
        )

        return response.choices[0].message.content


class MockAIEngine(AIEngine):
    """Mock AI Engine for testing without API calls."""

    async def generate_text(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Return mock response."""
        return f"Mock response to: {prompt[:100]}..."

    async def generate_structured(
        self,
        prompt: str,
        response_model: type[T],
        system_prompt: str | None = None,
    ) -> T:
        """Return mock structured response with default values."""
        # Create instance with minimal required fields
        return response_model.model_construct()

    async def analyze_essay(
        self,
        essay_content: str,
        prompt: str,
        criteria: list[str],
    ) -> dict[str, Any]:
        """Return mock analysis."""
        return {
            "overall_score": 7.5,
            "criteria_scores": {c: 7.5 for c in criteria},
            "strengths": ["Clear writing", "Good structure"],
            "improvements": ["Add more specific examples"],
            "specific_feedback": "This is a mock analysis.",
        }

    async def chat(
        self,
        messages: list[dict[str, str]],
        system_prompt: str | None = None,
    ) -> str:
        """Return mock chat response."""
        last_message = messages[-1]["content"] if messages else ""
        return f"Mock response to: {last_message[:100]}..."


def create_ai_engine(
    provider: str = "anthropic",
    api_key: str | None = None,
    model: str | None = None,
) -> AIEngine:
    """Factory function to create an AI engine."""
    if provider == "anthropic":
        return AnthropicEngine(api_key=api_key, model=model or "claude-sonnet-4-20250514")
    elif provider == "openai":
        return OpenAIEngine(api_key=api_key, model=model or "gpt-4")
    elif provider == "mock":
        return MockAIEngine()
    else:
        raise ValueError(f"Unknown AI provider: {provider}")
