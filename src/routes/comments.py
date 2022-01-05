import os
from flask import redirect, render_template, request, session, abort, flash, escape
from app import app
from services.feature_service import feature_service
from services.task_service import task_service
from services.comment_service import comment_service
from services.user_service import user_service
from utils.exceptions import NotExistingException, UsernameDuplicateException, ValueShorterThanException, EmptyValueException, DatabaseException, UnvalidInputException
from utils.validators import validate_uuid4

baseUrl = '/comments'


@app.route(f'{baseUrl}/edit', methods=['GET', 'POST'])
def edit_comment():
    try:
        cid = request.args.get('id')

        if not validate_uuid4(cid):
            raise UnvalidInputException('comment id')

        comment = comment_service.get_by_id(cid)
    except UnvalidInputException as error:
        flash(str(error), 'is-danger')
        return redirect('/')
    except DatabaseException as error:
        flash(str(error), 'is-danger')
        return redirect('/')
    except NotExistingException as error:
        flash(str(error), 'is-danger')
        return redirect('/')

    if comment.assignee_id != session['user'] or session['user_role'] < 2:
        flash('Not enough permissions.', 'is-danger')
        return redirect('/')

    # GET shows comment edit form
    if request.method == 'GET':
        return render_template('comments/comments_edit.html', comment=comment)

    # POST updates comment
    if request.method == 'POST':
        if session['token'] != request.form['token']:
            abort(403)
        mode = request.form.get('mode')
        cid = request.form.get('id')
        try:
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
        except NotExistingException as error:
            flash(str(error), 'is-danger')
            return redirect(f'/{mode}/{cid}')
        except EmptyValueException as error:
            flash(str(error), 'is-danger')
            return redirect(f'/{mode}/{cid}')
        except UnvalidInputException as error:
            flash(str(error), 'is-danger')
            return redirect(f'/{mode}/{cid}')
        except DatabaseException as error:
            flash(str(error), 'is-danger')
            return redirect(f'/{mode}/{cid}')


@app.route(f'{baseUrl}/add', methods=['GET', 'POST'])
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

    # POST creates new comment for feature
    if request.method == 'POST':
        if session['token'] != request.form['token']:
            abort(403)
        mode = request.form.get('mode')
        cid = request.form.get('id')
        try:
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
        except NotExistingException as error:
            flash(str(error), 'is-danger')
            return redirect(f'/{mode}/{cid}')
        except EmptyValueException as error:
            flash(str(error), 'is-danger')
            return redirect(f'/{mode}/{cid}')
        except UnvalidInputException as error:
            flash(str(error), 'is-danger')
            return redirect(f'/{mode}/{cid}')
        except DatabaseException as error:
            flash(str(error), 'is-danger')
            return redirect(f'/{mode}/{cid}')


@app.route(f'{baseUrl}/remove/<uuid:comment_id>', methods=['GET'])
def remove_comment(comment_id):
    try:
        comment = comment_service.get_by_id(comment_id)

        if comment.assignee_id != session['user'] or session['user_role'] < 2:
            flash('Not enough permissions.', 'is-danger')
            return redirect('/')

        comment_service.remove(comment_id)
        flash(f'Comment with id {comment_id} removed successfully',
              'is-success')
        return redirect(request.args.get('came_from'))
    except NotExistingException as error:
        flash(str(error), 'is-danger')
        return redirect(request.args.get('came_from'))
    except DatabaseException as error:
        flash(str(error), 'is-danger')
        return redirect(request.args.get('came_from'))
    except UnvalidInputException as error:
        flash(str(error), 'is-danger')
        return redirect(request.args.get('came_from'))