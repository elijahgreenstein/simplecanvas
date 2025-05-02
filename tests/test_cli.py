import pytest

from simplecanvas import cli


@pytest.fixture
def user_input():
    user = {
        "course": {
            "token": "12345ABCDE",
            "course_url": "example/api",
            "course_id": "987",
            "unlock_at": "12:00:00",
            "due_at": "13:00:00",
            "lock_at": "14:00:00",
        },
        "mod": {
            "title": "Test module 1",
            "position": "3",
            "prefix": "1",
            "date": "2025-05-01",
        },
    }
    return user


class TestTemplates:

    @pytest.fixture
    def tpl_names_course(self):
        files = ["settings.yaml", "token", "quiz-desc.md"]
        return [f"_conf/{file}" for file in files]

    @pytest.fixture
    def tpl_names_module(self):
        files = ["_conf.yaml", "intro.md", "quiz.yaml", "disc.md"]
        return [f"modules/{file}" for file in files]

    def test_get_course_templates(self, tpl_names_course):
        for file in tpl_names_course:
            assert file in cli.get_template_paths_from("_conf")

    def test_get_module_templates(self, tpl_names_module):
        for file in tpl_names_module:
            assert file in cli.get_template_paths_from("modules")

    @pytest.fixture
    def rendered_course_settings(self):
        settings = '''course:
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
  lock_at: "14:00:00"'''
        return settings

    @pytest.fixture
    def rendered_course_token(self):
        return "12345ABCDE"

    def test_render_course_settings(self, user_input, rendered_course_settings):
        tpl = "_conf/settings.yaml"
        rendered = cli.render_template(tpl, user_input["course"])
        assert rendered_course_settings == rendered

    def test_render_course_token(self, user_input, rendered_course_token):
        tpl = "_conf/token"
        rendered = cli.render_template(tpl, user_input["course"])
        assert rendered_course_token == rendered
