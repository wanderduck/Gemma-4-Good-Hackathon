"""Tests for county programs lookup tool."""

import pytest
from navigator.tools.county_programs import CountyProgramsTool


@pytest.fixture
def tool():
    return CountyProgramsTool()


def test_ramsey_has_dislocated_worker(tool):
    programs = tool.get_programs("Ramsey")
    names = [p["name"] for p in programs]
    assert any("Dislocated Worker" in n for n in names)


def test_ramsey_has_caprw(tool):
    programs = tool.get_programs("Ramsey")
    caps = [p for p in programs if p["type"] == "cap"]
    assert len(caps) > 0
    assert any("CAPRW" in p["name"] for p in caps)


def test_hennepin_has_pathways(tool):
    programs = tool.get_programs("Hennepin")
    names = [p["name"] for p in programs]
    assert any("Pathways" in n for n in names)


def test_dakota_served_by_cap_agency(tool):
    programs = tool.get_programs("Dakota")
    caps = [p for p in programs if p["type"] == "cap"]
    assert any("CAP Agency" in p["name"] for p in caps)


def test_unknown_county_returns_empty(tool):
    programs = tool.get_programs("FakeCounty")
    assert programs == []


def test_get_cap_agency(tool):
    cap = tool.get_cap_agency("Ramsey")
    assert cap is not None
    assert "CAPRW" in cap["name"]
    assert "phone" in cap
