"""CLI的配置、常量和模型创建。"""

import os
import sys
from pathlib import Path

from ..prompt.prompt_template import system_prompt,memory_default_prompt

import dotenv
from rich.console import Console

try:
    import code_guard

    package_dir = Path(code_guard.__file__).parent
    env_file = package_dir / ".env"
    if env_file.exists():
        dotenv.read_dotenv(env_file)
    else:
        dotenv.load_dotenv()
except Exception as e:
    dotenv.load_dotenv()

model_name = os.environ.get("MODEL_NAME")
base_url = os.environ.get("BASE_URL")

# Color scheme with deep green and deep blue
COLORS = {
    "primary":"#00ffff",  # 青色 - 在深色和浅色背景下都清晰
    "secondary":"#0000ff",  # 蓝色 - 标准终端色彩
    "accent":"#00ff00",  # 绿色 - 明亮易识别
    "dim":"#808080",  # 灰色文本
    "user":"#ffffff",  # 白色 - 用户消息
    "agent":"#00ffff",  # 青色 - AI消息
    "thinking":"#ff00ff",  # 洋红色 - 思考状态
    "tool":"#ffff00",  # 黄色 - 工具调用
    "warning":"#ffff00",  # 黄色 - 警告信息
    "success":"#00ff00",  # 绿色 - 成功状态
    "info":"#0000ff",  # 蓝色 - 信息提示
}

# Rich console 实例
console = Console(highlight = False)

# Maximum argument length for display
MAX_ARG_LENGTH = 150

# Agent configuration
config = {"recursion_limit":1000}


def get_project_version():
    try:
        pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
        if pyproject_path.exists():
            with open(pyproject_path,"r",encoding = "utf-8") as f:
                content = f.read()
                for line in content.strip("\n"):
                    if line.strip().startswith("version = "):
                        return line.split("=")[1].strip().strip("\"")
        return "0.1.0"
    except Exception:
        return "0.1.0"


def get_ascii_banner():
    """Generate dynamic ASCII banner with pyfiglet."""
    from pyfiglet import figlet_format
    from rich.console import Console

    cwd = str(Path.cwd())
    version = get_project_version()

    banner = figlet_format("Code    Guard")
    info = f"[bold cyan]Working directory:[/bold cyan] {cwd}\n"
    info += f"[bold cyan]Version:[/bold cyan] v{version}\n"
    info += f"[bold cyan]Model:[/bold cyan] {modelName}\n"
    info += f"[bold cyan]Base URL:[/bold cyan] {baseUrl}"

    return banner + "\n" + info
    # console = Console()
    # console.print(info , style = "bold cyan")


# ASCII art banner function
CODE_GUARD_ASCII_BANNER = get_ascii_banner()

# Interactive commands: 交互式命令
COMMANDS = {
    "clear":"Clear screen and reset conversation",
    "help":"Show help information",
    "tokens":"Show token usage for current session",
    "memory":"Manage agent memory and knowledge base",
    "memory help":"Show memory detail",
    "cd":"Change working directory",
    "config":"Edit .env configuration file",
    "sys":"Show system information and platform features",
    "system":"Show system information and platform features",
    "info":"Show system information and platform features",
    "services":"Manage Windows services (Windows only)",
    "svc":"Manage Windows services (Windows only)",
    "quit":"Exit the CLI",
    "exit":"Exit the CLI",
}

# Common bash commands for autocomplete: 可补全命令数据库
COMMON_BASH_COMMANDS = {
    "ls":"List directory contents",
    "ls -la":"List all files with details",
    "cd":"Change directory",
    "pwd":"Print working directory",
    "cat":"Display file contents",
    "grep":"Search text patterns",
    "find":"Find files",
    "mkdir":"Make directory",
    "rm":"Remove file",
    "cp":"Copy file",
    "mv":"Move/rename file",
    "echo":"Print text",
    "touch":"Create empty file",
    "head":"Show first lines",
    "tail":"Show last lines",
    "wc":"Count lines/words",
    "chmod":"Change permissions",
}


def get_system_prompt():
    return system_prompt


def get_default_coding_instructions():
    """Get the default coding agent instructions.

     These are the immutable base instructions that cannot be modified by the agent.
     Long-term memory (agent.md) is handled separately by the middleware.
     """

    # 修复路径问题，prompt 文件在 prompt 目录下
    current_dir = Path(__file__).parent
    default_prompt_path = current_dir.parent / "prompt" / "default_agent_prompt.md"

    # 如果文件不存在，提供默认内容
    if not default_prompt_path.exists():
        return get_fallback_prompt()

    # 修复 Windows 编码问题，强制使用 UTF-8 编码
    try:
        return default_prompt_path.read_text(encoding = "utf-8")
    except UnicodeDecodeError:
        try:
            # 如果 UTF-8 失败，尝试GBK编码
            return default_prompt_path.read_text(encoding = "gbk")
        except UnicodeDecodeError:
            # 如果都失败，使用备用内容
            return get_fallback_prompt()


def get_fallback_prompt():
    """提供备用提示内容，当文件不存在时使用"""
    return memory_default_prompt


def create_model():
    """Create the appropriate model based on available API keys.

    Returns:
        ChatModel instance (OpenAI or Anthropic)

    Raises:
        SystemExit if no API key is configured
    """
    # 获取通用配置
    temperature = float(os.environ.get("MODEL_TEMPERATURE","0.3"))
    max_tokens = os.environ.get("MODEL_MAX_TOKENS")
    timeout = os.environ.get("MODEL_TIMEOUT")
    max_retries = int(os.environ.get("MODEL_MAX_RETRIES","3"))

    openai_key = os.environ.get("OPENAI_API_KEY")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")

    if openai_key:
        from langchain_openai import ChatOp
        openai = OpenAI(api_key = openai_key)

    if anthropic_key:
        pass
