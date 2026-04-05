"""Tests for the readability checker."""

import pytest
from navigator.readability import check_readability, meets_reading_level
from navigator.models import ReadingLevel


def test_check_readability_returns_scores():
    text = "The cat sat on the mat. It was a nice day."
    result = check_readability(text)
    assert "flesch_kincaid_grade" in result
    assert "flesch_reading_ease" in result
    assert isinstance(result["flesch_kincaid_grade"], float)


def test_simple_text_low_grade():
    text = "I need food. My kids are hungry. We need help now."
    result = check_readability(text)
    assert result["flesch_kincaid_grade"] < 5.0


def test_complex_text_high_grade():
    text = (
        "The Supplemental Nutrition Assistance Program eligibility determination "
        "necessitates comprehensive evaluation of household income relative to "
        "categorical eligibility thresholds established pursuant to federal "
        "poverty guidelines promulgated annually by the Department of Health "
        "and Human Services."
    )
    result = check_readability(text)
    assert result["flesch_kincaid_grade"] > 12.0


def test_meets_simple_level():
    simple = "I lost my job. I have two kids. I need help with food and rent."
    assert meets_reading_level(simple, ReadingLevel.SIMPLE)


def test_complex_fails_simple_level():
    complex_text = (
        "The categorical eligibility determination for supplemental nutrition "
        "assistance requires comprehensive evaluation of modified adjusted gross "
        "income relative to federally mandated poverty thresholds."
    )
    assert not meets_reading_level(complex_text, ReadingLevel.SIMPLE)


def test_any_text_meets_detailed():
    text = "Any text should pass the detailed reading level check."
    assert meets_reading_level(text, ReadingLevel.DETAILED)
