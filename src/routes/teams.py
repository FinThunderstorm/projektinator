import os
from flask import redirect, render_template, request, session, abort, flash
from app import app
from services.feature_service import feature_service
from services.user_service import user_service
from services.team_service import team_service
from services.task_service import task_service
from utils.exceptions import NotExistingException, UsernameDuplicateException, ValueShorterThanException, EmptyValueException, DatabaseException, UnvalidInputException

baseUrl = "/teams"


@app.route(f"{baseUrl}", methods=["GET"])
def teams():
    try:
        teams = team_service.get_all()
    except NotExistingException as error:
        teams = []
    except DatabaseException as error:
        flash(str(error), 'is-danger')
        return redirect("/")
    return render_template('teams/teams.html', teams=teams)


@app.route(f"{baseUrl}/<uuid:team_id>", methods=["GET", "POST"])
def team(team_id):
    # GET shows task
    if request.method == "GET":
        team = team_service.get_by_id(team_id)
        print(team.members)
        return render_template('teams/teams_team.html', team=team)

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
            flash(f'Saved team {updated_task.task_id} successfully',
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
def create_team():
    # GET shows creation page
    if request.method == "GET":
        users = user_service.get_users()
        return render_template('teams/teams_add.html', users=users)

    # POST creates new task
    if request.method == "POST":
        try:
            new_team = team_service.new(request.form['name'],
                                        request.form['description'],
                                        request.form['team_leader'])
            for member in request.form.getlist('members'):
                added = team_service.add_member(new_team.team_id, member)
            flash(f'New team {new_team.team_id} created successfully',
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


@app.route(f"{baseUrl}/remove", methods=["POST"])
def remove_team():
    try:
        team_service.remove(request.form['team_id'])
        flash(f'Team with id {request.form["team_id"]} removed successfully',
              'is-success')
        return redirect(baseUrl)
    except NotExistingException as error:
        flash(str(error), 'is-danger')
        return redirect(baseUrl)
    except DatabaseException as error:
        flash(str(error), 'is-danger')
        return redirect(baseUrl)