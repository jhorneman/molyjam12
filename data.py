import sys
import os
import os.path
import markdown
import re

__author__ = 'jhorneman'

SCRIPT_DIR = os.path.abspath(os.path.dirname(sys.argv[0])) + os.sep

scenes = {}
scene_files = []

def load_data():
    for path, dirs, files in os.walk(os.path.join(SCRIPT_DIR, "scenes")):
        for filename in files:
            if filename.startswith("."):
                continue
            full_path = os.path.join(path, filename)
            scene_name = os.path.splitext(filename)[0]
            with open(full_path, "r") as f:
                d = f.read()
                d = d.strip()
                if '------' in d:
                    text, option_string = d.split('------')
                    options = parse_options(option_string)
                else:
                    text = d
                    options = []
                html = markdown.markdown(text)
                scenes[scene_name] = (html, options)
                scene_files.append(full_path)

def parse_options(_option_string):
    options = []
    for option in re.findall(r'\[(.*)\](.*)', _option_string, re.MULTILINE):
        options.append(option)
    return options
