import shutil

from jinja2 import Environment, PackageLoader, select_autoescape
from pathlib import Path

USER = {
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


def get_user_input(prompt_dict):
    res = {}
    for key in prompt_dict:
        res[key] = input(prompt_dict[key])
    return res


def render_tpl(prompt_dict, env, template, output_path):
    template = env.get_template(template)
    user = get_user_input(prompt_dict)
    with open(output_path, "w") as f:
        f.write(template.render(user))


def newcourse(name, pkgdir, verb):
    """Create a new course from templates."""
    # Create directories
    conf = Path("_conf")
    for dir_path in [name, name / conf, name / "modules"]:
        dir_path.mkdir()
    # Render templates and write
    env = Environment(
        loader=PackageLoader("simplecanvas"), autoescape=select_autoescape
    )
    templates = ["token", "settings.yaml"]
    for tpl in templates:
        render_tpl(USER[tpl], env, (conf / tpl).as_posix(), name / conf / tpl)
    # Copy quiz description template
    quiz_desc = conf / "quiz-desc.md"
    shutil.copy(pkgdir / "templates" / quiz_desc, name / quiz_desc)


def addmod(name, pkgdir, verb):
    """Add a module with template files."""
    pass


def upmod(name, pkgdir, verb):
    """Upload a module to Canvas through API calls."""
    pass
