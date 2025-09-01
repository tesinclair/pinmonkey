from ..models.Admin import Admin
from ..utils.validation import inputs_exist

from sqlalchemy import select

from werkzeug.security import generate_password_hash, check_password_hash

"""
    
    All functions can throw ValueError!

    **Even if they do not now, I make no guarentee they won't in the future without warning.

"""

def get_admin(session, username: str):
    inputs_exist(session, username)
    with session() as s:
        with s.begin():
            stmt = select(Admin).filter_by(username=username)
            admin = s.scalar(stmt)

    return admin

def admins_exist(session, include_default=False):
    # include_default -> return True even if the only admin is the default MASTER 
    inputs_exist(session)
    with session() as s:
        with s.begin():
            stmt = select(Admin)
            admins = s.scalars(stmt).all()

    if len(admins) <= 0:
        return False

    if not include_default and admins[0].username == "MASTER":
        return False

    return True

    

def create_admin(session, username: str, password: str):
    inputs_exist(session, username, password)
    if get_admin(username):
        raise ValueError("Admin with username already exists")

    with session() as s:
        with s.begin():
            a = Admin(username=username, password_hash=generate_password_hash(password))
            s.add(a)

    # Ensure 'Master' admin is removed
    if username != "MASTER":
        try:
            remove_admin("MASTER")
        except ValueError:
            pass

def remove_admin(session, username: str):
    inputs_exist(session, username)
    admin = get_admin(username)
    if not admin:
        raise ValueError("No such admin")

    with session() as s:
        with s.begin():
            s.delete(admin)


def check_admin_credentials(session, username: str, password: str):
    inputs_exist(session, username, password)
    admin = get_admin(session, username)
    return bool(admin and check_password_hash(admin.password_hash, password))


