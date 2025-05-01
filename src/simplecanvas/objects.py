from pathlib import Path
from urllib.parse import urlparse

class User:

    def __init__(self, token):
        self.token = token
        self.auth = {"Authorization": f"Bearer {self.token}"}
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)


class Course:

    def __init__(self, settings, quiz_desc):
        self.id = settings["course"]["course_id"]
        self.url = urlparse(settings["course"]["course_url"])
        self.path = Path(self.url.path) / "courses" / self.id
        self.disc = settings["discussion"]
        self.quiz = settings["quiz"]
