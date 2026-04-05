"""Readability checking via textstat for reading level adaptation."""

import textstat

from navigator.config import TARGET_READING_LEVELS
from navigator.models import ReadingLevel


def check_readability(text: str) -> dict:
    """Compute readability scores for the given text."""
    return {
        "flesch_kincaid_grade": textstat.flesch_kincaid_grade(text),
        "flesch_reading_ease": textstat.flesch_reading_ease(text),
        "text_length_words": textstat.lexicon_count(text),
    }


def meets_reading_level(text: str, level: ReadingLevel) -> bool:
    """Check if text meets the target reading level."""
    target_grade = TARGET_READING_LEVELS[level.value]
    actual_grade = textstat.flesch_kincaid_grade(text)
    return actual_grade <= target_grade
