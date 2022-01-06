from flask import redirect, render_template, request, session, abort, flash
from app import app
from services.user_service import user_service
from services.team_service import team_service
from utils.exceptions import NotExistingException, EmptyValueException, DatabaseException, UnvalidInputException

base_url = '/teams'


@app.route(f'{base_url}', methods=['GET'])
def teams():
    if session['user_role'] < 2:
        flash('Not enough permissions.', 'is-danger')
        return redirect('/')
    try:
        all_teams = team_service.get_all()
    except DatabaseException as error:
        flash(str(error), 'is-danger')
        return redirect('/')

    return render_template('teams/teams.html', teams=all_teams)


@app.route(f'{base_url}/<uuid:team_id>', methods=['GET'])
def view_team(team_id):
    try:
        team = team_service.get_by_id(team_id)
        team_leader_profile_image = user_service.get_profile_image(
            team.team_leader_id)
    except (NotExistingException, UnvalidInputException,
            DatabaseException) as error:
        flash(str(error), 'is-danger')
        return redirect(base_url)

    return render_template('teams/teams_view.html',
                           team=team,
                           team_leader_profile_image=team_leader_profile_image)


@app.route(f'{base_url}/edit/<uuid:team_id>', methods=['GET', 'POST'])
def edit_team(team_id):
    try:
        team = team_service.get_by_id(team_id)

        if (team.team_leader_id != session['user']
                and session['user_role'] < 3) or session['user_role'] < 3:
            flash('Not enough permissions.', 'is-danger')
            return redirect('/')

        # GET shows edit page
        if request.method == 'GET':
            users = user_service.get_users()
            return render_template('teams/teams_edit.html',
                                   team=team,
                                   users=users)

        # POST updates team
        if request.method == 'POST':
            if session['token'] != request.form['token']:
                abort(403)

            updated_team = team_service.update(request.form['team_id'],
                                               request.form['name'],
                                               request.form['description'],
                                               request.form['team_leader'])

            flash(f'Saved team {updated_team.team_id} successfully',
                  'is-success')
            return redirect(base_url)

    except (NotExistingException, EmptyValueException, UnvalidInputException,
            DatabaseException) as error:
        flash(str(error), 'is-danger')
        return redirect(base_url)


@app.route(f'{base_url}/edit/<uuid:team_id>/members', methods=['GET', 'POST'])
def edit_team_members(team_id):
    try:
        team = team_service.get_by_id(team_id)

        if (team.team_leader_id != session['user']
                and session['user_role'] < 3) or session['user_role'] < 3:
            flash('Not enough permissions.', 'is-danger')
            return redirect('/')

        # GET shows team
        if request.method == 'GET':
            teamusers = user_service.get_team_users(team_id)
            users = user_service.get_users()
            return render_template('teams/teams_members.html',
                                   team=team,
                                   teamusers=teamusers,
                                   users=users)

        # POST updates team
        if request.method == 'POST':
            if session['token'] != request.form['token']:
                abort(403)
            team_id = request.form['team_id']
            teamusers = user_service.get_team_users(request.form['team_id'])
            teamusers_id = [teamuser[0] for teamuser in teamusers]

            wanted = request.form.getlist('members')
            to_be_added = filter(lambda x: x not in teamusers_id, wanted)
            to_be_removed = filter(lambda x: x not in wanted, teamusers_id)

            for user_id in to_be_added:
                team_service.add_member(team_id, user_id)
            for user_id in to_be_removed:
                team_service.remove_member(team_id, user_id)

            flash('Saved team successfully', 'is-success')
            return redirect(base_url)

    except (NotExistingException, EmptyValueException, UnvalidInputException,
            DatabaseException) as error:
        flash(str(error), 'is-danger')
        return redirect(base_url)


@app.route(f'{base_url}/add', methods=['GET', 'POST'])
def create_team():
    try:
        if session['user_role'] < 2:
            flash('Not enough permissions.', 'is-danger')
            return redirect('/')

        # GET shows creation page
        if request.method == 'GET':
            users = user_service.get_users()
            return render_template('teams/teams_add.html', users=users)

        # POST creates new task
        if request.method == 'POST':
            if session['token'] != request.form['token']:
                abort(403)

            new_team = team_service.new(request.form['name'],
                                        request.form['description'],
                                        request.form['team_leader'])

            for member in request.form.getlist('members'):
                if member != request.form['team_leader']:
                    team_service.add_member(new_team.team_id, member)

            flash(f'New team {new_team.team_id} created successfully',
                  'is-success')
            return redirect(base_url)

    except (NotExistingException, EmptyValueException, UnvalidInputException,
            DatabaseException) as error:
        flash(str(error), 'is-danger')
        return redirect(base_url)


@app.route(f'{base_url}/remove', methods=['POST'])
def remove_team():
    try:
        team = team_service.get_by_id(request.form['team_id'])
        if (team.team_leader_id != session['user']
                and session['user_role'] < 3) or session['user_role'] < 3:
            flash('Not enough permissions.', 'is-danger')
            return redirect('/')

        team_service.remove(team.team_id)
        flash(f'Team with id {team.team_id} removed successfully', 'is-success')
        return redirect(base_url)
    except (NotExistingException, UnvalidInputException,
            DatabaseException) as error:
        flash(str(error), 'is-danger')
        return redirect(base_url)
