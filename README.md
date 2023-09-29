# pocket-fridge
## Pet project to create website that provide news

# Installation
## Requirements
* Python 3.10+
* PostgreSQL 12
* Redis
* MongoDB

## Local setup
### clone
```bash
git clone git@github.com:GoGei/pocket-fridge.git
```
### Add hosts
* Ubuntu: /etc/hosts
* Windows: c:\Windows\System32\Drivers\etc\hosts
* MacOS: /private/etc/hosts
```bash
127.0.0.1           pocket-fridge.local
127.0.0.1        my.pocket-fridge.local
127.0.0.1       api.pocket-fridge.local
127.0.0.1   manager.pocket-fridge.local
```

### Add database
```postgresql
CREATE USER pocket_fridge WITH ENCRYPTED PASSWORD 'pocket-fridge-password' SUPERUSER CREATEDB;
CREATE DATABASE pocket_fridge WITH OWNER pocket_fridge ENCODING 'UTF8';
```

### Setup environment
Create virtual environment
```bash
cd pocket-fridge/
python3.10 -m venv env
source env/bin/activate
pip install -r requirements.txt
./manage.py migrate
```

Copy settings
```bash
cp config/settings_example.py config/settings.py
```

## Useful commands

### Launch server
```bash
fab runserver
```

### Run async tasks
```bash
fab celeryd
```

### Create class diagram of DB
```bash
fab creategraphmodels
```

### Check with flake8
```bash
fab check
```

### Deploy local
```bash
fab deploylocal
```
