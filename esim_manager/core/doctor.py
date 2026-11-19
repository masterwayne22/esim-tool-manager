import shutil
import subprocess
import re
from pathlib import Path
from esim_manager.config import TOOLS_CONFIG, IS_WINDOWS
from esim_manager.utils.logger import logger

class SystemDoctor:
    def check_tool(self, tool_id: str) -> dict:
        info = TOOLS_CONFIG.get(tool_id)
        if not info:
            return {"status": "error", "message": f"Unknown tool: {tool_id}"}

        binary = info["binary_name"]
        
        # 1. Check if binary is in active system PATH
        path_in_env = shutil.which(binary)
        detected_path = path_in_env
        is_in_path = path_in_env is not None

        # 2. If not in PATH, probe standard default installation locations
        if not detected_path:
            probe_paths = info["default_paths_windows"] if IS_WINDOWS else info["default_paths_linux"]
            for p in probe_paths:
                candidate = Path(p) / binary
                if candidate.is_file():
                    detected_path = str(candidate)
                    break

        if not detected_path:
            logger.warning(f"Doctor: {info['display_name']} NOT found on system.")
            return {
                "name": info["display_name"],
                "installed": False,
                "in_path": False,
                "path": "Not found",
                "version": "N/A",
                "category": info["category"]
            }

        # 3. Extract version using subprocess
        version = self._get_version(detected_path, info["version_flag"])
        logger.info(f"Doctor: Found {info['display_name']} at {detected_path} (Version: {version})")

        return {
            "name": info["display_name"],
            "installed": True,
            "in_path": is_in_path,
            "path": detected_path,
            "version": version,
            "category": info["category"]
        }

    def _get_version(self, path: str, flag: str) -> str:
        try:
            res = subprocess.run(
                [path, flag],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5
            )
            output = res.stdout or res.stderr
            # Regex to find semver (e.g. 42, 8.0.1, 4.0.0)
            match = re.search(r"(\d+(\.\d+)+|\b\d{2,}\b)", output)
            return match.group(0) if match else "Detected"
        except Exception as e:
            logger.debug(f"Version check error for {path}: {e}")
            return "Detected"

    def diagnose_all(self) -> list:
        return [self.check_tool(t_id) for t_id in TOOLS_CONFIG]