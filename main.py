#!/usr/bin/env python3

# import argparse
import git
import json
import os
import random
from decouple import config
from functools import cache
from icecream import ic
from pathlib import Path
from PIL import Image
from traits import *

# env
cwd = Path.cwd()
env = Path('.env')

# pinata.cloud information (hard-coded)
IMAGES_BASE_URL = ""
PROJECT_NAME = ""

if env.exists():
    IMAGES_BASE_URL = config("IMAGES_BASE_URL")
    PROJECT_NAME = config("PROJECT_NAME")
else:
    IMAGES_BASE_URL = os.environ.get("IMAGES_BASE_URL")
    PROJECT_NAME = os.getenv("PROJECT_NAME")

# Validate pinata env variables
if IMAGES_BASE_URL == "" or PROJECT_NAME == "":
    print("Please enter the base url for your images and the name of your project")
    IMAGES_BASE_URL = input("IMAGES_BASE_URL: ")
    PROJECT_NAME = input("PROJECT_NAME: ")

# generate images directory
Path(cwd/'images').mkdir(parents=True, exist_ok=True)
# use pathlib to glob the substrapunks directory in working directory
# face_parts = Path('substrapunks/scripts/face_parts')

# clone substrapunks repo
if not Path(cwd/'substrapunks').exists():
    print("Cloning substrapunks repo...")
    git.Repo.clone_from('https://github.com/UniqueNetwork/substrapunks.git', cwd/'substrapunks')
else:
    print("Pulling latest changes from substrapunks repo")
    git.Repo(cwd/'substrapunks').git.pull()

# face directory
for p in cwd.rglob('**/substra*/scripts/*'):
    if p.is_dir() and p.name == 'face_parts':
        print(f"found {p}")
        face_parts = p
        break

TOTAL_IMAGES = 100 # Number of random unique images we want to generate
all_images = []


# TODO: `RecursionError: maximum recursion depth exceeded`
def rando_image():
    """ A recursive function to generate unique image combinations """
    new_image = {}

    # For each trait category, select a random trait based on the weightings
    new_image ["Face"] = random.choices(face, face_weights)[0]
    new_image ["Ears"] = random.choices(ears, ears_weights)[0]
    new_image ["Eyes"] = random.choices(eyes, eyes_weights)[0]
    new_image ["Hair"] = random.choices(hair, hair_weights)[0]
    new_image ["Mouth"] = random.choices(mouth, mouth_weights)[0]
    new_image ["Nose"] = random.choices(nose, nose_weights)[0]

    if new_image in all_images:
        return rando_image()
    else:
        return new_image


# Returns true if all images are unique
def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)


def trait_counts():
    # TODO: golf redundant for loops
    """ Get Trait Counts """
    face_count = {}
    for item in face:
        face_count[item] = 0

    ears_count = {}
    for item in ears:
        ears_count[item] = 0

    eyes_count = {}
    for item in eyes:
        eyes_count[item] = 0

    hair_count = {}
    for item in hair:
        hair_count[item] = 0

    mouth_count = {}
    for item in mouth:
        mouth_count[item] = 0

    nose_count = {}
    for item in nose:
        nose_count[item] = 0

    for image in all_images:
        face_count[image["Face"]] += 1
        ears_count[image["Ears"]] += 1
        eyes_count[image["Eyes"]] += 1
        hair_count[image["Hair"]] += 1
        mouth_count[image["Mouth"]] += 1
        nose_count[image["Nose"]] += 1

    print(f"{face_count}\n{ears_count}\n{eyes_count}\n{hair_count}\n{mouth_count}\n{nose_count}")
    return face_count, ears_count, eyes_count, hair_count, mouth_count, nose_count


