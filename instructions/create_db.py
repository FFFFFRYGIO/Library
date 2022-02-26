import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from db_login.login_data_manage import init_login_info

if not os.path.isfile('db_login/key.key'):
    if not init_login_info():
        # print("Error with login initialization")
        quit()
init_login_info()
