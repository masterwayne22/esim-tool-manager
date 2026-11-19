import pytest
from esim_manager.core.doctor import SystemDoctor
from esim_manager.config import TOOLS_CONFIG

def test_system_doctor_structure():
    doc = SystemDoctor()
    res = doc.check_tool("ngspice")
    assert "installed" in res
    assert "in_path" in res
    assert "version" in res
    assert "category" in res

def test_all_tools_configured():
    assert "ngspice" in TOOLS_CONFIG
    assert "kicad" in TOOLS_CONFIG
    assert "ghdl" in TOOLS_CONFIG