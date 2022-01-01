import os
from flask import redirect, render_template, request, session, abort, flash
from app import app
from services.feature_service import feature_service
from services.project_service import project_service
from services.user_service import user_service
from utils.exceptions import NotExistingException, UsernameDuplicateException, ValueShorterThanException, EmptyValueException, DatabaseException, UnvalidInputException

baseUrl = "/features"


@app.route(f"{baseUrl}", methods=["GET"])
def features():
    try:
        features = feature_service.get_all()
    except NotExistingException as error:
        features = []
    except DatabaseException as error:
        flash(error.message, 'is-danger')
        return redirect("/")
    return render_template('features/features.html', features=features)


@app.route(f"{baseUrl}/<uuid:feature_id>", methods=["GET", "POST"])
def feature(feature_id):
    # GET shows feature
    if request.method == "GET":
        feature = feature_service.get_by_id(feature_id)
        return render_template('features/features_feature.html',
                               feature=feature)

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


@app.route(f"{baseUrl}/add", methods=["GET", "POST"])
def create_feature():
    # GET shows creation page
    if request.method == "GET":
        users = user_service.get_users()
        projects = project_service.get_projects()
        return render_template('features/features_add.html',
                               users=users,
                               projects=projects)

    # POST creates new feature
    if request.method == "POST":
        try:
            new_feature = feature_service.new(
                request.form['project'], request.form['feature_owner'],
                request.form['name'], request.form['description'],
                request.form['status'], request.form['feature_type'],
                request.form['priority'], request.form['flags'])
            flash(f'New feature {new_feature.feature_id} created successfully',
                  'is-success')
            return redirect(baseUrl)
        except NotExistingException as error:
            flash(error.message, 'is-danger')
            return redirect(baseUrl)
        except EmptyValueException as error:
            flash(error.message, 'is-danger')
            return redirect(baseUrl)
        except UnvalidInputException as error:
            flash(error.message, 'is-danger')
            return redirect(baseUrl)
        except DatabaseException as error:
            flash(error.message, 'is-danger')
            return redirect(baseUrl)


@app.route(f"{baseUrl}/remove", methods=["POST"])
def remove_feature():
    try:
        feature_service.remove(request.form['feature_id'])
        flash(
            f'Feature with id {request.form["feature_id"]} removed successfully',
            'is-success')
        return redirect(baseUrl)
    except NotExistingException as error:
        flash(error.message, 'is-danger')
        return redirect(baseUrl)
    except DatabaseException as error:
        flash(error.message, 'is-danger')
        return redirect(baseUrl)