# Al Trecolore menu
# System requirements
    Version of python: python 3.7.9
    Virtual environment: venv
    Framework: Flask
    WSGI-server: Waitress

# Project Setup Instruction
## Pyenv and Python 3.7.9 version installation

### On Windows
Open PowerShell as administrator and paste code below:
```PowerShell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```
1. Add PYENV, PYENV_HOME and PYENV_ROOT to your Environment Variables:
```PowerShell
[System.Environment]::SetEnvironmentVariable('PYENV',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")

[System.Environment]::SetEnvironmentVariable('PYENV_ROOT',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")

[System.Environment]::SetEnvironmentVariable('PYENV_HOME',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")
```
2. Add the following paths to your USER PATH variable in order to access the pyenv command:
```PowerShell
[System.Environment]::SetEnvironmentVariable('path', $env:USERPROFILE + "\.pyenv\pyenv-win\bin;" + $env:USERPROFILE + "\.pyenv\pyenv-win\shims;" + [System.Environment]::GetEnvironmentVariable('path', "User"),"User")
```
Installation is done.
Now install python 3.7.9 version using code below:
```PowerShell
pyenv install 3.7.9
```
Installation will take a lot of time, so don't worry.
Don't forget to add python.exe path to PATHs in System.
Copy python.exe file and create python3.7.9.exe file.

## Create virtual environment (venv)
Paste code below to create venv
```PowerShell
python -m venv ap-menu-env
```

## Activate installed venv
```PowerShell
ap-menu-env\Scripts\Activate
```
Check python version:
```PowerShell
python --version
```
Paste code below to see python paths:
```PowerShell
where.exe python
```

## Install Flask, Waitress and requirements.txt
```PowerShell
pip install Flask
```
```PowerShell
pip install waitress
```
```PowerShell
pip install -r requirements.txt
```

## Run project using Waitress
```PowerShell
waitress-serve --host 127.0.0.1 --port 5000 server:menuapp
```

## Deactivate venv
```PowerShell
deactivate
```


 