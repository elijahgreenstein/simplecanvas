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
    for dname in [name / DirNames().course, name / DirNames().mod]:
        log.log(1, log.msgs["create"].format(name=dname))
    # Write files
    log.log(1, log.msgs["create_files"])
    for tpl in rendered:
        with open(tpl, "w") as f:
            f.write(rendered[tpl])
        log.log(1, log.msgs["create"].format(name=tpl))


def load_yaml(file):
    with open(file) as f:
        text = f.read()
    return yaml.safe_load(text)


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
    # Create a logger for verbose output
    log = VerboseLog(verb)
    log.log(1, _LOG["addmod"].format(mod=name))
    # Load course settings
    cset = _load_yaml(_CONF / _CSET)
    # Get user input and add course settings
    user_input = _get_user_input(_USER["mod"])
    user_input.update(cset["times"])
    # Create directories
    log.log(1, _LOG["create_dir"])
    _mkdirs([_MOD / name], log)
    # Render templates
    env = _get_env()
    tpaths = env.list_templates(filter_func=lambda x: x.startswith(str(_MOD)))
    tpls = _render_tpls(tpaths, user_input)
    # Write files
    log.log(1, _LOG["create_files"])
    for tpl in tpls:
        _write_file(tpls[tpl], _MOD / name / Path(tpl).name, log)


def upmod(name, pkgdir, verb):
    """Upload a module to Canvas through API calls."""
    if not (_MOD / name).exists():
        print(f"ERROR: Module '{name}' does not exist.")
    else:
        if (_CONF / _CSET).exists():
            _upmod(name, pkgdir, verb)
        else:
            print(f"ERROR: No course settings file, '{_CONF / _CSET}'")


def _upmod(name, pkgdir, verb):
    pass
