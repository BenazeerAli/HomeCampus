from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from auth2 import get_user_by_username, create_user, hash_password, User

auth_bp = Blueprint('auth', __name__)
from flask import jsonify
@auth_bp.route('/Register', methods=['POST'])
def register():
    username = request.form.get('email')
    password = request.form.get('parent_password')
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax or request.args.get('async') == 'true':
        if not username or not password:
            return jsonify(success=False, error="Username and password are required"), 400

        if get_user_by_username(username):
            return jsonify(success=False, error="User already exists"), 409

        user = create_user(username, password, is_parent=True)
        if user:
            login_user(user)
            return jsonify(success=True, continue_url=url_for('auth.myProfile'))
        else:
            return jsonify(success=False, error="Error creating user"), 500

    else:
        if not username or not password:
            flash('Username and password are required')
            return redirect(url_for('auth.register'))

        if get_user_by_username(username):
            flash('User already exists')
            return redirect(url_for('auth.register'))

        user = create_user(username, password, is_parent=True)
        if user:
            login_user(user)
            return redirect(url_for('auth.myProfile'))
        else:
            flash('Error creating user')
            return redirect(url_for('auth.register'))

        # This line will never be reached, but kept for fallback
        return render_template('RegisterPage.html')

from flask import request, jsonify, redirect, url_for, render_template, flash
from werkzeug.security import check_password_hash


@auth_bp.route('/SignIn', methods=['POST'])
def signin():
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    username = request.form.get('username')
    password = request.form.get('password')

    print("Username submitted:", username)
    print("Password submitted:", password)

    user = get_user_by_username(username)

    print("User found:", bool(user))
    if user:
        print("Stored hash:", user.password_hash)
        print("Password check:", check_password_hash(user.password_hash, password))

    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        if is_ajax:
            return jsonify(success=True, continue_url=url_for('index'))
        else:
            return redirect(url_for('index'))
    else:
        if is_ajax:
            return jsonify(success=False, error="Invalid username or password"), 401
        else:
            flash("Invalid username or password")
            return redirect(url_for('auth.login'))

from auth2 import get_child_users_for_parent
@auth_bp.route('/MyProfile', methods=['GET', 'POST'])
@login_required
def myProfile():
    form_error = None
    first_name_val = ''
    last_name_val = ''
    user_added = False
    new_child_username = None

    if request.method == 'POST':
        fname = request.form.get('child_first_name')
        lname = request.form.get('child_last_name')
        skill_grade = request.form.get('skill_grade')

        first_name_val = fname
        last_name_val = lname

        if not fname:
            form_error = -1
        elif not lname:
            form_error = -2
        elif not skill_grade:
            form_error = -3
        else:
            username = fname + lname
            password = fname + lname
            if get_user_by_username(username):
                form_error = -4  # Optional error code for "user exists"
            else:
                if not get_user_by_username(username):
                    user = create_user(
                        username=username,
                        password=password,
                        is_parent=False,
                        first_name=fname,
                        parent_id=current_user.id  # << this links the child to the current parent
                    )
                if user:
                    user_added = True
                    new_child_username = username

    # Always fetch updated child data
    child_user_data = get_child_users_for_parent(current_user.id)

    

    return render_template(
        'MyProfile.html',
        ChildUserData=child_user_data
    )


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return f'Hello, {current_user.username}! You are logged in.'
