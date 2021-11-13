import json
from flask import request, url_for
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from app.users.models import Users
from app.users.utils import regex
from . import users
import re
from app.extentions import db
from datetime import timedelta
from random import randint
from werkzeug.utils import secure_filename


@users.route('/login/', methods=['POST'])
def auth_with_number():
    """
        Check the phone number and send a text message if that number is valid
    """
    args = request.get_json()
    phone_number = args.get('phone_number')
    user = db.get(Users, phone_number=phone_number)
    if user:
        return {'success': 'code sent!'}, 200
    else:
        return {'error': 'sorry, you must be register !'}, 403


@users.route('/login/check_code/',methods=['POST'])
def check_code():
    """
        Check the sent code
    """
    # code = randint(100,999)
    code = 5656
    args = request.get_json()
    code_entered = args.get('code')
    if code == code_entered:
        return {'success': 'code is true!'}, 200
    else:
        return {'error': 'sorry, your code is inccorent!'}


@users.route('/auth/', methods=['POST'])
def login():
    """
        login user with username and password
    """

    if not request.is_json:
        return {'error': 'json only!!'}
    args = request.get_json()
    username = args.get('username')
    password = args.get('password')
    user = db.get(Users, username=username, password=password)
    if user:
        access_token = create_access_token(identity=user.username,
                                           fresh=True)
        # expires_delta=timedelta(seconds=15)
        refresh_token = create_refresh_token(identity=user.username)
        return {'access_token': access_token, 'resresh_token': refresh_token}, 200
    else:
        return {'error': 'Username / Password does not match.'}, 403


@users.route('/auth/', methods=['PUT'])
@jwt_required(refresh=True)
def refresh_token():
    """
        Give a new authentication code
    """
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return {'access_token': access_token}


@users.route('/profile/', methods=['POST'])
def profile():
    """
        Receiving a user profile with username 
        username must be sent by post method
    """
    args = request.get_json()
    username = args.get('username')
    user = db.get(Users, username=username)
    # check url validations
    img = re.match(regex, f"{user.image}")

    # image saved on our local storage
    image = user.image

    # image is only a url address
    if img is None:
        image=  url_for('static', filename='img/users/profile/'+user.image, _external=True) 
    if user:
        return {'username': user.username, 'password': user.password, 'image':image,
                'email': user.email, 'bio': user.bio, 'phone_number': user.phone_number}
    else:
        return {'error': 'user with this username does not exist!'}


@users.route('/profile/edit/<string:username>/', methods=['POST'])
@jwt_required()
def update_profile(username):
    """
        edit user profile with username
    """
    identity = get_jwt_identity()
    if identity == username:
        data = request.form.get('json')
        args=json.loads(data)
        my_key = ['username', 'password', 'email',
                  'bio', 'image', 'phone_number']
        values = {key: value for key, value in args.items() if key in my_key}
        user = db.get(Users, username=username)

        # Checking a username that no one has selected
        if values.get('username'):
            check_username = db.get(Users, username=values.get('username'))
            if check_username and check_username.username != values.get('username'):
                return {'err': 'your username used! take another'}

        # Checking a email that no one has selected
        if values.get('email'):
            check_email = db.get(Users, email=values.get('email'))
            if check_email and check_email.email != values.get('email'):
                return {'err': 'your email used! take another'}

        username = values.get('username') if values.get(
            'username') else user.username
        email = values.get('email') if values.get('email') else user.email
        bio = values.get('bio') if values.get('bio') else user.bio
        phone_number = values.get('phone_number') if values.get(
            'phone_number') else user.phone_number

        # get image file 
        file = request.files.get('image')
        if file:
            image = secure_filename(file.filename)
            file.save(f'app/static/img/users/profile/{image}')
        # or image url address
        elif file is None:
            image = values.get('image') if values.get('image') else user.image
        password = values.get('password') if values.get(
            'password') else user.password
        db.update(Users, conditions={'username': identity}, username=username, image=image,
                  password=password, bio=bio, email=email, phone_number=phone_number)
        return {'success': 'DONE!'}, 200
    else:
        return{'error': 'your not allowd /if your username changed ,so you have to login again'}
