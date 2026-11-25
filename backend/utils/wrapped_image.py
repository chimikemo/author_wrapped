import glob
import random
from PIL import Image, ImageDraw, ImageFont
from collections import Counter
import os
from backend.utils.images import apply_blend_mode

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def get_top_5(list_of_items):
    counter = Counter(list_of_items)
    top5 = [item for item, _ in counter.most_common(5)]

    while len(top5) > 0 and len(top5) < 5:
        top5 = [item for item in top5 for _ in range(2)]

    top5 = top5[0:5]
    return top5

def authors_top_5(list_of_works):
    total_tags = []
    total_characters = []
    total_ships = []
    total_words = 0
    for work in list_of_works:
        total_tags.extend(work.tags)
        total_words += work.words
        total_ships.extend(work.ships)
    tags = get_top_5(total_tags)
    print(tags)
    characters = get_top_5(total_characters)
    print(characters)
    ships = get_top_5(total_ships)
    print(ships)
    print("author's top5 fully identified")
    return tags, characters, ships, total_words


def print_top5(image, section_name, top5_list, font_title, font_text, spacing, v_spacing, h_spacing, fill):
    image.text((h_spacing, v_spacing), f"{section_name}", font=font_title, fill=fill)
    image.text((h_spacing, v_spacing + 50 + spacing), f"1.   {top5_list[0]}", font=font_text, fill=fill)
    image.text((h_spacing, v_spacing + 50 + 2 * spacing), f"2.  {top5_list[1]}", font=font_text, fill=fill)
    image.text((h_spacing, v_spacing + 50 + 3 * spacing), f"3.  {top5_list[2]}", font=font_text, fill=fill)
    image.text((h_spacing, v_spacing + 50 + 4 * spacing), f"4.  {top5_list[3]}", font=font_text, fill=fill)
    image.text((h_spacing, v_spacing + 50 + 5 * spacing), f"5.  {top5_list[4]}", font=font_text, fill=fill)


def get_character_pic(characters):
    for c in characters:
        try:
            pics = glob.glob(f"backend/images/tags/characters/{c}/*.jpg")
            pic = random.choice(pics)
            c1 = Image.open(pic).convert("RGBA")
            c1 = c1.resize((600, 600))
            return c1
        except:
            continue
    pics = glob.glob(f"backend/images/tags/characters/No Character/*.jpg")
    pic = random.choice(pics)
    c1 = Image.open(pic).convert("RGBA")
    c1 = c1.resize((600, 600))
    return c1


def create_wrapped_image(author_name, tags, characters, ships, geometric_bg):

    print(f"STARTED WRAPPED IMAGE")
    img = Image.new('RGB', (3076, 3076), "rgb(0,0,0)")

    side_image = Image.open(geometric_bg).convert("RGB")

    img.paste(side_image, (0, 0))

    c1 = get_character_pic(characters)
    try:
        img.paste(c1, (900, 174), c1)
    except:
        print("{author_name}: There was an error with the character picture.")

    I1 = ImageDraw.Draw(img)


    font_black_path = os.path.join(
        BASE_DIR,
        "backend",
        "fonts",
        "consola_mono",
        "ConsolaMono-Bold.ttf"
    )

    font_bold_path = os.path.join(
        BASE_DIR,
        "backend",
        "fonts",
        "creato_display",
        "CreatoDisplay-Bold.otf"
    )

    font_thin_path = os.path.join(
        BASE_DIR,
        "backend",
        "fonts",
        "creato_display",
        "CreatoDisplay-Thin.otf"
    )


    font_black = ImageFont.truetype(font_black_path, 175)
    font_bold = ImageFont.truetype(font_bold_path, 80)
    font_thin = ImageFont.truetype(font_thin_path, 130)

    white = (255, 255, 255)

    h_spacing = 800

    a1 = author_name[0:20]
    a2 = author_name[20:]
    if a2:  # formatting for long name
        I1.text((h_spacing, 800), f"hi, ", font=font_black, fill=white)
        I1.text((h_spacing, 975), f"{a1}", font=font_black, fill=white)
        I1.text((h_spacing, 1150), f"{a2}!", font=font_black, fill=white)
    else:
        I1.text((h_spacing, 1150), f"hi, {a1}!", font=font_black, fill=white)

    print_top5(I1, "tags", tags, font_thin, font_bold, 100, 1500, h_spacing, white)
    print_top5(I1, "ships", ships, font_thin, font_bold, 100, 2300, h_spacing, white)

    temp_img_file = f"backend/images/generated_images/{author_name}/wrapped.png"
    img.save(temp_img_file)





def create_wrapped_for_author(list_of_works, author_name, geometric_bg, gradient_bg):
    print(f"### CREATING WRAPPED ###")

    file_name = f"backend/images/generated_images/{author_name}/wrapped.png"

    tags, characters, ships, total_words = authors_top_5(list_of_works)
    create_wrapped_image(author_name, tags, characters, ships, geometric_bg)
    apply_blend_mode(file_name, gradient_bg, file_name, "addition", 0.3)



