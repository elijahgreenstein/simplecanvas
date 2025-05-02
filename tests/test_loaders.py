import pytest

from pathlib import Path
from simplecanvas import objects, loaders, util


FS = util.FileStructure()
DATADIR = Path(__file__).parent / "data"
TEST101 = DATADIR / "TEST101"


@pytest.fixture
def mdjson():
    return DATADIR / "metadata.json"


@pytest.fixture
def user_example():
    return objects.User("12345ABCDE")


@pytest.fixture
def course_example():
    settings = {
        "course": {
            "course_id": "987",
            "course_url": "example/api",
        },
        "discussion": {
            "discussion_type": "threaded",
            "published": False,
        },
        "quiz": {
            "hide_results": "always",
            "quiz_type": "assignment",
            "shuffle_answers": True,
        },
        "times": {
            "unlock_at": "12:00:00",
            "due_at": "13:00:00",
            "lock_at": "14:00:00",
        },
    }
    qdesc = '''<h2 id="overview">Overview</h2>
<p>A modified quiz description for the test module.</p>
'''
    return objects.Course(settings, qdesc)


@pytest.fixture
def module_example():
    return objects.Module("A test module", 3)


@pytest.fixture
def page_example():
    return objects.Page(
        "1.1. Introduction",
        '<h2 id="overview">Overview</h2>\n<p>This is a test module.</p>\n'
    )


@pytest.fixture
def disc_example():
    return objects.Discussion(
        "1.3. Discussion",
        '''<h2 id="overview">Overview</h2>
<p>A test discussion.</p>
<h2 id="to-do">To-Do</h2>
<ul>
<li>Item 1</li>
<li>Item 2</li>
</ul>
''',
        {"discussion_type": "threaded", "published": False}
)


@pytest.fixture
def quiz_example():
    title = "1.2. Quiz"
    body = '''<h2 id="overview">Overview</h2>
<p>A modified quiz description for the test module.</p>
'''
    settings = {
        "hide_results": "always",
        "quiz_type": "assignment",
        "shuffle_answers": True,
        "unlock_at": "2025-05-01T12:00:00Z",
        "due_at": "2025-05-01T13:00:00Z",
        "lock_at": "2025-05-01T14:00:00Z",
    }
    question1 = objects.QuizQuestion(
        "What are the correct answers?",
        correct = ["Answer 1", "Answer 2"],
        incorrect = ["Answer 3", "Answer 4"],
    )
    question2 = objects.QuizQuestion("Write about a test case.")
    return objects.Quiz(title, body, settings, [question1, question2])


def test_load_user(user_example):
    res = loaders.load_user(TEST101 / FS.token)
    assert res.token == user_example.token
    assert res.auth == user_example.auth


def test_load_course(course_example):
    res = loaders.load_course(TEST101 / FS.cset, TEST101 / FS.qdesc)
    assert course_example.uid == res.uid
    assert course_example.url == res.url
    assert course_example.path == res.path
    assert course_example.disc == res.disc
    assert course_example.quiz == res.quiz
    assert course_example.qdesc == res.qdesc


def test_load_module(module_example, mdjson, page_example, quiz_example,
                     disc_example):
    course = loaders.load_course(TEST101 / FS.cset)
    moddir = TEST101 / FS.mod / "W01"
    res = loaders.load_module(moddir, FS.mset, course, mdjson)
    assert module_example.title == res.title
    assert module_example.position == res.position
    assert res.path == "modules"
    assert res.uid == None
    assert res.id_name == "id"
    new_id = "123456"
    res.set_id(new_id)
    assert res.uid == new_id
    assert type(res.items[0]) == objects.Page
    assert res.items[0].title == page_example.title
    assert type(res.items[1]) == objects.Quiz
    assert res.items[1].title == quiz_example.title
    assert type(res.items[2]) == objects.Discussion
    assert res.items[2].title == disc_example.title


def test_load_page(page_example, mdjson):
    course = loaders.load_course(TEST101 / FS.cset)
    res = loaders.load_page(TEST101 / FS.get_intro("W01"), course, mdjson)
    assert res.itype == "Page"
    assert res.path == "pages"
    assert res.body_name == "body"
    assert res.param == "wiki_page"
    assert res.id_name == "url"
    assert res.content_name == "page_url"
    assert res.title == page_example.title
    assert res.body == page_example.body


def test_load_disc(disc_example, mdjson):
    course = loaders.load_course(TEST101 / FS.cset)
    discpath = TEST101 / FS.get_disc("W01")
    res = loaders.load_disc(discpath, course, mdjson)
    assert res.itype == "Discussion"
    assert res.path == "discussion_topics"
    assert res.body_name == "message"
    assert res.param == None
    assert res.id_name == "id"
    assert res.content_name == "content_id"
    assert res.title == disc_example.title
    assert res.body == disc_example.body
    assert res.get_settings() == disc_example.get_settings()


def test_load_quiz(quiz_example, mdjson):
    course = loaders.load_course(TEST101 / FS.cset, TEST101 / FS.qdesc)
    quizpath = TEST101 / FS.get_quiz("W01")
    res = loaders.load_quiz(quizpath, course, mdjson)
    assert res.itype == "Quiz"
    assert res.path == "quizzes"
    assert res.body_name == "description"
    assert res.param == "quiz"
    assert res.id_name == "id"
    assert res.content_name == "content_id"
    assert res.title == quiz_example.title
    assert res.body == quiz_example.body
    assert res.get_settings() == quiz_example.get_settings()
    assert len(res.questions) == len(quiz_example.questions)
    for idx in range(len(res.questions)):
        resQQ = res.questions[idx]
        checkQQ = quiz_example.questions[idx]
        assert resQQ.question == checkQQ.question
        assert resQQ.correct == checkQQ.correct
        assert resQQ.incorrect == checkQQ.incorrect
