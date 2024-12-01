from flask import request, jsonify
from services.soap_service import create_user_soap, get_user_by_id_soap

# Method to create a user
def create_user_service():
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

# Method to get a user by its id
def get_user_by_id_service(user_id):
    try:
        response = get_user_by_id_soap(user_id)
        return jsonify({"data": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500