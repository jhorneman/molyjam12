import sys
import os
import os.path
import markdown
import logging
import re

__author__ = 'jhorneman'

SCRIPT_DIR = os.path.abspath(os.path.dirname(sys.argv[0])) + os.sep

scene_options_marker = "=== SCENE OPTIONS ==="

scenes = {}
scene_files = []
warnings = []


class Option(object):
    def __init__(self):
        self.next_scene_name = ""
        self.text = ""
        self.sparkle_bonus = 0
        self.min_sparkle = 0


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
        new_option = None
        if scene_options_marker in d:
            description, options = d.split(scene_options_marker)
            for line in options.splitlines():
                line = line.strip()
                if len(line):
                    r = re.match(r"\[(.*)\]", line)
                    if r:
                        if new_option:
                            new_scene.options.append(new_option)
                        new_option = Option()
                        new_option.next_scene_name = r.group(1)
                    else:
                        r =re.match(r"(.*)=(.*)", line)
                        if r:
                            parameter_name = r.group(1).rstrip()
                            parameter_value = r.group(2).lstrip()
                            if new_option.__dict__.has_key(parameter_name):
                                if type(new_option.__dict__[parameter_name]) == type(1):
                                    new_option.__dict__[parameter_name] = int(parameter_value)
                                else:
                                    new_option.__dict__[parameter_name] = str(parameter_value)
                            else:
                                warning = "Unknown parameter '%s' in scene '%s'" % (parameter_name, _scene_name)
                                warnings.append(warning)
                                _main_logger.log(logging.WARNING, warning)
                        else:
                            warning = "Could not parse option '%s' of scene '%s'" % (line, _scene_name)
                            warnings.append(warning)
                            _main_logger.log(logging.WARNING, warning)
        else:
            warning = "Could not find options in scene '%s'" % _scene_name
            warnings.append(warning)
            _main_logger.log(logging.WARNING, warning)
            description = d
        if new_option:
            new_scene.options.append(new_option)

        # Convert the text from Markdown to HTML
        new_scene.description = markdown.markdown(description)

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
