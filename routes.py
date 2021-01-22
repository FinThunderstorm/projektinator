from app import app
import os
from flask import redirect, render_template, request, session, abort
import queries


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/projects")
def list_projects():
    projects = queries.get_project()
    return render_template("projects.html", projects=projects)


@app.route("/projects/new", methods=["GET", "POST"])
def new_project():
    if request.method == "GET":
        return render_template("projects_new.html")
    if request.method == "POST":
        if session["token"] != request.form["token"]:
            abort(403)
        name = request.form["name"]
        description = request.form["description"]
        flags = request.form["flags"]
        if queries.add_project(name, description, flags):
            return redirect("/projects")
        else:
            return "error"


@app.route("/projects/remove/<int:id>", methods=["POST"])
def remove_project(id):
    if session["token"] != request.form["token"]:
        abort(403)
    if queries.remove_project(id):
        return redirect("/projects")
    else:
        return "error"


@app.route("/projects/<int:id>", methods=["GET", "POST"])
def update_project(id):
    if request.method == "GET":
        project = queries.get_project(id)
        if project == None:
            return redirect("/projects")
        else:
            return render_template("project_info.html", project=project)
    if request.method == "POST":
        if session["token"] != request.form["token"]:
            abort(403)
        name = request.form["name"]
        description = request.form["description"]
        flags = request.form["flags"]
        added_on = request.form["added_on"]
        print('project_id', id)
        if queries.update_project(id, name, description, flags, added_on):
            return redirect("/projects/" + id)
        else:
            return "error"


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    result = queries.login(username, password)
    if result == None:
        return "error"
    else:
        session["user"] = result
        session["token"] = os.urandom(16).hex()
        return redirect("/")


@app.route("/logout")
def logout():
    del session["user"]
    del session["token"]
    return redirect("/")


@app.route("/settings/users")
def users():
    users = queries.get_all_users()
    return render_template("settings_users.html", users=users)


@app.route("/settings/users/modify/<int:id>", methods=["GET", "POST"])
def modify_user(id):
    if request.method == "GET":
        user = queries.find_user(id)
        if user != None:
            return render_template("settings_users_modify.html", user=user)
        else:
            return redirect("/settings/users")
    if request.method == "POST":
        if session["token"] != request.form["token"]:
            abort(403)
        username = request.form["username"]
        password = request.form["password"]
        name = request.form["name"]
        email = request.form["email"]
        user_role = request.form["user_role"]
        if queries.update_user(id, username, user_role, password, name, email):
            return redirect("/settings/users/modify/" + id)
        else:
            return "error"


@app.route("/settings/users/remove/<int:id>", methods=["POST"])
def remote_user(id):
    if session["token"] != request.form["token"]:
        abort(403)
    if queries.remove_user(id):
        return redirect("/settings/users")
    else:
        return "error"


@app.route("/settings/users/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("settings_users_register.html")
    if request.method == "POST":
        if session["token"] != request.form["token"]:
            abort(403)
        username = request.form["username"]
        password = request.form["password"]
        name = request.form["name"]
        email = request.form["email"]
        user_role = int(request.form["user_role"])
        if queries.add_user(username, password, name, email, user_role):
            return redirect("/settings/users")
        else:
            return "error"
