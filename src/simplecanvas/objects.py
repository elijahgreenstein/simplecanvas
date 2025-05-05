from pathlib import Path
from urllib.parse import urlparse


class User:

    def __init__(self, token, courses={}):
        self.token = token
        self.auth = {"Authorization": f"Bearer {token}"}
        self.courses = courses

    def add_course(self, course):
        self.courses[course.cname] = course

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

    def move(self, course, module, item, test=False):
        path = course.path / module.path / module.uid / "items"
        url = course.url._replace(path=str(path)).geturl()
        params = {"module_item": {item.content_name: item.uid}}
        if test:
            return {"TEST": {"URL": url, "-H": self.auth, "json": params}}
        else:
            resp = requests.post(url, headers=self.auth, json=params)
            return {"RESPONSE": resp}

    def add_quiz_questions(self, course, quiz, test=False):
        path = course.path / quiz.path / quiz.uid / "questions"
        url = course.url._replace(path=str(path)).geturl()
        resps = []
        for question in quiz.questions:
            params = question.get_json()
            if test:
                resp = {"TEST": {"URL": url, "-H": self.auth, "json": params}}
                resps.append(resp)
            else:
                resp = requests.post(url, headers=self.auth, json=params)
                resp.append(resp)
        return resps

    def update_quiz_pts(self, course, quiz, test=False):
        path = course.path / quiz.path / quiz.uid
        url = course.url._replace(path=str(path)).geturl()
        params = {"points_possible": len(quiz.questions)}
        if test:
            return {"TEST": {"URL": url, "-H": self.auth, "json": params}}


class Course:

    modules = {}

    def __init__(self, settings, qdesc=None):
        self.cname = settings["course"]["course_name"]
        self.uid = settings["course"]["course_id"]
        self.url = urlparse(settings["course"]["course_url"])
        self.path = Path(self.url.path) / "courses" / self.uid
        self.disc = settings["discussion"]
        self.quiz = settings["quiz"]
        self.qdesc = qdesc

    def add_mod(self, mod):
        self.modules[mod.mname] = mod


class Module:

    path = "modules"
    uid = None
    id_name = "id"

    def __init__(self, title, position, mname, items=[]):
        self.title = title
        self.position = position
        self.mname = mname
        self.items = items

    def get_settings(self):
        return {"module": {"name": self.title, "position": self.position}}

    def set_id(self, uid):
        self.uid = uid


class Item:

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def set_id(self, uid):
        self.uid = uid

    def get_settings(self):
        settings = self.settings if self.settings else {}
        settings["title"] = self.title
        settings[self.body_name] = self.body
        settings = {self.param: settings} if self.param else settings
        return settings


class Page(Item):

    itype = "Page"
    path = "pages"
    body_name = "body"
    param = "wiki_page"
    id_name = "url"
    content_name = "page_url"
    settings = None

    def __init__(self, title, body):
        super().__init__(title, body)


class Discussion(Item):

    itype = "Discussion"
    path = "discussion_topics"
    body_name = "message"
    param = None
    id_name = "id"
    content_name = "content_id"

    def __init__(self, title, body, settings):
        super().__init__(title, body)
        self.settings = settings


class Quiz(Item):

    itype = "Quiz"
    path = "quizzes"
    body_name = "description"
    param = "quiz"
    id_name = "id"
    content_name = "content_id"

    def __init__(self, title, body, settings, questions):
        super().__init__(title, body)
        self.settings = settings
        self.questions = questions


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
