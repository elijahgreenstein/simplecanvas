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
