from os import path, sep
import subprocess

THIS_FOLDER = path.dirname(path.abspath(__file__))
print(THIS_FOLDER)
FAB_PATH = path.join(
    'c:', sep, 'Users', 'laurence', 'AppData', 'Local',
    'Continuum', 'Anaconda3', 'envs', 'fabric', 'Scripts',
    'fab.EXE'
)


def create_session_on_server(host, email):
    from fabfile import KEY_FILE
    # session_key = subprocess.check_output(
    #     [
    #         FAB_PATH,
    #         'create_session_on_server:email={}'.format(email),
    #         '--host={}'.format(host),
    #         '--hide=everthing, status',
    #     ],
    #     cwd=THIS_FOLDER
    # ).decode().strip()
    max_wait = 180
    waited = 0
    step = 1

    print('$$$$$$ server_tools.create_session_on_server $$$$$$')
    while (not os.path.exists(file_path)) and waited < max_wait:
        time.sleep(step)
        waited += step
        print('waiting')

    if os.path.isfile(file_path):
        with open(KEY_FILE, 'r') as file_:
            file_.read(session_key)
            session_key = session_key.decode().strip()
    else:
        raise ValueError('{} isn\'t a file!'.format(file_path))
    return session_key


def reset_database(host):
    subprocess.check_call(
        [FAB_PATH, 'reset_database', '--host={}'.format(host)],
        cwd=THIS_FOLDER
    )
