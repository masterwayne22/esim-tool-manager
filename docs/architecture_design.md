# System Architecture & Technical Design Document
# Automated Tool and Dependency Manager for eSim EDA Suite (`esim-manager`)

**Candidate:** Krishiv Sarva  
**Branch & Year:** Computer Science & Engineering, [2024-2028]  
**Institution:** VIT BHOPAL UNIVERSITY  
**Program:** eSim Semester-Long Internship (Autumn/Winter 2026), FOSSEE, IIT Bombay  
**Target Screening Task:** Task 5: Tool Manager (CSE and related fields)  
**Repository Link:** https://github.com/masterwayne22/esim-tool-manager (Private)  

---

## 1. Executive Summary & Problem Context

### 1.1 Background
**eSim** is an open-source Electronic Design Automation (EDA) suite developed by the FOSSEE project at IIT Bombay. It enables schematic capture, analog/digital/mixed-signal circuit simulation, and PCB layout creation. 

Unlike monolithic commercial EDA packages, eSim functions as an integration platform coordinating multiple specialized open-source tools:
- **KiCad (eSchema & Pcbnew):** Schematic capture, netlist generation, and PCB layout.
- **Ngspice:** Mixed-signal and analog SPICE engine.
- **GHDL:** IEEE-compliant VHDL simulation engine.
- **Verilator / Makerchip:** Verilog digital synthesis and simulation interfaces.
- **Python / Matplotlib:** Scripting interface, waveform plotting, and data post-processing.

### 1.2 The Problem
Because eSim operates as an orchestration layer over heterogeneous sub-tools, installation and maintenance present significant points of failure for students and researchers:
1. **The PATH Resolution Problem:** Users frequently have tool binaries present on disk (e.g., `C:\Spice64\bin\ngspice.exe` or `C:\Program Files\KiCad\bin`), yet eSim fails with *"Command not found"* because directory paths were not registered in system environment variables.
2. **Academic Lab Administrative Restrictions:** Many student machines and college lab workstations restrict administrative access (`HKEY_LOCAL_MACHINE`). Standard installers fail when attempting global machine modifications.
3. **Silent Upstream API & Format Drift:** Tools frequently update version flags, binary names, and archive packaging formats (e.g., Ngspice transitioning from `.zip` to `.7z`), breaking static installation scripts.
4. **Cross-Platform Divergence:** Dependency resolution, binary paths, and environment variable registries differ fundamentally between Windows (`winreg`) and Linux (`~/.bashrc`).

### 1.3 Proposed Solution
The **`esim-manager`** is an automated system diagnostics and lifecycle management suite. Designed with inspiration from developer utilities such as `flutter doctor` and `rustup`, it provides:
- Automated system health inspection and dependency discovery.
- Safe, non-destructive, non-admin user-level environment PATH persistence.
- Multi-strategy binary acquisition and extraction.
- Upstream release tracking via public REST APIs.
- Comprehensive local logging for auditability and error diagnostics.

---

## 2. System Architecture & Component Interaction

The architecture follows a strict **Layered Architectural Pattern** to decouple the user presentation interface from core diagnostic logic and operating-system-level APIs:

```
+-------------------------------------------------------------+
|                      PRESENTATION LAYER                     |
|    Typer CLI Interface  |  Rich Terminal Formatting         |
|         (doctor, fix-paths, update, install, logs)          |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                     ORCHESTRATION LAYER                     |
|  [SystemDoctor]       [EnvironmentManager]  [ToolInstaller] |
|   Diagnostics          Registry / PATH       Multi-Strategy |
|  [UpdateManager]      [CentralLogger]                       |
|   Upstream REST APIs   Audit Trail                          |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                 PLATFORM ABSTRACTION LAYER                  |
|     Windows (winreg, curl.exe)   |   Linux (sh, .bashrc)    |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                      MANAGED EDA TOOLS                      |
|   Ngspice Engine  |  KiCad EDA Suite  |  GHDL  |  Python    |
+-------------------------------------------------------------+
```

---

## 3. Data Flow & Algorithmic Workflows

### 3.1 Diagnostic Flow (`esim doctor`)

```
[Start: User runs 'esim doctor']
               │
               ▼
   [1. Probe System PATH via shutil.which]
               │
       ┌───────┴───────┐
       ▼               ▼
   [Found]          [Not Found]
       │               │
       │               ▼
       │     [2. Probe Default Folders]
       │     (C:\Spice64, Program Files)
       │               │
       │         ┌─────┴─────┐
       │         ▼           ▼
       │      [Found]    [Not Found]
       │         │           │
       ▼         ▼           ▼
   [3. Invoke Version]  [Status: MISSING]
   [4. Regex Parse]          │
       │                     │
       └─────────┬───────────┘
                 │
                 ▼
[Render Rich Health Matrix Table]
```

### 3.2 Non-Destructive Environment Resolution Flow (`esim fix-paths`)

