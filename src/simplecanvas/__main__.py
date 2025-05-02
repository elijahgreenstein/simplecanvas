import argparse

from pathlib import Path

from .cli import newcourse, addmod, upmod


def main():
    pkgdir = Path(__file__).parent
    parser = argparse.ArgumentParser(
        prog="Simple Canvas",
        description="Create a course, add a module, or upload a module.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="increase verbosity level",
        action="count",
        default=0,
    )
    subparsers = parser.add_subparsers(required=True)
    parser_newcourse = subparsers.add_parser(
        "newcourse", help="create new course"
    )
    parser_newcourse.set_defaults(func=newcourse)
    parser_addmod = subparsers.add_parser("addmod", help="add module to course")
    parser_addmod.set_defaults(func=addmod)
    parser_upmod = subparsers.add_parser(
        "upmod", help="upload module to Canvas"
    )
    parser_upmod.set_defaults(func=upmod)
    parser.add_argument("name", help="name of the course or module")
    args = parser.parse_args()
    args.func(Path(args.name), pkgdir, args.verbose)


if __name__ == "__main__":
    main()
