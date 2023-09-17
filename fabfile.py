import os
import random
from datetime import datetime

from fabric import task
from config import settings as dj_settings

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__)) + '/'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
VIRTUAL_ENV = os.environ.get('VIRTUAL_ENV') or os.path.join(PROJECT_ROOT, 'env')
VIRTUAL_ENV_ACTIVATE = '. %s' % os.path.join(VIRTUAL_ENV, 'bin/activate')


@task
def runserver(c):
    port = dj_settings.HOST_PORT
    if not port:
        summ = sum([ord(char) for char in PROJECT_ROOT.split('/')[-1]])
        random.seed(summ)
        port = random.randrange(1024, 5000)

    server_address = '127.0.0.1'
    if os.path.exists('/etc/hosts'):
        with open('/etc/hosts') as f:
            if f.read().find(dj_settings.SITE_URL) != -1:
                server_address = dj_settings.SITE_URL

    with c.prefix(VIRTUAL_ENV_ACTIVATE):
        with c.cd(PROJECT_ROOT):
            c.run(f'./manage.py runserver {server_address}:{port}', pty=True)


@task
def dumpdb(c, user='postgres'):
    db_name = dj_settings.DATABASES['default']['NAME']

    date = datetime.now().strftime("%Y-%m-%d_%H%M")
    dump_name = f'dumps/{db_name}_{date}.sql'

    with c.prefix(VIRTUAL_ENV_ACTIVATE):
        with c.cd(PROJECT_ROOT):
            c.run('mkdir -p dumps')
            c.run(f'sudo -u {user} pg_dump {db_name} > {dump_name} | bzip2 -9 > {dump_name}.bz2')


@task
def restoredb(c):
    db_user = dj_settings.DATABASES['default']['USER']
    db_name = dj_settings.DATABASES['default']['NAME']

    with c.prefix(VIRTUAL_ENV_ACTIVATE):
        with c.cd(PROJECT_ROOT):
            with c.lcd('dumps'):
                last_dump = 'dumps/' + c.run('ls -1tr', capture=True).stdout.strip().split('\n')[-1]
            c.run(f'sudo psql -U {db_user} -d {db_name} < {last_dump}')


#
#
@task
def deploylocal(c, branch=None):
    with c.prefix(VIRTUAL_ENV_ACTIVATE):
        branch = branch or 'main'

        c.run('git checkout %s && git pull' % branch)
        c.run('pip3 install -r requirements.txt')
        c.run('./manage.py migrate')
        c.run('./manage.py collectstatic --noinput')


@task
def check(c):
    with c.prefix(VIRTUAL_ENV_ACTIVATE):
        # c.run('python manage.py test')
        c.run('python manage.py check')
        c.run('time flake8 ./Api ./core ./Manager ./Public')


@task
def creategraphmodels(c, *args):
    date = datetime.now().strftime("%Y-%m-%d_%H%M")
    dot_file_name = f'graphs/project_{date}.dot'

    models = ''
    if args:
        models = f' -I {",".join(args)} '

    with c.prefix(VIRTUAL_ENV_ACTIVATE):
        with c.cd(PROJECT_ROOT):
            c.run('mkdir -p graphs')
            c.run(f'./manage.py graph_models -a {models} -o {dot_file_name}')
