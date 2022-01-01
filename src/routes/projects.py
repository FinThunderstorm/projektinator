import os
from flask import redirect, render_template, request, session, abort, flash
from app import app
from services.project_service import project_service
from utils.exceptions import UnvalidInputException, NotExistingException, EmptyValueException, DatabaseException

baseUrl = "/projects"


@app.route(f"{baseUrl}", methods=["GET"])
def projects():
    projects = project_service.get_all()
    return render_template('projects/projects.html', projects=projects)


@app.route(f"{baseUrl}/<uuid:project_id>", methods=["GET", "POST"])
def project(project_id):
    # GET shows project
    if request.method == "GET":
        project = project_service.get_by_id(project_id)
        return render_template('projects/projects_project.html',
                               project=project)

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
        return render_template("projects/projects_add.html")

    # POST creates new project
    if request.method == "POST":
        try:
            new_project = project_service.new(request.form['project_owner'],
                                              request.form['name'],
                                              request.form['description'])
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


@app.route(f"{baseUrl}/remove", methods=["POST"])
def remove_project():
    try:
        project_service.remove(request.form['project_id'])
        flash(
            f'Project with id {request.form["project_id"]} removed successfully',
            'is-success')
        return redirect(baseUrl)
    except NotExistingException as error:
        flash(error.message, 'is-danger')
        return redirect(baseUrl)
    except DatabaseException as error:
        flash(error.message, 'is-danger')
        return redirect(baseUrl)
