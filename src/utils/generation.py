import random, string, os

from werkzeug.utils import secure_filename
from PIL import Image

from ..app import app

def random_secure_string(length=8):
    return ''.join(random.SystemRandom().choices(
                    string.ascii_letters + 
                    string.digits +
                    string.punctuation, k=length))

"""
    Takes an img path relative to the home directory (~)
    validates, copies and compresses the image into a useable directory
    and returns that path
"""
ALLOWED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png']
def generate_safe_image(img):
    if not img or img.split(".") < 2 or img.split(".")[1] not in ALLOWED_IMAGE_FORMATS:
        raise ValueError(f"Image {img} is either not a valid image file or not an allowed type")

    filename = f"{int(datetime.datetime.utcnow().timestamp())}_{os.path.splitext(secure_filename(img))}.jpeg"
    path = os.path.join(app.config['IMAGE_FOLDER'], filename)

    try:
        with Image.open(os.path.expanduser(img)) as i:
            i.save(path, format="JPEG")
    finally:
        os.remove(os.path.expanduser(img))

    return path




