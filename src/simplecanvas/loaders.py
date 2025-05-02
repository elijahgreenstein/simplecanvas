import yaml

from pathlib import Path
from simplecanvas.objects import (
    User,
    Course,
    Page,
    Discussion,
    Quiz,
    QuizQuestion,
)
from simplecanvas.util import md2html, load_yaml


def load_user(token_path):
    with open(token_path) as f:
        user = User(f.read().strip())
    return user


def load_course(cset, qdesc=None):
    settings = load_yaml(cset)
    if qdesc:
        with open(qdesc) as f:
            quiz_desc = md2html(f.read())
        course = Course(settings, qdesc)
    else:
        course = Course(settings)
    return course
