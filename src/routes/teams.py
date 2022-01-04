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


@app.route(f"{baseUrl}/<uuid:team_id>", methods=["GET"])
def view_team(team_id):
    team = team_service.get_by_id(team_id)
    team_leader_profile_image = user_service.get_profile_image(
        team.team_leader_id)
    return render_template('teams/teams_view.html',
                           team=team,
                           team_leader_profile_image=team_leader_profile_image)


@app.route(f"{baseUrl}/edit/<uuid:team_id>", methods=["GET", "POST"])
def edit_team(team_id):
    # GET shows task
    if request.method == "GET":
        team = team_service.get_by_id(team_id)
        users = user_service.get_users()
        return render_template('teams/teams_edit.html', team=team, users=users)

    # POST updates task
    if request.method == "POST":
        if session["token"] != request.form["token"]:
            abort(403)
        team = team_service.get_by_id(request.form['team_id'])
        try:
            updated_team = team_service.update(request.form['team_id'],
                                               request.form['name'],
                                               request.form['description'],
                                               request.form['team_leader'])
            flash(f'Saved team {updated_team.team_id} successfully',
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


@app.route(f"{baseUrl}/edit/<uuid:team_id>/members", methods=["GET", "POST"])
def edit_team_members(team_id):
    # GET shows task
    if request.method == "GET":
        team = team_service.get_by_id(team_id)
        teamusers = user_service.get_team_users(team_id)
        users = user_service.get_users()
        return render_template('teams/teams_members.html',
                               team=team,
                               teamusers=teamusers,
                               users=users)

    # POST updates task
    if request.method == "POST":
        if session["token"] != request.form["token"]:
            abort(403)
        team_id = request.form['team_id']
        teamusers = user_service.get_team_users(request.form['team_id'])
        teamusers_id = list(map(lambda x: str(x[0]), teamusers))
        try:
            wanted = request.form.getlist('members')
            to_be_added = filter(lambda x: x not in teamusers_id, wanted)
            to_be_removed = filter(lambda x: x not in wanted, teamusers_id)

            for user_id in to_be_added:
                result = team_service.add_member(team_id, user_id)
            for user_id in to_be_removed:
                result = team_service.remove_member(team_id, user_id)

            flash(f'Saved team successfully', 'is-success')
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
        if session["token"] != request.form["token"]:
            abort(403)
        try:
            new_team = team_service.new(request.form['name'],
                                        request.form['description'],
                                        request.form['team_leader'])
            for member in request.form.getlist('members'):
                added = team_service.add_member(new_team.team_id, member)
            if request.form['team_leader'] not in request.form.getlist(
                    'members'):
                team_service.add_member(new_team.team_id,
                                        request.form['team_leader'])
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