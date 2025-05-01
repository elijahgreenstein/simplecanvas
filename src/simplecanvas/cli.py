import shutil

from jinja2 import Environment, PackageLoader, select_autoescape
from pathlib import Path

_CONF = Path("_conf")
_MOD = Path("modules")
_TPL = Path("templates")
_TOKEN = "token"
_CSET = "settings.yaml"
_QDESC = "quiz-desc.md"
_MCONF = "_conf.yaml"
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
_MOD = {
    "title": "> Enter module title: ",
    "mod_no": "> Enter module number: ",
    "prefix": "> Enter module prefix: ",
    "date": "> Enter quiz date: ",
}
_LOG = {
    "newcourse": "Creating new course: '{course}'",
    "addmod": "Adding a module: '{mod}'",
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
    templates = [_TOKEN, _CSET]
    user_input = {}
    for tpl in templates:
        user_input[tpl] = get_user_input(_USER[tpl])
    # Create directories
    log.log(1, _LOG["create_dir"])
    for dir_path in [name, name / _CONF, name / _MOD]:
        dir_path.mkdir()
        log.log(1, _LOG["create"].format(name=dir_path))
    # Render templates and write
    env = Environment(
        loader=PackageLoader("simplecanvas"), autoescape=select_autoescape
    )
    log.log(1, _LOG["create_files"])
    for tpl in templates:
        template = env.get_template(str(_CONF / tpl))
        with open(name / _CONF / tpl, "w") as f:
            f.write(template.render(user_input[tpl]))
        log.log(1, _LOG["create"].format(name=name / _CONF / tpl))
    # Copy quiz description template
    quiz_desc = _CONF / _QDESC
    shutil.copy(pkgdir / _TPL / quiz_desc, name / quiz_desc)
    log.log(1, _LOG["create"].format(name=name / quiz_desc))


def addmod(name, pkgdir, verb):
    """Add a module with template files."""
    if (_MOD / name).exists():
        print(f"ERROR: '{name}' already exists.")
    else:
        if (_CONF / _CSET).exists():
            _addmod(name, pkgdir, verb)
        else:
            print(f"ERROR: No course settings file, '{_CONF / _CSET}'")


def _addmod(name, pkgdir, verb):
    # Check for settings
    log = VerboseLog(verb)
    log.log(1, _LOG["addmod"].format(mod=name))


def upmod(name, pkgdir, verb):
    """Upload a module to Canvas through API calls."""
    pass
