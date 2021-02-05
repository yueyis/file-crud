import os
from collections import namedtuple
from flask import Flask, render_template, request, abort
from werkzeug.utils import redirect

import filehelpers as fh

app = Flask(__name__)


def _make_filepath(path):
    root_dir = "C:/tmp"
    return os.path.join(root_dir, path)

jottle_base_url = "/admin/update-query/"

def jottle_browse(path):
    File = namedtuple("File", "path_url name")
    dirs = []
    files = []
    parent, _ = os.path.split(path)

    for name in os.listdir(_make_filepath(path)):
        path_url = jottle_base_url + os.path.join(path, name)
        f = File(path_url, name)
        if os.path.isdir(_make_filepath(f.path_url[1:])):
            dirs.append(f)
        else:
            files.append(f)

    return render_template("jottle_browse.html", path=path, parent=parent, dirs=sorted(dirs), files=sorted(files))


def jottle_edit(path):
    with open(_make_filepath(path), 'r') as f:
        content = f.read()
    path_url = jottle_base_url + path
    return render_template("jottle_edit.html", content=content, path=path_url)


def jottle_view(path):

    with open(_make_filepath(path), 'r') as f:
        content = "<pre><code>{}</code></pre>".format(f.read())
    parent_url, filename = os.path.split(path)
    parent_url = jottle_base_url + parent_url
    file_url = jottle_base_url + path
    return render_template("jottle_view.html", content=content, parent_url=parent_url, file_url=file_url)


@app.route("/admin/update-query/", methods=["GET", "POST"])
@app.route("/admin/update-query/<path:path>", methods=["GET", "POST"])
def index(path="", access_role=("it")):
    filepath = _make_filepath(path)

    # parse POST request, used for simple file commands
    if request.method == "POST":
        if request.form['command'] == "make_file":
            fh.make_file(filepath, request.form['name'])

        elif request.form['command'] == "make_dir":
            fh.make_dir(filepath, request.form['name'])

        elif request.form['command'] == "rename":
            fh.rename(filepath, request.form['new_name'])

        elif request.form['command'] == "save":
            fh.save(filepath, request.form['text'])

        elif request.form['command'] == "delete_dir":
            fh.delete_dir(filepath)

        elif request.form['command'] == "delete_file":
            fh.delete_file(filepath)

        else:
            return "could not understand POST request"
        return "done"

    # if directory then browse
    if os.path.isdir(filepath):
        return jottle_browse(path)

    # if not a directory and not a file then 404
    if not os.path.isfile(filepath):
        abort(404)

    # edit
    if "edit" in request.args:
        return jottle_edit(path)

    # view
    return jottle_view(path)


if __name__ == "__main__":
    app.run(debug=True)

