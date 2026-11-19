import os
import platform
from pathlib import Path

IS_WINDOWS = platform.system().lower() == "windows"
IS_LINUX = platform.system().lower() == "linux"

HOME = Path.home()

TOOLS_CONFIG = {
    "python": {
        "display_name": "Python Environment",
        "binary_name": "python.exe" if IS_WINDOWS else "python3",
        "version_flag": "--version",
        "default_paths_windows": [],
        "default_paths_linux": ["/usr/bin"],
        "category": "Core Runtime"
    },
    "ngspice": {
        "display_name": "Ngspice Circuit Simulator",
        "binary_name": "ngspice.exe" if IS_WINDOWS else "ngspice",
        "version_flag": "-v",
        "upstream_api": "https://sourceforge.net/projects/ngspice/best_release.json",
        "default_paths_windows": [
            r"C:\Spice64\bin",
            r"C:\Program Files\Ngspice\bin",
            r"C:\FOSSEE\eSim\Ngspice\bin",
            str(HOME / ".esim" / "tools" / "ngspice" / "Spice64" / "bin")
        ],
        "default_paths_linux": [
            "/usr/bin",
            "/usr/local/bin"
        ],
        # Direct mirrors using plain HTTP to avoid expired SSL certificates
        "direct_mirrors_win": [
            "http://freefr.dl.sourceforge.net/project/ngspice/ng-spice-rework/old-releases/34/ngspice-34_64.zip",
            "http://master.dl.sourceforge.net/project/ngspice/ng-spice-rework/old-releases/34/ngspice-34_64.zip",
            "http://phoenixnap.dl.sourceforge.net/project/ngspice/ng-spice-rework/old-releases/34/ngspice-34_64.zip",
            "https://freefr.dl.sourceforge.net/project/ngspice/ng-spice-rework/old-releases/34/ngspice-34_64.zip"
        ],
        "category": "Simulation Engine"
    },
    "kicad": {
        "display_name": "KiCad EDA Suite",
        "binary_name": "kicad.exe" if IS_WINDOWS else "kicad",
        "version_flag": "--version",
        "upstream_api": "https://api.github.com/repos/KiCad/kicad-source-mirror/releases/latest",
        "default_paths_windows": [
            r"C:\Program Files\KiCad\8.0\bin",
            r"C:\Program Files\KiCad\7.0\bin",
            r"C:\Program Files\KiCad\bin"
        ],
        "default_paths_linux": [
            "/usr/bin",
            "/usr/local/bin"
        ],
        "category": "Schematic & PCB"
    },
    "ghdl": {
        "display_name": "GHDL (VHDL Simulator)",
        "binary_name": "ghdl.exe" if IS_WINDOWS else "ghdl",
        "version_flag": "--version",
        "upstream_api": "https://api.github.com/repos/ghdl/ghdl/releases/latest",
        "default_paths_windows": [
            r"C:\GHDL\bin",
            r"C:\FOSSEE\eSim\GHDL\bin",
            str(HOME / ".esim" / "tools" / "ghdl" / "bin")
        ],
        "default_paths_linux": [
            "/usr/bin",
            "/usr/local/bin"
        ],
        "category": "Digital Engine"
    }
}