from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from core.auth import login_required
from core.db import create_conn
from .models import Actions, User, Items
from PIL import Image
import os

bp = Blueprint('main', __name__)


@bp.route('/')
def hello():
    cnx, cursor = create_conn()
    actions = Actions.get_all(cursor)
    cnx.close()
    return render_template('main/index.html', actions=actions)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        descriptions = request.form['descriptions']
        date = request.form['date']
        img = request.files['image']

        error = None

        if not title:
            error = 'Title is required.'

        if not date:
            error = 'Date is required.'

        if img is None:
            image_name = 'core/static/media/ico.png'
        else:
            try:
                image_name = 'core/static/media/' + str(img.filename)
                opened_img = Image.open(img)
                if opened_img.format.lower() not in ['png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif']:
                    error = 'invalid image format'
            except:
                error = 'invalid image format'

        if error is not None:
            flash(error)
        else:
            cnx, cursor = create_conn()
            action = Actions(id_user=g.user.id, title=title, descriptions=descriptions, date=date, image=image_name)
            if action.create(cursor) != 'Error date format!':
                if image_name != 'core/static/media/ico.png':
                    opened_img.save(os.path.join(str(os.getcwd()), image_name))
                cnx.close()
                return redirect(url_for('index'))
            flash('Error date format!')

    return render_template('main/create.html')


def get_action(id, check_author=True):
    cnx, cursor = create_conn()
    action = Actions.get_by_id(cursor, id)
    cnx.close()
    if action is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and action.id_user != g.user.id:
        abort(403)

    return action


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    action = get_action(id)

    if request.method == 'POST':
        title = request.form['title']
        descriptions = request.form['descriptions']
        date = request.form['date']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            cnx, cursor = create_conn()
            action.title = title
            action.descriptions = descriptions
            action.date = date
            create = action.create(cursor)
            cnx.close()
            if create is True:
                return redirect(url_for('index'))
            flash('Error date format!')

    return render_template('main/update.html', action=action)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    action = get_action(id)
    cnx, cursor = create_conn()
    action.delete(cursor)
    cnx.close()
    return redirect(url_for('index'))


@bp.route('/<int:id>/action', methods=('GET', 'POST'))
@login_required
def action(id):
    action = get_action(id)
    cnx, cursor = create_conn()
    items = Items.get_items(cursor, action.id)
    if action.img is None:
        action.img = 'ico.png'
    cnx.close()
    if request.method == 'POST':
        text = request.form['text']
        if not text:
            flash('text is required')
        else:
            cnx, cursor = create_conn()
            item = Items(id_action=action.id, text=text, yes_no=False)
            created = item.create(cursor)
            cnx.close()
            if created is not False:
                return redirect(url_for('main.action', id=id))
    return render_template('main/action.html', action=action, items=items)