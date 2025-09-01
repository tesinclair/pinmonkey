from ..utils.generation import random_secure_string, generate_safe_image
from ..utils.misc import flagify_from_cli, remove_current_images
from ..utils.verification import cli_tools_admin_login_required
from ..queries.admin import create_admin, admins_exist
from ..queries.seeding import drop_table, create_table
from ..queries.item import get_items, create_item
from flask.cli import with_appcontext
from flask import current_app

from enum import Flag, auto
import click, json, os
"""
    Flag summary:
        SEED_ALL: Required if using other flags (e.g. PRESERVE) but want all tables seeded
        ADMIN_ONLY: only seed the admin table
        ITEM_ONLY: Only seed the item table

        PRESERVE: Preserve the current values in the tables (Not available for admins table)
        JUST_DROP: Just drops all the tables without seeding data

    Image Seed data:
        Should be a json file relative path from the home directory (~)

        in the form:

            { 
             1: {
                 "img": location of image from home directory (~)
                 "title": title: Str (max 32 characters),
                 "price": price: float
                 },
             2: ...
            }
"""

class SeederFlags(Flag):
    SEED_ALL = auto() # only required if other flags are used
    ADMIN_ONLY = auto()
    ITEM_ONLY = auto()
    PRESERVE = auto()
    JUST_DROP = auto()
    REMOVE_SRC_IMAGES = auto()

class Seeder():
    def __init__(self, flags=None, file=None):
        self.flags = flags
        self.file = os.path.expanduser(file)

    def seed(self):
        if not self.flags or SeederFlags.SEED_ALL in self.flags:
            if self.flags and SeederFlags.JUST_DROP in self.flags:
                self._drop('admins', 'items')

            elif self.flags and SeederFlags.PRESERVE in self.flags:
                print("==== Seeding 'items' ====")
                self._seed_item(preserve=True)
                print("==== Seeding 'admin' ====")
                self._seed_admin()

            else:
                print("==== Seeding 'items' ====")
                self._seed_item()
                print("==== Seeding 'admins' ====")
                self._seed_admin()

            return

        if SeederFlags.ADMIN_ONLY in self.flags:
            if SeederFlags.JUST_DROP in self.flags:
                self._drop('admins')
            else:
                self._seed_admin()

            return

        if SeederFlags.ITEM_ONLY in self.flags:
            if SeederFlags.JUST_DROP in self.flags:
                self._drop('items')
            elif SeederFlags.PRESERVE in self.flags:
                self._seed_item(preserve=True)
            else:
                self._seed_item()

            return

        print("Unrecognised flags.")

    def _drop(self, *args):
        print(f"Dropping tables {args}")
        fails = []
        for tablename in args:
            try:
                drop_table(current_app.config.get('DB_ENGINE'), tablename)
                print(f"Dropped '{tablename}'.")
            except ValueError as e:
                print(e)
                print(f"Failed to drop '{tablename}'. Skipping...")
                fails.append(tablename)

        return fails

    def _create(self, *args):
        print("Creating tables {args}")
        fails = []
        for tablename in args:
            try:
                create_table(current_app.config.get('DB_ENGINE'), tablename)
                print(f"Created '{tablename}'.")
            except ValueError as e:
                print(e)
                print(f"Failed to create '{tablename}'. Skipping...")
                fails.append(tablename)

        return fails

    def _seed_admin(self):
        print("==== Warning ====")
        print("This will remove ALL current admins, and seed a default master admin that should be replaced with the 'create-admin' command ASAP")
        print("This should only be used on initial creation of the database, or as a LAST RESORT.")
        print("=================")
        print("Are you certain you understand what this means and would like to proceed (case sensitive). [YES/n]")
        print()
        if input() != "YES":
            print("Aborting...")
            return

        if 'admins' in self._drop('admins'):
            print("Failed to seed 'admins'. Skipping...")
            return 
        if 'admins' in self._create('admins'):
            print("Failed to seed 'admins'. Skipping...")
            return

        password = random_secure_string()

        try:
            create_admin(current_app.config.get('DB_SESSION'), username="MASTER", password=password)
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
        print("Attempting to seed 'itmes'")
        if self.file is None:
            print("'items' needs a source file to seed from. No default provided.")
            return

        if not preserve:
            if 'items' in self._drop('items'):
                print("Failed to seed 'items'. Skipping...")
                return
            remove_current_images()
            if 'items' in self._create('items'):
                print("Failed to seed 'items'. Skipping...")
                return

        with open(self.file, "rb") as f:
            seed_data = json.loads(f.read())

        current_items = [x.title for x in get_items(current_app.config.get('DB_SESSION'))]

        for item in seed_data.values():
            if item['title'] in current_items:
                continue

            try:
                if SeederFlags.REMOVE_SRC_IMAGES in self.flags:
                    img_filename = generate_safe_image(item['img'], remove=True)
                else:
                    img_filename = generate_safe_image(item['img'])
                create_item(current_app.config.get('DB_SESSION'), item['title'], img_filename, item['price'])
            except ValueError as e:
                print(e)
                print("Failed to seed 'items'")
                return

        
# ==== Command ====

@click.command("seed")
@click.option('--flags', multiple=True, callback=flagify_from_cli, type=click.Choice(SeederFlags, case_sensitive=False))
@click.option('--file')
@with_appcontext
def cli_tools_seed(flags, file):
    seeder = Seeder(flags, file)

    try: 
        if admins_exist(current_app.config.get('DB_SESSION')): # If non default admins exist, user must login to seed
            cli_tools_admin_login_required(seeder.seed())
        else:
            seeder.seed()

    except ValueError as e:
        print(e)
        print("Failed to begin seeding. Aborting...")
        
