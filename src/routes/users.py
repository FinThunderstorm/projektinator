import os
from flask import redirect, render_template, request, session, abort, flash
from app import app
from services.user_service import user_service
from services.role_service import role_service
from utils.exceptions import UnvalidInputException, LoginException, UsernameDuplicateException, ValueShorterThanException, EmptyValueException, DatabaseException

baseUrl = "/users"


@app.route(f"{baseUrl}/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    try:
        uid, fullname, user_role = user_service.login(username, password)
        session["user"] = uid
        session["username"] = fullname
        session["user_role"] = user_role
        session["token"] = os.urandom(16).hex()
    except LoginException as error:
        flash(str(error), "is-danger")

    return redirect("/")


@app.route(f"{baseUrl}/logout", methods=["GET"])
def logout():
    del session["user"]
    del session["username"]
    del session["token"]
    return redirect("/")


@app.route(f"{baseUrl}", methods=["GET"])
def users():
    users = user_service.get_all()
    return render_template('users/users.html', users=users)


@app.route(f"{baseUrl}/<uuid:user_id>", methods=["GET", "POST"])
def view_user(user_id):
    user = user_service.get_by_id(user_id)
    return render_template('users/users_view.html', user=user)


@app.route(f"{baseUrl}/edit/<uuid:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    if user_id != session["user"] or session["user_role"] < 3:
        flash("Not enough permissions.", 'is-danger')
        return redirect("/")

    # GET shows profile editor
    if request.method == "GET":
        user = user_service.get_by_id(user_id)
        user_roles = role_service.get_all()
        return render_template('users/users_edit.html',
                               user=user,
                               user_roles=user_roles)

    # POST updates profile
    if request.method == "POST":
        if session["token"] != request.form["token"]:
            abort(403)
        user = user_service.get_by_id(request.form['user_id'])
        try:
            user_service.update(request.form['user_id'],
                                request.form['username'],
                                int(request.form['user_role']),
                                request.form['password'],
                                request.form['firstname'],
                                request.form['lastname'], request.form['email'],
                                "")
            profile_image = request.files["profile_image"]
            img_type = profile_image.content_type
            img_data = profile_image.read()

            user_service.update_profile_image(request.form['user_id'], img_type,
                                              img_data)

            flash(f'Saved user {user.user_id} successfully', 'is-success')
            return redirect(baseUrl)
        except UnvalidInputException as error:
            flash(str(error), 'is-danger')
            return redirect("/")
        except ValueShorterThanException as error:
            flash(str(error), 'is-danger')
            return redirect("/")
        except EmptyValueException as error:
            flash(str(error), 'is-danger')
            return redirect("/")
        except DatabaseException as error:
            flash(str(error), 'is-danger')
            return redirect("/")
        except UsernameDuplicateException as error:
            flash(str(error), 'is-danger')
            return redirect("/")


@app.route(f"{baseUrl}/add", methods=["GET", "POST"])
def create_user():
    if session["user_role"] < 3:
        flash("Not enough permissions.", 'is-danger')
        return redirect("/")

    # GET shows creation page
    if request.method == "GET":
        user_roles = role_service.get_all()
        return render_template("users/users_add.html", user_roles=user_roles)

    # POST creates new user
    if request.method == "POST":
        if session["token"] != request.form["token"]:
            abort(403)
        try:
            user_service.new(request.form["username"],
                             request.form["user_role"],
                             request.form["password"],
                             request.form["firstname"],
                             request.form["lastname"], request.form["email"])
            return redirect(baseUrl)
        except ValueShorterThanException as error:
            flash(str(error), 'is-danger')
            return redirect("/")
        except EmptyValueException as error:
            flash(str(error), 'is-danger')
            return redirect("/")
        except DatabaseException as error:
            flash(str(error), 'is-danger')
            return redirect("/")
        except UsernameDuplicateException as error:
            flash(str(error), 'is-danger')
            return redirect("/")


@app.route(f"{baseUrl}/register", methods=["GET", "POST"])
def register_user():
    # GET shows creation page
    if request.method == "GET":
        return render_template("users/users_register.html")

    # POST creates new user
    if request.method == "POST":
        try:
            user_service.new(request.form["username"], 1,
                             request.form["password"],
                             request.form["firstname"],
                             request.form["lastname"], request.form["email"])
            return redirect("/")
        except ValueShorterThanException as error:
            flash(str(error), 'is-danger')
            return redirect("/")
        except EmptyValueException as error:
            flash(str(error), 'is-danger')
            return redirect("/")
        except DatabaseException as error:
            flash(str(error), 'is-danger')
            return redirect("/")
        except UsernameDuplicateException as error:
            flash(str(error), 'is-danger')
            return redirect("/")
        except Exception as error:
            flash(str(error), 'is-danger')
            return redirect("")


@app.route(f"{baseUrl}/remove/<uuid:user_id>", methods=["GET"])
def remove_user(user_id):
    if user_id != session["user"] or session["user_role"] < 3:
        flash("Not enough permissions.", 'is-danger')
        return redirect("/")

    try:
        user_service.remove(user_id)
        flash(f"User with id {user_id} removed successfully", "is-success")
        return redirect(baseUrl)
    except Exception as error:
        flash(str(error), 'is-danger')
        return redirect(baseUrl)