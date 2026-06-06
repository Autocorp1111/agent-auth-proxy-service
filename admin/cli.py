"""
Admin CLI for Agent Auth Proxy
"""

import typer
import httpx

app = typer.Typer()


@app.command()
def register(name: str):
    """Register a new agent"""
    print(f"Registering agent: {name}")
    # Implementation would call the admin API


if __name__ == "__main__":
    app()