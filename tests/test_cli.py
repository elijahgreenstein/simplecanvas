import pytest

from pathlib import Path
from simplecanvas import cli, util, objects


FS = util.FileStructure()
DATADIR = Path(__file__).parent / "data"
TEST101 = DATADIR / "TEST101"


@pytest.fixture
def mdjson():
    return DATADIR / "metadata.json"


@pytest.fixture
def user_input_course():
    return {
        "course_name": "TEST101",
        "token": "12345ABCDE",
        "course_url": "example/api",
        "course_id": "987",
        "unlock_at": "12:00:00",
        "due_at": "13:00:00",
        "lock_at": "14:00:00",
    }


@pytest.fixture
def user_input_mod():
    return {
        "module_name": "W01",
        "title": "Test module 1",
        "position": "3",
        "prefix": "1",
        "date": "2025-05-01",
        "unlock_at": "12:00:00",
        "due_at": "13:00:00",
        "lock_at": "14:00:00",
    }


@pytest.fixture
def mod_name():
    return "W01"


test_tpl_paths = [
    ("_conf", ["settings.yaml", "token", "quiz-desc.md"]),
    ("modules", ["_conf.yaml", "intro.md", "quiz.yaml", "disc.md"]),
]


test_tpl_render_crs = [
    (
        "_conf/settings.yaml",
        '''course:
  course_name: "TEST101"
  course_id: "987"
  course_url: example/api
discussion:
  discussion_type: threaded
  published: false
quiz:
  hide_results: always
  quiz_type: assignment
  shuffle_answers: true
times:
  unlock_at: "12:00:00"
  due_at: "13:00:00"
  lock_at: "14:00:00"''',
    ),
    ("_conf/token", "12345ABCDE"),
    ("_conf/quiz-desc.md", "# Overview\n\nDefault quiz description."),
]


test_tpl_render_mod = [
    ("modules/intro.md", '---\ntitle: "1.1. Introduction"\n---'),
    ("modules/disc.md", '---\ntitle: "1.3. Discussion"\n---'),
    (
        "modules/quiz.yaml",
        '''title: "1.2. Quiz"
description: null
times:
  unlock_at: "2025-05-01T12:00:00Z"
  due_at: "2025-05-01T13:00:00Z"
  lock_at: "2025-05-01T14:00:00Z"
questions:
  - question: "What is ..."
    correct:
      - "Answer 1"
      - "Answer 2"
    incorrect:
      - "Answer 3"
      - "Answer 4"
  - question: "Write about ..."''',
    ),
    (
        "modules/_conf.yaml",
        """module_name: "W01"
title: "Test module 1"
position: 3
item_order:
  - [intro.md, page]
  - [quiz.yaml, quiz]
  - [disc.md, disc]""",
    ),
]

test_tpl_render_ids_crs = [
    "_conf/settings.yaml",
    "_conf/token",
    "_conf/quiz-desc.md",
]


test_tpl_render_ids_mod = [
    "modules/intro.md",
    "modules/disc.md",
    "modules/quiz.yaml",
    "modules/_conf.yaml",
]


class TestTemplates:

    @pytest.mark.parametrize("dirn,files", test_tpl_paths)
    def test_get_template_paths(self, dirn, files):
        for file in files:
            assert f"{dirn}/{file}" in cli.get_template_paths(dirn)

    @pytest.mark.parametrize(
        "tpl,rendered", test_tpl_render_crs, ids=test_tpl_render_ids_crs
    )
    def test_render_template_crs(self, tpl, rendered, user_input_course):
        res = cli.render_template(tpl, user_input_course)
        assert rendered == res

    @pytest.mark.parametrize(
        "tpl,rendered", test_tpl_render_mod, ids=test_tpl_render_ids_mod
    )
    def test_render_template_mod(self, tpl, rendered, user_input_mod):
        res = cli.render_template(tpl, user_input_mod)
        assert rendered == res


class TestNewCourse:

    def test_get_newcourse(self, user_input_course):
        res = cli.get_newcourse(user_input_course)
        assert dict(test_tpl_render_crs) == res


class TestAddMod:
    def test_get_mod_tpls(self, mod_name, user_input_mod):
        check = {}
        for tpl in test_tpl_render_mod:
            original = Path(tpl[0])
            newpath = Path("modules") / mod_name / original.name
            check[newpath] = tpl[1]
        res = cli.get_mod_tpls(mod_name, user_input_mod)
        assert check == res


class TestUpMod:

    @pytest.fixture
    def user(self, mod_name, mdjson):
        modpath = TEST101 / FS.mod / mod_name
        return cli.load_mod(TEST101, modpath, mdjson)

    def test_load_mod(self, user):
        assert user.token == "12345ABCDE"
        assert "TEST101" in user.courses
        assert user.courses["TEST101"].uid == "987"
        assert "W01" in user.courses["TEST101"].modules
        assert user.courses["TEST101"].modules["W01"].title == "A test module"
        res_items = user.courses["TEST101"].modules["W01"].items
        type_check = [objects.Page, objects.Quiz, objects.Discussion]
        title_check = ["1.1. Introduction", "1.2. Quiz", "1.3. Discussion"]
        for idx in range(len(res_items)):
            assert type(res_items[idx] == type_check[idx])
            assert res_items[idx].title == title_check[idx]

    @pytest.fixture
    def auth(self):
        return {"Authorization": "Bearer 12345ABCDE"}

    @pytest.fixture
    def mod_resp_example(self, auth):
        resp = {
            "TEST": {
                "URL": "example/api/courses/987/modules",
                "-H": auth,
                "json": {
                    "module": {
                        "name": "A test module",
                        "position": 3,
                    }
                },
            }
        }
        return resp

    @pytest.fixture
    def page_resp_ex(self, auth):
        resp = {
            "TEST": {
                "URL": "example/api/courses/987/pages",
                "-H": auth,
                "json": {
                    "wiki_page": {
                        "title": "1.1. Introduction",
                        "body": '<h2 id="overview">Overview</h2>\n<p>This is a test module.</p>\n',
                    }
                },
            }
        }
        return resp

    @pytest.fixture
    def quiz_resp_ex(self, auth):
        resp = {
            "TEST": {
                "URL": "example/api/courses/987/quizzes",
                "-H": auth,
                "json": {
                    "quiz": {
                        "title": "1.2. Quiz",
                        "description": '<h2 id="overview">Overview</h2>\n<p>A modified quiz description for the test module.</p>\n',
                        "shuffle_answers": True,
                        "hide_results": "always",
                        "quiz_type": "assignment",
                        "unlock_at": "2025-05-01T12:00:00Z",
                        "due_at": "2025-05-01T13:00:00Z",
                        "lock_at": "2025-05-01T14:00:00Z",
                    },
                },
            }
        }
        return resp

    def test_upload_seq(
        self, user, mod_resp_example, page_resp_ex, quiz_resp_ex
    ):
        # Give example id numbers to items
        user.courses["TEST101"].modules["W01"].set_id("MOD123")
        id_examples = ["P101", "Q102", "D103"]
        for idx in range(len(id_examples)):
            uid = id_examples[idx]
            user.courses["TEST101"].modules["W01"].items[idx].set_id(uid)
        assert user.courses["TEST101"].modules["W01"].items[0].uid == "P101"
        resp = cli.upload_seq(user, mod_name, 0, test=True)
        assert "TEST" in resp["module_response"]
        assert mod_resp_example == resp["module_response"]
        assert page_resp_ex == resp["item_responses"][0]
        assert quiz_resp_ex == resp["item_responses"][1]
