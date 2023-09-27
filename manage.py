import subprocess
from enum import Enum
from typing import Union

from pydantic import BaseModel
from typer import Typer

app = Typer()


class PostgresConfig(BaseModel):
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str


class Modes(str, Enum):
    development = "development"
    staging = "staging"
    production = "production"
    ignore_smtp = "ignore-smtp"


@app.command()
def deploy(mode: Union[str, None] = "development"):
    try:
        if mode not in Modes.__members__.values():
            raise KeyError

        with open("auth/.env", "w") as writer:
            writer.write(f"MODE={mode}")

        with open(f"auth/secrets/{mode}.json") as reader:
            secrets = PostgresConfig.model_validate_json(reader.read())

        with open("auth/.env.postgres", "w") as writer:
            for key, value in secrets.model_dump().items():
                writer.write(f"{key}={value}\n")

        subprocess.run("docker compose up --build")
    except KeyError:
        print("Invalid mode")


@app.command()
def terminate():
    subprocess.run("docker compose down")
    subprocess.run('docker image prune --force --filter "dangling=true"', shell=True)


if __name__ == "__main__":
    app()
