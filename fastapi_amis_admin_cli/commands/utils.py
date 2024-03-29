import functools
import importlib
import locale
import os
import sys
from pathlib import Path
from typing import Optional, List, TypeVar, Dict, Any, Union

import typer
from click import Choice


def get_language() -> str:
    language = os.getenv('LANGUAGE') or os.getenv('LANG') or locale.getdefaultlocale()[0] or "en_US"
    return 'zh_CN' if language.lower().startswith('zh') else language


@functools.lru_cache()
def get_settings() -> Dict[str, Any]:
    backend = get_backend_path(must=True)
    sys.path.append(str(backend))
    os.chdir(backend)  # 切换到backend目录
    try:
        module = importlib.import_module('core.settings')
    except ImportError as e:
        return {}
    return module.settings.dict()


def get_setting_value(key: str, default: Any = None) -> Any:
    return get_settings().get(key, default)


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
        return path.resolve()
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
    return path.resolve() if path else None


def check_requirement(name: str, install: Union[str, bool] = False) -> bool:
    try:
        importlib.import_module(name)
        return True
    except ImportError:
        if install:
            name = name if install is True else install
            os.system(f'pip install {name}')
            return True
        return False

def find_process_by_port(port):
    """根据端口号查找进程"""
    import psutil

    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port:
            try:
                proc = psutil.Process(conn.pid)
                return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    return None
