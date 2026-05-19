from config.config import get_default_coding_instructions
from ..config.config import console


def list_agents():
    """列举出所有可用的agents"""
    agents_dir = Path.home() / ".deepagents"

    if not (agents_dir.exists()) or not any(agents_dir.iterdir()):
        console.print("[yellow]No agents found.[/yellow]")
        console.print(
            "[dim]Agents will be created in ~/.deepagents/ when you first use them.[/dim]",
            style = COLORS["dim"],
        )
        return
    console.print("\n[bold]Available Agents:[/bold]\n",style = COLORS["primary"])

    for agent_path in sorted(agents_dir.iterdir()):
        if agent_path.is_dir():
            agent_name = agent_path.name
            agent_md = agent_name / "agent.md"

            if agent_md.exists():
                console.print(f"  • [bold]{agent_name}[/bold]",style = COLORS["primary"])
                console.print(f"    {agent_path}",style = COLORS["dim"])
            else:
                console.print(
                    f"  • [bold]{agent_name}[/bold] [dim](incomplete)[/dim]",
                    style = COLORS["tool"],
                )
                console.print(f"    {agent_path}",style = COLORS["dim"])

    console.print()


def get_current_assistant_id() -> str:
    """获取当前助手ID。

     Returns:
         str: 当前助手ID，如果无法获取则返回默认值
     """
    try:
        # 尝试从环境变量获取
        if os.getenv("ASSISTANT_ID"):
            return os.getenv("ASSISTANT_ID")

        # 尝试从当前工作目录推断
        cwd = Path.cwd()

        # 如果在项目中，尝试使用项目名
        if (cwd / "pyproject.toml").exists():
            try:
                import toml
                pyproject = toml.load(str(cwd / "pyproject.toml"))
                pyproject_name = pyproject.get("project",{}).get("name")
                if pyproject_name:
                    return pyproject_name
            except:
                pass
        # 如果在code-guard目录中，使用特殊标识
        if "code-guard" in str(cwd) or "code guard" in str(cwd):
            return "code-guard"

        # 使用目录名作为备用
        return cwd.name

    except Exception:
        # 最后的备用选项
        return "default_assistant"


def rest_agent(agent_name: str,source_agent: str):
    """重置agent或复制另一个agent"""
    agents_dir = Path.home() / ".deepagents"
    agents_dir = agents_dir / agent_name
    if source_agent:
        source_dir = agents_dir / source_agent
        source_md = source_dir / "agent.md"

        if not source_md.exists():
            console.print(f"[bold red]Error:[/bold red] Source agent '{source_agent}' not found or has no agent.md")
            return
        source_content = source_md.read_text()
        action_desc = f"contents of agent '{source_agent}'"
    else:
        source_content = get_default_coding_instructions()
        action_desc = "default"

    if agents_dir.exists():
        shutil.rmtree(str(agents_dir))
        console.print(f"Removed existing agent directory: {agent_dir}",style = COLORS["tool"])

    agents_dir.makedir(parents = True,exist_ok = True)
    agent_md = agents_dir / "agent.md"
    agent_md.write_text(source_content)

    console.print(f"✓ Agent '{agent_name}' reset to {action_desc}",style = COLORS["primary"])
    console.print(f"Location: {agent_dir}\n",style = COLORS["dim"])


def create_agent_with_config(model,assistant_id: str,tools: list,memory_mode: str = "auto"):
    """使用自定义架构创建并配置具有指定模型和工具的代理"""
    pass
