from pathlib import Path
from urllib.parse import urlparse


class User:

    def __init__(self, token):
        self.token = token
        self.auth = {"Authorization": f"Bearer {self.token}"}
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)

    def create(self, course, item, test=False):
        path = course.path / item.path
        url = course.url._replace(path=str(path)).geturl()
        iset = item.get_settings()
        if test:
            return {"TEST": {"URL": url, "-H": self.auth, "json": iset}}
        else:
            resp = requests.post(url, headers=self.auth, json=settings)
            item.set_id(resp.json()[item.id_name])
            return {"RESPONSE": resp}


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


class Item:

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.settings = None
        self.body_name = None
        self.id = None
        self.id_name = None

    def set_id(self, uid):
        self.id = uid

    def get_settings(self):
        settings = self.settings if self.settings else {}
        settings["title"] = self.title
        settings[self.body_name] = self.body
        settings = {self.param: settings} if self.param else settings
        return settings
