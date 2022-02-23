import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

from login_data_manage import init_login_info, get_admin as admin_settings


def db_create():
    if not init_login_info():
        print("Error with login initialization")
        quit()
    admin_login_data = admin_settings()
    u = admin_login_data['user']
    pd = admin_login_data['passwd']
    h = admin_login_data['host']
    pt = admin_login_data['port']
    db = admin_login_data['db']
    url = f"postgresql://{u}:{pd}@{h}:{pt}/{db}"
    if database_exists(url):
        print("Database already exist!")
        quit()
    else:
        create_database(url)

    print('Database created')


def get_database():
    log = logging.getLogger(__name__)
    # connect to db
    try:
        engine = get_engine_from_settings()
        log.info("Connected to db")
    except IOError:
        log.exception("Failed connection")
        return None, 'fail'
    return engine


def get_engine_from_settings():
    # set db connection based on "local_settings.py"
    keys = ['user', 'passwd', 'host', 'port', 'db']
    admin_login_data = admin_settings()
    if not all(key in keys for key in admin_login_data.keys()):
        raise Exception('Bad config file')
    return get_engine(
        admin_login_data['user'],
        admin_login_data['passwd'],
        admin_login_data['host'],
        admin_login_data['port'],
        admin_login_data['db'],
        )


def get_engine(user, passwd, host, port, db):
    # get sqlalchemy engine
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, pool_size=50, echo=False)
    return engine


db = get_database()
Base = declarative_base()
