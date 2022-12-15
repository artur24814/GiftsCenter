from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from flask_mail import Mail, Message
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

@bp.route('/search', methods=['POST'])
def search():
    cnx, cursor = create_conn()
    if request.method == 'POST':
        search = request.form['search']
        users = User.search(cursor, search)
        actions = Actions.search(cursor, search)
    cnx.close()
    return render_template('main/search.html', actions=actions, users=users)


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
            image_name = '/media/ico.png'
        else:
            try:
                image_name = '/media/' + str(img.filename)
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
                if image_name != '/media/ico.png':
                    print(str(os.getcwd()))
                    current_path = str(os.getcwd()) + '/core/static'
                    print(os.path.join(os.path.normcase(current_path), image_name))
                    opened_img.save(current_path + image_name)
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

    # if check_author and action.id_user != g.user.id:
    #     abort(403)

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
            item = Items(id_action=action.id, text=text, yes_no=False, id_user=g.user.id)
            created = item.create(cursor)
            cnx.close()
            if created is not False:
                return redirect(url_for('main.action', id=id))
    return render_template('main/action.html', action=action, items=items)

def get_item(id, check_author=True):
    cnx, cursor = create_conn()
    item = Items.get_by_id(cursor,id)
    if item is None:
        abort(404, f"Post id {id} doesn't exist.")

    # if Items.check_user(cursor, g.user.id, item.id_actions) == False:
    #     return False
    cnx.close()
    return item


@bp.route('/confirm/<int:id>/action', methods=('GET', 'POST'))
@login_required
def confirm_item(id):
    item = get_item(id)
    cnx, cursor = create_conn()
    if Items.check_user(cursor, g.user.id, item.id_actions) != False:
        item.yes_no = True
        item.id_user = g.user.id
        item.create(cursor)
        mail = Mail(current_app)
        msg = Message('Hello', sender='flaskApp@gmail.com', recipients=['artur24814@gmail.com'])
        msg.body = f"Hello {g.user.username}, you reserve {item.text} for your present"
        mail.send(msg)
        cnx.close()
    else:
        flash("you already chosen one item, can't choose new")
    return redirect(url_for('main.action', id=item.id_actions))