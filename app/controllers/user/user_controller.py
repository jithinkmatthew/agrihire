import re
import os
import secrets
from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from app import flask_bcrypt
from app.Utils import Utils
from app.controllers.auth.auth_controller import auth_required, get_user_destination
from app.controllers.user.profile_form import MyProfileForm
from app.model.dashboard import DashboardRepository
from app.model.user import UserRepository

user = Blueprint('user', __name__)

@user.route('/signup', methods=['GET', 'POST'])
def signup():
    
    errors = {}
    user_input = {}
        
    
    if request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form and 'username' in request.form and 'email' in request.form and 'password' in request.form:
        
        firstname = request.form['firstname'].strip().capitalize()
        lastname = request.form['lastname'].strip().capitalize()
        username = request.form['username'].strip().lower()
        email = request.form['email'].strip()
        password = request.form['password']
        # confirm_password = request.form['confirm_password']
        # location = request.form['location'].strip()

        user_input = {'firstname': firstname, 'lastname': lastname, 'username': username, 'email': email}

        email_regex = current_app.config['EMAIL_REGEX']
        email_length = int(current_app.config['EMAIL_LENGTH'])
        if len(email) > email_length or not re.match(email_regex, email):
            errors['email'] = "Invalid email format or exceeds 50 characters."
        if len(password) < 8:
            errors['password'] = "Password must be at least 8 characters long."
        elif not any(char.isdigit() for char in password):
            errors['password'] = "Password must contain at least one number."
        elif not any(char.islower() for char in password):
            errors['password'] = "Password must contain at least one lowercase letter."
        elif not any(char.isupper() for char in password):
            errors['password'] = "Password must contain at least one uppercase letter."
        elif not any(char in current_app.config['PASSWORD_CHAR'] for char in password):
            errors['password'] = "Password must contain at least one special character."

    
        # if password != confirm_password:
        #     errors['confirm'] = "Password and confirm password do not match!"
        
    
        password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

        # user_exists_username = UserRepository.get_user(username=username)
        # user_exists_email = UserRepository.get_user(email=email, username=username)
        # if user_exists_username:
            # errors['username'] = "Username already exists!"
        # if user_exists_email:
            # errors['email'] = "Email already exists!"
        
        if errors:
            # flash(errors, 'danger')
            return render_template('auth/signup.html', user_input=user_input, errors=errors)
        
        # role_id = AuthorityRepository.get_role_id(current_app.config['DEFAULT_USER_ROLE'])
        user_data = {'username': username, 'first_name': firstname, 'last_name': lastname, 'email': email, 'password_hash': password_hash}
        result = UserRepository.add_user(user_data)
        if result > 0:
            flash('Registration successful! You can now log in.', 'success')
        
            return redirect(url_for('auth.login'))

    elif 'username' in session:
        
        # return redirect(url_for('login'))
        return redirect(url_for('user.dashboard'))
    
    return render_template('auth/signup.html', user_input=user_input, errors=errors) 



@user.route('/dashboard', methods=['GET'])
@auth_required
def dashboard():
    
    land_data = DashboardRepository.get_land_dashboard_details()
    equip_data = DashboardRepository.get_equipment_dashboard_details()

    return render_template('dashboard.html', 
                           land_data=land_data,
                           equip_data=equip_data)


@user.route('/profile', methods=['GET'])
@auth_required
def profile():
    
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    user_name = session['username']
    user = UserRepository.get_user(username=user_name)
    print(user)
    
    user_object = {
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'email': user['email'],
            'mobile': user['mobile'],
            'location': user['location'],
            'profile_image': user['profile_image']
        }
        
    form = MyProfileForm(data=user_object)
    print(form)
    
    return render_template('user/profile.html', form=form, user=user)


@user.route('/profile/edit', methods=['GET', 'POST'])
def profile_edit():
    
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    user_name = session['username']
    user = UserRepository.get_user(username=user_name)
    
    if request.method == 'POST':
        
        form = MyProfileForm()
        update_user_data = {}
        
        if form.validate_on_submit():
            
            #Handle profile image updation
            profile_image = form.profile_image.data
            if profile_image and profile_image.filename:
                # Save the file
                newname = f"{user['user_id']}.{profile_image.filename.rsplit('.', 1)[1].lower()}"
                upload_folder = os.path.join(current_app.static_folder, current_app.config['UPLOAD_FOLDER_PROFILE'])
                result = Utils.upload_file(profile_image, upload_folder, newname)
                
                if result:
                    print("file uploaded")
                else:
                    print("file uploading failed")
                
                image_path=f"{current_app.config['UPLOAD_FOLDER_PROFILE']}/{newname}"
                update_user_data = {
                        'profile_image': image_path
                    }
            else:
                update_user_data = {
                        'profile_image': user['profile_image']
                    }
            
            #Handle profile details updation
            update_user_data['first_name'] = form.first_name.data
            update_user_data['last_name'] = form.last_name.data
            update_user_data['email'] = form.email.data
            update_user_data['mobile'] = form.mobile.data
            update_user_data['location'] = form.location.data
        
            UserRepository.update_user(user_id=user['user_id'], update_data=update_user_data)
            return redirect(url_for('user.profile'))
        else:        
            print(form.errors)
            
    else:
        user_object = {
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'email': user['email'],
            'mobile': user['mobile'],
            'location': user['location'],
            'profile_image': user['profile_image']
            }
        
        form = MyProfileForm(data=user_object)
    
    return render_template('user/profile_edit.html', form=form, user=user)
