import json


def json_mapping(json_tags, used_tags):
    mapped_tags = [json_tags[value] if value in json_tags else None for value in used_tags]
    clean_tags = [m for m in mapped_tags if m is not None]

    t = [u.split(',') for u in clean_tags]
    t = [x for xs in t for x in xs]
    return t
