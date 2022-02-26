import pickle

from cryptography.fernet import Fernet

from db_login.user_settings import user_login_data, admin_login_data


def write_key(key_file):
    key = Fernet.generate_key()
    with open(key_file, "wb") as kf:
        kf.write(key)


def load_key(key_file):
    with open(key_file, "rb") as kf:
        key = kf.read()
    return key


def export_login_data(login_data, file, key_file):
    # print('EXPORT', login_data['passwd'])
    with open(file, "wb") as f:
        fer = Fernet(load_key(key_file))
        enc = fer.encrypt(login_data['passwd'].encode()).decode()
        login_data['passwd'] = enc
        # print('EXPORT', login_data['passwd'])
        pickle.dump(login_data, f)  # read dict from file


def import_login_data(file, key_file):
    with open(file, "rb") as f:
        login_data = pickle.load(f)  # read dict from file
        # print('IMPORT', login_data['passwd'])
        fer = Fernet(load_key(key_file))
        dec = fer.decrypt(login_data['passwd'].encode()).decode()
        login_data['passwd'] = dec
        # print('IMPORT', login_data['passwd'])
    return login_data


def init_login_info(admin_file="db_login/admin", user_file="db_login/user", key_file="db_login/key.key",
                    user_login=user_login_data, admin_login=admin_login_data):
    if os.environ.get['heroku']:
        heroku_login_data = {
            'user': os.environ.get['user'],
            'passwd': os.environ.get['passwd'],
            'host': os.environ.get['host'],
            'port': os.environ.get['port'],
            'db': os.environ.get['db'],
        }
        user_login = heroku_login_data
        admin_login = heroku_login_data
    try:
        write_key(key_file)
        export_login_data(user_login, user_file, key_file)
        export_login_data(admin_login, admin_file, key_file)
        return True
    except Exception as e:
        print(e)
        return False


def get_user(user_file="db_login/user", key_file="db_login/key.key"):
    user_data = import_login_data(user_file, key_file)
    return user_data


def get_admin(admin_file="db_login/admin", key_file="db_login/key.key"):
    admin_data = import_login_data(admin_file, key_file)
    return admin_data
