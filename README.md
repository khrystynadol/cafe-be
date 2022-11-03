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
## Для роботи з базою даних mysql необхідно встановити бібліотеку SQLAlchemy ORM , знаходячись у віртуальному середовищі:
```
pip install Flask Flask-SQLAlchemy
```
## Вказати URI до бази даних :
   Для mysql : ```app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://username:password@host:port/database_name"```
   Для postgresql : ```app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://username:password@host:port/database_name"```

## Для створення міграцій необхідно встановити бібліотку Alembic у віртуальному середовищі :
```
pip install alembic
```
## Проініцюлювати Alembic:
```
alembic init alembic
```
## Змінити налаштування в alembic.ini файлі:

sqlalchemy.url = mysql+mysqldb://root:root@localhost:3306/database_name
## Встановити пакет mysqlclient:
```
pip install mysqlclient
```
## Для створення міргації виконуємо команду
```
alembic upgrade head
```

## Опис проекту
Написати сервіс для роботи меню кафе. 
Провізор (менеджер) може додавати страви в базу, видаляти, редагувати інформацію про них. 
Можливість замовлення страви на ВЖЕ залежить від наявності страви (якщо наявні всі інгредієнти (для цього база даних)). 
В списку буде можливість переглянути всі страви, щоб зробити передзамовлення (на майбутнє число). 
Користувач може переглядати інформацію про всі страви, 
здійснювати замовлення на вже та майбутнє (майбутнє вимагає підтвердження провізора).

## Сутності:
- User
- Address
- Order
- Details
- Menu
- Ingredient
- Product

## Ролі
- role_viewer
- role_client
- role_manager

## Дії над сутностями + хто має доступ:
1) User:
- Add // role_viewer
- UpdatePersonalInform // role_client, role_manager
- Login // role_client, role_manage
- Logout // role_client, role_manager
- Delete // role_client, role_manager
- GetUser // role_client, role_manager
- GetAllUsers // role_manager
- SetRole // role_manager
2) Address:
- Add // role_client, role_manager
- Delete // role_manager
- GetAddress // role_client, role_manager
- GetAllAddresses // role_manager
3) Order:
- Add // role_client, role_manager
- SetStatus // role_manager
- GetOrder // role_client, role_manager
- GetAllOrders // role_manager
- Delete // role_client, role_manager
4) Details:
- Update // role_manager
- GetAllDetailsForOrder // role_client, role_manager
- GetAllDetails // role_manager
5) Menu:
- GetAllMenu // role_viewer, role_client, role_manager
- GetMenu // role_viewer, role_client, role_manager
- AddToDemand // role_client, role_manager
- Add // role_manager
- Update // role_manager
- Delete // role_manager
6) Ingredient:
- Add // role_manager
- Update // role_manager
- GetIngredient // role_manager
- GetAllIngredients // role_manager
- Delete // role_manager
7) Product:
- Add // role_manager
- Update // role_manager
- GetProduct // role_manager
- GetAllProducts // role_manager
- Delete // role_manager


 