import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Confirm
from pathlib import Path

from esim_manager.core.doctor import SystemDoctor
from esim_manager.core.environment import EnvironmentManager
from esim_manager.core.updater import UpdateManager
from esim_manager.core.installer import ToolInstaller
from esim_manager.utils.logger import LOG_FILE

app = typer.Typer(help="eSim Automated Tool & Dependency Manager")
console = Console()

@app.command()
def doctor():
    """Diagnose all eSim external dependencies and environment variables."""
    console.print("\n[bold cyan]🔍 Running eSim System Diagnostics...[/bold cyan]\n")
    
    doc = SystemDoctor()
    results = doc.diagnose_all()
    
    table = Table(title="eSim Dependency Health Matrix", show_header=True, header_style="bold magenta")
    table.add_column("Category", style="dim")
    table.add_column("Component", style="bold")
    table.add_column("Status")
    table.add_column("In PATH?")
    table.add_column("Version")
    table.add_column("Path Location")

    all_good = True
    missing_paths = []

    for r in results:
        status_badge = "[green]✓ Installed[/green]" if r["installed"] else "[red]✗ Missing[/red]"
        path_badge = "[green]Yes[/green]" if r["in_path"] else "[yellow]No (Fix needed)[/yellow]"
        
        if not r["installed"]:
            all_good = False
        elif not r["in_path"]:
            all_good = False
            missing_paths.append(str(Path(r["path"]).parent))

        table.add_row(
            r["category"],
            r["name"],
            status_badge,
            path_badge if r["installed"] else "-",
            r["version"],
            r["path"]
        )

    console.print(table)

    if all_good:
        console.print("\n[bold green]🎉 All eSim dependencies are configured and ready![/bold green]\n")
    else:
        console.print("\n[bold yellow]⚠️  Issues detected:[/bold yellow]")
        if missing_paths:
            console.print("   • Some tools are installed but not in your environment PATH.")
            console.print("   • Run: [bold cyan]python -m esim_manager.cli fix-paths[/bold cyan] to auto-configure them.")
        console.print("   • Run: [bold cyan]python -m esim_manager.cli update[/bold cyan] to check for newer releases.\n")

@app.command()
def update():
    """Check for upstream updates of external tools."""
    console.print("\n[bold cyan]🌐 Querying Upstream Repositories for Updates...[/bold cyan]\n")
    doc = SystemDoctor()
    
    for tool_id in ["ngspice", "kicad", "ghdl"]:
        current = doc.check_tool(tool_id)
        upstream = UpdateManager.check_upstream_version(tool_id)
        
        console.print(f"[bold]{current['name']}[/bold]")
        console.print(f"  • Local Version:    [yellow]{current['version']}[/yellow]")
        console.print(f"  • Upstream Version: [green]{upstream['latest']}[/green]")
        console.print("-" * 50)

@app.command()
def fix_paths():
    """Automatically discover installed tools and append their directories to the system PATH."""
    console.print("\n[bold cyan]🔧 Resolving Missing System PATH Configurations...[/bold cyan]\n")
    doc = SystemDoctor()
    results = doc.diagnose_all()
    
    fixed_count = 0
    for r in results:
        if r["installed"] and not r["in_path"]:
            parent_dir = str(Path(r["path"]).parent)
            if Confirm.ask(f"Add [yellow]{parent_dir}[/yellow] to system PATH?"):
                success = EnvironmentManager.add_to_path(parent_dir)
                if success:
                    console.print(f"[green]✓ Successfully configured {r['name']} in PATH![/green]")
                    fixed_count += 1
                else:
                    console.print(f"[red]✗ Failed to write PATH configuration for {r['name']}[/red]")

    if fixed_count == 0:
        console.print("[dim]No paths needed fixing.[/dim]")

@app.command()
def install(tool_id: str):
    """Download and install an external tool automatically."""
    installer = ToolInstaller()
    console.print(f"\n[bold cyan]🚀 Starting Automated Setup for '{tool_id}'...[/bold cyan]\n")
    success = installer.download_and_extract(tool_id)
    if success:
        console.print(f"[bold green]✓ Successfully installed {tool_id}![/bold green]")
        console.print("Run [cyan]python -m esim_manager.cli doctor[/cyan] to verify.")
    else:
        console.print(f"[bold red]✗ Failed to install {tool_id}. Check log file for details.[/bold red]")

@app.command()
def logs():
    """Display the recent log entries."""
    if LOG_FILE.exists():
        console.print(Panel(LOG_FILE.read_text()[-2000:], title="Recent eSim Manager Logs", border_style="blue"))
    else:
        console.print("[dim]No logs recorded yet.[/dim]")

if __name__ == "__main__":
    app()