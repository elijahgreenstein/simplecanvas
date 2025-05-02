import pytest

from simplecanvas import cli

class TestGeneral:

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
