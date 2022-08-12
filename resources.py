import sys
import os
import json


# For packaging relevant data files with program. Borrowed with much gratitude from Stackoverflow:
# https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile)
def resource_path(relative_path):
    """ Get the absolute path to the resource.
    """
    try:
        # Pyinstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Opens languages.json and makes its contents accessible as a dictionary, and the keys to that dictionary accessible
# as a list
with open(resource_path("languages.json"), "r") as file:
    contents = json.load(file)
    languages = list(contents.keys())
