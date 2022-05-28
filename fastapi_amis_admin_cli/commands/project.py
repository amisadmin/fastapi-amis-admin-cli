import random
import string

import typer
from cookiecutter.main import cookiecutter

from fastapi_amis_admin_cli import BASE_PATH
from fastapi_amis_admin_cli.commands.utils import get_language, get_backend_path


def new_project(name: str, out: str = None, **kwargs):
    context={
            "name": name,
            "port": typer.prompt("The project port?", default=8000, type=int),
            "use_user_auth": typer.confirm("Do you want to use `FastAPI-User-Auth`?", default=True),
            "use_scheduler": typer.confirm("Do you want to use `FastAPI-Scheduler`?", default=True),
            "language": get_language(),
            "secret_key": ''.join(random.choices(string.ascii_lowercase + string.digits, k=64)),
            **kwargs
        }
    print('context',context)
    cookiecutter(
        template=str((BASE_PATH / 'Project').resolve()),
        no_input=True,
        extra_context=context,
        output_dir=(out or '.'),
    )


def new_app(name: str, out: str = None, **kwargs):
    if not out:
        backend = get_backend_path(must=False)
        if backend:
            out = str(backend / 'apps')
        else:
            new_project('project', app_name=name)
            return new_app(name, **kwargs)
    cookiecutter(
        template=str((BASE_PATH / 'App').resolve()),
        no_input=True,
        extra_context={"name": name, **kwargs},
        output_dir=out,
        **kwargs
    )
    typer.echo(f'Output Dir: "{out}"')
