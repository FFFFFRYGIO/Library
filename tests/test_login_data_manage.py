from os import path, remove

import pytest

import db_login.login_data_manage as program

KEY_FILE = 'tests/test_key.key'
USER_FILE = "tests/test_user"
ADMIN_FILE = "tests/test_admin"
TEST_USER_DATA = {
    'user': 'test_user',
    'passwd': 'test_user_passwd',
    'host': 'test_user_host',
    'port': 1111,
    'db': 'test_user_db_name',
    }
TEST_ADMIN_DATA = {
    'user': 'test_admin',
    'passwd': 'test_admin_passwd',
    'host': 'test_admin_host',
    'port': 2222,
    'db': 'test_admin_db_name',
    }


@pytest.mark.pickling
def test_init_login_info():
    program.init_login_info(key_file=KEY_FILE, user_file=USER_FILE, admin_file=ADMIN_FILE)

    # if init_login_info creates files
    assert path.isfile(KEY_FILE)
    assert path.isfile(USER_FILE)
    assert path.isfile(ADMIN_FILE)

    remove(KEY_FILE)
    remove(USER_FILE)
    remove(ADMIN_FILE)


@pytest.mark.pickling
def test_create_data():
    program.write_key(KEY_FILE)
    program.export_login_data(TEST_USER_DATA.copy(), USER_FILE, KEY_FILE)
    program.export_login_data(TEST_ADMIN_DATA.copy(), ADMIN_FILE, KEY_FILE)

    # if methods to create data creates files
    assert path.isfile(KEY_FILE)
    assert path.isfile(USER_FILE)
    assert path.isfile(ADMIN_FILE)

    # if key file contains key
    with open(KEY_FILE, "rb") as kf:
        assert len(kf.read())

    remove(KEY_FILE)
    remove(USER_FILE)
    remove(ADMIN_FILE)


@pytest.mark.pickling
def test_passwords():
    program.init_login_info(key_file=KEY_FILE, user_file=USER_FILE, admin_file=ADMIN_FILE,
                            user_login=TEST_USER_DATA.copy(), admin_login=TEST_ADMIN_DATA.copy())

    # if passwords are correctly encrypted
    password_from_file_admin = program.import_login_data(ADMIN_FILE, KEY_FILE)
    assert password_from_file_admin['passwd'] == TEST_ADMIN_DATA['passwd']
    password_from_file_user = program.import_login_data(USER_FILE, KEY_FILE)['passwd']
    assert password_from_file_user == TEST_USER_DATA['passwd']

    # if "get" functions returns the same dict as passed to export function
    user_dict = program.get_user(USER_FILE, KEY_FILE)
    assert TEST_USER_DATA == user_dict
    admin_dict = program.get_admin(ADMIN_FILE, KEY_FILE)
    assert TEST_ADMIN_DATA == admin_dict

    remove(KEY_FILE)
    remove(USER_FILE)
    remove(ADMIN_FILE)
