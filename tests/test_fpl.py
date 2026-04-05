"""Tests for the Federal Poverty Level calculator tool."""

import pytest
from navigator.tools.fpl import calculate_fpl, check_fpl_threshold


def test_fpl_single_person():
    result = calculate_fpl(income=15000, household_size=1)
    assert result["fpl_threshold"] == 15_650
    assert round(result["fpl_percentage"], 1) == 95.8
    assert result["household_size"] == 1


def test_fpl_family_of_three():
    result = calculate_fpl(income=32000, household_size=3)
    # FPL for 3 = 15650 + 5380*2 = 26410
    assert result["fpl_threshold"] == 26_410
    pct = result["fpl_percentage"]
    assert 121 < pct < 122  # 32000/26410 = 121.2%


def test_fpl_family_of_four():
    result = calculate_fpl(income=40000, household_size=4)
    # FPL for 4 = 15650 + 5380*3 = 31790
    assert result["fpl_threshold"] == 31_790


def test_check_threshold_below():
    result = check_fpl_threshold(income=20000, household_size=3, threshold_pct=200)
    assert result["below_threshold"] is True
    assert result["threshold_pct"] == 200


def test_check_threshold_above():
    result = check_fpl_threshold(income=60000, household_size=3, threshold_pct=200)
    assert result["below_threshold"] is False


def test_fpl_zero_income():
    result = calculate_fpl(income=0, household_size=1)
    assert result["fpl_percentage"] == 0.0


def test_mn_snap_bbce_threshold():
    """MN uses 200% FPL BBCE threshold for SNAP."""
    result = check_fpl_threshold(income=32000, household_size=3, threshold_pct=200)
    assert result["below_threshold"] is True


def test_mn_medicaid_threshold():
    """MN Medicaid (MA) uses 138% FPL."""
    result = check_fpl_threshold(income=32000, household_size=3, threshold_pct=138)
    assert result["below_threshold"] is True


def test_mn_minnesotacare_threshold():
    """MinnesotaCare uses 200% FPL."""
    result = check_fpl_threshold(income=50000, household_size=3, threshold_pct=200)
    assert result["below_threshold"] is True
