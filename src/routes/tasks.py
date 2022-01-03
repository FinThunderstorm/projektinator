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
        tasks = task_service.get_all()
        for task in tasks:
            print(task)
    except NotExistingException as error:
        tasks = []
    except DatabaseException as error:
        flash(str(error), 'is-danger')
        return redirect("/")
    return render_template('tasks/tasks.html', tasks=tasks)


@app.route(f"{baseUrl}/<uuid:task_id>", methods=["GET", "POST"])
def view_task(task_id):
    task = task_service.get_by_id(task_id)
    return render_template('tasks/tasks_view.html', task=task)


@app.route(f"{baseUrl}/edit/<uuid:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    # GET shows task
    if request.method == "GET":
        task = task_service.get_by_id(task_id)
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
        task = task_service.get_by_id(request.form['task_id'])
        try:
            updated_task = task_service.update(
                request.form['task_id'], request.form['feature_id'],
                request.form['assignee_id'], request.form['name'],
                request.form['description'], request.form['status'],
                request.form['task_type'], request.form['priority'],
                request.form['flags'])
            flash(f'Saved task {updated_task.task_id} successfully',
                  'is-success')
            return redirect(baseUrl)
        except NotExistingException as error:
            flash(str(error), 'is-danger')
            return redirect(baseUrl)
        except EmptyValueException as error:
            flash(str(error), 'is-danger')
            return redirect(baseUrl)
        except UnvalidInputException as error:
            flash(str(error), 'is-danger')
            return redirect(baseUrl)
        except DatabaseException as error:
            flash(str(error), 'is-danger')
            return redirect(baseUrl)


@app.route(f"{baseUrl}/add", methods=["GET", "POST"])
def create_task():
    # GET shows creation page
    if request.method == "GET":
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
        try:
            new_task = task_service.new(
                request.form['feature_id'], request.form['assignee_id'],
                request.form['name'], request.form['description'],
                request.form['status'], request.form['task_type'],
                request.form['priority'], request.form['flags'])
            flash(f'New tasks {new_task.task_id} created successfully',
                  'is-success')
            return redirect(baseUrl)
        except NotExistingException as error:
            flash(str(error), 'is-danger')
            return redirect(baseUrl)
        except EmptyValueException as error:
            flash(str(error), 'is-danger')
            return redirect(baseUrl)
        except UnvalidInputException as error:
            flash(str(error), 'is-danger')
            return redirect(baseUrl)
        except DatabaseException as error:
            flash(str(error), 'is-danger')
            return redirect(baseUrl)


@app.route(f"{baseUrl}/remove/<uuid:task_id>", methods=["POST"])
def remove_task(task_id):
    try:
        task_service.remove(task_id)
        flash(f'Task with id {task_id} removed successfully', 'is-success')
        return redirect(baseUrl)
    except NotExistingException as error:
        flash(str(error), 'is-danger')
        return redirect(baseUrl)
    except DatabaseException as error:
        flash(str(error), 'is-danger')
        return redirect(baseUrl)