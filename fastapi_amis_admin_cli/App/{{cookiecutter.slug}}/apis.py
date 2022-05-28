from fastapi import APIRouter

router = APIRouter(prefix='/{{cookiecutter.slug}}', tags=['{{cookiecutter.name}}'])


@router.get('/hello')
async def hello(name: str = '') -> str:
    return f'hello {name}'
