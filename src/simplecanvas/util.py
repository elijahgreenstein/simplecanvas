from pathlib import Path

class DirStructure:

    def __init__(self):
        self.course = Path("_conf")
        self.mod = Path("modules")
        self.tpl = Path("templates")


class UserInput:

    def __init__(self):
        self.course = {
            "token": "> Enter API token: ",
            "course_url": "> Enter API URL: ",
            "course_id": "> Enter course unique identifier: ",
            "unlock_at": "> Enter quiz unlock time: ",
            "due_at": "> Enter quiz deadline: ",
            "lock_at": "> Enter quiz lock time: ",
        }
        self.mod = {
            "title": "> Enter module title: ",
            "position": "> Enter module position: ",
            "prefix": "> Enter module prefix: ",
            "date": "> Enter quiz date: ",
        }


class Logger:

    def __init__(self, verbosity):
        self.verbosity = verbosity
        self.msgs = {
            "newcourse": "Creating new course: '{course}'",
            "addmod": "Adding a module: '{mod}'",
            "create_dir": "- Creating directories:",
            "create_files": "- Creating files from templates:",
            "create": "    - {name}",
        }

    def log(self, level, message):
        if self.verbosity >= level:
            print(message)
        else:
            pass
