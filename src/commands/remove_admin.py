from ..utils.verification import cli_tools_admin_login_required
from ..queries.admin import remove_admin
from ..app import app
import time

@app.cli.command("remove-admin")
@cli_tools_admin_login_required
def cli_tools_remove_admin():
    TIMEOUT = 7 * 60
    print("==== Remove Admin ====")
    print("Enter 'q!' at any field to quit.")

    _valid = False
    _start_time = time.time()
    while not _valid:
        username = input("Username: ")
        if (time.time() - _start_time) >= TIMEOUT:
            print("Timeout. Please restart")
            break
            
        if username == "q!":
            print("Aborting...")
            break

        try:
            remove_admin(username)
        except ValueError as e:
            print("Error: ", e)
            print("Try again.")
            continue

        print("Admin removed successfully")
        _valid = True


