import os
from pathlib import Path
from typing import List

from fastapi_amis_admin.amis_admin.settings import Settings as AmisSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(AmisSettings):
    name: str = '{{ cookiecutter.name|capitalize }}'
    host: str = '{{ cookiecutter.host }}'
    port: int = {{cookiecutter.port}}
    secret_key: str = ''
    allow_origins: List[str] = None


settings = Settings(_env_file=os.path.join(BASE_DIR, '.env'))
