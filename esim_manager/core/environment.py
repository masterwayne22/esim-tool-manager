import os
import sys
from pathlib import Path
from esim_manager.config import IS_WINDOWS
from esim_manager.utils.logger import logger

class EnvironmentManager:
    @staticmethod
    def add_to_path(dir_path: str) -> bool:
        norm_path = str(Path(dir_path).resolve())
        if not Path(norm_path).is_dir():
            logger.error(f"Cannot add non-existent directory to PATH: {norm_path}")
            return False

        if IS_WINDOWS:
            return EnvironmentManager._add_windows_path(norm_path)
        else:
            return EnvironmentManager._add_linux_path(norm_path)

    @staticmethod
    def _add_windows_path(new_dir: str) -> bool:
        try:
            import winreg
            # Access User Environment Registry
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Environment",
                0,
                winreg.KEY_READ | winreg.KEY_WRITE
            )
            try:
                current_path, _ = winreg.QueryValueEx(key, "Path")
            except FileNotFoundError:
                current_path = ""

            # Check if directory already present
            paths = current_path.split(";") if current_path else []
            if new_dir in paths:
                logger.info(f"{new_dir} already in Windows PATH.")
                winreg.CloseKey(key)
                return True

            updated_path = current_path + (";" if current_path and not current_path.endswith(";") else "") + new_dir
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, updated_path)
            winreg.CloseKey(key)

            # Update current running process PATH as well
            os.environ["PATH"] += f";{new_dir}"
            logger.info(f"Successfully added {new_dir} to User PATH Registry.")
            return True
        except Exception as e:
            logger.error(f"Failed to update Windows Registry PATH: {e}")
            return False

    @staticmethod
    def _add_linux_path(new_dir: str) -> bool:
        try:
            bashrc = Path.home() / ".bashrc"
            export_line = f'export PATH="$PATH:{new_dir}"\n'
            
            if bashrc.exists():
                content = bashrc.read_text()
                if new_dir in content:
                    logger.info(f"{new_dir} already in ~/.bashrc")
                    return True
            
            with open(bashrc, "a") as f:
                f.write(export_line)
                
            os.environ["PATH"] += f":{new_dir}"
            logger.info(f"Appended {new_dir} to ~/.bashrc")
            return True
        except Exception as e:
            logger.error(f"Failed to update ~/.bashrc: {e}")
            return False