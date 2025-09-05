import random, string, os, datetime
from flask import current_app

from werkzeug.utils import secure_filename
import PIL
from PIL import Image

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
ALLOWED_IMAGE_FORMATS = ['jpg', 'jpeg', 'png']
def generate_safe_image(img, remove=False):
    print(img)
    if not img or len(img.split(".")) < 2 or img.split(".")[-1] not in ALLOWED_IMAGE_FORMATS:
        raise ValueError(f"Image {img} is either not a valid image file or not an allowed type")

    filename = f"{int(datetime.datetime.utcnow().timestamp())}_{os.path.splitext(secure_filename(img))[0]}.jpeg"
    path = os.path.join(current_app.config.get('IMAGE_FOLDER'), filename)

    try:
        with Image.open(img) as i:
            if i.mode == "RGBA":
                background = Image.new('RGB', i.size, (255, 255, 255))
                background.paste(i, mask=i.split()[-1])
                i = background
            i.save(path, format="JPEG")
    except (FileNotFoundError, PIL.UnidentifiedImageError) as e:
        print(f'[ERROR]: Failed to open image {img} with error: {e}')
        raise ValueError(f"failed to open {img}")

    finally:
        if remove:
            os.remove(os.path.expanduser(img))

    return filename 




