import json
from infrastructure.postgres import get_connection

def create_dog_service(name, gender, size, weight, birth_date, adopted):
    """Handles the creation of a dog resource."""
    try:
        # Validate required fields
        required_fields = [name, gender, size, weight, birth_date]
        if not all(required_fields):
            return "Error: All required fields must be present."

        # Convert weight to float
        try:
            weight = float(weight)
        except ValueError:
            return "Error: Weight must be a number."

        # Prepare data
        json_data = {
            "name": name,
            "gender": gender,
            "size": size,
            "weight": weight,
            "birth_date": birth_date,
            "adopted": adopted.lower() == 'true'
        }

        # Insert into database
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO dogs (data) VALUES (%s) RETURNING id;", (json.dumps(json_data),))
        dog_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return f"Resource created with ID: {dog_id}"
    except Exception as e:
        return f"Error creating resource: {str(e)}"

def get_dog_by_id_service(dog_id):
    """Fetches a dog resource by its ID."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT data FROM dogs WHERE id = %s;", (dog_id,))
        dog = cur.fetchone()
        cur.close()
        conn.close()

        if dog:
            return json.dumps(dog[0])
        else:
            return f"Resource with ID {dog_id} not found."
    except Exception as e:
        return f"Error fetching resource: {str(e)}"