def gen_image():
    """ Creates composites for each trait """
    # TODO: traverse iteritems by directory
    for item in all_images:
        im1 = Image.open(f'{face_parts}/face/{face_files[item["Face"]]}.png').convert('RGBA')
        im2 = Image.open(f'{face_parts}/eyes/{eyes_files[item["Eyes"]]}.png').convert('RGBA')
        im3 = Image.open(f'{face_parts}/ears/{ears_files[item["Ears"]]}.png').convert('RGBA')
        im4 = Image.open(f'{face_parts}/hair/{hair_files[item["Hair"]]}.png').convert('RGBA')
        im5 = Image.open(f'{face_parts}/mouth/{mouth_files[item["Mouth"]]}.png').convert('RGBA')
        im6 = Image.open(f'{face_parts}/nose/{nose_files[item["Nose"]]}.png').convert('RGBA')

        # Create each composite
        com1 = Image.alpha_composite(im1, im2)
        com2 = Image.alpha_composite(com1, im3)
        com3 = Image.alpha_composite(com2, im4)
        com4 = Image.alpha_composite(com3, im5)
        com5 = Image.alpha_composite(com4, im6)

        # Convert to RGB
        rgb_im = com5.convert('RGB')
        file_name = str(item["tokenId"]) + ".png"
        rgb_im.save(f"images/{file_name}")


def getAttribute(key, value):
    return {
        "trait_type": key,
        "value": value
    }

def create_new_image():
    """ Create a new image """
    rando_image()

    """
    TODO: `RecursionError: maximum recursion depth exceeded`; was working under `main` and global definitions
    File "/Users/lance/git/nft_meetup/main.py", line 190, in main
    create_new_image()
    File "/Users/lance/git/nft_meetup/main.py", line 159, in create_new_image
        new_trait_image = create_new_image()
    File "/Users/lance/git/nft_meetup/main.py", line 159, in create_new_image
        new_trait_image = create_new_image()
    File "/Users/lance/git/nft_meetup/main.py", line 159, in create_new_image
        new_trait_image = create_new_image()
    [Previous line repeated 979 more times]
    """
    # Generate the unique combinations based on trait weightings
    for i in range(TOTAL_IMAGES):
        new_trait_image = create_new_image()
        all_images.append(new_trait_image)
    all_images_unique(all_images)
    print("Are all images unique?", all_images_unique(all_images))

    # Add token ID to each image
    i = 0
    for item in all_images:
        item["tokenId"] = i
        i += 1
    print(all_images)

    trait_counts()
    gen_image()


def main():
    """
    Pt 1: Generate NFT images
    """
    # check if images directory is empty, if not, user input to continue
    count_files = sum(1 for x in Path(cwd/'images').glob('*') if x.is_file())
    if count_files > 0:
        print("Images directory is not empty, overwrite? (y/n)")
        if input() == 'y':
            print("Continuing...")
            create_new_image()
        else:
            print("Using previous images...")
    else:
        print("Images directory is empty, continuing...")
        create_new_image()


    """
    Pt II: Generate NFT metadata
    """
    # Export to json
    meta_file = f"{cwd}/metadata/metadata.json"
    try:
        Path(meta_file).parents[0].mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        pass

    # Check if file exists or is empty then write
    if not Path(meta_file).exists() or Path(meta_file).stat().st_size > 0:
        Path(meta_file).write_text(json.dumps(all_images, indent=4))
    elif Path(meta_file).exists():
        print(f"{meta_file} already exists. Overwrite? (y/n)")
        if input() == 'y':
            Path(meta_file).write_text(json.dumps(all_images, indent=4))

    """
    Generate metadata for each image
    """
    # clean up json file with nested dicts
    json_list = []
    with open(meta_file, "a+") as fn:
        for _ in fn:
            data = json.loads(_)
            json_list.append(data)

    # TODO: debug empty json_list
    # Generate metadata for each image
    for i in json_list:
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

        with open(f"{cwd}/metadata/" + str(token_id) + ".json", 'w') as outfile:
            json.dump(token, outfile, indent=4)


if __name__ == "__main__":
    main()
