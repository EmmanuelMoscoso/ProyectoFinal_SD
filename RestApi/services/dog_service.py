from bson import json_util, ObjectId
from infrastructure.mongo import mongo
from errors.error_handlers import *
from models.dog_model import Dog

# Method to create a dog
def create_dog_service():
    try:
        dog_data = request.get_json()

        # Validate required fields
        required_fields = ['name', 'gender', 'size', 'weight', 'birth_date']
        for field in required_fields:
            if not dog_data.get(field):
                return bad_request(f'{field.capitalize()} is required.')

        # Extract fields
        name = dog_data.get('name')
        gender = dog_data.get('gender')
        size = dog_data.get('size')
        weight = dog_data.get('weight')
        birth_date = dog_data.get('birth_date')
        adopted = dog_data.get('adopted', False)

        # Create dog model
        new_dog = Dog(name, gender, size, weight, birth_date, adopted)
        response = mongo.db.dogs.insert_one(new_dog.to_dict())
        return created({
            'id': str(response.inserted_id),
            **new_dog.to_dict()
        })
    except Exception as e:
        return internal_server_error(str(e))

# Method to get all dogs
def get_all_dogs_service():
    try:
        dog_data = list(mongo.db.dogs.find())
        if not dog_data:
            return no_content()
        result = json_util.dumps(dog_data)
        return result
    except Exception as e:
        return internal_server_error(str(e))

# Method to get a dog by its id
def get_dog_by_id_service(id):
    try:
        if not ObjectId.is_valid(id):
            return bad_request('Invalid Dog ID format')

        dog_data = mongo.db.dogs.find_one({'_id': ObjectId(id)})
        if not dog_data:
            return not_found()

        result = json_util.dumps(dog_data)
        return result
    except Exception as e:
        return internal_server_error(str(e))

# Method to search dogs through various ways
def get_dogs_by_data_service(page=1, limit=10):
    try:
        query_params = request.args.to_dict()
        filter = {}

        if 'name' in query_params:
            filter['name'] = query_params['name']
        if 'gender' in query_params:
            filter['gender'] = query_params['gender']
        if 'size' in query_params:
            filter['size'] = query_params['size']
        if 'birth_date' in query_params:
            filter['birth_date'] = query_params['birth_date']

        skip = (page - 1) * limit
        total = mongo.db.dogs.count_documents(filter)

        dog_data = mongo.db.dogs.find(filter).skip(skip).limit(limit)

        formatted_data = []
        for dog in dog_data:
            dog["_id"] = str(dog["_id"])
            formatted_data.append(dog)

        if not formatted_data:
            return no_content()

        return {
            "message": "Retrieved from database",
            "total": total,
            "page": page,
            "limit": limit,
            "data": formatted_data
        }
    except Exception as e:
        return internal_server_error(str(e))

# Method to delete a dog by id
def delete_dog_by_id_service(id):
    try:
        if not ObjectId.is_valid(id):
            return bad_request('Invalid Dog ID format')

        dog_data = mongo.db.dogs.delete_one({'_id': ObjectId(id)})
        if dog_data.deleted_count == 1:
            return success(f'Dog {id} deleted successfully')
        else:
            return not_found()
    except Exception as e:
        return internal_server_error(str(e))

# Method to fully update a dog by id
def update_dog_by_id_service(id):
    try:
        if not ObjectId.is_valid(id):
            return bad_request('Invalid Dog ID format')

        dog_data = mongo.db.dogs.find_one({'_id': ObjectId(id)})
        if not dog_data:
            return not_found()

        update_data = request.get_json()

        required_fields = ['name', 'gender', 'size', 'weight', 'birth_date']
        for field in required_fields:
            if not update_data.get(field):
                return bad_request(f'{field.capitalize()} is required.')

        dog_data.update(update_data)

        result = mongo.db.dogs.update_one({'_id': ObjectId(id)}, {'$set': dog_data})
        if result.modified_count == 1:
            return success(f'Dog {id} updated successfully')
        else:
            return bad_request('No changes were made')
    except Exception as e:
        return internal_server_error(str(e))

# Method to change dog status into 'adopted'
def update_dog_adopted_service(id):
    try:
        if not ObjectId.is_valid(id):
            return bad_request('Invalid Dog ID format')

        dog_data = mongo.db.dogs.find_one({'_id': ObjectId(id)})
        if not dog_data:
            return not_found()

        dog_data['adopted'] = True
        result = mongo.db.dogs.update_one({'_id': ObjectId(id)}, {'$set': dog_data})
        if result.modified_count == 1:
            return success(f'Dog {id} adopted successfully')
        else:
            return bad_request('No changes were made')
    except Exception as e:
        return internal_server_error(str(e))

# Method to partially update a dog
def update_dog_data_service(id):
    try:
        if not ObjectId.is_valid(id):
            return bad_request('Invalid Dog ID format')

        dog_data = mongo.db.dogs.find_one({'_id': ObjectId(id)})
        if not dog_data:
            return not_found()

        update_data = request.get_json()
        fields_to_update = {}

        if 'name' in update_data:
            fields_to_update['name'] = update_data['name']
        if 'gender' in update_data:
            fields_to_update['gender'] = update_data['gender']
        if 'size' in update_data:
            fields_to_update['size'] = update_data['size']
        if 'weight' in update_data:
            fields_to_update['weight'] = update_data['weight']
        if 'birth_date' in update_data:
            fields_to_update['birth_date'] = update_data['birth_date']
        if 'adopted' in update_data:
            fields_to_update['adopted'] = update_data['adopted']

        if fields_to_update:
            result = mongo.db.dogs.update_one({'_id': ObjectId(id)}, {'$set': fields_to_update})
            if result.modified_count == 1:
                return success(f'Dog {id} updated successfully')
            else:
                return bad_request('No changes were made')
        else:
            return bad_request('No fields provided to update')
    except Exception as e:
        return internal_server_error(str(e))
