# System Architecture & Design Document
## Automated Tool and Dependency Manager for eSim EDA Suite
**Candidate:** Screening Task 5 Submission  
**Program:** eSim Semester-Long Internship (Autumn/Winter 2026), FOSSEE, IIT Bombay  

---

## 1. Executive Summary & Problem Statement

### 1.1 Context
eSim is an open-source EDA tool developed by FOSSEE, IIT Bombay, for circuit design, simulation, and PCB fabrication. Unlike monolithic EDA platforms, eSim functions as an orchestrator that integrates multiple best-in-class open-source tools:
- **KiCad** for schematic capture and PCB layout
- **Ngspice** for mixed-signal analog simulation
- **GHDL** for VHDL digital simulation
- **Makerchip / Verilator** for Verilog simulation
- **Python / Matplotlib** for waveform plotting and scripting

### 1.2 The Core Problem
Because eSim relies on an ecosystem of disparate external tools, user onboarding and maintenance are notoriously prone to environment friction:
1. **Broken `PATH` Variables**: Users frequently install tools (e.g., Ngspice in `C:\Spice64` or KiCad in `Program Files`), but eSim cannot invoke them because the binary directory was not appended to the system environment variables.
2. **Version Incompatibilities**: Silent API shifts between tool releases (e.g., KiCad 7 vs 8 vs 9, or Ngspice rework releases) lead to unexpected simulation crashes.
3. **Platform Drift**: Dependency resolution differs significantly between Windows environments (which rely on registry keys and manual ZIP extractions) and Linux distributions (which rely on package managers like `apt` and shell profiles).

### 1.3 Solution
The **`esim-manager`** provides a unified diagnostic and management suite modeled after developer-grade tools (such as `flutter doctor` and `rustup`). It introduces automated health scanning, safe environment path persistence, automated multi-strategy installation, upstream release tracking, and comprehensive event logging.

---

## 2. High-Level System Architecture

The tool is organized into a modular, layered architecture to ensure separation of concerns and cross-platform extensibility:

```
+-------------------------------------------------------------------+
|                        Presentation Layer                         |
|      Typer CLI Interface  |  Rich Terminal UI (Tables, Spinners)   |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|                        Orchestration Layer                        |
|  [doctor.py]      [installer.py]     [environment.py]  [updater.py]
|  Diagnostics       Multi-Strategy     Registry / PATH   Upstream API
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|                     Platform Abstraction Layer                    |
|       Windows (winreg / curl.exe / winget)   |   Linux (apt / sh) |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|                         External Ecosystem                        |
|    Ngspice Engine   |   KiCad Suite   |   GHDL   |   Python Core  |
+-------------------------------------------------------------------+
```

---

## 3. Module Breakdown & Design Patterns

### 3.1 Dependency Checker (`core/doctor.py`)
- **Design Pattern**: Inspector / Facade
- **Functionality**:
  1. Inspects the active `os.environ["PATH"]` using `shutil.which`.
  2. If the binary is not found in `PATH`, it iteratively probes default operating-system installation directories (e.g., `C:\Spice64\bin`, `C:\Program Files\KiCad`, and `~/.esim/tools/`).
  3. Uses asynchronous/safe subprocess execution to invoke tool version flags (`-v`, `--version`) and extracts semantic version patterns via regular expressions.
  4. Returns a normalized dictionary containing installation status, PATH discovery, version, and category.

### 3.2 Environment Manager (`core/environment.py`)
- **Functionality**:
  - Resolves orphaned tool directories and writes them permanently into user environment configurations.
  - **On Windows**: Leverages Python's native `winreg` module to read and write to `HKEY_CURRENT_USER\Environment\Path`. It ensures directory deduplication and dynamically updates the current runtime process environment (`os.environ["PATH"]`) without requiring a system reboot.
  - **On Linux**: Safely inspects and appends `export PATH="$PATH:<directory>"` to `~/.bashrc`.

### 3.3 Multi-Strategy Tool Installer (`core/installer.py`)
- **Design Pattern**: Strategy Pattern
- **Functionality**:
  Because download architectures differ across open-source vendors, the installer implements multiple strategies:
  - **Strategy A (Native Transfer Agent)**: Employs `curl.exe -L` with follow-redirects and user-agent impersonation to bypass mirror redirection issues.
  - **Strategy B (Package Manager Integration)**: Integrates directly with the Windows Package Manager (`winget install --id KiCad.KiCad`) for major software suites.
  - **Strategy C (GitHub Releases API)**: Direct asset streaming for developer utilities.
  - **Payload Verification**: Validates file size thresholds and verifies archive signatures using Python's `zipfile` module before attempting disk extraction.

### 3.4 Upstream Release Tracker (`core/updater.py`)
- **Functionality**:
  - Interrogates upstream REST APIs (GitHub Releases API and SourceForge Release Feeds).
  - Normalizes semantic versions and displays real-time comparison tables so users know whether security or feature upgrades are available.

### 3.5 Centralized Logger (`utils/logger.py`)
- **Functionality**:
  - All operations, diagnostic warnings, subprocess return codes, and exceptions are appended with timestamps to `~/.esim/manager.log`.
  - Accessible directly in the console via `python -m esim_manager.cli logs`.

---

## 4. Requirement Verification Matrix

| Official Screening Requirement | Implemented Feature | Implementation File | Status |
| :--- | :--- | :--- | :--- |
| **1. Tool Installation Management** | Multi-strategy automated download & extraction with integrity verification | `esim_manager/core/installer.py` | **Complete** |
| **2. Update and Upgrade System** | Real-time upstream semver comparison via GitHub / SourceForge APIs | `esim_manager/core/updater.py` | **Complete** |
| **3. Configuration Handling** | Windows Registry (`winreg`) & Linux shell persistence for PATH variables | `esim_manager/core/environment.py` | **Complete** |
| **4. Dependency Checker** | Comprehensive `doctor` matrix diagnosing runtimes, engines, and EDA tools | `esim_manager/core/doctor.py` | **Complete** |
| **5. User Interface & Logs** | Modern terminal UI with `rich` tables and persistent logging in `~/.esim/` | `esim_manager/cli.py` & `logger.py` | **Complete** |
| **Bonus: Cross-Platform Support** | Operating-system abstraction supporting both Windows and Linux paths | `esim_manager/config.py` | **Complete** |
| **Bonus: Test Automation** | Automated test suite verifying diagnostic matrix and configuration dictionaries | `tests/test_doctor.py` | **Complete** |

---

## 5. Testing & Verification

Automated testing was conducted using `pytest`. The test suite validates:
1. Schema integrity of the diagnostic engine dictionary (`installed`, `in_path`, `version`, `category`).
2. Completeness of the tools configuration database (`ngspice`, `kicad`, `ghdl`, `python`).

```powershell
(venv) PS C:\Users\Lenovo\esim-tool-manager> python -m pytest -v
============================= test session starts =============================
platform win32 -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Users\Lenovo\esim-tool-manager
configfile: pyproject.toml
collected 2 items

tests/test_doctor.py::test_system_doctor_structure PASSED                [ 50%]
tests/test_doctor.py::test_all_tools_configured PASSED                   [100%]

============================== 2 passed in 4.38s ==============================
```

---

## 6. Conclusion & Integration Roadmap for eSim

The **`esim-manager`** prototype successfully fulfills all screening criteria for Task 5. Its modular structure allows seamless integration into the upcoming eSim 2.6/3.0 core distributions:
- Can be packaged directly with PyInstaller as a standalone single-binary utility (`esim-manager.exe`).
- Can serve as a pre-flight check executed whenever a user opens the eSim GUI.
