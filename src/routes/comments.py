from flask import redirect, render_template, request, session, abort, flash, escape
from app import app
from services.comment_service import comment_service
from utils.exceptions import NotExistingException, EmptyValueException, DatabaseException, UnvalidInputException
from utils.validators import validate_uuid4

base_url = '/comments'


@app.route(f'{base_url}/edit', methods=['GET', 'POST'])
def edit_comment():
    try:
        cid = request.args.get('id')

        if not validate_uuid4(cid):
            raise UnvalidInputException('comment id')

        comment = comment_service.get_by_id(cid)

        if (comment.assignee_id != session['user']
                and session['user_role'] < 2) or session['user_role'] < 2:
            flash('Not enough permissions.', 'is-danger')
            return redirect('/')

        # GET shows comment edit form
        if request.method == 'GET':
            return render_template('comments/comments_edit.html',
                                   comment=comment)

        # POST updates comment
        if request.method == 'POST':
            if session['token'] != request.form['token']:
                abort(403)
            mode = request.form.get('mode')
            cid = request.form.get('id')

            if mode == 'features':
                updated_comment = comment_service.update(
                    request.form['comment_id'], request.form['assignee_id'],
                    escape(request.form['comment']), request.form['time_spent'],
                    request.form['feature_id'])
                flash(
                    f'Saved comment {updated_comment.comment_id} successfully',
                    'is-success')
                return redirect(
                    f'/{updated_comment.mode}/{updated_comment.feature_id}')
            elif mode == 'tasks':
                updated_comment = comment_service.update(
                    request.form['comment_id'], request.form['assignee_id'],
                    escape(request.form['comment']), request.form['time_spent'],
                    request.form['task_id'])
                flash(
                    f'Saved comment {updated_comment.comment_id} successfully',
                    'is-success')
                return redirect(
                    f'/{updated_comment.mode}/{updated_comment.task_id}')
            else:
                raise NotExistingException('Mode')

    except (NotExistingException, UnvalidInputException, DatabaseException,
            EmptyValueException) as error:
        flash(str(error), 'is-danger')
        return redirect('/')


@app.route(f'{base_url}/add', methods=['GET', 'POST'])
def create_comment():
    # GET shows creation page
    if request.method == 'GET':
        mode = request.args.get('mode')

        cid = request.args.get('id')
        if not validate_uuid4(cid):
            flash('Given id is unvalid.', 'is-danger')
            return redirect('/')

        if mode not in ['features', 'tasks']:
            flash('Given mode is unvalid.', 'is-danger')
            return redirect('/')

        return render_template('comments/comments_add.html', mode=mode, id=cid)

    try:
        # POST creates new comment for feature
        if request.method == 'POST':
            if session['token'] != request.form['token']:
                abort(403)
            mode = request.form.get('mode')
            cid = request.form.get('id')

            if mode == 'features':
                new_comment = comment_service.new(request.form['assignee'],
                                                  escape(
                                                      request.form['comment']),
                                                  request.form['tspent'],
                                                  fid=cid)
            elif mode == 'tasks':
                new_comment = comment_service.new(request.form['assignee'],
                                                  escape(
                                                      request.form['comment']),
                                                  request.form['tspent'],
                                                  tid=cid)
            else:
                raise NotExistingException('Mode')

            flash(f'New comment {new_comment.comment_id} created successfully',
                  'is-success')
            return redirect(f'/{mode}/{cid}')

    except (NotExistingException, UnvalidInputException, DatabaseException,
            EmptyValueException) as error:
        flash(str(error), 'is-danger')
        return redirect('/')


@app.route(f'{base_url}/remove/<uuid:comment_id>', methods=['GET'])
def remove_comment(comment_id):
    try:
        comment = comment_service.get_by_id(comment_id)

        if (comment.assignee_id != session['user']
                and session['user_role'] < 2) or session['user_role'] < 2:
            flash('Not enough permissions.', 'is-danger')
            return redirect('/')

        comment_service.remove(comment_id)
        flash(f'Comment with id {comment_id} removed successfully',
              'is-success')
        return redirect(request.args.get('came_from'))
    except (NotExistingException, UnvalidInputException,
            DatabaseException) as error:
        flash(str(error), 'is-danger')
        return redirect(request.args.get('came_from') or '/')
