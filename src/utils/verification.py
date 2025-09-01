from functools import wraps
from flask import current_app
from ..queries.admin import check_admin_credentials
from getpass import getpass


def cli_tools_admin_login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print("You must log in.")
        username = input("Admin Username: ").strip()
        password = getpass("Password: ")

        try:
            if check_admin_credentials(current_app.config.get('DB_SESSION'), username, password):
                print("Logged in successfully.")
                return fn(*args, **kwargs)
            print("Dubious Credentials.")
        except ValueError as e:
            print("Error: ", e)

        print("Failed to login")
    return wrapper
