import os
from flask import redirect, render_template, request, session, abort, flash
from app import app
from services.feature_service import feature_service
from services.user_service import user_service
from services.task_service import task_service
from services.type_service import type_service
from services.status_service import status_service
from utils.exceptions import NotExistingException, UsernameDuplicateException, ValueShorterThanException, EmptyValueException, DatabaseException, UnvalidInputException

baseUrl = "/tasks"


@app.route(f"{baseUrl}", methods=["GET"])
def tasks():
    try:
        all_tasks = task_service.get_all()
    except DatabaseException as error:
        flash(str(error), 'is-danger')
        return redirect("/")
    return render_template('tasks/tasks.html', tasks=all_tasks)


@app.route(f"{baseUrl}/<uuid:task_id>", methods=["GET", "POST"])
def view_task(task_id):
    try:
        task = task_service.get_by_id(task_id)
        assignee_profile_image = user_service.get_profile_image(
            task.assignee_id)
    except (NotExistingException, UnvalidInputException,
            DatabaseException) as error:
        flash(str(error), 'is-danger')
        return redirect(baseUrl)

    return render_template('tasks/tasks_view.html',
                           task=task,
                           assignee_profile_image=assignee_profile_image)


@app.route(f"{baseUrl}/edit/<uuid:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    try:
        task = task_service.get_by_id(task_id)

        if task.assignee_id != session["user"] or session["user_role"] < 2:
            flash("Not enough permissions.", 'is-danger')
            return redirect("/")

        # GET shows task
        if request.method == "GET":
            if session["user_role"] == 1:
                users = user_service.get_team_users(session["team_id"])
                if len(users) == 0:
                    users = [(session["user"], session["username"])]
            else:
                users = user_service.get_users()
            features = feature_service.get_features()
            statuses = status_service.get_all()
            types = type_service.get_all()

            return render_template('tasks/tasks_edit.html',
                                   task=task,
                                   users=users,
                                   features=features,
                                   statuses=statuses,
                                   types=types)

        # POST updates task
        if request.method == "POST":
            if session["token"] != request.form["token"]:
                abort(403)

            updated_task = task_service.update(
                request.form['task_id'], request.form['feature_id'],
                request.form['assignee_id'], request.form['name'],
                request.form['description'], request.form['status'],
                request.form['task_type'], request.form['priority'],
                request.form['flags'])

            flash(f'Saved task {updated_task.task_id} successfully',
                  'is-success')
            return redirect(baseUrl)

    except (NotExistingException, EmptyValueException, UnvalidInputException,
            DatabaseException) as error:
        flash(str(error), 'is-danger')
        return redirect(baseUrl)


@app.route(f"{baseUrl}/add", methods=["GET", "POST"])
def create_task():
    try:
        # GET shows creation page
        if request.method == "GET":
            if session["user_role"] == 1:
                users = user_service.get_team_users(session["team_id"])
                if len(users) == 0:
                    users = [(session["user"], session["username"])]
            else:
                users = user_service.get_users()
            features = feature_service.get_features()
            statuses = status_service.get_all()
            types = type_service.get_all()

            return render_template('tasks/tasks_add.html',
                                   users=users,
                                   features=features,
                                   statuses=statuses,
                                   types=types)

        # POST creates new task
        if request.method == "POST":
            if session["token"] != request.form["token"]:
                abort(403)

            new_task = task_service.new(
                request.form['feature_id'], request.form['assignee_id'],
                request.form['name'], request.form['description'],
                request.form['status'], request.form['task_type'],
                request.form['priority'], request.form['flags'])

            flash(f'New tasks {new_task.task_id} created successfully',
                  'is-success')
            return redirect(baseUrl)

    except (NotExistingException, EmptyValueException, UnvalidInputException,
            DatabaseException) as error:
        flash(str(error), 'is-danger')
        return redirect(baseUrl)


@app.route(f"{baseUrl}/remove/<uuid:task_id>", methods=["POST"])
def remove_task(task_id):
    try:
        task = task_service.get_by_id(task_id)

        if task.assignee_id != session["user"] or session["user_role"] < 2:
            flash("Not enough permissions.", 'is-danger')
            return redirect("/")

        task_service.remove(task_id)

        flash(f'Task with id {task_id} removed successfully', 'is-success')
        return redirect(baseUrl)

    except (NotExistingException, UnvalidInputException,
            DatabaseException) as error:
        flash(str(error), 'is-danger')
        return redirect(baseUrl)
