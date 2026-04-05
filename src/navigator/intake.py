"""Stage 1: Intake & Extraction — parse user situation into a structured profile."""

import logging

from navigator.models import UserProfile, Dependent, ReadingLevel
from navigator.ollama_client import OllamaClient
from navigator.prompts import INTAKE_SYSTEM_PROMPT, INTAKE_MISSING_INFO_PROMPT

logger = logging.getLogger(__name__)

# Fields that are critical for eligibility determination
CRITICAL_FIELDS = ["income", "county", "household_size"]


class IntakeProcessor:
    """Extracts a structured UserProfile from natural language input."""

    def __init__(self, client: OllamaClient | None = None):
        self.client = client or OllamaClient()

    def extract(self, user_message: str) -> tuple[UserProfile, list[str]]:
        """Extract a UserProfile from the user's situation description.

        Returns:
            Tuple of (profile, missing_fields). If missing_fields is non-empty,
            the caller should ask follow-up questions.
        """
        raw = self.client.chat_json(user_message, system_prompt=INTAKE_SYSTEM_PROMPT)
        profile = self._json_to_profile(raw)
        missing = self._get_missing_fields(profile)
        return profile, missing

    def ask_followup(self, missing_fields: list[str]) -> str:
        """Generate a friendly follow-up question for missing information."""
        prompt = INTAKE_MISSING_INFO_PROMPT.format(missing_fields=", ".join(missing_fields))
        return self.client.chat(
            f"Missing fields: {', '.join(missing_fields)}",
            system_prompt=prompt,
        )

    def _json_to_profile(self, data: dict) -> UserProfile:
        """Convert raw JSON from the model into a UserProfile."""
        dependents = []
        for dep in data.get("dependents") or []:
            if isinstance(dep, dict):
                dependents.append(Dependent(
                    age=dep.get("age", 0),
                    relationship=dep.get("relationship", "child"),
                ))

        language = data.get("language", "en") or "en"

        return UserProfile(
            income=data.get("income"),
            household_size=data.get("household_size", 1) or 1,
            county=data.get("county"),
            state="MN",
            employment_status=data.get("employment_status"),
            dependents=dependents,
            age=data.get("age"),
            is_veteran=data.get("is_veteran", False) or False,
            is_disabled=data.get("is_disabled", False) or False,
            citizenship_status=data.get("citizenship_status", "citizen") or "citizen",
            concerns=data.get("concerns") or [],
            language=language,
        )

    def _get_missing_fields(self, profile: UserProfile) -> list[str]:
        """Identify critical fields that are still missing."""
        missing = []
        if profile.income is None:
            missing.append("income")
        if profile.county is None:
            missing.append("county")
        if profile.household_size == 1 and len(profile.dependents) > 0:
            missing.append("household_size")
        return missing
