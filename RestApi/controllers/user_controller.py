from flask import Blueprint
from services.user_service import *

user_api = Blueprint('user_api', __name__)

# REST-SOAP endpoint to create a user 
@user_api.route('/', methods=['POST'])
def create_user():
    return create_user_service()

# REST-SOAP endpoint to get a user by ID 
@user_api.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    return get_user_by_id_service(user_id)