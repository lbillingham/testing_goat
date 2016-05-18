from os import path, sep
import subprocess

THIS_FOLDER = path.dirname(path.abspath(__file__))
FAB_PATH = path.join(
    'c:', sep, 'Users', 'laurence', 'AppData', 'Local',
    'Continuum', 'Anaconda3', 'envs', 'fabric', 'Scripts',
    'fab.EXE'
)


def create_session_on_server(host, email):
    return subprocess.check_output(
        [
            FAB_PATH,
            'create_session_on_server:email={}'.format(email),
            '--host={}'.format(host),
            '--hide=everthing, status',
        ],
        cwd=THIS_FOLDER
    ).decode().strip()


def reset_database(host):
    subprocess.check_call(
        [FAB_PATH, 'reset_database', '--host={}'.format(host)],
        cwd=THIS_FOLDER
    )
