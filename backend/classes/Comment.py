class Comment:
    def __init__(self, item, work_id):
        self.work_id = work_id
        self.user_name = item.select_one('a[href*="/users/"]')['href'].split('/')[-1]
        self.day =  item.find("span", class_="day")
        self.date =  item.find("span", class_="date")
        self.month =  item.find("span", class_="month")
        self.year =  item.find("span", class_="year")
        self.time =  item.find("span", class_="time")
        self.timezone =  item.find("span", class_="timezone")
        self.text = item.find("blockquote", class_="userstuff").text

    def __str__(self):
        return (
            f"user_name: {self.user_name}, "
            f"day: {self.day}, "
            f"date: {self.date}, "
            f"month: {self.month}, "
            f"text: {self.text}, "
        )
