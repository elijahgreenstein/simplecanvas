import pathlib

import pytest

from simplecanvas import util

DATADIR = pathlib.Path(__file__).parent / "data"


@pytest.fixture
def md_example():
    return """---
title: "A Markdown example"
---

# Level 1 heading

Some content goes here.

## Level 2 heading

- List 1
- List 2

## Level 2 heading

1. Enumerated 1
2. Enumerated 2

### Level 3 heading

More content here.
"""


@pytest.fixture
def html_from_md():
    return """<h2 id="level-1-heading">Level 1 heading</h2>
<p>Some content goes here.</p>
<h3 id="level-2-heading">Level 2 heading</h3>
<ul>
<li>List 1</li>
<li>List 2</li>
</ul>
<h3 id="level-2-heading-1">Level 2 heading</h3>
<ol type="1">
<li>Enumerated 1</li>
<li>Enumerated 2</li>
</ol>
<h4 id="level-3-heading">Level 3 heading</h4>
<p>More content here.</p>
"""


def test_md2html(md_example, html_from_md):
    res = util.md2html(md_example)
    assert html_from_md == res


def test_get_meta(md_example):
    res = util.get_meta(md_example, str(DATADIR / "metadata.json"))
    assert res["title"] == "A Markdown example"
