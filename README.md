# Al Trecolore menu
## Project description 
The purpose of this project is to develop the server side of the system for a cafe. 
The system provides for 2 types of users: a client and a manager. The client has the ability to create orders and add dishes to the demand. The manager adds dishes, changes the status of the order (registered, deleted, etc.), adds products to the database, has access to all the data stored in the database. 
The result of the system is the ability to view the menu, place orders without leaving home for the client, and keep track of available products and dishes for the manager.

## Entities:
- User
- Address
- Order
- Details
- Menu
- Ingredient
- Product

## Roles
- role_viewer
- role_client
- role_manager

## Actions on entities + who has access:
1) User:
- Add // role_viewer
- UpdatePersonalInform // role_client, role_manager
- Login // role_client, role_manage
- Logout // role_client, role_manager
- Delete // role_client, role_manager
- GetUser // role_client, role_manager
- GetAllUsers // role_manager
- SetRole // role_manager
2) Address
3) Order:
- Add // role_client, role_manager
- SetStatus // role_manager
- UpdateOrder // role_manager
- GetOrder // role_client, role_manager
- GetAllOrders // role_manager
- Delete // role_client, role_manager
4) Details
5) Menu:
- GetAllMenu // role_viewer, role_client, role_manager
- GetMenu // role_viewer, role_client, role_manager
- AddToDemand // role_client, role_manager
- Add // role_manager
- Update // role_manager
- Delete // role_manager
- FilterMenu // role_client, role_manager
6) Ingredient
7) Product:
- Add // role_manager
- Update // role_manager
- GetProduct // role_manager
- GetAllProducts // role_manager
- Delete // role_manager


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
Install virtualenv
```PowerShell
python3.7.9 -m pip install --user virtualenv
```
Create venv
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

## Install requirements.txt
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

## To work with the mysql database, you need to install the SQLAlchemy ORM library in a virtual environment:
```
pip install Flask Flask-SQLAlchemy
```
## Specify URI to the data base:
   For mysql : ```app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://username:password@host:port/database_name"```
   
   For postgresql : ```app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://username:password@host:port/database_name"```

## To create migrations, you need to install the Alembic library in a virtual environment:
```
pip install alembic
```
## Initiate Alembic:
```
alembic init alembic
```
## Change the settings in the alembic.ini file:

sqlalchemy.url = postgresql://postgres:12345@localhost:5432/al-trecolore-menu
## Install mysqlclient:
```
pip install mysqlclient
```
## To create a migration, run the command
```
alembic upgrade head
```
