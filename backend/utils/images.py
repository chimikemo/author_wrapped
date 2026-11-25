from wand.image import Image
import os
from PIL import Image as ImagePIL
import numpy as np
from blend_modes import soft_light, lighten_only, addition, dodge, subtract, divide
import random
import glob
from backend.utils.json_utils import json_mapping
from collections import Counter
from pathlib import Path

def make_image_square(images):
    for image in images:
        try:
            with Image(filename=image) as img:
                width = img.width
                height = img.height
                margin_x, margin_y = 0, 0
                if width < height:
                    max_val = width
                    margin_y = int((height - width) / 2)
                else:
                    max_val = height
                    margin_x = int((width - height) / 2)
                img.crop(top=margin_y, left=margin_x, height=max_val, width=max_val)
                img.save(filename=image)
        except:
            print(f"failed on {image}")


def delete_small_images(images, size):
    for image in images:
        with Image(filename=image) as img:
            w = img.width
            h = img.height
            if h < size or w < size:
                os.remove(image)


def make_collage(images, size, save_as, gradient_bg):
    with Image() as img:
        for i in images:
            with Image(filename=i) as item:
                img.image_add(item)
        img.montage(tile='3x3', thumbnail=f'{size}x{size}+0+0')
        img.border('white', 2, 2)
        img.save(filename=save_as)
    apply_blend_mode(save_as, gradient_bg, save_as, "addition", 0.3)


def apply_blend_mode(bg_img, fg_image, out_file, blending_mode, opacity):
    background_img_raw = ImagePIL.open(bg_img).convert('RGBA')
    foreground_img_raw = ImagePIL.open(fg_image).convert('RGBA')

    background_img = np.array(background_img_raw).astype(float)
    foreground_img = np.array(foreground_img_raw).astype(float)

    if background_img.shape != foreground_img.shape:
        print("Error: Background and foreground images must be the same size.")
    else:
        if blending_mode == "addition":
            blended_img_float = addition(background_img, foreground_img, opacity)
        elif blending_mode == "soft_light":
            blended_img_float = soft_light(background_img, foreground_img, opacity)
        elif blending_mode == "lighten_only":
            blended_img_float = lighten_only(background_img, foreground_img, opacity)
        elif blending_mode == "dodge":
            blended_img_float = dodge(background_img, foreground_img, opacity)
        elif blending_mode == "subtract":
            blended_img_float = subtract(background_img, foreground_img, opacity)
        elif blending_mode == "divide":
            blended_img_float = divide(background_img, foreground_img, opacity)
        else:
            blended_img_float = addition(background_img, foreground_img, opacity)
        blended_img_uint8 = blended_img_float.astype(np.uint8)
        blended_img_raw = ImagePIL.fromarray(blended_img_uint8, 'RGBA')
        blended_img_raw.save(out_file)


def create_collage_for_author(list_of_works, json_tags, size, out_file, gradient_bg):
    print("### CREATING COLLAGE ###")

    filler_images = ['college', 'creative', 'fluff', 'slowburn', 'foreplay', 'hope', 'longing', 'romance']

    used_tags = []
    char_tags = []
    for work in list_of_works:
        used_tags.extend(work.tags)
        char_tags.extend(work.characters)

    tags = json_mapping(json_tags, used_tags)
    # sample = random.sample(tags, 9)

    char_counter = Counter(char_tags)

    try:
        top2_char = [i[0] for i in char_counter.most_common(2)]
    except:
        try:
            top2_char = [i[0] for i in char_counter.most_common(1)]
        except:
            top2_char = False

    top_tags = []

    t_count = Counter(tags)
    if top2_char:
        if len(top2_char) > 0 and Path(f"characters/{top2_char[0]}").is_dir():
            top_tags.append(f"characters/{top2_char[0]}")
            top_tags = [i[0] for i in t_count.most_common(8)]

        elif len(top2_char) > 1 and Path(f"characters/{top2_char[1]}").is_dir():
            top_tags.append(f"characters/{top2_char[1]}")
            top_tags = [i[0] for i in t_count.most_common(8)]
        else:
            top_tags = [i[0] for i in t_count.most_common(9)]
    else:
        top_tags = [i[0] for i in t_count.most_common(9)]


    while len(top_tags) < 9:
        top_tags.append(random.choice(filler_images))

    chosen_images = []
    random.shuffle(top_tags)

    for s in top_tags:
        possible_images = glob.glob(f"backend/images/tags/{s}/*.jpg")
        chosen_images.extend(random.sample(possible_images, k=min(len(possible_images), 1)))
    make_collage(chosen_images, size, out_file, gradient_bg)
