import collections
import random
from PIL import Image, ImageDraw, ImageFont
from backend.utils.json_utils import json_mapping
import json
from backend.utils.images import apply_blend_mode
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def match_aura (mapped_tags, aura_names, non_smut_flag = False, random_flag = False):
    counter = collections.Counter(mapped_tags)
    top4 = counter.most_common(4)
    match1, match2 = "", ""
    if len(mapped_tags) == 1:
        match1 = aura_names[mapped_tags]
        match2 = random.choice(list(aura_names.keys()))
    elif len(mapped_tags) == 0:
        matches = random.sample(list(aura_names.keys()), 2)
        match2 = matches[0]
        match2 = matches[1]
    elif non_smut_flag:
        non_nsfw = [x for x in top4 if "smut" not in x[0] and "foreplay" not in x[0]]
        match1 = aura_names[non_nsfw[0][0]]
        match2 = aura_names[non_nsfw[1][0]]
    elif random_flag:
        tags_set = sorted(set(mapped_tags))
        match = random.sample(tags_set, 2)
        match1 = aura_names[match[0]]
        match2 = aura_names[match[1]]
    else:
        match1 = aura_names[top4[0][0]]
        match2 = aura_names[top4[1][0]]
    return random.choice(match1), random.choice(match2)

def create_aura_image_new(author_name, aura1, aura2, out_file, gradient_bg, geometric_bg):
    img = Image.new('RGB', (3076, 3076), "rgb(0,0,0)")
    side_image = Image.open(geometric_bg).convert("RGBA")
    side_image = side_image.crop((0,0,800, side_image.height))
    img.paste(side_image, (0, 0), side_image)
    I1 = ImageDraw.Draw(img)

    font_bold_path = os.path.join(
        BASE_DIR,
        "backend",
        "fonts",
        "consola_mono",
        "ConsolaMono-Bold.ttf"
    )
    font_thin_path = os.path.join(
        BASE_DIR,
        "backend",
        "fonts",
        "creato_display",
        "CreatoDisplay-Thin.otf"
    )

    font_bold = ImageFont.truetype(font_bold_path, 350)
    font_thin = ImageFont.truetype(font_thin_path, 250)

    white = (255, 255, 255)
    I1.text((600, 520), "your fic writer", font=font_thin, fill=white)
    I1.text((600, 770), "aura is", font=font_thin, fill=white)
    I1.text((600, 1330), f"{aura1}", font=font_bold, fill=white)
    I1.text((800, 1800), "&", font=font_thin, fill=white)
    I1.text((600, 2000), f"{aura2}", font=font_bold, fill=white)
    temp_img_file = f"backend/images/generated_images/temp_{author_name}_aura.png"
    img.save(temp_img_file)
    apply_blend_mode(temp_img_file, gradient_bg, out_file, "addition", 0.3)
    os.remove(temp_img_file)


def create_aura_image(author_name, aura1, aura2, out_file, gradient_bg):
    img = Image.new('RGB', (3076, 3076), "rgb(0,0,0)")
    I1 = ImageDraw.Draw(img)

    font_bold_path = os.path.join(
        BASE_DIR,
        "backend",
        "fonts",
        "creato_display",
        "CreatoDisplay-BlackItalic.otf"
    )
    font_thin_path = os.path.join(
        BASE_DIR,
        "backend",
        "fonts",
        "creato_display",
        "CreatoDisplay-Thin.otf"
    )

    font_bold = ImageFont.truetype(font_bold_path, 400)
    font_thin = ImageFont.truetype(font_thin_path, 300)
    font_url = ImageFont.truetype(font_thin_path, 120)

    white = (255, 255, 255)
    I1.text((200, 500), "your fic writer aura is", font=font_thin, fill=white)
    I1.text((200, 1000), f"{aura1}", font=font_bold, fill=white)
    I1.text((400, 1450), "&", font=font_thin, fill=white)
    I1.text((200, 1800), f"{aura2}", font=font_bold, fill=white)
    temp_img_file = f"backend/images/generated_images/temp_{author_name}_aura.png"
    img.save(temp_img_file)
    apply_blend_mode(temp_img_file, gradient_bg, out_file, "addition", 1.0)
    os.remove(temp_img_file)


def create_authors_aura_image(list_of_works, author_name, gradient_bg):
    print("### CREATING AURA IMAGE ###")
    used_tags = []
    for work in list_of_works:
        used_tags.extend(work.tags)

    aura_tags = json.load(open("backend/maps/aura.json", "r"))
    aura_names = json.load(open("backend/maps/aura_name.json", "r"))

    mapped_tags = json_mapping(aura_tags, used_tags)

    aura1, aura2 = match_aura(mapped_tags, aura_names, False, True)

    create_aura_image(author_name, aura1, aura2, f"backend/images/generated_images/{author_name}/aura.png", gradient_bg)

def create_authors_aura_image_new(list_of_works, author_name, gradient_bg, geometric_bg):
    print("### CREATING AURA IMAGE ###")
    used_tags = []
    for work in list_of_works:
        used_tags.extend(work.tags)

    aura_tags = json.load(open("backend/maps/aura.json", "r"))
    aura_names = json.load(open("backend/maps/aura_name.json", "r"))

    mapped_tags = json_mapping(aura_tags, used_tags)

    aura1, aura2 = match_aura(mapped_tags, aura_names, False, True)

    create_aura_image_new(author_name, aura1, aura2, f"backend/images/generated_images/{author_name}/aura.png", gradient_bg, geometric_bg)
