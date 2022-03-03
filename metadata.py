#!/usr/bin/env python3

from email.policy import default
import json
import os
from decouple import config
from pathlib import Path

# SOURCE: https://gist.github.com/BgtEwoud/ec4dd21f6c82ca4bcd2c92af5d5d0ac9#file-metadata-py

# TODO: move to main.py in dev branch
"""
Generate metadata for each image (Script 2/2)

Use this script after metadata_all.py to generate metadata for each image
"""
f = open('./metadata/all-traits.json',)
data = json.load(f)

env = Path('.env')

# Changes this IMAGES_BASE_URL to yours
if env.exists():
    IMAGES_BASE_URL = config('IMAGES_BASE_URL', default="https://gateway.pinata.cloud/ipfs/<your-ipfs-hash>")
    PROJECT_NAME = config('PROJECT_NAME', default="<your-project-name>")
else:
    HOST = os.getenv('IMAGES_BASE_URL')
    PROJECT_NAME = os.getenv('PROJECT_NAME')


def getAttribute(key, value):
    return {
        "trait_type": key,
        "value": value
    }
for i in data:
    token_id = i['tokenId']
    token = {
        "image": IMAGES_BASE_URL + str(token_id) + '.png',
        "tokenId": token_id,
        "name": PROJECT_NAME + ' ' + str(token_id),
        "attributes": []
    }
    token["attributes"].append(getAttribute("Face", i["Face"]))
    token["attributes"].append(getAttribute("Ears", i["Ears"]))
    token["attributes"].append(getAttribute("Eyes", i["Eyes"]))
    token["attributes"].append(getAttribute("Hair", i["Hair"]))
    token["attributes"].append(getAttribute("Mouth", i["Mouth"]))
    token["attributes"].append(getAttribute("Nose", i["Nose"]))

    with open('./metadata/' + str(token_id) + ".json", 'w') as outfile:
        json.dump(token, outfile, indent=4)

f.close()
