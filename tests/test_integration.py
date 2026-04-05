"""End-to-end integration tests for the Navigator pipeline.

Tests the full flow: UserProfile -> EligibilityEngine -> ResponseGenerator.
Ollama calls are mocked; everything else runs for real.
"""

import pytest
from unittest.mock import patch, MagicMock
from navigator.models import UserProfile, Dependent, ReadingLevel
from navigator.eligibility import EligibilityEngine
from navigator.response import ResponseGenerator
from navigator.tools.county_programs import CountyProgramsTool
from navigator.tools.document_requirements import DocumentRequirementsTool


@pytest.fixture
def profile():
    """The canonical test scenario: single mom, Ramsey County, laid off."""
    return UserProfile(
        income=32000,
        household_size=3,
        county="Ramsey",
        state="MN",
        employment_status="recently_unemployed",
        dependents=[Dependent(age=3), Dependent(age=7)],
        concerns=["food", "housing"],
        language="en",
        reading_level=ReadingLevel.SIMPLE,
    )


def test_full_pipeline_no_ollama(profile):
    """Test eligibility engine produces correct results without Ollama."""
    engine = EligibilityEngine()
    response = engine.evaluate(profile)

    # Should find multiple programs
    program_ids = [r.program_id for r in response.eligible_programs]
    assert "snap" in program_ids, "SNAP should be eligible at 121% FPL"
    assert "mfip" in program_ids, "MFIP should be eligible (has children, low income)"
    assert "medical_assistance" in program_ids, "MA should be eligible at 121% FPL < 138%"
    assert "unemployment_insurance" in program_ids, "UI should be eligible (recently unemployed)"
    assert "wic" in program_ids, "WIC should be eligible (child under 5, below 185% FPL)"

    # Should have documents
    assert len(response.documents_needed) > 0
    assert "Government-issued photo ID" in response.documents_needed

    # Should have application groups
    assert "MNbenefits.mn.gov" in response.application_groups
    assert "uimn.org" in response.application_groups

    # Should have disclaimer
    assert "not legal advice" in response.disclaimer


def test_county_programs_included(profile):
    """Ramsey County should include Dislocated Worker and CAPRW."""
    engine = EligibilityEngine()
    response = engine.evaluate(profile)
    names = [r.program_name for r in response.eligible_programs]

    assert any("Dislocated Worker" in n for n in names), \
        "Ramsey County Dislocated Worker should be included"
    assert any("CAPRW" in n for n in names), \
        "CAPRW community programs should be included"


def test_high_income_fewer_programs():
    """High income household should have fewer eligible programs."""
    profile = UserProfile(
        income=120000,
        household_size=3,
        county="Ramsey",
        employment_status="employed",
    )
    engine = EligibilityEngine()
    response = engine.evaluate(profile)
    eligible = [r for r in response.eligible_programs]
    # Should not qualify for income-based programs
    ids = [r.program_id for r in eligible]
    assert "snap" not in ids
    assert "mfip" not in ids
    assert "medical_assistance" not in ids


@patch("navigator.response.OllamaClient")
def test_response_generation(MockClient, profile):
    """Test that response generation calls Ollama with correct context."""
    mock_instance = MockClient.return_value
    mock_instance.chat.return_value = "Based on your situation, you may be eligible for..."

    engine = EligibilityEngine()
    benefits_response = engine.evaluate(profile)

    gen = ResponseGenerator(client=mock_instance)
    text = gen.generate(benefits_response, profile)

    assert isinstance(text, str)
    # Verify the system prompt includes reading level
    call_args = mock_instance.chat.call_args
    system_prompt = call_args[1].get("system_prompt") or call_args[0][1]
    assert "simple" in system_prompt.lower()
