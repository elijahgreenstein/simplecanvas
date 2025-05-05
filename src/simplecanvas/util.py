import json
import subprocess
import yaml

from pathlib import Path


class FileStructure:

    course = Path("_conf")
    mod = Path("modules")
    cset = course / "settings.yaml"
    qdesc = course / "quiz-desc.md"
    token = course / "token"
    mset = "_conf.yaml"
    intro = "intro.md"
    quiz = "quiz.yaml"
    disc = "disc.md"
    mdjson = Path("data") / "metadata.json"

    def get_mset(self, modname):
        return self.mod / modname / self.mset

    def get_intro(self, modname):
        return self.mod / modname / self.intro

    def get_quiz(self, modname):
        return self.mod / modname / self.quiz

    def get_disc(self, modname):
        return self.mod / modname / self.disc


class DirNames:

    def __init__(self):
        self.course = Path("_conf")
        self.mod = Path("modules")


class UserInput:

    def __init__(self):
        self.course = {
            "token": "> Enter API token: ",
            "course_url": "> Enter API URL: ",
            "course_id": "> Enter course unique identifier: ",
            "unlock_at": "> Enter quiz unlock time: ",
            "due_at": "> Enter quiz deadline: ",
            "lock_at": "> Enter quiz lock time: ",
        }
        self.mod = {
            "title": "> Enter module title: ",
            "position": "> Enter module position: ",
            "prefix": "> Enter module prefix: ",
            "date": "> Enter quiz date: ",
        }


class Logger:

    def __init__(self, verbosity):
        self.verbosity = verbosity
        self.msgs = {
            "newcourse": "Creating new course: '{course}'",
            "addmod": "Adding a module: '{mod}'",
            "updmod": "Uploading module: '{mod}'",
            "create_dir": "- Creating directories:",
            "create_files": "- Creating files from templates:",
            "create": "    - {name}",
            "upmod_mod": "- Posting module ...",
            "status": "    - Status: {status}",
            "details": "    - Details: {resp}",
        }

    def log(self, level, message):
        if self.verbosity >= level:
            print(message)
        else:
            pass


def md2html(text, shift="1"):
    btext = str.encode(text)
    cmd = ["pandoc", "-f", "markdown", "-t", "html"]
    if shift:
        cmd.append(f"--shift-heading-level-by={shift}")
    res = subprocess.run(cmd, input=btext, capture_output=True)
    return res.stdout.decode("utf-8")


def get_meta(text, metadata_template):
    btext = str.encode(text)
    cmd = ["pandoc", "-f", "markdown", "--template", metadata_template]
    res = subprocess.run(cmd, input=btext, capture_output=True)
    return json.loads(res.stdout.decode("utf-8"))


def load_yaml(file):
    with open(file) as f:
        text = f.read()
    return yaml.safe_load(text)
