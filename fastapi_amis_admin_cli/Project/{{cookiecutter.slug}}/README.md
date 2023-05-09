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

- Use pip to install

```shell
# 1.Change to the project root directory
cd ./{{ cookiecutter.slug }}/backend
# 2.Install dependencies.(Recommend to use virtual environment)
pip3 install -r requirements.txt
# 3.Run server.
faa run
```

- Use [pdm](https://pdm.fming.dev/latest/) to install

```shell
# 1.Install pdm
pip3 install --user pdm
# 2.Install dependencies.
pdm install
# 3.Run server.
pdm run run
```

### Preview

- Open http://127.0.0.1:8000/admin/ in your browser.