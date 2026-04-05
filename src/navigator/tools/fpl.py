"""Federal Poverty Level calculator.

Uses 2026 HHS Poverty Guidelines for the 48 contiguous states.
This is a deterministic calculation, not a model inference.
"""

import json
from pathlib import Path

from navigator.config import FPL_DIR

_FPL_DATA_PATH = FPL_DIR / "fpl_2026.json"

# Default values matching 2026 guidelines
_BASE = 15_650
_PER_ADDITIONAL = 5_380


def _load_fpl_data() -> tuple[int, int]:
    """Load FPL thresholds from data file, fall back to defaults."""
    if _FPL_DATA_PATH.exists():
        data = json.loads(_FPL_DATA_PATH.read_text())
        return data["base_amount"], data["per_additional_person"]
    return _BASE, _PER_ADDITIONAL


def fpl_threshold(household_size: int) -> int:
    """Return the FPL dollar threshold for a given household size."""
    base, per_additional = _load_fpl_data()
    size = max(1, household_size)
    return base + per_additional * (size - 1)


def calculate_fpl(income: float, household_size: int) -> dict:
    """Calculate FPL percentage for given income and household size."""
    threshold = fpl_threshold(household_size)
    percentage = (income / threshold) * 100 if threshold > 0 else 0.0
    return {
        "income": income,
        "household_size": household_size,
        "fpl_threshold": threshold,
        "fpl_percentage": round(percentage, 1),
        "year": 2026,
    }


def check_fpl_threshold(
    income: float, household_size: int, threshold_pct: float
) -> dict:
    """Check if income is below a specific FPL percentage threshold."""
    result = calculate_fpl(income, household_size)
    below = result["fpl_percentage"] <= threshold_pct
    return {
        **result,
        "threshold_pct": threshold_pct,
        "below_threshold": below,
    }
