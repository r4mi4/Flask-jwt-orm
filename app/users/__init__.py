from flask import Blueprint
from app.users.models import Users

users = Blueprint('users', __name__,url_prefix='/users/')


from . import api_routes

from app.extentions import db
# db.create(Users)
# user1 = Users(username='ramin',password='ramin',email= 'ramin@email.com',image='test image',bio='this is bio',phone_number='09393366602')
# db.save(user1)