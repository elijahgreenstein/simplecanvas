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
        self.param = None

    def set_id(self, uid):
        self.id = uid

    def get_settings(self):
        settings = self.settings if self.settings else {}
        settings["title"] = self.title
        settings[self.body_name] = self.body
        settings = {self.param: settings} if self.param else settings
        return settings


class Page(Item):

    def __init__(self, title, body):
        super().__init__(title, body)
        self.type = "Page"
        self.path = "pages"
        self.body_name = "body"
        self.param = "wiki_page"
        self.id_name = "url"
        self.content_name = "page_url"


class Discussion(Item):

    def __init__(self, title, body, settings):
        super().__init__(title, body)
        self.type = "Discussion"
        self.path = "discussion_topics"
        self.settings = settings
        self.body_name = "message"
        self.param = None
        self.id_name = "id"
        self.content_name = "content_id"


class Quiz(Item):

    def __init__(self, title, body, settings, questions):
        super().__init__(title, body)
        self.type = "Quiz"
        self.path = "quizzes"
        self.settings = settings
        self.body_name = "description"
        self.questions = questions
        self.param = "quiz"
        self.id_name = "id"
        self.content_name = "content_id"


class QuizQuestion:

    def __init__(self, question, correct=[], incorrect=[]):
        self.question = question
        self.correct = correct
        self.incorrect = incorrect
        if not correct and not incorrect:
            self.type = "essay_question"
        elif len(correct) > 1:
            self.type = "multiple_answers_question"
        else:
            self.type = "multiple_choice_question"

    def get_json(self):
        res = {
            "question_name": "Question",
            "question_type": self.type,
            "points_possible": 1,
            "question_text": self.question,
        }
        answers = []
        for answer in self.correct:
            answers.append({"answer_text": answer, "answer_weight": 100.0})
        for answer in self.incorrect:
            answers.append({"answer_text": answer, "answer_weight": 0.0})
        if answers:
            res["answers"] = answers
        else:
            pass
        return res
