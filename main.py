#!/usr/bin/env python3

import random
from pathlib import Path
from PIL import Image

# TODO: use requests to clone substra repo and unzip with os(?)

# env
cwd = Path.cwd()

# generate images directory
Path(cwd/'images').mkdir(parents=True, exist_ok=True)
# use pathlib to glob the substrapunks directory in working directory
# face_parts = Path('substrapunks/scripts/face_parts')

# face directory
for p in cwd.rglob('**/substra*/scripts/*'):
    if p.is_dir() and p.name == 'face_parts':
        print(f"found {p}")
        face_parts = p
        break

# TODO: split up traits into separate files, then import
"""
Each image is made up a series of traits
The weightings for each trait drive the rarity and add up to 100%
"""
face = ["White", "Black"]
face_weights = [60, 40]

ears = ["No Earring", "Left Earring", "Right Earring", "Two Earrings"]
ears_weights = [25, 30, 44, 1]

eyes = ["Regular", "Small", "Rayban", "Hipster", "Focused"]
eyes_weights = [70, 10, 5 , 1 , 14]

hair = [
    'Up Hair',
    'Down Hair',
    'Mohawk',
    'Red Mohawk',
    'Orange Hair',
    'Bubble Hair',
    'Emo Hair',
    'Thin Hair',
    'Bald',
    'Blonde Hair',
    'Caret Hair',
    'Pony Tails'
]
hair_weights = [10 , 10 , 10 , 10 ,10, 10, 10 ,10 ,10, 7 , 1 , 2]

mouth = ['Black Lipstick', 'Red Lipstick', 'Big Smile', 'Smile', 'Teeth Smile', 'Purple Lipstick']
mouth_weights = [10, 10,50, 10,15, 5]

nose = ['Nose', 'Nose Ring']
nose_weights = [90, 10]


# TODO: separate file
"""
Classify traits
"""
face_files = {
    "White": "face1",
    "Black": "face2"
}

ears_files = {
    "No Earring": "ears1",
    "Left Earring": "ears2",
    "Right Earring": "ears3",
    "Two Earrings": "ears4"
}

eyes_files = {
    "Regular": "eyes1",
    "Small": "eyes2",
    "Rayban": "eyes3",
    "Hipster": "eyes4",
    "Focused": "eyes5"
}

hair_files = {
    "Up Hair": "hair1",
    "Down Hair": "hair2",
    "Mohawk": "hair3",
    "Red Mohawk": "hair4",
    "Orange Hair": "hair5",
    "Bubble Hair": "hair6",
    "Emo Hair": "hair7",
    "Thin Hair": "hair8",
    "Bald": "hair9",
    "Blonde Hair": "hair10",
    "Caret Hair": "hair11",
    "Pony Tails": "hair12"
}

mouth_files = {
    "Black Lipstick": "m1",
    "Red Lipstick": "m2",
    "Big Smile": "m3",
    "Smile": "m4",
    "Teeth Smile": "m5",
    "Purple Lipstick": "m6"
}

nose_files = {
    "Nose": "n1",
    "Nose Ring": "n2"
}


# TODO: separate file
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

# TODO: augmented operator `+=`
# Add token ID to each image
i = 0
for item in all_images:
    item["tokenId"] = i
    i = i + 1
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

# TODO: print f-string w/newline
print(face_count)
print(ears_count)
print(eyes_count)
print(hair_count)
print(mouth_count)
print(nose_count)


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

    # TODO: remove relative directory dot reference
    # Convert to RGB
    rgb_im = com5.convert('RGB')
    file_name = str(item["tokenId"]) + ".png"
    rgb_im.save("./images/" + file_name)
