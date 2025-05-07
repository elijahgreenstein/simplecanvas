# Simple Canvas

Simple Canvas is a Python library that enables instructors to quickly develop course materials and upload them to [Canvas LMS by Instructure](https://www.instructure.com/canvas) through API calls.

## Installation

Simple Canvas requires installations of [Python](https://www.python.org) and [Pandoc](https://pandoc.org). First install Python and Pandoc. Then clone this repository, change the working directory to `simplecanvas`, and use `pip` to install Simple Canvas:

```
git clone https://github.com/elijahgreenstein/simplecanvas.git
cd simplecanvas
pip install .
```

`pip` will also install the following dependencies:

- `jinja2` ([Jinja](https://jinja.palletsprojects.com/en/stable/))
- `requests` ([Requests](https://docs.python-requests.org/en/latest/index.html))
- `pyyaml` ([PyYAML](https://pyyaml.org))

## Command line interface

To set up a new course, select a directory for your courses and make it the current working directory. Then type the following and press `enter`:

```
python -m simplecanvas newcourse TEST101
```

Answer the prompts that follow to set up a new course in `TEST101`. To set up a new module in your course, enter the following commands:

```
cd TEST101
python -m simplecanvas addmod Week01
```

Answer the prompts and Simple Canvas will create a directory with files for an introduction page, quiz, and discussion board. Edit the pages in `TEST101/Week01` (`intro.md`, `quiz.yaml`, and `disc.md`). To upload the module contents to Canvas, type the following and press `enter`:

```
python -m simplecanvas upmod Week01
```

Simple Canvas will create a new module in Canvas, convert the content in `TEST101/Week01` to HTML, and upload that content to Canvas. It's that simple.
