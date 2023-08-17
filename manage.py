import os
import subprocess
from pathlib import Path
from typing import Union

from typer import Typer

app = Typer()


@app.command()
def run_service(app_name: Union[str, None] = None):
    if app_name:
        app_dir = Path(f"{Path.cwd()}/{app_name}")
        os.chdir(app_dir)
        subprocess.run("docker compose up --build")


@app.command()
def stop_service(app_name: Union[str, None] = None):
    if app_name:
        app_dir = Path(f"{Path.cwd()}/{app_name}")
        os.chdir(app_dir)
        subprocess.run("docker compose down")


if __name__ == "__main__":
    app()
