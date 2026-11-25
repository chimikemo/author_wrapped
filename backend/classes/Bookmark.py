class Bookmark:
    def __init__(self, item, fic_id):
        self.fic_id         = fic_id
        summary             = item.find("p", class_="summary")
        self.user_id        = item.select_one('a[href*="/users/"]')['href'].split('/')[-1]
        self.date           = item.find("p", class_="datetime").text
        self.text           = summary.text if summary else None

    def __str__(self):
        return (
            f"fic_id: {self.fic_id}, "
            f"User_id: {self.user_id}, "
            f"date: {self.date}, "
            f"text: {self.text}, "
        )
