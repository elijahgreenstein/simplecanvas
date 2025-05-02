import shutil
import yaml

from jinja2 import Environment, PackageLoader, select_autoescape
from pathlib import Path
from simplecanvas.util import UserInput, Logger, DirNames


def get_env():
    return Environment(
        loader=PackageLoader("simplecanvas"), autoescape=select_autoescape
    )


def get_user_input(prompt_dict):
    res = {}
    for key in prompt_dict:
        res[key] = input(prompt_dict[key])
    return res


def get_template_paths(dirname):
    env = get_env()
    return env.list_templates(filter_func=lambda x: x.startswith(str(dirname)))


def render_template(tpl_name, variables):
    env = get_env()
    template = env.get_template(tpl_name)
    return template.render(variables)


def newcourse(name, pkgdir, verb):
    """Create a new course from templates."""
    if name.exists():
        raise FileExistsError(f"'{name}' already exists.")
    else:
        user_prompts = UserInput()
        user_input = get_user_input(user_prompts.course)
        tpls = get_newcourse(user_input)
        write_newcourse(name, tpls, verb)


def get_newcourse(user_input):
    # Get templates
    tpl_names = get_template_paths(str(DirNames().course))
    # Render templates
    rendered = {}
    for tpl in tpl_names:
        rendered[tpl] = render_template(tpl, user_input)
    return rendered


def write_newcourse(name, tpls, verb):
    # Set up logger
    log = Logger(verb)
    log.log(1, log.msgs["newcourse"].format(course=name))
    # Make directories
    log.log(1, log.msgs["create_dir"])
    for dname in [name, name / DirNames().course, name / DirNames().mod]:
        dname.mkdir()
        log.log(1, log.msgs["create"].format(name=dname))
    # Write files
    log.log(1, log.msgs["create_files"])
    for tpl in tpls:
        with open(name/tpl, "w") as f:
            f.write(tpls[tpl])
        log.log(1, log.msgs["create"].format(name=tpl))


def load_yaml(file):
    with open(file) as f:
        text = f.read()
    return yaml.safe_load(text)


def addmod(name, pkgdir, verb):
    """Add a module with template files."""
    cset = DirNames().course / "settings.yaml"
    mpath = DirNames().mod / name
    if cset.exists() and not mpath.exists():
        # Load course settings and get user input
        cset = load_yaml(cset)
        user_input = get_user_input(UserInput().mod)
        # Update user input with times from course settings
        user_input.update(cset["times"])
        # Get templates and write
        tpls = get_mod_tpls(name, user_input)
        write_mod(name, tpls, verb)
    elif mpath.exists():
        raise FileExistsError(f"'{name}' already exists.")
    else:
        raise FileNotFoundError(f"No course settings file, '{cset}'.")


def get_mod_tpls(name, user_input):
    # Get templates
    tpl_names = get_template_paths(str(DirNames().mod))
    # Render templates and change output path in process
    rendered = {}
    for tpl in tpl_names:
        outpath = DirNames().mod / name / Path(tpl).name
        rendered[outpath] = render_template(tpl, user_input)
    return rendered


def write_mod(name, tpls, verb):
    # Set up logger
    log = Logger(verb)
    log.log(1, log.msgs["addmod"].format(mod=name))
    # Make module directory
    log.log(1, log.msgs["create_dir"])
    (DirNames().mod/name).mkdir()
    log.log(1, log.msgs["create"].format(name=DirNames().mod/name))
    # Write files
    log.log(1, log.msgs["create_files"])
    for tpl in tpls:
        with open(tpl, "w") as f:
            f.write(tpls[tpl])
        log.log(1, log.msgs["create"].format(name=tpl))


def upmod(name, pkgdir, verb):
    """Upload a module to Canvas through API calls."""
    cset = UserInput().course / "settings.yaml"
    mpath = UserInput().mod / name
    if cset.exists() and mpath.exists():
        # Load course and module settings
        cset = load_yaml(cset)
        mset = load_yaml(mpath / "_conf.py")
        # TODO: Load files
    elif not mpath.exists():
        raise FileNotFoundError(f"'{name}' does not exist.")
    else:
        raise FileNotFoundError(f"No course settings file, '{cset}'.")
