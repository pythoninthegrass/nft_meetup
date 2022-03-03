#!/usr/bin/env python3

import git
import random
from pathlib import Path
from PIL import Image
from traits import *

# env
cwd = Path.cwd()

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

# TODO: fix image listing check
# check if images directory is empty, if not, user input to continue
if len(list(cwd.rglob('**/images/*'))) > 0:
    print("Images directory is not empty, overwrite? (y/n)")
    if input() == 'y':
        print("Continuing...")
    else:
        print("Exiting...")
        exit()

"""
Generate Traits
"""
TOTAL_IMAGES = 100 # Number of random unique images we want to generate

all_images = []

# A recursive function to generate unique image combinations
def create_new_image():
    new_image = {}

    # For each trait category, select a random trait based on the weightings
    new_image ["Face"] = random.choices(face, face_weights)[0]
    new_image ["Ears"] = random.choices(ears, ears_weights)[0]
    new_image ["Eyes"] = random.choices(eyes, eyes_weights)[0]
    new_image ["Hair"] = random.choices(hair, hair_weights)[0]
    new_image ["Mouth"] = random.choices(mouth, mouth_weights)[0]
    new_image ["Nose"] = random.choices(nose, nose_weights)[0]

    if new_image in all_images:
        return create_new_image()
    else:
        return new_image


# Generate the unique combinations based on trait weightings
for i in range(TOTAL_IMAGES):
    new_trait_image = create_new_image()
    all_images.append(new_trait_image)


# Returns true if all images are unique
def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)
print("Are all images unique?", all_images_unique(all_images))

# Add token ID to each image
i = 0
for item in all_images:
    item["tokenId"] = i
    i += 1
print(all_images)

# TODO: golf redundant for loops
"""
Get Trait Counts
"""
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
    rgb_im.save("images/" + file_name)
