import os

_ICON_FOLDER = 'icons'


def get_icon_path(icon_name):
    return os.path.join('src', 'image_converter', 'resources', _ICON_FOLDER, icon_name)
