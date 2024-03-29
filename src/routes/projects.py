from flask import redirect, render_template, request, session, abort, flash
from app import app
from services.project_service import project_service
from services.user_service import user_service
from utils.exceptions import UnvalidInputException, NotExistingException, EmptyValueException, DatabaseException

base_url = '/projects'


@app.route(f'{base_url}', methods=['GET'])
def projects():
    try:
        all_projects = project_service.get_all()
    except DatabaseException as error:
        flash(str(error), 'is-danger')
        return redirect(base_url)

    return render_template('projects/projects.html', projects=all_projects)


@app.route(f'{base_url}/<uuid:project_id>', methods=['GET'])
def view_project(project_id):
    try:
        project = project_service.get_by_id(project_id)
        project_owner_profile_image = user_service.get_profile_image(
            project.project_owner_id)
    except (NotExistingException, UnvalidInputException,
            DatabaseException) as error:
        flash(str(error), 'is-danger')
        return redirect(base_url)

    return render_template(
        'projects/projects_view.html',
        project=project,
        project_owner_profile_image=project_owner_profile_image)


@app.route(f'{base_url}/edit/<uuid:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    try:
        project = project_service.get_by_id(project_id)

        if (project.project_owner_id != session['user']
                and session['user_role'] < 3) or session['user_role'] < 3:
            flash('Not enough permissions.', 'is-danger')
            return redirect('/')

        # GET shows edit page
        if request.method == 'GET':
            if session['user_role'] == 1:
                try:
                    users = user_service.get_team_users(session['team_id'])
                except (UnvalidInputException, NotExistingException):
                    users = [(session['user'], session['username'],
                              user_service.get_profile_image(session['user']))]
            else:
                users = user_service.get_users()

            return render_template('projects/projects_edit.html',
                                   project=project,
                                   users=users)
        # POST updates project
        if request.method == 'POST':
            if session['token'] != request.form['token']:
                abort(403)

            project_service.update(request.form['project_id'],
                                   request.form['project_owner'],
                                   request.form['name'],
                                   request.form['description'],
                                   request.form['flags'])
            flash(f'Saved project {project.project_id} successfully',
                  'is-success')
            return redirect(base_url)

    except (NotExistingException, UnvalidInputException, DatabaseException,
            EmptyValueException) as error:
        flash(str(error), 'is-danger')
        return redirect(base_url)


@app.route(f'{base_url}/add', methods=['GET', 'POST'])
def create_project():
    try:
        # GET shows creation page
        if request.method == 'GET':

            if session['user_role'] == 1:
                try:
                    users = user_service.get_team_users(session['team_id'])
                except (UnvalidInputException, NotExistingException):
                    users = [(session['user'], session['username'],
                              user_service.get_profile_image(session['user']))]
            else:
                users = user_service.get_users()

            return render_template('projects/projects_add.html', users=users)

        # POST creates new project
        if request.method == 'POST':
            if session['token'] != request.form['token']:
                abort(403)

            new_project = project_service.new(request.form['project_owner'],
                                              request.form['name'],
                                              request.form['description'],
                                              request.form['flags'])

            flash(f'New project {new_project.project_id} created successfully',
                  'is-success')
            return redirect(base_url)

    except (NotExistingException, UnvalidInputException, DatabaseException,
            EmptyValueException) as error:
        flash(str(error), 'is-danger')
        return redirect(base_url)


@app.route(f'{base_url}/remove/<uuid:project_id>', methods=['GET'])
def remove_project(project_id):
    try:
        project = project_service.get_by_id(project_id)
        if (project.project_owner_id != session['user']
                and session['user_role'] < 3) or session['user_role'] < 3:
            flash('Not enough permissions.', 'is-danger')
            return redirect('/')

        project_service.remove(project_id)

        flash(f'Project with id {project_id} removed successfully',
              'is-success')
        return redirect(base_url)

    except (NotExistingException, UnvalidInputException,
            DatabaseException) as error:
        flash(str(error), 'is-danger')
        return redirect(base_url)