```
[Identify Installed Tool missing from PATH]
                    │
                    ▼
   [Prompt User Confirmation: y/n]
                    │ (if Yes)
         ┌──────────┴──────────┐
         ▼                     ▼
     [Windows]              [Linux]
         │                     │
         ▼                     ▼
[Open HKCU\Environment]  [Inspect ~/.bashrc]
[Deduplicate Entries]    [Check duplication]
[Append with ';']        [Append export PATH]
[Write REG_EXPAND_SZ]    [Save to disk]
         │                     │
         └──────────┬──────────┘
                    │
                    ▼
[Update os.environ & Commit to manager.log]
```

---

## 4. Software Engineering Principles & Design Patterns

### 4.1 SOLID Principles Adherence
- **Single Responsibility Principle (SRP):** Each module handles exactly one operational domain. `SystemDoctor` only inspects; `EnvironmentManager` only manages environment variables; `ToolInstaller` only acquires payloads.
- **Open/Closed Principle (OCP):** Supported tools are defined in a centralized data dictionary (`TOOLS_CONFIG` in `config.py`). Adding a new tool (e.g., Verilator or GTKWave) requires zero changes to core diagnostic or installation logic.
- **Dependency Inversion / Strategy Pattern:** The `ToolInstaller` implements distinct acquisition strategies based on vendor platform constraints without coupling the caller to the underlying protocol.

### 4.2 Key Engineering Design Choices
1. **User-Space Registry Manipulation (`HKEY_CURRENT_USER`):**
   Standard Windows installers write to `HKEY_LOCAL_MACHINE`, requiring Administrator privileges. By targeting `HKEY_CURRENT_USER\Environment`, `esim-manager` allows students on restricted lab PCs to install and configure tools without requiring elevation.
2. **Subprocess Isolation & Safe Execution:**
   When extracting tool versions (`ngspice -v`, `kicad --version`), subprocess calls are bounded by hard timeouts (`timeout=5`) and run with detached standard output buffers. This prevents zombie processes or terminal freezing if an external binary stalls.
3. **Resilient Payload Verification:**
   Downloaded archives undergo byte-size threshold checks and zip header verification (`zipfile.is_zipfile`) before extraction, preventing partial or corrupted payloads from polluting local tool directories.

---

## 5. Requirement Verification & Mapping Matrix

The official screening guidelines mandate fulfilling **at least 2** of the screening requirements. The prototype meets **all 5 requirements** plus optional criteria:

| Official Task 5 Requirement | Implementation in `esim-manager` | File Reference | Status |
| :--- | :--- | :--- | :---: |
| **1. Tool Installation Management** | Multi-strategy automated download, archive verification, and directory extraction for external EDA tools. | `esim_manager/core/installer.py` | **Complete** |
| **2. Update and Upgrade System** | Dynamic query engine polling GitHub REST APIs and SourceForge release feeds to identify newer upstream versions. | `esim_manager/core/updater.py` | **Complete** |
| **3. Configuration Handling** | Automated path discovery and persistent environment variable configuration via `winreg` and shell profiles. | `esim_manager/core/environment.py` | **Complete** |
| **4. Dependency Checker** | Comprehensive system health engine diagnosing compilers, runtimes, simulators, and environment paths. | `esim_manager/core/doctor.py` | **Complete** |
| **5. User Interface & Action Logs** | Rich Terminal UI (tables, colored status badges, prompt confirmations) + persistent file logging (`manager.log`). | `esim_manager/cli.py`<br>`esim_manager/utils/logger.py` | **Complete** |
| **Optional: Cross-Platform Support** | Operating-system abstraction supporting Windows and Linux directory structures and shells. | `esim_manager/config.py` | **Complete** |
| **Code Quality: Automated Tests** | Unit test suite verifying diagnostic matrix output and dictionary configurations with `pytest`. | `tests/test_doctor.py` | **Complete** |

---

## 6. Verification and Test Results

The suite was verified using automated unit testing via `pytest`:

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

### Manual Acceptance Testing
1. **Fresh PC Scan:** Diagnosed clean system state correctly identifying missing external dependencies.
2. **Extraction & Installation:** Acquired and placed `ngspice-34` executable suite inside user tool tree (`~/.esim/tools/ngspice/Spice64/bin`).
3. **Environment Persistence:** Successfully registered tool binary in `HKEY_CURRENT_USER\Environment\Path`; confirmed persistence across new terminal sessions.
4. **Upstream Release Query:** Queried live GitHub and SourceForge APIs, successfully returning remote release versions.

---

## 7. Future Roadmap & eSim Core Integration

The modular design of `esim-manager` allows straightforward integration into future eSim distributions:
1. **PyInstaller Compilation:** Package `esim-manager` into a standalone, zero-dependency executable (`esim-manager.exe`) bundled with the eSim installer.
2. **eSim GUI Pre-Flight Check:** Integrate `SystemDoctor` into eSim's PyQt startup sequence to display a visual configuration dialog if any prerequisite tool becomes unlinked or corrupted.
3. **Automated Library Updater:** Expand the updater module to synchronize KiCad symbol libraries (`.kicad_sym`) and Ngspice device models directly from FOSSEE repository mirrors.

---
*Report prepared for the FOSSEE EDA Team, Indian Institute of Technology Bombay (IIT Bombay).*
