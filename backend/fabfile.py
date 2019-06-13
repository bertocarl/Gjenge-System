from fabric.api import run, cd, env, local

CONF = {
    'backend': {
        'hosts': ['edgica@142.93.235.78'],
        'project': 'wishlist',
        'root': '/home/edgica/edgica/backend',
        'uwsgi_conf': '/etc/uwsgi/available/backend.ini',
    }
}


def pull():
    with cd('%(root)s/' % env):
        run('git pull')


def pip_install():
    run('%(root)s/env/bin/pip install -r %(root)s/requirements.txt' % env)


def collect_static():
    run(django_command('collectstatic --noinput -v0') % env)


def reload_uwsgi():
    run('sudo touch --no-dereference %(uwsgi_conf)s' % env)


def push():
    local('git push')


def syncdb():
    run(django_command('migrate') % env)


def python(command):
    return 'DJANGO_SETTINGS_MODULE=backend.settings.prod %(root)s/env/bin/python' + ' ' + command


def django_command(command):
    return python('%(root)s/manage.py') + ' ' + command


def init_env(name):
    for k, v in CONF[name].items():
        setattr(env, k, v)


init_env('backend')


def update():
    # push()
    pull()
    pip_install()
    collect_static()
    syncdb()
    reload_uwsgi()


def update_fast():
    push()
    pull()
    collect_static()
    reload_uwsgi()


def only_reload():
    reload_uwsgi()
