import functools
import importlib
import locale
import os
import sys
from pathlib import Path
from typing import Optional, List, TypeVar, Dict, Any

import typer
from click import Choice


def get_language() -> str:
    language = os.getenv('LANGUAGE') or os.getenv('LANG') or locale.getdefaultlocale()[0]
    return 'zh_CN' if language.lower().startswith('zh') else 'en_US'


def get_settings() -> Dict[str, Any]:
    backend = get_backend_path(must=True)
    sys.path.append(str(backend.resolve()))
    try:
        settings = importlib.import_module('core.settings')
    except ImportError as e:
        return {}
    return settings.settings.dict()


_VT = TypeVar("_VT")


def list_prompt(text: str, lst: List[_VT], default: _VT = None, **kwargs) -> _VT:
    if not lst:
        return default
    if len(lst) == 1:
        return lst[0]
    typer.echo(text)
    choices = []
    for i, v in enumerate(lst):
        typer.secho(f"[{i}]{v}", fg=typer.colors.GREEN)
        choices.append(str(i))
    index = typer.prompt("Input Choices", default='0', type=Choice(choices), **kwargs)
    return lst[int(index)]


@functools.lru_cache()
def get_backend_path(must: bool = False) -> Optional[Path]:
    path = Path('.')
    if (path / "core/__init__.py").is_file() and str(path.resolve()).endswith('backend'):
        return path
    lst = [
        p.parent.parent for p in path.glob("**/backend/core/__init__.py")
        if p.is_file() and '{{cookiecutter.slug}}' not in str(p)
    ]
    path = list_prompt("Where is the backend path?", lst)
    if not path and must:
        while True:
            path: Path = typer.prompt("Where is the backend path?", type=Path)
            if (path / "core/__init__.py").is_file():
                break
            else:
                typer.secho("Cannot find backend in current folder!", fg=typer.colors.RED)
    return path
