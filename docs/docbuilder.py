import subprocess
import sys

from bs4 import BeautifulSoup


tpl = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <link rel="stylesheet" href="{styles}">
  </head>
  <body>
    {topline}
    {body}
  </body>
</html>"""

topline = '<p><a id="topline" href="index.html">Home</a></p>'


def gethtml(text):
    cmd = ["pandoc", "-f", "markdown", "-t", "html", "--wrap=none"]
    btext = str.encode(text)
    res = subprocess.run(cmd, input=btext, capture_output=True, check=True)
    return res.stdout.decode("utf-8")


def build_docs(in_file, out_file, css):
    with open(in_file) as f:
        md = f.read()
    body = BeautifulSoup(gethtml(md), "html.parser")
    title = body.h1.text
    if "index.md" in in_file:
        res = tpl.format(title=title, body=body, styles=css, topline="").strip()
    else:
        res = tpl.format(
            title=title, body=body, styles=css, topline=topline
        ).strip()
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(res)


build_docs(sys.argv[1], sys.argv[2], sys.argv[3])
