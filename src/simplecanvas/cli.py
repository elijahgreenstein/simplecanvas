import pathlib
import pprint

import jinja2

from simplecanvas import loaders, objects, util
from simplecanvas.util import DirNames


FS = util.FileStructure()


def get_env():
    return jinja2.Environment(
        loader=jinja2.PackageLoader("simplecanvas"), autoescape=jinja2.select_autoescape
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


def newcourse(name, verb):
    """Create a new course from templates."""
    if name.exists():
        raise FileExistsError(f"'{name}' already exists.")
    else:
        user_prompts = util.UserInput()
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
    log = util.Logger(verb)
    log.log(1, log.msgs["newcourse"].format(course=name))
    # Make directories
    log.log(1, log.msgs["create_dir"])
    for dname in [name, name / DirNames().course, name / DirNames().mod]:
        dname.mkdir()
        log.log(1, log.msgs["create"].format(name=dname))
    # Write files
    log.log(1, log.msgs["create_files"])
    for tpl in tpls:
        with open(name / tpl, "w") as f:
            f.write(tpls[tpl])
        log.log(1, log.msgs["create"].format(name=tpl))


def addmod(name, verb):
    """Add a module with template files."""
    cset = DirNames().course / "settings.yaml"
    mpath = DirNames().mod / name
    if cset.exists() and not mpath.exists():
        # Load course settings and get user input
        cset = util.load_yaml(cset)
        user_input = get_user_input(util.UserInput().mod)
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
        outpath = DirNames().mod / name / pathlib.Path(tpl).name
        rendered[outpath] = render_template(tpl, user_input)
    return rendered


def write_mod(name, tpls, verb):
    # Set up logger
    log = util.Logger(verb)
    log.log(1, log.msgs["addmod"].format(mod=name))
    # Make module directory
    log.log(1, log.msgs["create_dir"])
    (DirNames().mod / name).mkdir()
    log.log(1, log.msgs["create"].format(name=DirNames().mod / name))
    # Write files
    log.log(1, log.msgs["create_files"])
    for tpl in tpls:
        with open(tpl, "w") as f:
            f.write(tpls[tpl])
        log.log(1, log.msgs["create"].format(name=tpl))


def upmod(name, pkgdir, verb, test):
    """Upload a module to Canvas through API calls."""
    cset = FS.cset
    mpath = FS.mod / name
    mdjson = pkgdir / FS.mdjson
    if cset.exists() and mpath.exists():
        # Load module
        user = load_mod(pathlib.Path("./"), mpath, pkgdir / FS.mdjson)
        # Run the upload sequence
        results = upload_seq(user, name, verb, test)
        # Print test results
        if test:
            print("TEST COMPLETE:")
            pprint.pprint(results["module"])
            for item in results["items"]:
                pprint.pprint(item)
            for item in results["moves"]:
                pprint.pprint(item)
    elif not mpath.exists():
        raise FileNotFoundError(f"'{name}' does not exist.")
    else:
        raise FileNotFoundError(f"No course settings file, '{cset}'.")


def load_mod(cpath, mpath, mdjson):
    cset = cpath / FS.cset
    qdesc_path = cpath / FS.qdesc
    user = loaders.load_user(cpath / FS.token)
    qdesc = qdesc_path if qdesc_path.exists() else None
    course = loaders.load_course(cset, qdesc)
    mod = loaders.load_module(mpath, FS.mset, course, mdjson)
    course.add_mod(mod)
    user.add_course(course)
    return user


def upload_seq(user, name, verb, test):
    # Set up logger for verbose output
    log = util.Logger(verb)
    log.log(1, log.msgs["upmod"].format(mod=name))
    # Get the course
    course = [crs for crs in user.courses.values()][0]
    module = [mod for mod in course.modules.values()][0]
    # Create module
    log.log(1, log.msgs["upmod_mod"])
    mod_resp = user.create(course, module, test)
    if not test:
        status = mod_resp.status_code
        log.log(1, log.msgs["status"].format(status=status))
        log.log(2, log.msgs["details"].format(resp=mod_resp.json()))
    # Create items
    item_resp = []
    for item in module.items:
        log.log(1, log.msgs["upmod_item"].format(item=item.title))
        resp = user.create(course, item, test)
        item_resp.append(resp)
        if not test:
            status = resp.status_code
            log.log(1, log.msgs["status"].format(status=status))
            log.log(2, log.msgs["details"].format(resp=resp.json()))
    # Move items to module
    move_resp = []
    for idx in range(len(module.items)):
        item = module.items[idx]
        log.log(1, log.msgs["upmod_move"].format(item=item.title))
        position = idx + 1
        resp = user.move(course, module, item, position, test)
        move_resp.append(resp)
        if not test:
            status = resp.status_code
            log.log(1, log.msgs["status"].format(status=status))
            log.log(2, log.msgs["details"].format(resp=resp.json()))
    # Handle quizzes
    quiz_resp = []
    for item in module.items:
        if type(item) == objects.Quiz:
            log.log(1, log.msgs["upmod_add_qst"].format(item=item.title))
            resps = user.add_quiz_questions(course, item, test)
            if not test:
                for resp in resps:
                    status = resp.status_code
                    log.log(1, log.msgs["status"].format(status=status))
                    log.log(2, log.msgs["details"].format(resp=resp.json()))
            quiz_resp.append(resps)
            log.log(1, log.msgs["upmod_update_pts"].format(item=item.title))
            resp = user.update_quiz_pts(course, item, test)
            if not test:
                status = resp.status_code
                log.log(1, log.msgs["status"].format(status=status))
                log.log(2, log.msgs["details"].format(resp=resp.json()))
            quiz_resp.append(resp)

    # Return responses
    return {
        "module": mod_resp,
        "items": item_resp,
        "moves": move_resp,
        "quiz": quiz_resp,
    }
