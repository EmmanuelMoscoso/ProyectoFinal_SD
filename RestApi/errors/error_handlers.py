from flask import jsonify, request

def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response

def bad_request(message="Bad Request"):
    response = jsonify({
        'message': message,
        'status': 400
    })
    response.status_code = 400
    return response

def success(data):
    response = jsonify({
        'data': data,
        'status': 200
    })
    response.status_code = 200
    return response

def created(data):
    response = jsonify({
        'data': data,
        'message': 'Resource Created',
        'status': 201
    })
    response.status_code = 201
    return response

def no_content():
    response = jsonify({
        'message': 'No Content',
        'status': 204
    })
    response.status_code = 204
    return response

def internal_server_error(message="Internal Server Error"):
    response = jsonify({
        'message': message,
        'status': 500
    })
    response.status_code = 500
    return response
