from app import app
import os
from flask import redirect, render_template, request, session, abort, flash
from services.user_service import user_service
from utils.exceptions import LoginException


@app.route("/")
def index():
    # flash("Hello world!", "is-danger")
    return render_template("index.html")

# /users


@app.route("/users/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    try:
        uid = user_service.login(username, password)
        session["user"] = uid
        session["token"] = os.urandom(16).hex()
    except LoginException as error:
        print('failed')
        flash(error.message, "is-danger")

    return redirect("/")


@app.route("/users/logout", methods=["GET"])
def logout():
    del session["user"]
    del session["token"]
    return redirect("/")

# @app.get("/users/<string:username>")
# def get_by_username(username):
#     user_repository.get_by_username(username)
#     return render_template("index.html")
# @app.get("/users/new")
# def test_new():
#     user_repository.new('toot1234567', 1, "toot123", "Timothy",
#                         "Tei", "timothy@tei.com")
#     return render_template('index.html')
# @ app.route("/projects")
# def list_projects():
#     projects = queries.get_project()
#     return render_template("projects.html", projects=projects)
# @ app.route("/projects/new", methods=["GET", "POST"])
# def new_project():
#     if request.method == "GET":
#         return render_template("projects_new.html")
#     if request.method == "POST":
#         if session["token"] != request.form["token"]:
#             abort(403)
#         name = request.form["name"]
#         description = request.form["description"]
#         flags = request.form["flags"]
#         if queries.add_project(name, description, flags):
#             flash("Uusi projekti " + name + " lisätty onnistuneesti.",
#                   "is-success")
#             return redirect("/projects")
#         else:
#             flash("Virhe lisättäessä uutta projektia, yritä uudelleen.",
#                   "is-danger")
#             return redirect("/projects")
# @app.route("/projects/remove/<int:id>", methods=["POST"])
# def remove_project(id):
#     if session["token"] != request.form["token"]:
#         abort(403)
#     if id == None:
#         flash("Virhe poistettaessa projektia, yritä uudelleen.", "is-danger")
#         return redirect("/projects")
#     if queries.remove_project(id):
#         return redirect("/projects")
#     else:
#         flash("Virhe poistettaessa projektia, yritä uudelleen.", "is-danger")
#         return redirect("/projects")
# @app.route("/projects/<int:id>", methods=["GET", "POST"])
# def update_project(id):
#     if request.method == "GET":
#         if id == None:
#             return "is-danger"
#         project = queries.get_project(id)
#         if project == None:
#             return redirect("/projects")
#         else:
#             return render_template("project_info.html", project=project)
#     if request.method == "POST":
#         if session["token"] != request.form["token"]:
#             abort(403)
#         name = request.form["name"]
#         description = request.form["description"]
#         flags = request.form["flags"]
#         added_on = request.form["added_on"]
#         if queries.update_project(id, name, description, flags, added_on):
#             flash("Projekti " + name + " päivitetty onnistuneesti.",
#                   "is-success")
#             return redirect("/projects/" + str(id))
#         else:
#             flash("Virhe päivitettäessä projektia, yritä uudelleen.",
#                   "is-danger")
#             return redirect("/projects" + str(id))
# @app.route("/settings/users")
# def users():
#     users = queries.get_all_users()
#     return render_template("settings_users.html", users=users)
# @app.route("/settings/users/modify/<int:id>", methods=["GET", "POST"])
# def modify_user(id):
#     if request.method == "GET":
#         if id == None:
#             flash("Etsittyä käyttäjää ei löydy.", "is-danger")
#             return redirect("/settings/users")
#         user = queries.find_user(id)
#         if user == None:
#             flash("Etsittyä käyttäjää ei löydy.", "is-danger")
#             return redirect("/settings/users")
#         else:
#             return render_template("settings_users_modify.html", user=user)
#     if request.method == "POST":
#         if session["token"] != request.form["token"]:
#             abort(403)
#         username = request.form["username"]
#         password = request.form["password"]
#         name = request.form["name"]
#         email = request.form["email"]
#         user_role = request.form["user_role"]
#         if queries.update_user(id, username, user_role, password, name, email):
#             flash("Käyttäjän " + name + " tiedot päivitetty onnistuneesti.",
#                   "is-success")
#             return redirect("/settings/users/modify/" + str(id))
#         else:
#             flash("Käyttäjän tietojen päivittämisessä tapahtui virhe.",
#                   "is-danger")
#             return redirect("/settings/users/modify/" + str(id))
# @app.route("/settings/users/remove/<string:uid>", methods=["GET"])
# def remote_user(uid):
#     print(uid)
#     user_repository.remove(uid)
#     return render_template('index.html')
#     # if session["token"] != request.form["token"]:
#     #     abort(403)
#     # if id == None:
#     #     flash("Virhe poistettaessa käyttäjää.", "is-danger")
#     #     return redirect("/settings/users")
#     # if queries.remove_user(id):
#     #     flash("Käyttäjä poistettu onnistuneesti.", "is-success")
#     #     return redirect("/settings/users")
#     # else:
#     #     flash("Virhe poistettaessa käyttäjää.", "is-danger")
#     #     return redirect("/settings/users")
# @app.route("/settings/users/register", methods=["GET", "POST"])
# def register():
#     if request.method == "GET":
#         return render_template("settings_users_register.html")
#     if request.method == "POST":
#         if session["token"] != request.form["token"]:
#             abort(403)
#         username = request.form["username"]
#         password = request.form["password"]
#         name = request.form["name"]
#         email = request.form["email"]
#         user_role = int(request.form["user_role"])
#         if queries.add_user(username, password, name, email, user_role):
#             flash("Uusi käyttäjä " + name + " lisätty onnistuneesti.",
#                   "is-success")
#             return redirect("/settings/users")
#         else:
#             flash("Käyttäjää lisättäessä tapahtui virhe.", "is-danger")
#             return redirect("/settings/users")
