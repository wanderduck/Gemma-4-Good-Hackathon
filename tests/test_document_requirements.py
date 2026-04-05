"""Tests for document requirements tool."""

import pytest
from navigator.tools.document_requirements import DocumentRequirementsTool
from navigator.models import UserProfile


@pytest.fixture
def tool():
    return DocumentRequirementsTool()


@pytest.fixture
def profile():
    return UserProfile(
        income=32000,
        household_size=3,
        county="Ramsey",
        employment_status="recently_unemployed",
    )


def test_snap_documents(tool, profile):
    docs = tool.get_documents("snap", profile)
    assert "Photo ID" in docs or "Government-issued photo ID" in docs
    assert any("income" in d.lower() for d in docs)


def test_ui_documents(tool, profile):
    docs = tool.get_documents("unemployment_insurance", profile)
    assert any("employer" in d.lower() or "layoff" in d.lower() for d in docs)


def test_consolidated_documents(tool, profile):
    programs = ["snap", "mfip", "medical_assistance"]
    docs = tool.get_consolidated_documents(programs, profile)
    # Should be deduplicated
    assert len(docs) == len(set(docs))
    assert "Government-issued photo ID" in docs
