import os
from flask import redirect, render_template, request, session, abort, flash
from app import app
from services.feature_service import feature_service
from services.task_service import task_service
from services.comment_service import comment_service
from services.user_service import user_service
from utils.exceptions import NotExistingException, UsernameDuplicateException, ValueShorterThanException, EmptyValueException, DatabaseException, UnvalidInputException

baseUrl = "/comments"


@app.route(f"{baseUrl}", methods=["GET"])
def comments():
    try:
        features = feature_service.get_all()
    except NotExistingException as error:
        features = []
    except DatabaseException as error:
        flash(error.message, 'is-danger')
        return redirect("/")
    return render_template('comments/comments.html', features=features)


@app.route(f"{baseUrl}/<uuid:comment_id>", methods=["GET", "POST"])
def comment(comment_id):
    # GET shows feature
    if request.method == "GET":
        feature = feature_service.get_by_id(comment_id)
        task = task_service.get_by_id(comment_id)
        return render_template('comments/comments_comment.html',
                               feature=feature,
                               task=task)

    # POST updates feature
    if request.method == "POST":
        feature = feature_service.get_by_id(request.form["feature_id"])
        try:
            updated_feature = feature_service.update(
                request.form['feature_id'], request.form['project_id'],
                request.form['feature_owner_id'], request.form['name'],
                request.form['description'], request.form['flags'],
                request.form['status'], request.form['feature_type'],
                request.form['priority'])
            flash(f'Saved feature {updated_feature.feature_id} successfully',
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


@app.route(f"{baseUrl}/add/feature/<uuid:feature_id>", methods=["GET", "POST"])
def create_feature_comment(feature_id):
    # GET shows creation page
    if request.method == "GET":
        feature_name = feature_service.get_name(feature_id)
        return render_template('comments/comments_add.html',
                               feature_id=feature_id,
                               feature_name=feature_name,
                               task_id=None,
                               task_name=None)

    # POST creates new comment for feature
    if request.method == "POST":
        try:
            new_comment = comment_service.new(request.form['assignee'],
                                              request.form['comment'],
                                              request.form['tspent'],
                                              fid=request.form['feature_id'])
            flash(f'New comment {new_comment.comment_id} created successfully',
                  'is-success')
            return redirect(f'/features/{request.form["feature_id"]}')
        except NotExistingException as error:
            flash(error.message, 'is-danger')
            return redirect(f'/features/{request.form["feature_id"]}')
        except EmptyValueException as error:
            flash(error.message, 'is-danger')
            return redirect(f'/features/{request.form["feature_id"]}')
        except UnvalidInputException as error:
            flash(error.message, 'is-danger')
            return redirect(f'/features/{request.form["feature_id"]}')
        except DatabaseException as error:
            flash(error.message, 'is-danger')
            return redirect(f'/features/{request.form["feature_id"]}')


@app.route(f"{baseUrl}/add/task/<uuid:task_id>", methods=["GET", "POST"])
def create_task_comment(task_id):
    # GET shows creation page
    if request.method == "GET":
        task_name = task_service.get_name(task_id)
        return render_template('comments/comments_add.html',
                               feature_id=None,
                               feature_name=None,
                               task_id=task_id,
                               task_name=task_name)

    # POST creates new comment for task
    if request.method == "POST":
        try:
            new_comment = comment_service.new(request.form['assignee'],
                                              request.form['comment'],
                                              request.form['tspent'],
                                              tid=request.form['task_id'])
            flash(f'New comment {new_comment.comment_id} created successfully',
                  'is-success')
            return redirect(f'/tasks/{request.form["task_id"]}')
        except NotExistingException as error:
            flash(error.message, 'is-danger')
            return redirect(f'/tasks/{request.form["task_id"]}')
        except EmptyValueException as error:
            flash(error.message, 'is-danger')
            return redirect(f'/tasks/{request.form["task_id"]}')
        except UnvalidInputException as error:
            flash(error.message, 'is-danger')
            return redirect(f'/tasks/{request.form["task_id"]}')
        except DatabaseException as error:
            flash(error.message, 'is-danger')
            return redirect(f'/tasks/{request.form["task_id"]}')


@app.route(f"{baseUrl}/remove", methods=["POST"])
def remove_comment():
    try:
        comment_service.remove(request.form['comment_id'])
        flash(
            f'Comment with id {request.form["comment_id"]} removed successfully',
            'is-success')
        return redirect(request.form['came_from'])
    except NotExistingException as error:
        flash(error.message, 'is-danger')
        return redirect(request.form['came_from'])
    except DatabaseException as error:
        flash(error.message, 'is-danger')
        return redirect(request.form['came_from'])