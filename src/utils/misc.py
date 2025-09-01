import os, glob
from flask import current_app

def flagify_from_cli(ctx, param, value):
    return flagify(value)

def flagify(flag_list):
    if flag_list is None:
        return flag_list

    flags = flag_list[0];

    for flag in flag_list[1:]:
        flags = flags | flag

    return flags


def remove_current_images():
    IMG_DIR = current_app.config.get('IMAGE_FOLDER')
    EXT = "*.jpeg"
    files = glob.glob(os.path.join(IMG_DIR, EXT))

    for file in files:
        try:
            os.remove(file)
        except OSError as e:
            print(e)
            continue

