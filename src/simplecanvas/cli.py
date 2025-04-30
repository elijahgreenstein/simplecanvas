import shutil

from jinja2 import Environment, PackageLoader, select_autoescape
from pathlib import Path

PROMPTS = {
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


def newcourse(name, pkgdir):
    """Create a new course from templates."""
    # Create directories
    course = Path(name)
    course.mkdir()
    conf = Path("_conf")
    (course / conf).mkdir()
    # Render templates and write
    env = Environment(
        loader=PackageLoader("simplecanvas"), autoescape=select_autoescape
    )
    templates = ["token", "settings.yaml"]
    for tpl in templates:
        template = env.get_template((conf / tpl).as_posix())
        variables = {}
        for key in PROMPTS[tpl]:
            variables[key] = input(PROMPTS[tpl][key])
        with open(course / conf / tpl, "w") as f:
            f.write(template.render(variables))
    # Copy quiz description template
    quiz_desc = conf / "quiz-desc.md"
    shutil.copy(pkgdir / "templates" / quiz_desc, course / quiz_desc)


def addmod(name, pkgdir):
    """Add a module with template files."""
    pass


def upmod(name, pkgdir):
    """Upload a module to Canvas through API calls."""
    pass
