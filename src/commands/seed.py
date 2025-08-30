from ..utils.generation import random_secure_string
from ..utils.misc import flagify_from_cli
from ..utils.verification import cli_tools_admin_login_required
from ..queries.admin import create_admin, admins_exist
from ..queries.seeding import drop_table, create_table
from ..app import app

from enum import Flag, auto
import click
"""
    Flag summary:
        SEED_ALL: this is default. Seeds all the database tables
        ADMIN_ONLY: only seed the admin table
        ITEM_ONLY: Only seed the item table

        PRESERVE: Preserve the current values in the tables (Not available for admins table)
        JUST_DROP: Just drops all the tables without seeding data
"""

class SeederFlags(Flag):
    SEED_ALL = auto() # not ever required, added for clarity
    ADMIN_ONLY = auto()
    ITEM_ONLY = auto()
    PRESERVE = auto()
    JUST_DROP = auto()

class Seeder():
    def __init__(self, flags=None, file=None):
        self.flags = flags
        self.file = file

    def seed(self):
        if not self.flags or SeederFlags.SEED_ALL in self.flags:
            if self.flags and SeederFlags.JUST_DROP in self.flags:
                self._drop()

            elif self.flags and SeederFlags.PRESERVE in self.flags:
                self._seed_item(preserve=True)

            else:
                self._seed_item()

            return

        if SeederFlags.ADMIN_ONLY in self.flags:
            if SeederFlags.JUST_DROP in self.flags:
                self._drop(item=False)
            else:
                self._seed_admin()

            return

        if SeederFlags.ITEM_ONLY in self.flags:
            if SeederFlags.JUST_DROP in self.flags:
                self._drop(admin=False)
            elif SeederFlags.PRESERVE in self.flags:
                self._seed_item(preserve=True)
            else:
                self._seed_item()

            return

        print("Unrecognised flags.")

    def _drop(self, admin=True, item=True):
        print("Dropping tables...")
        fails = []
        if admin:
            try:
                drop_table("admins")
                print("Dropped 'admins'.")
            except ValueError as e:
                print(e)
                print("Failed to drop 'admins'. Skipping...")
                fails.append('admins')

        if item:
            try:
                drop_table("items")
                print("Dropped 'items'.")
            except ValueError as e:
                print(e)
                print("Failed to drop 'items'. Skipping...")
                fails.append('items')

        return fails

    def _create(self, admin=True, item=True):
        print("Creating tables...")
        fails = []
        if admin:
            try:
                create_table("admins")
                print("Created 'admins'.")
            except ValueError as e:
                print(e)
                print("Failed to create 'admins'. Skipping...")
                fails.append('admins')

        if item:
            try:
                create_table("items")
                print("Created 'items'.")
            except ValueError as e:
                print(e)
                print("Failed to create 'items'. Skipping...")
                fails.append('items')

        return fails

    def _seed_admin(self):
        print("==== Warning ====")
        print("This will remove ALL current admins, and seed a default master admin that should be replaced with the 'create-admin' command ASAP")
        print("This should only be used on initial creation of the database, or as a LAST RESORT.")
        print("=================")
        print("Are you certain you understand what this means and would like to proceed (case sensitive). [YES/n]")
        if input() != "YES":
            print("Aborting...")
            return

        if 'admins' in self._drop(item=False):
            print("Failed to seed 'admins'. Skipping...")
            return 
        if 'admins' in self._create(item=False):
            print("Failed to seed 'admins'. Skipping...")
            return

        password = random_secure_string()

        try:
            create_admin(username="MASTER", password=password)
            print("MASTER admin created")
            print()
        except ValueError as e:
            print(e)
            print("Failed to seed 'admins'. Skipping...")
            return

        print("==== MASTER Admin ====")
        print("Please use the 'create-admin' command ASAP as this admin is NOT for long-term use.")
        print("Username: MASTER")
        print(f"Password: {password}")
        print("======================")
        

    def _seed_item(self, preserve=False):
        if self.file is None:
            print("'items' needs a source file to seed from. No default provided.")
            return

        print("Not Implemented.")


# ==== Command ====

@app.cli.command("seed")
@app.option('--flags', multiple=True, callback=flagify_from_cli, type=click.Choice(SeederFlags, case_sensitive=False))
@app.option('--file')
def seed(flags, file):
    seeder = Seeder(flags, file)

    try: 
        if admins_exist(): # If non default admins exist, user must login to seed
            cli_tools_admin_login_required(seeder.seed())
        else:
            seeder.seed()

    except ValueError as e:
        print(e)
        print("Failed to being seeding. Aborting...")
        
