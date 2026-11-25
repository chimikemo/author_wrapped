from backend.utils.retriever import find_items
from backend.classes.Bookmark import Bookmark


class Work:
    def __init__(self, item, author_name):
        kudos = item.find("dd", class_="kudos")
        bookmarks = item.find("dd", class_="bookmarks")
        hits = item.find("dd", class_="hits")
        comments = item.find("dd", class_="comments")
        words = item.find("dd", class_="words")
        self.author_name = author_name
        self.id = item.select_one('a[href*="/works/"]')['href'].split('/')[-1]
        self.title = item.find("a", href=lambda x: x and "/works" in x).text
        self.rating = item.find("span", class_="rating").text
        self.warnings = [w.text for w in item.find_all("li", class_="warnings")]
        self.ships = [w.text for w in item.find_all("li", class_="relationships")]
        self.characters = [w.text for w in item.find_all("li", class_="characters")]
        self.tags = [w.text for w in item.find_all("li", class_="freeforms")]
        self.fandoms = [w.text for w in item.find_all("a", class_="freeforms")]
        self.words = int(words.text.replace(",", "")) if words else None
        self.comments = comments.text if comments else None
        self.kudos = kudos.text if kudos else None
        self.bookmarks = bookmarks.text if bookmarks else None
        self.hits = hits.text if hits else None
        self.bookmarkers = []
        self.commenters = []
        self.comments_text = []
        self.date = item.find("p", class_="datetime").text

        print(f"{self.author_name}: {self.title}")

    def find_bookmarkers(self):
        self.bookmarkers = find_items(Bookmark, "works", self.id, "bookmarks")

    def __str__(self):
        return (
            f"Id: {self.id}, "
            f"Title: {self.title}, "
            f"Rating: {self.rating}, "
            f"Warnings: {self.warnings}, "
            f"Ships: {self.ships}, "
            f"Characters: {self.characters}, "
            f"Tags: {self.tags}, "
            f"Words: {self.words}, "
            f"Comments: {self.comments}, "
            f"Kudos: {self.kudos}, "
            f"Bookmarks: {self.bookmarks}, "
            f"Hits: {self.hits}, "
            f"Bookmarkers: {self.bookmarkers}"
        )
