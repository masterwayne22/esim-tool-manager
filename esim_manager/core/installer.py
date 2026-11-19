import os
import shutil
import subprocess
import zipfile
from pathlib import Path
from esim_manager.config import TOOLS_CONFIG, IS_WINDOWS
from esim_manager.utils.logger import logger
from rich.console import Console

console = Console()

class ToolInstaller:
    INSTALL_DIR = Path.home() / ".esim" / "tools"

    def __init__(self):
        self.INSTALL_DIR.mkdir(parents=True, exist_ok=True)

    def download_and_extract(self, tool_id: str) -> bool:
        info = TOOLS_CONFIG.get(tool_id)
        if not info:
            console.print(f"[red]Error: Tool '{tool_id}' not found in configuration.[/red]")
            return False

        if not IS_WINDOWS or "direct_mirrors_win" not in info:
            console.print(f"[red]Error: Automated installation not supported for '{tool_id}' on this platform.[/red]")
            return False

        mirrors = info["direct_mirrors_win"]
        dest_folder = self.INSTALL_DIR / tool_id
        dest_folder.mkdir(parents=True, exist_ok=True)
        archive_path = dest_folder / f"{tool_id}.zip"

        curl_bin = shutil.which("curl.exe") or shutil.which("curl")
        if not curl_bin:
            console.print("[red]Error: System transfer agent 'curl.exe' not found.[/red]")
            return False

        downloaded = False

        for idx, mirror_url in enumerate(mirrors, start=1):
            console.print(f"\n[cyan]Attempting direct download via Mirror {idx}/{len(mirrors)}...[/cyan]")
            console.print(f"[dim]{mirror_url}[/dim]")

            if archive_path.exists():
                try:
                    archive_path.unlink()
                except Exception:
                    pass

            cmd = [
                curl_bin,
                "-k",           # INSECURE: Ignores expired SSL certificates like SEC_E_CERT_EXPIRED
                "-L",           # Follow redirects
                "-#",           # Progress bar
                "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "-o", str(archive_path),
                mirror_url
            ]

            res = subprocess.run(cmd)

            if res.returncode == 0 and archive_path.is_file():
                size_mb = archive_path.stat().st_size / (1024 * 1024)
                if size_mb > 2.0 and zipfile.is_zipfile(archive_path):
                    console.print(f"[green]✓ Successfully downloaded valid archive! ({size_mb:.2f} MB)[/green]")
                    downloaded = True
                    break
                else:
                    console.print(f"[yellow]Mirror {idx} returned invalid payload ({size_mb:.2f} MB). Trying next mirror...[/yellow]")

        if not downloaded:
            console.print("[red]✗ All mirrors were blocked. Please check your network connection.[/red]")
            return False

        # Extract archive
        console.print(f"[cyan]Extracting {tool_id} into {dest_folder}...[/cyan]")
        try:
            with zipfile.ZipFile(archive_path, "r") as zip_ref:
                zip_ref.extractall(dest_folder)

            # Clean up archive
            archive_path.unlink()
            console.print(f"\n[bold green]🎉 Successfully installed {info['display_name']}![/bold green]")
            logger.info(f"Successfully installed {tool_id} at {dest_folder}")
            return True

        except Exception as e:
            console.print(f"[red]Extraction failed: {e}[/red]")
            logger.error(f"Extraction error for {tool_id}: {e}", exc_info=True)
            return False