import sys
import os
import os.path
import markdown
import re

__author__ = 'jhorneman'

SCRIPT_DIR = os.path.abspath(os.path.dirname(sys.argv[0])) + os.sep

scenes = {}
scene_files = []

class Scene(object):
    def __init__(self):
        self.description = ""
        self.options = []
        self.image_path = None

    @staticmethod
    def from_text_file(_file):
        new_scene = Scene()

        d = _file.read()
        d = d.strip()

        # Find the start of the options and parse them
        if '------' in d:
            text, options_string = d.split('------')
            for option_string in options_string.split('['):
                option_string = option_string.strip()
                if option_string:
                    #TODO: Add error check
                    next_scene_name, option_text = option_string.split(']')
                    new_scene.options.append((next_scene_name, option_text))
        else:
            text = d

        # Convert the text from Markdown to HTML
        new_scene.description = markdown.markdown(text)

        return new_scene


def load_data():
    load_scene_descriptions()
    return (len(scenes) > 0)


def load_scene_descriptions():
    # Iterate over all files in the scenes directory
    for path, dirs, files in os.walk(os.path.join(SCRIPT_DIR, "scenes")):
        for filename in files:
            # Skip hidden files and anything not ending in .txt
            if filename.startswith("."):
                continue
            if not filename.endswith(".txt"):
                continue

            full_path = os.path.join(path, filename)
            scene_name = os.path.splitext(filename)[0]

            # Open the scene file
            with open(full_path, "r") as f:
                # Build the scene and store it
                scenes[scene_name] = Scene.from_text_file(f)
                scene_files.append(full_path)


def load_scene_images():
    pass
