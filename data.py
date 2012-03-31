import sys
import os
import os.path
import markdown
import logging

__author__ = 'jhorneman'

SCRIPT_DIR = os.path.abspath(os.path.dirname(sys.argv[0])) + os.sep

scenes = {}
scene_files = []
warnings = []


class Scene(object):
    def __init__(self):
        self.description = ""
        self.options = []
        self.image_path = None

    @staticmethod
    def from_text_file(_file, _scene_name, _main_logger):
        new_scene = Scene()

        d = _file.read()
        d = d.strip()

        # Find the start of the options and parse them
        if '------' in d:
            text, options_string = d.split('------')
            for option_string in options_string.split('['):
                option_string = option_string.strip()
                if option_string:
                    try:
                        next_scene_name, option_text = option_string.split(']')
                    except ValueError:
                        warning = "Could not read option '%s' of scene '%s'" % (option_string, _scene_name)
                        warnings.append(warning)
                        _main_logger.log(logging.WARNING, warning)
                    else:
                        new_scene.options.append((next_scene_name, option_text))
        else:
            warning = "Could not find options in scene '%s'" % (_scene_name)
            warnings.append(warning)
            _main_logger.log(logging.WARNING, warning)
            text = d

        # Convert the text from Markdown to HTML
        new_scene.description = markdown.markdown(text)

        return new_scene


def load_data(_main_logger):
    load_scene_descriptions(_main_logger)

    if len(scenes):
        _main_logger.log(logging.DEBUG, "Successfully loaded data")
        return True
    else:
        _main_logger.log(logging.CRITICAL, "Could not load data - aborting")
        return False


def load_scene_descriptions(_main_logger):
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
                scenes[scene_name] = Scene.from_text_file(f, scene_name, _main_logger)
                scene_files.append(full_path)


def load_scene_images():
    pass
