# eSim Automated Tool & Dependency Manager (`esim-manager`)

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-GPLv3-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)]()

An automated management suite designed for **eSim (FOSSEE, IIT Bombay)** that automates the installation, environment configuration, dependency verification, and upstream release checking of external EDA tools (**Ngspice**, **KiCad**, **GHDL**, and **Python Runtimes**).

---

## 🎯 Features Implemented

1. **System Health & Dependency Checker (`doctor`)**:
   - Diagnoses local installations, identifies whether binaries reside in the system `PATH`, and dynamically extracts version metadata via CLI flags.
2. **Automated Tool Installation (`install`)**:
   - Multi-strategy installation engine supporting direct verified mirrors, native system transfer agents (`curl`), GitHub release assets, and Windows Package Manager (`winget`).
3. **Upstream Release Tracker (`update`)**:
   - Queries GitHub REST APIs and SourceForge release feeds to identify when newer upstream versions are available.
4. **Automated Environment & PATH Resolution (`fix-paths`)**:
   - Detects orphaned tool binaries and permanently configures user environment variables via the Windows Registry (`winreg`) and Linux profile configurations (`~/.bashrc`).
5. **Persistent Event Logging (`logs`)**:
   - Captures all system events, errors, and diagnostic traces in `~/.esim/manager.log`.
6. **Automated Test Suite**:
   - Includes full unit test coverage using `pytest`.

---

## 🏗️ Architecture Overview

```
esim-tool-manager/
├── esim_manager/
│   ├── __init__.py
│   ├── cli.py                     # Typer CLI Entrypoint & Rich Terminal UI
│   ├── config.py                  # Supported tools database & probing paths
│   ├── core/
│   │   ├── __init__.py
│   │   ├── doctor.py              # Diagnostic matrix engine
│   │   ├── environment.py         # Persistent PATH & Registry manager
│   │   ├── installer.py           # Multi-strategy installer & extractor
│   │   └── updater.py             # GitHub & SourceForge upstream APIs
│   └── utils/
│       └── logger.py              # Centralized logging subsystem
├── tests/
│   ├── conftest.py                # Test environment path resolver
│   └── test_doctor.py             # System doctor unit tests
├── docs/
│   └── architecture_design.md     # Full System Architecture Document
├── pyproject.toml                 # Packaging configuration
├── requirements.txt
└── README.md
```

---

## 🚀 Quickstart & Installation

### 1. Clone the Repository
```powershell
git clone <your-repo-link>
cd esim-tool-manager
```

### 2. Set Up Virtual Environment & Dependencies
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

*(Or install directly: `pip install rich requests typer pytest`)*

---

## 💻 CLI Usage Guide

### 1. Run System Diagnostics
Scans your system and displays an interactive health matrix:
```powershell
python -m esim_manager.cli doctor
```

### 2. Auto-Fix Missing Environment PATHs
Automatically configures installed tool paths in the Windows Registry:
```powershell
python -m esim_manager.cli fix-paths
```

### 3. Check for Upstream Updates
Compares locally installed tool versions with upstream repositories:
```powershell
python -m esim_manager.cli update
```

### 4. Install an External Tool
Installs verified dependencies with progress tracking:
```powershell
python -m esim_manager.cli install ngspice
```

### 5. View Diagnostic Logs
Displays recent actions and error logs:
```powershell
python -m esim_manager.cli logs
```

### 6. Run Automated Test Suite
```powershell
python -m pytest -v
```

---

## 🎥 Demonstration Video
- **Link:** [YouTube Unlisted Demo Video](https://youtu.be/your-video-link-here)
*(A 5-minute walkthrough demonstrating system diagnostics, path fixing, and architecture overview).*

---

## 📄 License & Attribution
Developed for the **FOSSEE eSim Semester Long Internship Screening Task (Autumn/Winter 2026)**, IIT Bombay.
