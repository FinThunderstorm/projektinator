from flask import redirect, render_template, request, session, abort, flash
from app import app
from services.feature_service import feature_service
from services.project_service import project_service
from services.status_service import status_service
from services.type_service import type_service
from services.user_service import user_service
from services.statistics_service import statistics_service
from utils.exceptions import NotExistingException, EmptyValueException, DatabaseException, UnvalidInputException

base_url = '/features'


@app.route(f'{base_url}', methods=['GET'])
def features():
    try:
        all_features = feature_service.get_all()
    except DatabaseException as error:
        flash(str(error), 'is-danger')
        return redirect('/')

    return render_template('features/features.html', features=all_features)


@app.route(f'{base_url}/<uuid:feature_id>', methods=['GET'])
def view_feature(feature_id):
    try:
        feature = feature_service.get_by_id(feature_id)
        time_spent = statistics_service.get_time_spent_by_feature(feature_id)
        feature_owner_profile_image = user_service.get_profile_image(
            feature.feature_owner)
    except (NotExistingException, UnvalidInputException,
            DatabaseException) as error:
        flash(str(error), 'is-danger')
        return redirect(base_url)

    return render_template(
        'features/features_view.html',
        feature=feature,
        time_spent=time_spent,
        feature_owner_profile_image=feature_owner_profile_image)


@app.route(f'{base_url}/edit/<uuid:feature_id>', methods=['GET', 'POST'])
def edit_feature(feature_id):
    try:
        feature = feature_service.get_by_id(feature_id)

        if (feature.feature_owner != session['user']
                and session['user_role'] < 2) or session['user_role'] < 2:
            flash('Not enough permissions.', 'is-danger')
            return redirect('/')

        # GET shows feature
        if request.method == 'GET':
            if session['user_role'] == 1:
                try:
                    users = user_service.get_team_users(session['team_id'])
                except (UnvalidInputException, NotExistingException):
                    users = [(session['user'], session['username'],
                              user_service.get_profile_image(session['user']))]
            else:
                users = user_service.get_users()
            projects = project_service.get_projects()
            statuses = status_service.get_all()
            types = type_service.get_all()

            return render_template('features/features_edit.html',
                                   feature=feature,
                                   users=users,
                                   projects=projects,
                                   statuses=statuses,
                                   types=types)

        # POST updates feature
        if request.method == 'POST':
            if session['token'] != request.form['token']:
                abort(403)

            updated_feature = feature_service.update(
                request.form['feature_id'], request.form['project_id'],
                request.form['feature_owner_id'], request.form['name'],
                request.form['description'], request.form['flags'],
                request.form['status'], request.form['feature_type'],
                request.form['priority'])
            flash(f'Saved feature {updated_feature.feature_id} successfully',
                  'is-success')
            return redirect(base_url)

    except (NotExistingException, UnvalidInputException, DatabaseException,
            EmptyValueException) as error:
        flash(str(error), 'is-danger')
        return redirect(base_url)


@app.route(f'{base_url}/add', methods=['GET', 'POST'])
def create_feature():
    # GET shows creation page
    try:
        if request.method == 'GET':
            if session['user_role'] == 1:
                try:
                    users = user_service.get_team_users(session['team_id'])
                except (UnvalidInputException, NotExistingException):
                    users = [(session['user'], session['username'],
                              user_service.get_profile_image(session['user']))]
            else:
                users = user_service.get_users()
            projects = project_service.get_projects()
            statuses = status_service.get_all()
            types = type_service.get_all()

            return render_template('features/features_add.html',
                                   users=users,
                                   projects=projects,
                                   statuses=statuses,
                                   types=types)

        # POST creates new feature
        if request.method == 'POST':
            if session['token'] != request.form['token']:
                abort(403)

            new_feature = feature_service.new(
                request.form['project'], request.form['feature_owner'],
                request.form['name'], request.form['description'],
                request.form['status'], request.form['feature_type'],
                request.form['priority'], request.form['flags'])
            flash(f'New feature {new_feature.feature_id} created successfully',
                  'is-success')
            return redirect(base_url)

    except (NotExistingException, UnvalidInputException, DatabaseException,
            EmptyValueException) as error:
        flash(str(error), 'is-danger')
        return redirect(base_url)


@app.route(f'{base_url}/remove/<uuid:feature_id>', methods=['GET'])
def remove_feature(feature_id):
    try:
        feature = feature_service.get_by_id(feature_id)

        if (feature.feature_owner != session['user']
                and session['user_role'] < 2) or session['user_role'] < 2:
            flash('Not enough permissions.', 'is-danger')
            return redirect('/')

        feature_service.remove(feature_id)
        flash(f'Feature with id {feature_id} removed successfully',
              'is-success')
        return redirect(base_url)
    except (NotExistingException, UnvalidInputException,
            DatabaseException) as error:
        flash(str(error), 'is-danger')
        return redirect(base_url)
