# eSim Tool Manager (`esim-manager`)

An automated CLI and diagnostic utility developed for **eSim (FOSSEE, IIT Bombay)** to handle the installation, environment configuration, dependency verification, and upstream version tracking of external EDA tools (**Ngspice**, **KiCad**, and **GHDL**).

**Author:** Krishiv Sarva  
**Institution:** VIT Bhopal University  
**Branch:** Computer Science & Engineering (2024–2028)  
**Task:** Screening Task 5 — Tool Manager (eSim Semester Long Internship Autumn/Winter 2026)  
**Repository:** Private (Access granted to `Eyantra698Sumanto`)  

---

## Motivation

eSim acts as an integration platform across multiple independent open-source EDA engines. In practice, students and researchers frequently encounter environment issues:
- External tools (such as Ngspice in `C:\Spice64` or KiCad in `Program Files`) are installed on disk, but missing from the system `PATH`.
- Lab systems in colleges often restrict administrative privileges, preventing global registry modifications.
- Upstream archives and binary names change across releases, breaking static install scripts.

This utility addresses these issues by providing a health diagnostic check (`doctor`), user-level environment variable configuration (`fix-paths`), upstream update tracking (`update`), and automated installation (`install`).

---

## Features Implemented

The screening guidelines require meeting at least two of the five task criteria. This project implements all five:

| Task 5 Requirement | Implementation Details | Key File |
| :--- | :--- | :--- |
| **1. Tool Installation** | Automated download, verification, and extraction of external tools (Ngspice, GHDL, KiCad). Supports native transfer agents (`curl`), GitHub release assets, and Windows Package Manager (`winget`). | `esim_manager/core/installer.py` |
| **2. Update System** | Real-time version queries against GitHub REST APIs and SourceForge feeds to compare local versus remote releases. | `esim_manager/core/updater.py` |
| **3. Configuration Handling** | Non-admin PATH persistence using `HKEY_CURRENT_USER\Environment` on Windows (via `winreg`) and `~/.bashrc` on Linux. | `esim_manager/core/environment.py` |
| **4. Dependency Checker** | Comprehensive system diagnostics scanning runtime compilers, simulation engines, binary availability, and version flags. | `esim_manager/core/doctor.py` |
| **5. User Interface & Logs** | Formatted terminal output using `rich` tables and persistent logging to `~/.esim/manager.log`. | `esim_manager/cli.py`<br>`esim_manager/utils/logger.py` |

---

## Project Structure

```
esim-tool-manager/
├── esim_manager/
│   ├── __init__.py
│   ├── cli.py                     # Typer CLI application & terminal UI
│   ├── config.py                  # Tool definitions, probing paths & URLs
│   ├── core/
│   │   ├── __init__.py
│   │   ├── doctor.py              # System dependency diagnostics
│   │   ├── environment.py         # PATH and Windows Registry manager
│   │   ├── installer.py           # Multi-strategy tool installer
│   │   └── updater.py             # GitHub & SourceForge upstream APIs
│   └── utils/
│       └── logger.py              # File-based logging (~/.esim/manager.log)
├── tests/
│   ├── conftest.py                # Pytest path configuration
│   └── test_doctor.py             # Unit tests
├── docs/
│   ├── architecture_design.md     # Architecture & technical design specification
│   └── architecture_design.pdf    # PDF submission document
├── pyproject.toml                 # Package configuration
├── requirements.txt               # Dependencies
└── README.md
```

---

## Setup and Installation

### Prerequisites
- Python 3.10 or newer (tested on Python 3.14 on Windows 11)
- Git

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/masterwayne22/esim-tool-manager.git
   cd esim-tool-manager
   ```

2. Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install project dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

---

## Usage

### 1. Run Dependency Diagnostics (`doctor`)
Scans the local environment, checks whether tools reside in `PATH`, and extracts installed versions:
```powershell
python -m esim_manager.cli doctor
```

Example output:
```text
eSim Dependency Health Matrix
+-------------------+---------------------------+-------------+-----------------+----------+-------------------------+
| Category          | Component                 | Status      | In PATH?        | Version  | Path Location           |
+-------------------+---------------------------+-------------+-----------------+----------+-------------------------+
| Core Runtime      | Python Environment        | Installed   | Yes             | 3.14.2   | C:\Users\...\python.exe |
| Simulation Engine | Ngspice Circuit Simulator | Installed   | Yes             | 34       | C:\Users\...\Spice64    |
| Schematic & PCB   | KiCad EDA Suite           | Missing     | -               | N/A      | Not found               |
| Digital Engine    | GHDL (VHDL Simulator)     | Missing     | -               | N/A      | Not found               |
+-------------------+---------------------------+-------------+-----------------+----------+-------------------------+
```

### 2. Auto-Configure Environment Variables (`fix-paths`)
Detects installed tools that are missing from `PATH` and appends their directories to the Windows User Registry (`HKEY_CURRENT_USER\Environment\Path`) or `~/.bashrc`:
```powershell
python -m esim_manager.cli fix-paths
```
*Note: Uses user-space registry entries so administrative privileges are not required.*

### 3. Check for Upstream Updates (`update`)
Queries upstream release APIs to check if newer stable releases exist:
```powershell
python -m esim_manager.cli update
```

### 4. Install Dependencies (`install`)
Downloads and configures external tools directly:
```powershell
python -m esim_manager.cli install ngspice
```

### 5. Inspect Event Logs (`logs`)
Displays recent actions and diagnostic logs stored in `~/.esim/manager.log`:
```powershell
python -m esim_manager.cli logs
```

---

## Running Unit Tests

Unit tests are written using `pytest` to verify the diagnostic dictionary structure and tool configuration schemas:

```powershell
python -m pytest -v
```

Output:
```text
tests/test_doctor.py::test_system_doctor_structure PASSED            [ 50%]
tests/test_doctor.py::test_all_tools_configured PASSED               [100%]

============================== 2 passed ==============================
```

---

## Demonstration Video

- **Video Link:** [YouTube Unlisted Walkthrough](https://youtu.be/mSZM3llyFd0)
*(A 5-minute screencast demonstrating CLI commands, path auto-configuration, and code architecture).*

---

## Design Document

A complete technical architecture document covering module interactions, design patterns (Strategy, Facade), and engineering trade-offs is available at [`docs/architecture_design.pdf`](https://docs.google.com/document/d/1bib4P2WFHv_zpcEKF9pYolk9kKvD09FHvEhvpsP9tyA/edit?usp=sharing).
