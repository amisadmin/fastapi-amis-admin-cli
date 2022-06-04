# {{ cookiecutter.name|capitalize }}

## Develop

### Install command line extension

`pip install fastapi_amis_admin[cli]`

### How to start

1. create your app using `faa new app_name` .
2. writing your apps under `{{ cookiecutter.slug }}/backend/apps` folder.
3. run your server using `faa run` .

### Documentation

See [Docs](https://docs.amis.work/)

## Deploy

### Install and run:

```shell
cd {{ cookiecutter.slug }}
./scripts/run.sh
```