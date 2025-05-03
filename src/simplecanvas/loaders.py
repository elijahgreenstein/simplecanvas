import yaml

from pathlib import Path
from simplecanvas.objects import (
    User,
    Course,
    Module,
    Page,
    Discussion,
    Quiz,
    QuizQuestion,
)
from simplecanvas.util import md2html, get_meta, load_yaml


def load_user(token_path):
    with open(token_path) as f:
        user = User(f.read().strip())
    return user


def load_course(cset, qdesc=None):
    settings = load_yaml(cset)
    if qdesc:
        with open(qdesc) as f:
            quiz_desc = md2html(f.read())
        course = Course(settings, quiz_desc)
    else:
        course = Course(settings)
    return course


def load_page(pagepath, course, md_tpl):
    with open(pagepath) as f:
        text = f.read()
    title = get_meta(text, md_tpl)["title"]
    body = md2html(text)
    return Page(title, body)


def load_disc(discpath, course, md_tpl):
    with open(discpath) as f:
        text = f.read()
    title = get_meta(text, md_tpl)["title"]
    body = md2html(text)
    return Discussion(title, body, course.disc)


def load_quiz(quizpath, course, md_tpl):
    quiz = load_yaml(quizpath)
    title = quiz["title"]
    if quiz["description"]:
        body = md2html(quiz["description"])
    else:
        body = course.qdesc
    settings = course.quiz
    settings.update(quiz["times"])
    questions = []
    for qst in quiz["questions"]:
        qtext = qst["question"]
        qcor = qst["correct"] if "correct" in qst else []
        qinc = qst["incorrect"] if "incorrect" in qst else []
        qq = QuizQuestion(qtext, qcor, qinc)
        questions.append(qq)
    return Quiz(title, body, settings, questions)


def load_module(mod_dir, mset, course, md_tpl):
    func = {
        "page": load_page,
        "quiz": load_quiz,
        "disc": load_disc,
    }
    mdir = Path(mod_dir)
    mset = load_yaml(mdir / mset)
    items = []
    for item in mset["item_order"]:
        load_func = func[item[1]]
        items.append(load_func(mdir / item[0], course, md_tpl))
    mod = Module(mset["title"], mset["position"], mset["module_name"], items)
    return mod
