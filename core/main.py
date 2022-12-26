from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from flask_mail import Mail, Message
from werkzeug.exceptions import abort
from core.auth import login_required
from core.db import create_conn
from .models import Actions, User, Items, UsersActions, UserFriends
from PIL import Image
import os

bp = Blueprint('main', __name__)


@bp.route('/')
def hello():
    '''
    Fancy HOME page
    '''
    cnx, cursor = create_conn()
    actions = Actions.get_all(cursor)
    cnx.close()
    return render_template('main/index.html', actions=actions)

@bp.route('/search', methods=['POST'])
def search():
    '''
    Search view
    : return: user and actions objects
    '''
    cnx, cursor = create_conn()
    if request.method == 'POST':
        search = request.form['search']
        #users objects
        users = User.search(cursor, search)
        #actions objects
        actions = Actions.search(cursor, search)
    cnx.close()
    return render_template('main/search.html', actions=actions, users=users)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """
    Create Actions
    :return: actions objects
    """
    cnx, cursor = create_conn()
    #get all friengs login user

    users = UserFriends.get_friends(cursor, g.user.id)
    if request.method == 'POST':
        title = request.form['title']
        descriptions = request.form['descriptions']
        date = request.form['date']
        img = request.files['image']
        #get list checked friends
        friends = request.form.getlist('friends')

        error = None

        #validate form
        if not title:
            error = 'Title is required.'
        if not date:
            error = 'Date is required.'
        #if image wasn't chousen set default image
        if img is None:
            image_name = '/media/ico.png'
        else:
            try:
                #create image path
                image_name = '/media/' + str(img.filename)
                #try open image
                opened_img = Image.open(img)
                #check format image
                if opened_img.format.lower() not in ['png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif']:
                    error = 'invalid image format'
            except:
                #if we get error in line 'Image.open()'
                error = 'invalid image format'
        #show an error
        if error is not None:
            flash(error)
        else:
            #create action
            action = Actions(id_user=g.user.id, title=title, descriptions=descriptions, date=date, image=image_name)
            #check if date not in a past or incorect format
            if action.create(cursor) != 'Error date format!':
                #if image not default save this image to 'media'
                if image_name != '/media/ico.png':
                    #get current path
                    current_path = str(os.getcwd()) + '/core/static'
                    opened_img.save(current_path + image_name)
                try:
                    #try to add all chousen friends and send email
                    for friend in friends:
                        user_action = UsersActions(int(friend), action.id)
                        user_action.create(cursor)
                except:
                    #if error get when sending email
                    flash('Upss... some friend not added, please add they manual')
                    pass
                cnx.close()
                return redirect(url_for('index'))
            #error date
            flash('Error date format!')

    return render_template('main/create.html', users=users)


def get_action(id, check_author=True):
    '''
    Get action from id
    :param id:
    :param check_author:
    :return: object action, objects users
    '''
    cnx, cursor = create_conn()
    #get action
    action = Actions.get_by_id(cursor, id)
    #get all invited users
    users = UsersActions.get_all_users(cursor, id)
    cnx.close()
    if action is None:
        abort(404, f"Post id {id} doesn't exist.")

    # if check_author and action.id_user != g.user.id:
    #     abort(403)

    return action, users


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    #get action and invited users
    action, users = get_action(id)

    if request.method == 'POST':
        title = request.form['title']
        descriptions = request.form['descriptions']
        date = request.form['date']
        error = None

        #validate form
        if not title:
            error = 'Title is required.'

        if error is None:
            cnx, cursor = create_conn()
            action.title = title
            action.descriptions = descriptions
            action.date = date
            #update action
            create = action.create(cursor)
            cnx.close()
            #redirect if updated
            if create is True:
                return redirect(url_for('index'))
            flash('Error date format!')
        else:
            flash(error)

    return render_template('main/update.html', action=action, users=users)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    #get action
    action = get_action(id)
    cnx, cursor = create_conn()
    action.delete(cursor)
    cnx.close()
    return redirect(url_for('index'))


