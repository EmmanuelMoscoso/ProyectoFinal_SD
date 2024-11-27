from flask import Blueprint
from services.dog_service import *
from config import redis_client
import json

dog_api = Blueprint('dog_api', __name__)

# Route to create a dog
@dog_api.route('/', methods=['POST'])
def create_dog():
    redis_client.delete('dogs')
    return create_dog_service()

# Route that return all dogs as a list
@dog_api.route('/', methods=['GET'])
def get_all_dogs():
    cached_data = redis_client.get('dogs')
    if cached_data:
        print("Cached data:", cached_data)
        return jsonify({"message": "Retrieved from cache", "data": json.loads(cached_data)})

    data = get_all_dogs_service()
    print("Fetched data:", data)

    redis_client.set('dogs', data.encode('utf-8'), ex=15)

    return jsonify({"message": "Retrieved from database", "data": json.loads(data)})

# Route to search for dog through various ways
@dog_api.route('/search', methods=['GET'])
def get_dogs_by_data():
    # Pagination
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    # Cache key
    cache_key = f'dogs_search:{request.args.to_dict()}_page:{page}_limit:{limit}'
    cached_data = redis_client.get(cache_key)

    if cached_data:
        return jsonify(json.loads(cached_data))

    data = get_dogs_by_data_service(page=page, limit=limit)
    redis_client.set(cache_key, json.dumps(data), ex=15)

    return jsonify(data)



# Route to search for a dog by its id
@dog_api.route('/<dog_id>', methods=['GET'])
def get_dog_by_id(dog_id):
    # Cache key
    cache_key = f'dogs_id:{dog_id}'
    cached_data = redis_client.get(cache_key)

    # Return data in cache
    if cached_data:
        return jsonify({"message": "Retrieved from cache", "data": json.loads(cached_data)})

    # If not in cache, obtain data from service
    data = get_dog_by_id_service(dog_id)

    redis_client.set(cache_key, data.encode('utf-8'), ex=15)

    return jsonify({"message": "Retrieved from database", "data": json.loads(data)})

# Route to delete a dog
@dog_api.route('/<dog_id>', methods=['DELETE'])
def delete_dog(dog_id):
    redis_client.delete(f"dogs_id:{dog_id}", "all_dogs")
    return delete_dog_by_id_service(dog_id)

# Route to fully update a dog
@dog_api.route('/<dog_id>', methods=['PUT'])
def update_dog(dog_id):
    redis_client.delete(f"dog:{dog_id}", "all_dogs")
    return update_dog_by_id_service(dog_id)

# Route to partially update a dog
@dog_api.route('/<dog_id>/', methods=['PATCH'])
def update_dog_data(dog_id):
    redis_client.delete(f"dog:{dog_id}", "all_dogs")
    return update_dog_data_service(dog_id)

# Route to change dog status into 'adopted'
@dog_api.route('/<dog_id>/adopted', methods=['PATCH'])
def update_dog_adopted(dog_id):
    redis_client.delete(f"dog:{dog_id}", "all_dogs")
    return update_dog_adopted_service(dog_id)





