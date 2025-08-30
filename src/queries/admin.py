from ..models.Admin import Admin
from ..app import get_session
from ..utils.validation import inputs_exist

from sqlalchemy import select

from werkzeug.security import generate_password_hash, check_password_hash

"""
    
    All functions can throw ValueError!

    **Even if they do not now, I make no guarentee they won't in the future without warning.

"""

def get_admin(username: str):
    inputs_exist(username)
    with get_session().begin() as s:
        stmt = select(Admin).filter_by(username=username)
        admin = s.scalar(stmt)

    return admin

def admins_exist(include_default=False):
    # include_default -> return True even if the only admin is the default MASTER 
    with get_session().begin() as s:
        stmt = select(Admin)
        admins = s.scalars(stmt).all()

    if len(admins) <= 0:
        return False

    if not include_default and admins[0].username == "MASTER":
        return False

    return True

    

def create_admin(username: str, password: str):
    inputs_exist(username, password)
    if get_admin(username):
        raise ValueError("Admin with username already exists")

    with get_session().begin() as s:
        a = Admin(username=username, password_hash=generate_password_hash(password))
        s.add(a)

    # Ensure 'Master' admin is removed
    if username != "MASTER":
        try:
            remove_admin("MASTER")
        except ValueError:
            pass

def remove_admin(username: str):
    inputs_exist(username)
    admin = get_admin(username)
    if not admin:
        raise ValueError("No such admin")

    with get_session().begin() as s:
        s.delete(admin)


def check_admin_credentials(username: str, password: str):
    inputs_exist(username, password)
    admin = get_admin(username)
    return bool(admin and check_password_hash(admin.password_hash, password))


