from flask import Blueprint, request, jsonify
from services.soap_service import create_user_soap, get_user_by_id_soap

user_api = Blueprint('user_api', __name__)

@user_api.route('/users', methods=['POST'])
def create_user():
    data = request.json
    try:
        response = create_user_soap(
            name=data['name'],
            age=data['age'],
            email=data['email'],
            phone=data['phone']
        )
        return jsonify({"message": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# REST endpoint to get a user by ID (calls SOAP)
@user_api.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        response = get_user_by_id_soap(user_id)
        return jsonify({"data": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500