@bp.route('/<int:id>/action', methods=('GET', 'POST'))
@login_required
def action(id):
    '''
    Action detail View
    :param id: int
    :return: template
    '''

    # get action and invited users
    action, users = get_action(id)
    cnx, cursor = create_conn()
    #get all items for this action
    items = Items.get_items(cursor, action.id)
    #get all users (for post method)
    all_users = UserFriends.get_friends(cursor, g.user.id)

    #set default image if not image in action
    if action.img is None:
        action.img = 'ico.png'
    cnx.close()
    if request.method == 'POST':
        text = request.form['text']
        #validate form
        if not text:
            flash('text is required')
        else:
            cnx, cursor = create_conn()
            #create item object
            item = Items(id_action=action.id, text=text, yes_no=False, id_user=g.user.id)
            created = item.create(cursor)
            cnx.close()
            #if successful add items
            if created is not False:
                return redirect(url_for('main.action', id=id))
    return render_template('main/action.html', action=action, items=items, users=users, all_users=all_users)

def get_item(id, check_author=True):
    '''
    Get item from id
    :param id:
    :param check_author:
    :return: object item
    '''
    cnx, cursor = create_conn()
    item = Items.get_by_id(cursor,id)
    #Show page 404
    if item is None:
        abort(404, f"Post id {id} doesn't exist.")

    # if Items.check_user(cursor, g.user.id, item.id_actions) == False:
    #     return False
    cnx.close()
    return item


@bp.route('/confirm/<int:id>/action', methods=('GET', 'POST'))
@login_required
def confirm_item(id):
    '''
    Confirm chosen item
    :param id:
    :return: set user in item object
    '''
    item = get_item(id)
    cnx, cursor = create_conn()
    #check if user not alredy chouse another item
    if Items.check_user(cursor, g.user.id, item.id_actions) != False:
        #set item to checked
        item.yes_no = True
        #set user in item
        item.id_user = g.user.id
        #update item
        item.create(cursor)
        #create Mail
        mail = Mail(current_app)
        msg = Message('Hello', sender='flaskApp@gmail.com', recipients=[f'{g.user.email}'])
        msg.body = f"Hello {g.user.username}, you reserve {item.text} for your present"
        mail.send(msg)
        cnx.close()
    else:
        flash("you already chosen one item, can't choose new")
    return redirect(url_for('main.action', id=item.id_actions))

@bp.route('/add_friend/<int:id>', methods=['GET'])
@login_required
def add_friend(id):
    '''
    Add friend view
    :param id:
    :return: object User_friend
    '''
    cnx, cursor = create_conn()
    #get friend
    user = User.get_user_by_id(cursor, id)
    if user is None:
        flash('This user is not exist')
        return redirect(url_for('index'))

    #create friend for loggin user
    user_friend = UserFriends(g.user.id, id)
    if user_friend.create(cursor) is True:
        flash(f'You and {user.username} now are friends')
    cnx.close()
    return redirect(url_for('index'))

@bp.route('/my_friends', methods=['GET'])
@login_required
def my_friends():
    '''
    All user login friend
    :return: objects user_friends
    '''
    cnx, cursor = create_conn()
    #get friends
    users = UserFriends.get_friends(cursor, g.user.id)
    cnx.close()
    return render_template('main/my_friends.html', users=users)

@bp.route('/add_friend_to_actions/<int:id>', methods=['POST'])
@login_required
def add_to_action(id):
    """
    Invite friends to action
    :param id:
    :return: object userAction
    """
    if request.method == 'POST':
        #get all cousen friends
        friends = request.form.getlist('friends')
        action, users = get_action(id)
        cnx, cursor = create_conn()
        try:
            #try create userActions and send invited message
            for friend in friends:
                user_action = UsersActions(int(friend), action.id)
                user_action.create(cursor)
        except:
            #if an error in mail
            flash('Upss... some friend not added, please add they manual')
            pass
        cnx.close()
        return redirect(url_for('main.action', id=id))

@bp.route('/users-actions/<int:id>', methods=['GET'])
@login_required
def user_actions(id):
    '''
    All user actions
    '''
    cnx, cursor = create_conn()
    actions = Actions.set_users_action(cursor, id)
    return render_template('main/user_actions.html', actions=actions)


