import os
from pathlib import Path
from typing import Optional

import fastapi_amis_admin_cli
import typer
from fastapi_amis_admin_cli.commands.project import new_project, new_app
from fastapi_amis_admin_cli.commands.utils import get_settings, get_backend_path

app = typer.Typer(no_args_is_help=True)


@app.callback(invoke_without_command=True)
def main(
        ctx: typer.Context,
        version: Optional[bool] = typer.Option(None, "--version", "--ver"),
):
    if version:
        typer.echo(f"FastAPI-Amis-Admin CLI Version: {fastapi_amis_admin_cli.__version__}")


@app.command(no_args_is_help=True)
def new(
        name: str = typer.Argument(..., help="Project or App Name"),
        init: bool = typer.Option(False, '--init', '-i'),
        out: Optional[Path] = typer.Option(None, '--out', '-o', help='Where to output the generated project dir into.')
):
    """Create A FastAPI-Amis-Admin App."""
    if init:
        new_project(name, out)
        out = name.lower().replace(' ', '-').replace('-', '_')
        name, out = 'Demo', f'./{out}/backend/apps'
    new_app(name, out)


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True}, add_help_option=False)
def run(ctx: typer.Context):
    """
    Run The FastAPI-Amis-Admin Server.
    To see the complete set of available options, use `uvicorn --help`.
    """
    args = ctx.args.copy()
    if args and args[0] == '--help':
        return os.system('uvicorn ' + ' '.join(args))
    settings = get_settings()
    if not args or args[0].startswith('-'):
        args.insert(0, 'main:app')
    if '--host' not in args:
        args.extend(['--host', settings.get('host')])
    if '--port' not in args:
        args.extend(['--port', str(settings.get('port'))])
    if '--reload' not in args and settings.get('debug'):
        args.append('--reload')
    if '--app-dir' not in args:
        os.chdir(get_backend_path(must=True))
    os.system('uvicorn ' + ' '.join(args))


@app.command()
def build():
    """todo"""
    typer.echo("build docker")
