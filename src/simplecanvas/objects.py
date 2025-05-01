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


class Module:

    def __init__(self, title, position, items):
        self.title = title
        self.position = position
        self.items = items
        self.path = "modules"
        self.id = None
        self.id_name = "id"

    def get_settings(self):
        return {"module": {"name": self.title, "position": self.position}}

    def set_id(self, uid):
        self.id = uid
