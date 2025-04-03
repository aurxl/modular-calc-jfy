[![Unittest](https://github.com/aurxl/modular-calc-jfy/actions/workflows/unittest.yml/badge.svg)](https://github.com/aurxl/modular-calc-jfy/actions/workflows/unittest.yml)
[![Pylint](https://github.com/aurxl/modular-calc-jfy/actions/workflows/pylint.yml/badge.svg)](https://github.com/aurxl/modular-calc-jfy/actions/workflows/pylint.yml)

---

# Rechnermodul 'JustForYou'
Projektteilnehmer:
- Sarah Zimmermann
- Kenny Schilde
- Tommy Pahlitzsch
- Jan Meineke


## Development

#### prerequisite
- [git](https://git-scm.com/downloads/win)
- [python 3.12](https://www.python.org/downloads/release/python-3120/)
    - CLICK *adding python to PATH* in installation Dialogue
- [poetry](https://python-poetry.org/)
    - install via pip is probably the most painless way
        ``` sh
        pip3 install poetry
        ``` 
    - otherwise when handling with multiple virtualenvs + different python versions, take a look at [pyenv](https://github.com/pyenv/pyenv)

#### install dependencies
- install dependencies via poetry
    ``` sh
    $ poetry install
    ```

#### add dependencies
- add dependencies to virtualenv via poetry
    ``` sh
    $ poetry add "packagae"
    ```

#### activate virtualenv
- activate virtualenv via poetry
    ``` sh
    $ poetry shell
    ```

#### automatically activate virtualenv in vscode
- to allow vscode to execute scripts
    ``` ps
    $ Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
    ```
- launch vscode in project dir
    ``` ps
    $ cd path\to\project
    $ code .
    ```

#### run the project
- run project with poetry via preconfigured script
    ``` sh
    $ poetry run jfy
    ```

- run project inside the virtualenv
    ``` sh
    $ poetry shell
    $ python modular_calc_jfy/__main__.py
    ```
    or
    ``` sh
    $ poetry run python modular_calc_jfy/__main__.py
    ```

#### build the project
Configure modules that should be available within the exe in the `modules.yaml` file.

To easily build our python project to wheel and .exe we can use the following:
``` sh
poetry build
```
This will build our `EXE` to `dist/pyinstaller/win_amd64/modular_calc_jfy/modular_calc_jfy.exe`.

This is due to the pyinstaller plugin for poetry. If pyinstaller change in pyinstaller config is needed, take a look at the `pyproject.toml`. All options are defined there.
