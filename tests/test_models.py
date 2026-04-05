"""Tests for navigator data models."""

import pytest
from navigator.models import (
    UserProfile,
    Dependent,
    Program,
    EligibilityResult,
    BenefitsResponse,
    ReadingLevel,
)


def test_user_profile_from_basic_info():
    profile = UserProfile(
        income=32000,
        household_size=3,
        county="Ramsey",
        state="MN",
        employment_status="recently_unemployed",
        dependents=[Dependent(age=3), Dependent(age=7)],
        concerns=["housing", "food"],
    )
    assert profile.income == 32000
    assert profile.household_size == 3
    assert profile.county == "Ramsey"
    assert len(profile.dependents) == 2


def test_user_profile_defaults():
    profile = UserProfile()
    assert profile.state == "MN"
    assert profile.household_size == 1
    assert profile.language == "en"
    assert profile.reading_level == ReadingLevel.STANDARD
    assert profile.dependents == []
    assert profile.concerns == []


def test_user_profile_fpl_percentage():
    # 2026 FPL for household of 3 is $26,070 (approx)
    profile = UserProfile(income=32000, household_size=3)
    # 32000 / 26070 = ~122.7% FPL
    pct = profile.fpl_percentage
    assert 120 < pct < 130


def test_program_model():
    program = Program(
        id="snap_mn",
        name="SNAP (Food Assistance)",
        category="food",
        jurisdiction="state:MN",
        description="Monthly food benefits loaded onto an EBT card.",
        eligibility_summary="Income below 200% FPL (MN BBCE threshold).",
        application_url="https://mnbenefits.mn.gov/",
        source="DHS Combined Manual Section 0007.06",
    )
    assert program.id == "snap_mn"
    assert program.jurisdiction == "state:MN"


def test_eligibility_result():
    result = EligibilityResult(
        program_id="snap_mn",
        program_name="SNAP (Food Assistance)",
        eligible=True,
        confidence="high",
        reason="Household income $32,000 = 123% FPL, below MN's 200% BBCE threshold.",
        estimated_benefit="$658/month for household of 3",
        source="DHS Combined Manual Section 0007.06",
    )
    assert result.eligible is True
    assert result.confidence == "high"


def test_benefits_response():
    result = EligibilityResult(
        program_id="snap_mn",
        program_name="SNAP",
        eligible=True,
        confidence="high",
        reason="Below threshold",
    )
    response = BenefitsResponse(
        eligible_programs=[result],
        documents_needed=["Photo ID", "Pay stubs"],
        application_groups={"mnbenefits.mn.gov": ["SNAP", "MFIP"]},
        disclaimer="This is an informational tool, not legal advice.",
    )
    assert len(response.eligible_programs) == 1
    assert "Photo ID" in response.documents_needed


def test_reading_level_enum():
    assert ReadingLevel.SIMPLE.value == "simple"
    assert ReadingLevel.STANDARD.value == "standard"
    assert ReadingLevel.DETAILED.value == "detailed"
