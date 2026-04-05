"""Tests for Stage 2: Eligibility Engine."""

import pytest
from unittest.mock import MagicMock, patch
from navigator.eligibility import EligibilityEngine
from navigator.models import UserProfile, Dependent, EligibilityResult


@pytest.fixture
def profile():
    return UserProfile(
        income=32000,
        household_size=3,
        county="Ramsey",
        employment_status="recently_unemployed",
        dependents=[Dependent(age=3), Dependent(age=7)],
        concerns=["food", "housing"],
    )


def test_check_snap_eligible(profile):
    """Family at 121% FPL should be SNAP eligible (MN BBCE: 200% FPL)."""
    engine = EligibilityEngine.__new__(EligibilityEngine)
    result = engine._check_snap(profile)
    assert result.eligible is True
    assert result.confidence == "high"
    assert "200%" in result.reason


def test_check_snap_over_income():
    """Family over 200% FPL should not be SNAP eligible."""
    profile = UserProfile(income=80000, household_size=3)
    engine = EligibilityEngine.__new__(EligibilityEngine)
    result = engine._check_snap(profile)
    assert result.eligible is False


def test_check_mfip_eligible(profile):
    """Family with children in poverty should be MFIP eligible."""
    engine = EligibilityEngine.__new__(EligibilityEngine)
    result = engine._check_mfip(profile)
    assert result.eligible is True


def test_check_mfip_no_children():
    """Single adult without children should not be MFIP eligible."""
    profile = UserProfile(income=20000, household_size=1)
    engine = EligibilityEngine.__new__(EligibilityEngine)
    result = engine._check_mfip(profile)
    assert result.eligible is False


def test_check_medical_assistance_eligible(profile):
    """Family at 121% FPL should be MA eligible (138% FPL threshold)."""
    engine = EligibilityEngine.__new__(EligibilityEngine)
    result = engine._check_medical_assistance(profile)
    assert result.eligible is True


def test_check_ui_eligible(profile):
    """Recently unemployed should be UI eligible."""
    engine = EligibilityEngine.__new__(EligibilityEngine)
    result = engine._check_unemployment(profile)
    assert result.eligible is True


def test_check_ui_still_employed():
    """Employed person should not be UI eligible."""
    profile = UserProfile(income=50000, employment_status="employed")
    engine = EligibilityEngine.__new__(EligibilityEngine)
    result = engine._check_unemployment(profile)
    assert result.eligible is False


def test_determine_all_programs(profile):
    """Integration: should find multiple programs for a laid-off single mom."""
    engine = EligibilityEngine.__new__(EligibilityEngine)
    results = engine._run_rule_checks(profile)
    program_ids = [r.program_id for r in results if r.eligible]
    assert "snap" in program_ids
    assert "mfip" in program_ids
    assert "medical_assistance" in program_ids
    assert "unemployment_insurance" in program_ids
