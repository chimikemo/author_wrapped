import requests
from bs4 import BeautifulSoup
import time
from getuseragent import UserAgent
import random
import logging
def retrieve_page(url):
    useragent = UserAgent("all", requestsPrefix=True).Random()
    time.sleep(random.uniform(2, 5))
    source = requests.get(url, headers=useragent)
    return BeautifulSoup(source.text, "lxml")


def find_total_pages(soup):
    next_button = soup.find("li", class_="next")
    try:
        total = next_button.find_previous_sibling("li")
        t = total.get_text(strip=True)
        return int(t)
    except:
        return False


def apply_matching(soup, type):
    if type == "works":
        return [li for li in soup.select('li[id*="work_"]')]
    elif type == "bookmarks":
        return soup.select('li[class^="user short blurb group"]')
    elif type == "": #comment
        return [li for li in soup.select('li[id*="comment_"]')]



def find_items(Class, base_url, item, end_url, final_part_url = ""):
    url = f"https://archiveofourown.org/{base_url}/{item}/{end_url}?page=1{final_part_url}"
    print(url)
    soup = retrieve_page(url)
    total_pages = find_total_pages(soup)
    print(f"total_pages: {total_pages}")
    items = apply_matching(soup, end_url)
    print(f"item: {item}")
    obj_items = [Class(i, item) for i in items]
    if total_pages:
        for page in range(2, total_pages + 1):
            print(f"page: {page}")
            soup = retrieve_page(f"https://archiveofourown.org/{base_url}/{item}/{end_url}?page={page}{final_part_url}")
            items = apply_matching(soup, end_url)
            obj_items += [Class(i, item) for i in items]
    return obj_items
