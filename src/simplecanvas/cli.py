import shutil
import yaml

from jinja2 import Environment, PackageLoader, select_autoescape
from pathlib import Path
from simplecanvas import util


def get_env():
    return Environment(
        loader=PackageLoader("simplecanvas"), autoescape=select_autoescape
    )


def get_user_input(prompt_dict):
    res = {}
    for key in prompt_dict:
        res[key] = input(prompt_dict[key])
    return res


def load_yaml(file):
    with open(file) as f:
        text = f.read()
    return yaml.safe_load(text)


def mkdirs(dirs, log):
    for dpath in dirs:
        dpath.mkdir()
        log.log(1, _LOG["create"].format(name=dpath))


def get_template_paths_from(dirname):
    env = get_env()
    return env.list_templates(filter_func=lambda x: x.startswith(str(dirname)))


def _render_tpls(tpls, variables):
    res = {}
    env = _get_env()
    for tpl in tpls:
        template = env.get_template(tpl)
        res[tpl] = template.render(variables)
    return res


def _write_file(text, path, log):
    with open(path, "w") as f:
        f.write(text)
    log.log(1, _LOG["create"].format(name=path))


def _copy_file(from_path, to_path, log):
    shutil.copy(from_path, to_path)
    log.log(1, _LOG["create"].format(name=to_path))


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
    user_input =  _get_user_input(_USER["crs"])
    # Create directories
    log.log(1, _LOG["create_dir"])
    _mkdirs([name, name / _CONF, name / _MOD], log)
    # Render templates
    tpaths = [str(_CONF / "token"), str(_CONF / "settings.yaml")]
    tpls = _render_tpls(tpaths, user_input)
    # Write files
    log.log(1, _LOG["create_files"])
    for tpl in tpls:
        _write_file(tpls[tpl], name / tpl, log)
    # Copy quiz description template
    _copy_file(pkgdir / _TPL / _CONF / _QDESC, name / _CONF / _QDESC, log)


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
