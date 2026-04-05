"""Tests for Stage 1: Intake & Extraction.

Uses mocked Ollama responses since we can't depend on a running server in CI.
"""

import json
import pytest
from unittest.mock import patch, MagicMock
from navigator.intake import IntakeProcessor
from navigator.models import UserProfile


@pytest.fixture
def processor():
    return IntakeProcessor()


def test_parse_profile_from_json(processor):
    raw_json = {
        "income": 32000,
        "household_size": 3,
        "county": "Ramsey",
        "employment_status": "recently_unemployed",
        "dependents": [{"age": 3}, {"age": 7}],
        "concerns": ["food", "housing"],
        "language": "en",
        "missing_info": [],
    }
    profile = processor._json_to_profile(raw_json)
    assert isinstance(profile, UserProfile)
    assert profile.income == 32000
    assert profile.county == "Ramsey"
    assert len(profile.dependents) == 2
    assert profile.household_size == 3


def test_parse_profile_with_missing_info(processor):
    raw_json = {
        "income": None,
        "household_size": 3,
        "county": None,
        "employment_status": "recently_unemployed",
        "dependents": [],
        "concerns": ["food"],
        "language": "en",
        "missing_info": ["income", "county"],
    }
    profile = processor._json_to_profile(raw_json)
    assert profile.income is None
    assert profile.county is None


def test_identify_missing_fields(processor):
    profile = UserProfile(household_size=3, employment_status="recently_unemployed")
    missing = processor._get_missing_fields(profile)
    assert "income" in missing
    assert "county" in missing


def test_no_missing_fields(processor):
    profile = UserProfile(
        income=32000,
        household_size=3,
        county="Ramsey",
    )
    missing = processor._get_missing_fields(profile)
    assert len(missing) == 0


@patch("navigator.intake.OllamaClient")
def test_extract_profile(MockClient, processor):
    mock_instance = MockClient.return_value
    mock_instance.chat_json.return_value = {
        "income": 32000,
        "household_size": 3,
        "county": "Ramsey",
        "employment_status": "recently_unemployed",
        "dependents": [{"age": 3}, {"age": 7}],
        "concerns": ["food", "housing"],
        "language": "en",
        "missing_info": [],
    }
    processor.client = mock_instance

    profile, missing = processor.extract("I'm a single mom with two kids...")
    assert profile.income == 32000
    assert profile.county == "Ramsey"
    assert len(missing) == 0
