from flask import current_app
from ..utils.verification import cli_tools_admin_login_required
from ..utils.validation import validate_password, PasswordValidationError
from ..queries.admin import create_admin
from getpass import getpass
import time
import click
from flask.cli import with_appcontext

@click.command("create-admin")
@with_appcontext
@cli_tools_admin_login_required
def cli_tools_create_admin():
    TIMEOUT = 7 * 60
    print("==== Create Admin ====")
    print("Enter 'q!' at any field to quit.")

    _valid = False
    _start_time = time.time()
    while not _valid:
        username = input("Username: ")
        if (time.time() - _start_time) >= TIMEOUT:
            print("Timeout. Please restart")
            break
            
        password = getpass("Password: ")
        if (time.time() - _start_time) >= TIMEOUT:
            print("Timeout. Please restart")
            break

        password_again = getpass("Password Again: ")
        if (time.time() - _start_time) >= TIMEOUT:
            print("Timeout. Please restart")
            break

        if username == "q!" or password == "q!" or password_again == "q!":
            print("Aborting...")
            break

        if password != password_again:
            print("Passwords don't match. Try again.")
            continue

        try:
            validate_password(password)
        except PasswordValidationError as e:
            print("Invalid Password: ", e)
            print("Try again.")
            continue

        try:
            create_admin(current_app.config.get('DB_SESSION'), username, password)
        except ValueError as e:
            print("Invalid Field: ", e)
            continue

        print("Admin created successfully")
        _valid = True

