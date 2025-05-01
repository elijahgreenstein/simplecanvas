import shutil

from jinja2 import Environment, PackageLoader, select_autoescape
from pathlib import Path

_USER = {
    "token": {
        "token": "> Enter API token: ",
    },
    "settings.yaml": {
        "course_url": "> Enter API URL: ",
        "course_id": "> Enter course unique identifier: ",
        "unlock_at": "> Enter quiz unlock time: ",
        "due_at": "> Enter quiz deadline: ",
        "lock_at": "> Enter quiz lock time: ",
    },
}


_LOG = {
    "newcourse": "Creating new course: '{course}'",
    "create_dir": "- Creating directories:",
    "create_files": "- Creating files from templates:",
    "create": "    - {name}",
}


class VerboseLog:

    def __init__(self, verbosity):
        self.verbosity = verbosity

    def log(self, level, message):
        if self.verbosity >= level:
            print(message)
        else:
            pass


def get_user_input(prompt_dict):
    res = {}
    for key in prompt_dict:
        res[key] = input(prompt_dict[key])
    return res


def newcourse(name, pkgdir, verb):
    """Create a new course from templates."""
    if name.exists():
        print(f"ERROR: '{name}' already exists.")
    else:
        _newcourse(name, pkgdir, verb)


def _newcourse(name, pkgdir, verb):
    # Create a logger for verbose output
    log = VerboseLog(verb)
    log.log(1, _LOG["newcourse"].format(course=name))
    # Get user input
    templates = ["token", "settings.yaml"]
    user_input = {}
    for tpl in templates:
        user_input[tpl] = get_user_input(_USER[tpl])
    # Create directories
    log.log(1, _LOG["create_dir"])
    conf = Path("_conf")
    for dir_path in [name, name / conf, name / "modules"]:
        dir_path.mkdir()
        log.log(1, _LOG["create"].format(name=dir_path))
    # Render templates and write
    env = Environment(
        loader=PackageLoader("simplecanvas"), autoescape=select_autoescape
    )
    log.log(1, _LOG["create_files"])
    for tpl in templates:
        template = env.get_template((conf / tpl).as_posix())
        with open(name / conf / tpl, "w") as f:
            f.write(template.render(user_input[tpl]))
        log.log(1, _LOG["create"].format(name=name / conf / tpl))
    # Copy quiz description template
    quiz_desc = conf / "quiz-desc.md"
    shutil.copy(pkgdir / "templates" / quiz_desc, name / quiz_desc)
    log.log(1, _LOG["create"].format(name=name / quiz_desc))


def addmod(name, pkgdir, verb):
    """Add a module with template files."""
    pass


def upmod(name, pkgdir, verb):
    """Upload a module to Canvas through API calls."""
    pass
