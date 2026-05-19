from config.config import console


def check_cli_dependencies():
    """检查CLI的可选依赖是否安装"""
    missing = []

    try:
        import rich
    except ImportError:
        missing.append("rich")

    try:
        import requests
    except ImportError:
        missing.append("requests")

    try:
        import dotenv
    except ImportError:
        missing.append("python-dotenv")

    try:
        import tavily
    except ImportError:
        missing.append("tavily-python")

    try:
        import prompt_toolkit
    except ImportError:
        missing.append("prompt-toolkit")

    if missing:
        print("\nn❌ The following packages are required to use the deepagents CLI:")
        for pkg in missing:
            print(f"  - {pkg}")
        print("\nPlease install them with:")
        print("  pip install deepagents[cli]")
        print("\nOr install all dependencies:")
        print("  pip install 'deepagents[cli]'")
        sys.exit(1)


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description = "DeepAgents - AI Coding Assistant",
        formatter_class = argparse.ArgumentDefaultsHelpFormatter,
        add_help = True,
    )

    subparsers = parser.add_subparsers(dest = "command",help = "command to run")

    # List command
    subparsers.add_parser("list",help = "list all available agents")

    # Help command
    subparsers.add_parser("help",help = "show help information")

    # Reset command
    reset_parse = subparsers.add_parser("reset",help = "Reset an agent")
    reset_parse.add_argument("--agent",required = True,help = "Name of agent to reset")
    reset_parse.add_argument("--target",dest = "source_agent",help = "Copy prompt from another agent")

    # Default interactive mode
    parser.add_argument(
        "--agent",
        default = "agent",
        help = "Agent identifier for separate memory stores (default: agent).",
    )
    parser.add_argument(
        "--auto-approve",
        action = "store_true",
        help = "Auto-approve tool usage without prompting (disables human-in-the-loop)",
    )


async def simple_cli(agent,instant_id: str | None,session_state,baseline_tokens: int = 0):
    """Main CLI循环"""
    console.clear()

    if tavily_client is None:
        pass


def cli_main():
    pass


if __name__ == "__main__":
    cli_main()
