import os
import time
from pathlib import Path

import typer
from typing_extensions import Annotated

import fastapi_amis_admin_cli
from fastapi_amis_admin_cli.commands.project import new_project, new_app
from fastapi_amis_admin_cli.commands.utils import get_setting_value, check_requirement, find_process_by_port

app = typer.Typer(no_args_is_help=True)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Annotated[bool, typer.Option("--version", "--ver")] = None,
):
    if version:
        typer.echo(f"FastAPI-Amis-Admin CLI Version: {fastapi_amis_admin_cli.__version__}")


@app.command(no_args_is_help=True)
def new(
    name: Annotated[str, typer.Argument(help="Project or App Name.")],
    init: Annotated[bool, typer.Option('--init', '-i', help='Initialize a new project.')] = False,
    out: Annotated[Path, typer.Option('--out', '-o', help='Where to output the generated project dir into.')] = None,
):
    """Create A FastAPI-Amis-Admin App."""
    if init:
        new_project(name, out)
        out = name.lower().replace(' ', '-').replace('-', '_')
        name, out = 'Demo', f'./{out}/backend/apps'
    new_app(name, out)


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True}, add_help_option=False)
def run(
    ctx: typer.Context,
    app: Annotated[str, typer.Option(default_factory=lambda: get_setting_value("app", "main:app"))],
    host: Annotated[str, typer.Option(default_factory=lambda: get_setting_value("host", "127.0.0.1"))],
    port: Annotated[int, typer.Option(default_factory=lambda: get_setting_value("port", 8000))],
    reload: Annotated[bool, typer.Option(default_factory=lambda: get_setting_value("debug", False))],
    workers: Annotated[int, typer.Option(default_factory=lambda: get_setting_value("workers", 1))],
):
    """
    Run The FastAPI-Amis-Admin Server. To see the complete set of available options, use `uvicorn --help`.
    """

    check_requirement('uvicorn', install=True)
    args = ctx.args.copy()
    if args and args[0] == '--help':
        return os.system('uvicorn ' + ' '.join(args))
    if not args or args[0].startswith('-'):
        args.insert(0, app)
    if reload:
        workers = 1
        args.append('--reload')
    args.extend(['--host', host, '--port', str(port), '--workers', str(workers)])
    return os.system('uvicorn ' + ' '.join(args))


@app.command()
def stop(
    port: Annotated[int, typer.Argument(default_factory=lambda: get_setting_value("port", 8000))],  # type: ignore
):
    """Stop Uvicorn Application"""
    while True:
        proc = find_process_by_port(port)
        if not proc:
            typer.echo(f"The process with port {port} was not found")
            break
        typer.echo(f"Shutting down the process({proc.name()}) on port {port}")
        proc.kill()
        time.sleep(0.5)


@app.command()
def build():
    """todo"""
    typer.echo("build docker")
