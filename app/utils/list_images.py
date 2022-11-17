import os

from config import Configuration

conf = Configuration()


def list_images():
    """Returns the list of available images."""
    img_names = filter(lambda x: not x.endswith('.json'),
                       os.listdir(conf.image_folder_path))
    return list(img_names)
