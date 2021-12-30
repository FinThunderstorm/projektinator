import os
from flask import redirect, render_template, request, session, abort, flash
from app import app
from services.user_service import user_service
from utils.exceptions import LoginException

baseUrl = "/users"


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


@app.route(f"{baseUrl}", methods=["GET"])
def users_management():
    return redirect("/")


@app.route(f"{baseUrl}/<uuid:user_id>", methods=["GET", "POST"])
def show_user():
    # GET shows profile
    if request.method == "GET":
        return redirect("/")

    # POST updates profile
    if request.method == "POST":
        return redirect("/")


@app.route(f"{baseUrl}/create", methods=["GET", "POST"])
def create_user():
    # GET shows creation page
    if request.method == "GET":
        user_service.new("teppo", 1, "teppo", "Teppo", "Matti",
                         "teppo@mattiteppo.fi")
        return redirect("/")

    # POST creates new user
    if request.method == "POST":
        return redirect("/")