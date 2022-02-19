#!/usr/bin/env python3

import json
from main import all_images
from pathlib import Path

# SOURCE: https://gist.github.com/BgtEwoud/88eb1dcc18f54f5c0f6f6b1657911c3d#file-metadata_all-py

# TODO: move to main.py in dev branch
"""
Generate metadata for all images (Script 1/2)

Use this script before metadata.py to generate metadata for all images
"""
Path("metadata").mkdir(parents=True, exist_ok=True)

METADATA_FILE_NAME = './metadata/all-traits.json'

with open(METADATA_FILE_NAME, 'w') as outfile:
    json.dump(all_images, outfile, indent=4)
