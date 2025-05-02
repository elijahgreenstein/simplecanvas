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
        course = Course(settings, qdesc)
    else:
        course = Course(settings)
    return course


def load_module(mod_dir, mset):
    mdir = Path(mod_dir)
    mset = load_yaml(mdir / mset)
    items = []
    for item in mset["item_order"]:
        pass    # TODO: Load each item by type
    mod = Module(mset["title"], mset["position"], items)
    return mod


def load_page(page, md_tpl):
    with open(page) as f:
        text = f.read()
    title = get_meta(text, md_tpl)["title"]
    body = md2html(text)
    return Page(title, body)
