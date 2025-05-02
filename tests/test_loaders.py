import pytest

from pathlib import Path
from simplecanvas import objects, loaders, util


FS = util.FileStructure()
DATADIR = Path(__file__).parent/"data"
TEST101 = DATADIR / "TEST101"


@pytest.fixture
def user_example():
    return objects.User("12345ABCDE")


def test_load_user(user_example):
    res = loaders.load_user(TEST101 / FS.token)
    assert res.token == user_example.token
    assert res.auth == user_example.auth


def test_load_course():
    res = loaders.load_course(TEST101 / FS.cset, TEST101 / FS.qdesc)
    assert res.id == "987"
    assert res.url = "example/api"
    assert res.path = Path("example/api/courses/987")
    assert res.disc = {
        "discussion_type": "threaded",
        "published": False,
    }
    assert res.quiz = {
        "hide_results": "always",
        "quiz_type": "assignment",
        "shuffle_answers": True,
    }
