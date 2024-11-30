import json
from infrastructure.postgres import get_connection

def create_user_service(name, age, email, phone):
    """Handles the creation of a user resource."""
    try:
        # Validate required fields
        required_fields = [name, age, email, phone]
        if not all(required_fields):
            return "Error: All required fields must be present."

        # Prepare data
        json_data = {
            "name": name,
            "age": age,
            "email": email,
            "phone":phone
        }

        # Insert into database
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (data) VALUES (%s) RETURNING id;", (json.dumps(json_data),))
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return f"Resource created with ID: {user_id}"
    except Exception as e:
        return f"Error creating resource: {str(e)}"

def get_user_by_id_service(user_id):
    """Fetches a dog resource by its ID."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT data FROM users WHERE id = %s;", (user_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            return json.dumps(user[0])
        else:
            return f"Resource with ID {user_id} not found."
    except Exception as e:
        return f"Error fetching resource: {str(e)}"
