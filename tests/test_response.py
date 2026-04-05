"""Tests for Stage 3: Response Generation."""

import pytest
from unittest.mock import patch, MagicMock
from navigator.response import ResponseGenerator
from navigator.models import (
    UserProfile, Dependent, EligibilityResult, BenefitsResponse, ReadingLevel,
)


@pytest.fixture
def generator():
    return ResponseGenerator()


@pytest.fixture
def sample_response():
    return BenefitsResponse(
        eligible_programs=[
            EligibilityResult(
                program_id="snap", program_name="SNAP",
                eligible=True, confidence="high", category="food",
                reason="Below 200% FPL", estimated_benefit="$768/month",
                source="DHS Combined Manual", priority="high",
            ),
            EligibilityResult(
                program_id="unemployment_insurance",
                program_name="Unemployment Insurance",
                eligible=True, confidence="medium", category="employment",
                reason="Recently unemployed", priority="high",
                source="MN Statutes 268",
            ),
        ],
        documents_needed=["Photo ID", "Pay stubs", "Layoff letter"],
        application_groups={
            "MNbenefits.mn.gov": ["SNAP"],
            "uimn.org": ["Unemployment Insurance"],
        },
    )


@pytest.fixture
def sample_profile():
    return UserProfile(
        income=32000, household_size=3, county="Ramsey",
        employment_status="recently_unemployed",
        dependents=[Dependent(age=3), Dependent(age=7)],
        reading_level=ReadingLevel.SIMPLE,
        language="en",
    )


def test_format_context(generator, sample_response, sample_profile):
    """Test that the context formatted for the LLM includes all key info."""
    context = generator._format_context(sample_response, sample_profile)
    assert "SNAP" in context
    assert "Unemployment Insurance" in context
    assert "Photo ID" in context
    assert "MNbenefits.mn.gov" in context


@patch("navigator.response.OllamaClient")
def test_generate_calls_ollama(MockClient, sample_response, sample_profile):
    mock_instance = MockClient.return_value
    mock_instance.chat.return_value = "Here are the programs you may be eligible for..."
    gen = ResponseGenerator(client=mock_instance)

    result = gen.generate(sample_response, sample_profile)
    assert isinstance(result, str)
    assert len(result) > 0
    mock_instance.chat.assert_called_once()


def test_format_context_includes_disclaimer(generator, sample_response, sample_profile):
    context = generator._format_context(sample_response, sample_profile)
    assert "informational tool" in context.lower() or "not legal advice" in context.lower()
