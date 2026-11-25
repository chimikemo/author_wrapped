from backend.utils.retriever import find_items
from backend.utils.images import create_collage_for_author
from backend.utils.aura import create_authors_aura_image, create_authors_aura_image_new
from backend.utils.wrapped_image import create_wrapped_for_author
from backend.classes.Work import Work
import os
import random
import json
from collections import defaultdict, deque
import time
from PIL import Image as PILImage
from IPython.display import display

def create_authors_images(author_name):
    author_name = author_name.strip()
    
    if author_name == "orphan_account":
        print("Can't run this for orphan_account -- it has too many works!")

    if not author_name:
        print("No author name provided")

    list_of_works = find_items(Work, "users", author_name, "works")
    shortened_author_name = author_name.split("/")[-1]

    if len(list_of_works) == 0:
        print (f"Author {author_name} has no works")

    print("filtering out works from 2025...")

    works_2025 = [l for l in list_of_works if "2025" in l.date]

    if works_2025:
        list_of_works = works_2025
        print("This author published in 2025 -- proceeding with only works frm this year")
    else:
        print("This author hasn't published in 2025 -- proceeding with historical wrapped")

    os.makedirs(f"backend/images/generated_images/{shortened_author_name}", exist_ok=True)

    colors = ["blue", "pink", "orange", "purple", "green", "red"]
    color = random.choice(colors)

    print(f"it has been (scientifically) determined that {author_name}'s color is {color}")

    geometric_bg = f"backend/images/geometric/{color}.png"
    gradient_bg = f"backend/images/gradients/{color}.jpg"

    json_tags = json.load(open("backend/maps/aura.json", "r"))

    print(f"using advanced math and science to generate {author_name}'s moodboard....")

    create_collage_for_author(
        list_of_works,
        json_tags,
        1024,
        f"backend/images/generated_images/{shortened_author_name}/collage.png",
        gradient_bg
    )

    print("moodboard completed!")
    print(f"using astrology and calculus to determine {author_name}'s aura...")

    create_authors_aura_image_new(list_of_works, shortened_author_name, gradient_bg, geometric_bg)

    print("aura completed!")
    print(f"for the grand finale, generate {author_name}'s wrapped!")

    create_wrapped_for_author(list_of_works, shortened_author_name, geometric_bg, gradient_bg)

    wrapped = PILImage.open(f"backend/images/generated_images/{shortened_author_name}/wrapped.png")
    collage = PILImage.open(f"backend/images/generated_images/{shortened_author_name}/collage.png")
    aura = PILImage.open(f"backend/images/generated_images/{shortened_author_name}/aura.png")
    display(wrapped)
    display(collage)
    display(aura)

    return
