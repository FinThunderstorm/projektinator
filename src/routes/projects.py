import os
from flask import redirect, render_template, request, session, abort, flash
from app import app
from services.project_service import project_service
from services.user_service import user_service
from utils.exceptions import UnvalidInputException, NotExistingException, EmptyValueException, DatabaseException

baseUrl = "/projects"


@app.route(f"{baseUrl}", methods=["GET"])
def projects():
    projects = project_service.get_all()
    return render_template('projects/projects.html', projects=projects)


@app.route(f"{baseUrl}/<uuid:project_id>", methods=["GET"])
def view_project(project_id):
    project = project_service.get_by_id(project_id)
    return render_template('projects/projects_view.html', project=project)


@app.route(f"{baseUrl}/edit/<uuid:project_id>", methods=["GET", "POST"])
def edit_project(project_id):
    if request.method == "GET":
        project = project_service.get_by_id(project_id)
        users = user_service.get_users()
        return render_template('projects/projects_edit.html',
                               project=project,
                               users=users)
    # POST updates project
    if request.method == "POST":
        project = project_service.get_by_id(request.form['project_id'])
        try:
            project_service.update(request.form['project_id'],
                                   request.form['project_owner_id'],
                                   request.form['name'],
                                   request.form['description'],
                                   request.form['flags'])
            flash(f'Saved project {project.project_id} successfully',
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


@app.route(f"{baseUrl}/add", methods=["GET", "POST"])
def create_project():
    # GET shows creation page
    if request.method == "GET":
        users = user_service.get_users()
        return render_template("projects/projects_add.html", users=users)

    # POST creates new project
    if request.method == "POST":
        try:
            new_project = project_service.new(request.form['project_owner'],
                                              request.form['name'],
                                              request.form['description'],
                                              request.form["flags"])
            flash(f'New project {new_project.project_id} created successfully',
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


@app.route(f"{baseUrl}/remove/<uuid:project_id>", methods=["GET"])
def remove_project(project_id):
    try:
        project_service.remove(project_id)
        flash(f'Project with id {project_id} removed successfully',
              'is-success')
        return redirect(baseUrl)
    except NotExistingException as error:
        flash(error.message, 'is-danger')
        return redirect(baseUrl)
    except DatabaseException as error:
        flash(error.message, 'is-danger')
        return redirect(baseUrl)
