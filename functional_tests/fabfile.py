from fabric.api import env, run
from os import path

from server_tools import THIS_FOLDER
KEY_FILE = path.join(THIS_FOLDER, 'key.f')


def _get_base_folder(host):
    return '~/sites' + host


def _get_manage_dot_py(host):
    print('!!!!! fabfile._get_manage_dot_py !!!!!')
    return '{path}/virtualenv/bin/python {path}/source/manage.py'.format(
        path=_get_base_folder(host)
    )


def reset_database():
    print('**** fabfile.reset_database *****')
    run('{manage_py} flush --noinput'.format(
        manage_py=_get_manage_dot_py(env.host)
    ))


def create_session_on_server(email):
    print('### fabfile.create_session_on_server ####')
    session_key = run('{manage_py} create_session {email}'.format(
        manage_py=_get_manage_dot_py(env.host),
        email=email
    ))
    print(session_key)
    with open(KEY_FILE, 'w') as file_:
        file_.write(session_key)
