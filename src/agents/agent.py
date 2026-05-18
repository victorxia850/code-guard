def list_agents() :
    """列举出所有可用的agents"""
    agents_dir = Path.home() / ".deepagents"

    if not (agents_dir.exists()) or not any(agents_dir.iterdir()) :
        pass