import os
from flask import redirect, render_template, request, session, abort, flash
from app import app
from services.user_service import user_service
from utils.exceptions import LoginException

baseUrl = "/projects"


@app.route(f"{baseUrl}/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    try:
        uid = user_service.login(username, password)
        session["user"] = uid
        session["token"] = os.urandom(16).hex()
    except LoginException as error:
        flash(error.message, "is-danger")

    return redirect("/")


@app.route(f"{baseUrl}/logout", methods=["GET"])
def logout():
    del session["user"]
    del session["token"]
    return redirect("/")
