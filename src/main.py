from pyfiglet import figlet_format
from rich.console import Console

def get_new_ascii_banner() :
    """Generate dynamic ASCII banner with pyfiglet."""


    cwd = "/victor/xxx"
    version = "0.1.0"
    console = Console()

    banner = figlet_format("Code    Guard")
    info = f"[bold cyan]Working directory:[/bold cyan] {cwd}\n"
    info += f"[bold cyan]Version:[/bold cyan] v{version}\n"
    info += f"[bold cyan]Model:[/bold cyan] {"model"}\n"
    info += f"[bold cyan]Base URL:[/bold cyan] {"baseUrl"}"

    return banner + "\n" + info
    # console.print(banner, style="bold cyan")
    # console.print(info)


if __name__ == '__main__' :
    print("Hello World")
    info = get_new_ascii_banner()
    console = Console()
    console.print(info, style="bold cyan")

    # console.print(info)
