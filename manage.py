import json
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


class PGAdminConfig(BaseModel):
    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str


class ElasticAPMConfig(BaseModel):
    ELASTIC_APM_SECRET_TOKEN: str
    ELASTIC_APM_SERVER_URL: str


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

        with open("gateway/.env", "w") as writer:
            writer.write(f"MODE={mode}")

        with open(f"gateway/secrets/{mode}.json") as reader:
            secrets = json.loads(reader.read())

        # with open(".env.elk-apm", "w") as writer:
        #     apm_secrets = ElasticAPMConfig.model_validate(secrets)
        #     for key, value in apm_secrets.model_dump().items():
        #         writer.write(f"{key}={value}\n")

        with open("gateway/.env.postgres", "w") as writer:
            pg_secrets = PostgresConfig.model_validate(secrets)
            for key, value in pg_secrets.model_dump().items():
                writer.write(f"{key}={value}\n")

        # with open("gateway/.env.pgadmin", "w") as writer:
        #     pgadmin_secrets = PGAdminConfig.model_validate(secrets)
        #     for key, value in pgadmin_secrets.model_dump().items():
        #         writer.write(f"{key}={value}\n")

        subprocess.run("docker compose up --build")
    except KeyError:
        print("Invalid mode")


@app.command()
def terminate():
    subprocess.run("docker compose down")
    subprocess.run('docker image prune --force --filter "dangling=true"', shell=True)


if __name__ == "__main__":
    app()
