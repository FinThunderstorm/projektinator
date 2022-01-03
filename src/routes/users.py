import os
from flask import redirect, render_template, request, session, abort, flash
from app import app
from services.user_service import user_service
from utils.exceptions import LoginException, UsernameDuplicateException, ValueShorterThanException, EmptyValueException, DatabaseException

baseUrl = "/users"


@app.route(f"{baseUrl}/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    try:
        uid, fullname = user_service.login(username, password)
        session["user"] = uid
        session["username"] = fullname
        session["token"] = os.urandom(16).hex()
    except LoginException as error:
        flash(str(error), "is-danger")

    return redirect("/")


@app.route(f"{baseUrl}/logout", methods=["GET"])
def logout():
    del session["user"]
    del session["token"]
    return redirect("/")


@app.route(f"{baseUrl}", methods=["GET"])
def users():
    users = user_service.get_all()
    return render_template('users/users.html', users=users)


@app.route(f"{baseUrl}/<uuid:user_id>", methods=["GET", "POST"])
def user(user_id):
    # GET shows profile
    if request.method == "GET":
        user = user_service.get_by_id(user_id)
        return render_template('users/users_user.html', user=user)

    # POST updates profile
    if request.method == "POST":
        user = user_service.get_by_id(request.form['user_id'])
        try:
            user_service.update(request.form['user_id'],
                                request.form['username'],
                                int(request.form['user_role']),
                                request.form['password'],
                                request.form['firstname'],
                                request.form['lastname'], request.form['email'],
                                request.form['profile_image'])
            flash(f'Saved user {user.user_id} successfully', 'is-success')
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


@app.route(f"{baseUrl}/add", methods=["GET", "POST"])
def create_user():
    # GET shows creation page
    if request.method == "GET":
        return render_template("users/users_add.html")

    # POST creates new user
    if request.method == "POST":
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
            print('f')
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


@app.route(f"{baseUrl}/remove", methods=["POST"])
def remove_user():
    try:
        user_service.remove(request.form["user_id"])
        flash(f"User with id {request.form['user_id']} removed successfully",
              "is-success")
        return redirect(baseUrl)
    except Exception as error:
        flash(str(error), 'is-danger')
        return redirect(baseUrl)